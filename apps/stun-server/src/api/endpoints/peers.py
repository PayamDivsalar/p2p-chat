"""
Peer-related API endpoints
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status

from ...models.peer import (
    PeerRegistration,
    PeerInfo,
    PeerListResponse,
    MessageResponse
)
from ...services.peer_service import PeerService
from ..dependencies import get_peer_service

router = APIRouter(prefix="/api/v1", tags=["peers"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse,
    summary="Register a new peer",
    responses={
        201: {"description": "Peer registered successfully"},
        409: {"description": "Username already exists"},
        422: {"description": "Validation error"}
    }
)
async def register_peer(
    peer: PeerRegistration,
    service: PeerService = Depends(get_peer_service)
):
    """
    Register peer credentials.
    
    - **username**: Unique username (3-50 characters, alphanumeric with _ and -)
    - **ip**: Valid IPv4 address
    - **port**: Port number (1024-65535)
    """
    try:
        peer_data = service.register_peer(peer)
        return MessageResponse(
            message=f"Peer '{peer.username}' registered successfully",
            details=peer_data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get(
    "/peers",
    response_model=PeerListResponse,
    summary="Get list of all peers",
    responses={
        200: {"description": "List of registered peers"}
    }
)
async def get_all_peers(service: PeerService = Depends(get_peer_service)):
    """
    Get list of all registered peers.
    
    Returns a list of all registered peer usernames.
    """
    peers = service.get_all_peers()
    return PeerListResponse(
        count=len(peers),
        peers=peers
    )


@router.get(
    "/peerinfo",
    response_model=PeerInfo,
    summary="Get information about a specific peer",
    responses={
        200: {"description": "Peer information retrieved"},
        404: {"description": "Peer not found"}
    }
)
async def get_peer_info(
    username: str = Query(..., description="Target peer username"),
    service: PeerService = Depends(get_peer_service)
):
    """
    Get information about a specific peer.
    
    - **username**: Target peer username
    """
    peer_data = service.get_peer(username)
    
    if peer_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Peer with username '{username}' not found"
        )
    
    return PeerInfo(**peer_data)


@router.delete(
    "/unregister/{username}",
    response_model=MessageResponse,
    summary="Remove a peer from the system",
    responses={
        200: {"description": "Peer unregistered successfully"},
        404: {"description": "Peer not found"}
    }
)
async def unregister_peer(
    username: str,
    service: PeerService = Depends(get_peer_service)
):
    """
    Remove peer from system.
    
    - **username**: Username of the peer to be removed
    """
    success = service.unregister_peer(username)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Peer with username '{username}' not found"
        )
    
    return MessageResponse(
        message=f"Peer '{username}' unregistered successfully"
    )
