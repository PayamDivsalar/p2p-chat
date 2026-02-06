"""
STUN Server - Peer Address Management Server
This HTTP server manages peer (user) information for the P2P chat system.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
import uvicorn
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="P2P Chat STUN Server",
    description="Peer address management server for P2P chat system",
    version="1.0.0"
)

# In-memory storage
# Can be replaced with Redis for persistence
peers_storage: Dict[str, dict] = {}


# Data Models (Pydantic Models)
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
    peers: List[str]


class MessageResponse(BaseModel):
    """General message response model"""
    message: str
    details: Optional[dict] = None


# Endpoints

@app.get("/", response_model=MessageResponse)
async def root():
    """Root endpoint - Server information"""
    return MessageResponse(
        message="P2P Chat STUN Server is running",
        details={
            "endpoints": [
                {"path": "/register", "method": "POST", "description": "Register peer"},
                {"path": "/peers", "method": "GET", "description": "Get list of peers"},
                {"path": "/peerinfo", "method": "GET", "description": "Get peer information"}
            ]
        }
    )


@app.post("/register", status_code=201, response_model=MessageResponse)
async def register_peer(peer: PeerRegistration):
    """
    Register peer credentials
    
    - **username**: Unique username
    - **ip**: Peer IP address
    - **port**: Port number
    """
    # Check if username exists
    if peer.username in peers_storage:
        logger.warning(f"Duplicate registration attempt: {peer.username}")
        raise HTTPException(
            status_code=409,  # Conflict
            detail=f"Username '{peer.username}' is already registered"
        )
    
    # Store peer information
    peers_storage[peer.username] = {
        "username": peer.username,
        "ip": peer.ip,
        "port": peer.port
    }
    
    logger.info(f"Peer registered: {peer.username} - {peer.ip}:{peer.port}")
    
    return MessageResponse(
        message=f"Peer '{peer.username}' registered successfully",
        details={
            "username": peer.username,
            "ip": peer.ip,
            "port": peer.port
        }
    )


@app.get("/peers", response_model=PeerListResponse)
async def get_all_peers():
    """
    Get list of all peers
    
    Returns a list of all registered peer usernames
    """
    peer_usernames = list(peers_storage.keys())
    
    logger.info(f"Peers list requested - count: {len(peer_usernames)}")
    
    return PeerListResponse(
        count=len(peer_usernames),
        peers=peer_usernames
    )


@app.get("/peerinfo", response_model=PeerInfo)
async def get_peer_info(username: str = Query(..., description="Target peer username")):
    """
    Get information about a specific peer
    
    - **username**: Target peer username
    """
    # Check if peer exists
    if username not in peers_storage:
        logger.warning(f"Peer not found: {username}")
        raise HTTPException(
            status_code=404,
            detail=f"Peer with username '{username}' not found"
        )
    
    peer_data = peers_storage[username]
    logger.info(f"Sending peer info: {username}")
    
    return PeerInfo(**peer_data)


@app.delete("/unregister/{username}", response_model=MessageResponse)
async def unregister_peer(username: str):
    """
    Remove peer from system (optional - for better management)
    
    - **username**: Username of the peer to be removed from system
    """
    if username not in peers_storage:
        raise HTTPException(
            status_code=404,
            detail=f"Peer with username '{username}' not found"
        )
    
    del peers_storage[username]
    logger.info(f"Peer unregistered: {username}")
    
    return MessageResponse(
        message=f"Peer '{username}' unregistered successfully"
    )


@app.get("/health")
async def health_check():
    """Server health check"""
    return {
        "status": "healthy",
        "peers_count": len(peers_storage)
    }


def main() -> None:
    """Run STUN server"""
    logger.info("Starting STUN server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()
