"""
Health check and system status endpoints
"""

from fastapi import APIRouter, Depends

from ...models.peer import MessageResponse
from ...services.peer_service import PeerService
from ...core.redis_client import get_redis_client
from ..dependencies import get_peer_service

router = APIRouter(tags=["health"])


@router.get("/", response_model=MessageResponse)
async def root():
    """Root endpoint - Server information"""
    return MessageResponse(
        message="P2P Chat STUN Server is running",
        details={
            "version": "1.0.0",
            "storage": "Redis",
            "endpoints": [
                {"path": "/api/v1/register", "method": "POST", "description": "Register peer"},
                {"path": "/api/v1/peers", "method": "GET", "description": "Get list of peers"},
                {"path": "/api/v1/peerinfo", "method": "GET", "description": "Get peer information"},
                {"path": "/api/v1/unregister/{username}", "method": "DELETE", "description": "Unregister peer"}
            ]
        }
    )


@router.get("/health")
async def health_check(service: PeerService = Depends(get_peer_service)):
    """
    Server health check.
    
    Checks Redis connection and returns peer count.
    """
    redis_client = get_redis_client()
    redis_healthy = redis_client.health_check()
    
    peer_count = service.get_peer_count() if redis_healthy else 0
    
    return {
        "status": "healthy" if redis_healthy else "unhealthy",
        "redis_connected": redis_healthy,
        "peers_count": peer_count
    }
