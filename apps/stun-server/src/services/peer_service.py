"""
Peer service - Business logic for peer operations
"""

import json
import logging
from typing import Optional
from redis import Redis

from ..models.peer import PeerRegistration, PeerInfo
from ..core.config import get_settings

logger = logging.getLogger(__name__)


class PeerService:
    """Service class handling peer operations with Redis storage"""
    
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.settings = get_settings()
        self.prefix = self.settings.redis_peer_prefix
    
    def _get_key(self, username: str) -> str:
        """Generate Redis key for a peer"""
        return f"{self.prefix}{username}"
    
    def register_peer(self, peer: PeerRegistration) -> dict:
        """
        Register a new peer in Redis.
        
        Args:
            peer: PeerRegistration model with username, ip, port
            
        Returns:
            dict with peer information
            
        Raises:
            ValueError: If username already exists
        """
        key = self._get_key(peer.username)
        
        # Check if peer already exists
        if self.redis.exists(key):
            logger.warning(f"Duplicate registration attempt: {peer.username}")
            raise ValueError(f"Username '{peer.username}' is already registered")
        
        # Store peer data as JSON
        peer_data = {
            "username": peer.username,
            "ip": peer.ip,
            "port": peer.port
        }
        
        self.redis.set(key, json.dumps(peer_data))
        logger.info(f"Peer registered: {peer.username} - {peer.ip}:{peer.port}")
        
        return peer_data
    
    def get_peer(self, username: str) -> Optional[dict]:
        """
        Get peer information by username.
        
        Args:
            username: Peer username
            
        Returns:
            dict with peer information or None if not found
        """
        key = self._get_key(username)
        data = self.redis.get(key)
        
        if data is None:
            logger.warning(f"Peer not found: {username}")
            return None
        
        logger.info(f"Retrieved peer info: {username}")
        return json.loads(data)
    
    def get_all_peers(self) -> list[str]:
        """
        Get list of all registered peer usernames.
        
        Returns:
            list of usernames
        """
        pattern = f"{self.prefix}*"
        keys = self.redis.keys(pattern)
        
        # Extract usernames from keys (remove prefix)
        usernames = [key.replace(self.prefix, '') for key in keys]
        
        logger.info(f"Retrieved peers list - count: {len(usernames)}")
        return sorted(usernames)
    
    def unregister_peer(self, username: str) -> bool:
        """
        Remove a peer from Redis.
        
        Args:
            username: Peer username to remove
            
        Returns:
            True if peer was removed, False if not found
        """
        key = self._get_key(username)
        deleted = self.redis.delete(key)
        
        if deleted:
            logger.info(f"Peer unregistered: {username}")
            return True
        else:
            logger.warning(f"Attempted to unregister non-existent peer: {username}")
            return False
    
    def get_peer_count(self) -> int:
        """
        Get total number of registered peers.
        
        Returns:
            Number of peers
        """
        pattern = f"{self.prefix}*"
        count = len(self.redis.keys(pattern))
        return count
