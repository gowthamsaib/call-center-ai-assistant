from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CallRequest(BaseModel):
    customer_name: str = Field(..., examples=["Alex"])
    member_id: str = Field(..., examples=["M-10293"])
    task: str = Field(..., examples=["Freeze membership for 2 months due to travel"])
    schema: List[str] = Field(default_factory=lambda: [
        "issue_type","requested_action","sentiment","resolution_summary","next_step"
    ])

class Turn(BaseModel):
    role: str  # "agent" | "user"
    text: str

class CallResult(BaseModel):
    transcript: List[Turn]
    extracted_fields: Dict[str, Any]
    tool_calls: int = 0
    fallback_rate: float = 0.0

class CallStatus(BaseModel):
    call_id: str
    status: str  # "completed"
    request: CallRequest
    transcript: List[Turn]
    extracted_fields: Dict[str, Any]
    metrics: Dict[str, Any]
