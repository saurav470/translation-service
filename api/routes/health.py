"""
Health check endpoints
"""

from fastapi import APIRouter, Depends
from api.models import HealthResponse
from core.translation_service import TranslationService
import time
import os

router = APIRouter()

# Global start time for uptime calculation
start_time = time.time()

def get_translation_service() -> TranslationService:
    """Dependency to get translation service instance"""
    from main import translation_service
    if translation_service is None:
        raise Exception("Translation service not initialized")
    return translation_service

@router.get("/health", response_model=HealthResponse)
async def health_check(service: TranslationService = Depends(get_translation_service)):
    """Health check endpoint"""
    try:
        # Check service health
        health_status = service.get_health_status()
        
        # Check dependencies
        dependencies = {
            "openai_api": bool(os.getenv("OPENAI_API_KEY")),
            "translation_service": health_status["agents_initialized"],
            "database": True  # For now, always true
        }
        
        # Determine overall status
        all_healthy = all(dependencies.values())
        status = "healthy" if all_healthy else "degraded"
        
        return HealthResponse(
            status=status,
            version="1.0.0",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            uptime=time.time() - start_time,
            dependencies=dependencies
        )
        
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            version="1.0.0",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            uptime=time.time() - start_time,
            dependencies={"error": str(e)}
        )

@router.get("/health/live")
async def liveness_check():
    """Liveness probe for Kubernetes"""
    return {"status": "alive", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

@router.get("/health/ready")
async def readiness_check(service: TranslationService = Depends(get_translation_service)):
    """Readiness probe for Kubernetes"""
    try:
        health_status = service.get_health_status()
        if health_status["agents_initialized"]:
            return {"status": "ready", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        else:
            return {"status": "not_ready", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    except Exception as e:
        return {"status": "not_ready", "error": str(e), "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

