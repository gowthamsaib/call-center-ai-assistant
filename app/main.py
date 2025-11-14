from fastapi import FastAPI
from app.api.router_calls import router as calls_router

app = FastAPI(title="Call Center AI Assistant Simulation", version="0.1.0")
app.include_router(calls_router, prefix="/calls", tags=["calls"])

@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs", "health": "/health"}