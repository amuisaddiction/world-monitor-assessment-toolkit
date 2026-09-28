from sqlalchemy.orm import Session
from database import models
from datetime import datetime, timezone
import uuid
import json

def create_scan(db: Session, target: str) -> models.Scan:
    scan_id = str(uuid.uuid4())
    db_scan = models.Scan(id=scan_id, target=target)
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan

def complete_scan(db: Session, scan_id: str, findings: list) -> models.Scan:
    db_scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not db_scan:
        return None
    db_scan.status = "Completed"
    db_scan.completed_at = datetime.now(timezone.utc)
    db_scan.total_findings = len(findings)
    db_scan.critical_count = sum(1 for f in findings if f.severity == "Critical")
    db_scan.high_count = sum(1 for f in findings if f.severity == "High")
    db_scan.medium_count = sum(1 for f in findings if f.severity == "Medium")
    db_scan.low_count = sum(1 for f in findings if f.severity == "Low")
    db.commit()
    db.refresh(db_scan)
    return db_scan

def save_finding(db: Session, scan_id: str, finding_data) -> models.FindingModel:
    db_finding = models.FindingModel(
        id=str(uuid.uuid4()),
        scan_id=scan_id,
        finding_id=finding_data.id,
        title=finding_data.title,
        description=finding_data.description,
        category=finding_data.category,
        affected_component=finding_data.affected_component,
        severity=finding_data.severity,
        cvss_score=finding_data.cvss_score,
        cvss_vector=finding_data.cvss_vector,
        impact=finding_data.impact,
        business_impact=finding_data.business_impact,
        root_cause=finding_data.root_cause,
        remediation=finding_data.remediation,
        status=finding_data.status
    )
    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)
    
    for ev in finding_data.evidence:
        save_evidence(db, db_finding.id, ev)
        
    return db_finding

def save_evidence(db: Session, db_finding_id: str, evidence) -> models.EvidenceModel:
    redacted = json.dumps(evidence.data)
    db_evidence = models.EvidenceModel(
        finding_id=db_finding_id,
        evidence_type="json",
        description=evidence.description,
        redacted_content=redacted
    )
    db.add(db_evidence)
    db.commit()
    return db_evidence

def get_scans(db: Session, limit: int = 100):
    return db.query(models.Scan).order_by(models.Scan.started_at.desc()).limit(limit).all()

def get_scan(db: Session, scan_id: str):
    return db.query(models.Scan).filter(models.Scan.id == scan_id).first()

def get_findings(db: Session, scan_id: str = None):
    q = db.query(models.FindingModel)
    if scan_id:
        q = q.filter(models.FindingModel.scan_id == scan_id)
    return q.all()

def save_report(db: Session, scan_id: str, file_path: str, report_type: str = "Markdown") -> models.Report:
    report = models.Report(
        id=str(uuid.uuid4()),
        scan_id=scan_id,
        file_path=file_path,
        report_type=report_type
    )
    db.add(report)
    db.commit()
    return report

def create_audit_log(db: Session, event: str, component: str, status: str, message: str):
    log = models.AuditLog(
        event=event,
        component=component,
        status=status,
        message=message
    )
    db.add(log)
    db.commit()
