"""FastAPI application entry point for XprojectX."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(
    title="XprojectX API",
    description="US Stock Price Movement Predictor — ML-powered directional predictions",
    version="1.0.0",
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


# Router imports
from app.routers import prediction
app.include_router(prediction.router)

# Chat router — will be added in Phase 3
# from app.routers import chat
# app.include_router(chat.router)
