from pydantic import BaseModel
from typing import List, Optional

class ScanRequest(BaseModel):
    target_url: str = "http://127.0.0.1:8080"
    
class ScanResponse(BaseModel):
    id: str
    target: str
    status: str
    
class UpdateFindingRequest(BaseModel):
    status: str
