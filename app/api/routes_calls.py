import time
import uuid
from fastapi import APIRouter, HTTPException
from app.agent.schemas import CallRequest, CallStatus
from app.agent.orchestrator import run_call
from app.data.store import Store
from app.observability.metrics import Metrics

router = APIRouter()
store = Store()
metrics = Metrics()

@router.post("", response_model=CallStatus)
def create_call(req: CallRequest):
    call_id = str(uuid.uuid4())
    start = time.time()

    # Persist initial state
    store.create_call(call_id, req)

    # Run “call” synchronously for MVP (real systems use async workers)
    result = run_call(call_id=call_id, req=req, store=store, metrics=metrics)

    metrics.observe_latency("call_total_latency_sec", time.time() - start)
    store.complete_call(call_id, result)

    return store.get_call(call_id)

@router.get("/{call_id}", response_model=CallStatus)
def get_call(call_id: str):
    call = store.get_call(call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call