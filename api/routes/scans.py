from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from api.schemas import ScanRequest, ScanResponse
from database.database import get_db
from database import repository
from scanner.security_headers import analyze_security_headers
from scanner.api_analysis import analyze_api_configuration
from scanner.authentication_analysis import analyze_authentication
from scanner.authorization_analysis import analyze_authorization
from scanner.client_security import analyze_client_security
from engine.risk_engine import assess_finding
from engine.correlation import deduplicate_findings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def validate_target(target: str):
    allowed = ["http://127.0.0.1", "http://localhost"]
    if not any(target.startswith(a) for a in allowed):
        raise HTTPException(status_code=400, detail="Target not authorized. Local/Staging only.")

def run_orchestrator(scan_id: str, target_url: str, db: Session):
    try:
        findings = []
        findings.extend(analyze_security_headers(target_url))
        findings.extend(analyze_api_configuration(target_url))
        findings.extend(analyze_authentication(target_url))
        findings.extend(analyze_authorization(target_url))
        findings.extend(analyze_client_security(target_url))
        
        assessed = [assess_finding(f) for f in findings]
        deduped = deduplicate_findings(assessed)
        
        for f in deduped:
            repository.save_finding(db, scan_id, f)
            
        repository.complete_scan(db, scan_id, deduped)
        repository.create_audit_log(db, "Scan Completed", "Orchestrator", "Success", f"Scan {scan_id} finished")
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        repository.create_audit_log(db, "Scan Error", "Orchestrator", "Error", str(e))

@router.post("/api/scans", response_model=ScanResponse)
def start_scan(request: ScanRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    validate_target(request.target_url)
    scan = repository.create_scan(db, request.target_url)
    repository.create_audit_log(db, "Scan Started", "Orchestrator", "Success", f"Scan {scan.id} started")
    background_tasks.add_task(run_orchestrator, scan.id, request.target_url, db)
    return ScanResponse(id=scan.id, target=scan.target, status=scan.status)

@router.get("/api/scans")
def get_scans(db: Session = Depends(get_db)):
    return repository.get_scans(db)

@router.get("/api/scans/{scan_id}")
def get_scan(scan_id: str, db: Session = Depends(get_db)):
    scan = repository.get_scan(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan
