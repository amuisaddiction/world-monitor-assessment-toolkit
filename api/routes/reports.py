from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import repository
from ai_triage.generate_report import run_report_generation
import os

router = APIRouter()

@router.post("/api/reports/{scan_id}")
def generate_report(scan_id: str, db: Session = Depends(get_db)):
    scan = repository.get_scan(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    findings = repository.get_findings(db, scan_id)
    findings_list = []
    for f in findings:
        findings_list.append({
            "id": f.finding_id,
            "title": f.title,
            "severity": f.severity,
            "cvss_score": f.cvss_score,
            "category": f.category,
            "description": f.description,
            "remediation": f.remediation,
            "impact": f.impact
        })
        
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/security_assessment_report_{scan_id}.md"
    run_report_generation(findings_list, report_path)
    
    rep = repository.save_report(db, scan_id, report_path)
    return {"status": "success", "report_id": rep.id, "file_path": report_path}

@router.get("/api/reports/{scan_id}")
def get_reports(scan_id: str, db: Session = Depends(get_db)):
    return db.query(repository.models.Report).filter(repository.models.Report.scan_id == scan_id).all()
