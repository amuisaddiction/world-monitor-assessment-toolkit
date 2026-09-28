from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database import repository
from database.models import FindingModel

router = APIRouter()

@router.get("/api/findings")
def get_findings(scan_id: str = None, db: Session = Depends(get_db)):
    return repository.get_findings(db, scan_id)

@router.get("/api/findings/{finding_id}")
def get_finding(finding_id: str, db: Session = Depends(get_db)):
    finding = db.query(FindingModel).filter(FindingModel.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return finding
