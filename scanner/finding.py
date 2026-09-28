from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

class Evidence(BaseModel):
    description: str
    data: Dict[str, Any]

class Finding(BaseModel):
    id: str = Field(default_factory=lambda: f"SEC-{str(uuid.uuid4())[:8].upper()}")
    title: str
    description: str
    category: str
    affected_component: str
    severity: str
    cvss_score: float = 0.0
    cvss_vector: Optional[str] = None
    evidence: List[Evidence] = []
    impact: str
    business_impact: str
    root_cause: str
    remediation: str
    status: str = "Open"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
