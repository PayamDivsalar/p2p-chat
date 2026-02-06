"""
API module - FastAPI routes and dependencies
"""

from .dependencies import get_redis, get_peer_service
from .endpoints import peers_router, health_router

__all__ = [
    'get_redis',
    'get_peer_service',
    'peers_router',
    'health_router'
]
