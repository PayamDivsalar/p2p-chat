"""
Pydantic models for peer data structures
"""

from pydantic import BaseModel, Field, validator
from typing import Optional


class PeerRegistration(BaseModel):
    """Peer registration model"""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    ip: str = Field(..., description="Peer IP address")
    port: int = Field(..., ge=1024, le=65535, description="Port number (1024-65535)")
    
    @validator('username')
    def username_alphanumeric(cls, v):
        """Validate that username contains only letters, numbers, _ and -"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, _ and -')
        return v
    
    @validator('ip')
    def validate_ip(cls, v):
        """Simple IP format validation"""
        parts = v.split('.')
        if len(parts) != 4:
            raise ValueError('Invalid IP format')
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                raise ValueError('Invalid IP format')
        return v


class PeerInfo(BaseModel):
    """Peer information model"""
    username: str
    ip: str
    port: int


class PeerListResponse(BaseModel):
    """Peer list response model"""
    count: int
    peers: list[str]


class MessageResponse(BaseModel):
    """General message response model"""
    message: str
    details: Optional[dict] = None

