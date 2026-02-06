"""
Application configuration - Settings loaded from environment variables
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Peer node settings loaded from environment variables"""
    
    # Peer identity
    peer_username: str = "user1"
    peer_ip: str = "0.0.0.0"
    peer_port: int = 9000
    
    # STUN server connection
    stun_server_url: str = "http://localhost:8000"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to avoid reading .env multiple times.
    """
    return Settings()
