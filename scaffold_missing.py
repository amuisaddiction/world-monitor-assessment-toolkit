import os

workspace = "c:/Users/ankit/Downloads/world-monitor-security-assessment 2"

files = {
    "test_target/security_profile.json": """{
  "application": "World Monitor Demo",
  "authentication": {
    "enabled": true,
    "session_secure": false
  },
  "authorization": {
    "admin_route_requires_role": true,
    "broken_access_control_demo": true
  },
  "headers": {
    "content_security_policy": false,
    "x_content_type_options": true,
    "strict_transport_security": false
  },
  "dependencies": [
    {
      "package": "requests",
      "version": "2.20.0",
      "vulnerable": true,
      "cve": "CVE-2018-18074"
    }
  ]
}""",
    "test_target/app.py": """from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os
import uvicorn

app = FastAPI(title="Mock World Monitor Target", description="Safe local target for SIH demonstration")

PROFILE_PATH = os.path.join(os.path.dirname(__file__), "security_profile.json")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "test_target"}

@app.get("/api/status")
def api_status():
    return {"status": "operational", "version": "1.0.0"}

@app.get("/api/config")
def get_security_profile():
    try:
        with open(PROFILE_PATH, "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except FileNotFoundError:
        return JSONResponse(status_code=500, content={"error": "Security profile not found"})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
""",
    "scanner/finding.py": """from pydantic import BaseModel, Field
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
"""
}

for path, content in files.items():
    full_path = os.path.join(workspace, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Missing files generated successfully.")
