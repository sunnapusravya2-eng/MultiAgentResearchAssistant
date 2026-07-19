from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.logging import logger

app = FastAPI(
    title="Multi-Agent AI Research Assistant",
    version="1.0.0",
    description="Backend API for document ingestion, retrieval, chat, and report generation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

logger.info("Backend application initialized")