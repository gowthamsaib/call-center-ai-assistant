from __future__ import annotations

from typing import Any, Dict, Optional

from app.agent.schemas import CallRequest, CallResult, CallStatus


class Store:
    """
    In-memory store for MVP. In production, this would be backed by Postgres/Redis.
    """
    def __init__(self):
        self._calls: Dict[str, Dict[str, Any]] = {}

    def create_call(self, call_id: str, req: CallRequest) -> None:
        self._calls[call_id] = {
            "call_id": call_id,
            "status": "running",
            "request": req,
            "transcript": [],
            "extracted_fields": {},
            "metrics": {},
        }

    def complete_call(self, call_id: str, result: CallResult) -> None:
        if call_id not in self._calls:
            # For safety in case of misuse
            return

        self._calls[call_id]["status"] = "completed"
        self._calls[call_id]["transcript"] = result.transcript
        self._calls[call_id]["extracted_fields"] = result.extracted_fields
        self._calls[call_id]["metrics"] = {
            "tool_calls": result.tool_calls,
            "fallback_rate": result.fallback_rate,
        }

    def get_call(self, call_id: str) -> Optional[CallStatus]:
        if call_id not in self._calls:
            return None

        obj = self._calls[call_id]
        # Pydantic will validate nested models (CallRequest, Turn, etc.)
        return CallStatus(**obj)
