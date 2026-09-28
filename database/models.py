from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class Scan(Base):
    __tablename__ = "scans"
    id = Column(String, primary_key=True, index=True)
    target = Column(String)
    started_at = Column(DateTime, default=utc_now)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String, default="Running")
    total_findings = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)
    informational_count = Column(Integer, default=0)

    findings = relationship("FindingModel", back_populates="scan")
    reports = relationship("Report", back_populates="scan")

class FindingModel(Base):
    __tablename__ = "findings"
    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scans.id"))
    finding_id = Column(String)
    title = Column(String)
    description = Column(Text)
    category = Column(String)
    affected_component = Column(String)
    severity = Column(String)
    cvss_score = Column(Float)
    cvss_vector = Column(String, nullable=True)
    impact = Column(Text)
    business_impact = Column(Text)
    root_cause = Column(Text)
    remediation = Column(Text)
    status = Column(String, default="Open")
    created_at = Column(DateTime, default=utc_now)

    scan = relationship("Scan", back_populates="findings")
    evidence = relationship("EvidenceModel", back_populates="finding")

class EvidenceModel(Base):
    __tablename__ = "evidence"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    finding_id = Column(String, ForeignKey("findings.id"))
    evidence_type = Column(String)
    description = Column(Text)
    source = Column(String)
    timestamp = Column(DateTime, default=utc_now)
    redacted_content = Column(Text)

    finding = relationship("FindingModel", back_populates="evidence")

class Report(Base):
    __tablename__ = "reports"
    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scans.id"))
    report_type = Column(String)
    file_path = Column(String)
    created_at = Column(DateTime, default=utc_now)

    scan = relationship("Scan", back_populates="reports")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=utc_now)
    event = Column(String)
    component = Column(String)
    status = Column(String)
    message = Column(Text)
