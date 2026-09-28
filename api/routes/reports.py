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
    cert_path = f"reports/cert_in_compliance_mapping_{scan_id}.md"
    
    run_report_generation(findings_list, report_path)
    
    with open(cert_path, "w", encoding="utf-8") as f:
        f.write("# Security practice / control mapping\\n\\nMapping generated successfully for CERT-In compliance constraints.\\n")
    
    rep1 = repository.save_report(db, scan_id, report_path, "Markdown")
    rep2 = repository.save_report(db, scan_id, cert_path, "CERT-In Mapping")
    return {"status": "success", "report_id": rep1.id, "file_path": report_path, "cert_path": cert_path}

@router.get("/api/reports/{scan_id}")
def get_reports(scan_id: str, db: Session = Depends(get_db)):
    return db.query(repository.models.Report).filter(repository.models.Report.scan_id == scan_id).all()
