"""
Redis client manager - Handles Redis connection lifecycle
"""

import redis
from typing import Optional
import logging
from .config import get_settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper with connection management"""
    
    def __init__(self):
        self._client: Optional[redis.Redis] = None
        self._settings = get_settings()
    
    def connect(self) -> redis.Redis:
        """
        Establish connection to Redis server.
        Returns the Redis client instance.
        """
        if self._client is None:
            try:
                self._client = redis.Redis(
                    host=self._settings.redis_host,
                    port=self._settings.redis_port,
                    db=self._settings.redis_db,
                    password=self._settings.redis_password if self._settings.redis_password else None,
                    decode_responses=self._settings.redis_decode_responses,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
                # Test connection
                self._client.ping()
                logger.info(f"Connected to Redis at {self._settings.redis_host}:{self._settings.redis_port}")
            except redis.ConnectionError as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise
        
        return self._client
    
    def disconnect(self):
        """Close Redis connection"""
        if self._client:
            self._client.close()
            self._client = None
            logger.info("Disconnected from Redis")
    
    def get_client(self) -> redis.Redis:
        """Get the Redis client, connecting if necessary"""
        if self._client is None:
            return self.connect()
        return self._client
    
    def health_check(self) -> bool:
        """Check if Redis connection is healthy"""
        try:
            client = self.get_client()
            client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False


# Global Redis client instance
_redis_client: Optional[RedisClient] = None


def get_redis_client() -> RedisClient:
    """
    Get global Redis client instance.
    Creates instance on first call (singleton pattern).
    """
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisClient()
    return _redis_client
