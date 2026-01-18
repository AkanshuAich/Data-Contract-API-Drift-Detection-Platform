from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class APIEventCreate(BaseModel):
    service: str
    environment: str
    endpoint: str
    method: str
    request_body: Optional[Dict[str, Any]]
    response_body: Optional[Dict[str, Any]]
    status_code: int
    timestamp: datetime
