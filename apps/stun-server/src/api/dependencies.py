"""
FastAPI dependencies - Shared dependencies for endpoints
"""

from fastapi import Depends
from redis import Redis

from ..core.redis_client import get_redis_client, RedisClient
from ..services.peer_service import PeerService


def get_redis() -> Redis:
    """
    Dependency to get Redis client.
    Used by FastAPI dependency injection.
    """
    redis_client = get_redis_client()
    return redis_client.get_client()


def get_peer_service(redis: Redis = Depends(get_redis)) -> PeerService:
    """
    Dependency to get PeerService instance.
    Used by FastAPI dependency injection.
    """
    return PeerService(redis)
