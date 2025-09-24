from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from api.routes import translation, health, quality
from core.translation_service import TranslationService
from core.config import settings


load_dotenv()

# Global service instance
translation_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global translation_service
    # Startup
    translation_service = TranslationService()
    yield
    # Shutdown
    translation_service = None

# Create FastAPI app 
# Todo: fix local docs_url
app = FastAPI(
    title=" Translation Service",
    description="Professional AI Translation Microservice with Multi-Agent Architecture",
    root_path="/translation-service",
    version="1.0.0",
    # docs_url="/translation-service/docs",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(translation.router, prefix="/api/v1", tags=["translation"])
app.include_router(quality.router, prefix="/api/v1", tags=["quality"])

@app.get("/")
async def root():

    return {
        "message": "langTranslator Translation Service",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "type": "internal_error"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

