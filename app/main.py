from fastapi import FastAPI
from app.api.routes_calls import router as calls_router

app = FastAPI(title="Call Center AI Assistant (Local Simulation)", version="0.1.0")
app.include_router(calls_router, prefix="/calls", tags=["calls"])