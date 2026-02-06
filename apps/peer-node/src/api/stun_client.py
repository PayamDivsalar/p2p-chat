"""
HTTP Client - Communicates with STUN server
"""

import requests
from typing import List, Optional
from rich.console import Console
from ..models.message import PeerInfo

console = Console()


class STUNClient:
    """HTTP client for STUN server communication"""
    
    def __init__(self, stun_url: str):
        self.stun_url = stun_url.rstrip('/')
        self.api_base = f"{self.stun_url}/api/v1"
    
    def register(self, username: str, ip: str, port: int) -> bool:
        """Register this peer with STUN server"""
        try:
            response = requests.post(
                f"{self.api_base}/register",
                json={
                    "username": username,
                    "ip": ip,
                    "port": port
                },
                timeout=5
            )
            
            if response.status_code == 200:
                console.print(f"[green]✓[/green] Registered with STUN server as '{username}'")
                return True
            else:
                console.print(f"[red]✗[/red] Registration failed: {response.json().get('message', 'Unknown error')}")
                return False
                
        except requests.exceptions.ConnectionError:
            console.print(f"[red]✗[/red] Cannot connect to STUN server at {self.stun_url}")
            return False
        except Exception as e:
            console.print(f"[red]✗[/red] Registration error: {e}")
            return False
    
    def get_peers(self) -> List[PeerInfo]:
        """Get list of all registered peers"""
        try:
            response = requests.get(f"{self.api_base}/peers", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                peers = [PeerInfo(**peer) for peer in data.get('peers', [])]
                return peers
            else:
                console.print(f"[red]✗[/red] Failed to get peers: {response.status_code}")
                return []
                
        except Exception as e:
            console.print(f"[red]✗[/red] Error getting peers: {e}")
            return []
    
    def get_peer_info(self, username: str) -> Optional[PeerInfo]:
        """Get specific peer information"""
        try:
            response = requests.get(
                f"{self.api_base}/peerinfo",
                params={"username": username},
                timeout=5
            )
            
            if response.status_code == 200:
                return PeerInfo(**response.json())
            else:
                console.print(f"[red]✗[/red] Peer '{username}' not found")
                return None
                
        except Exception as e:
            console.print(f"[red]✗[/red] Error getting peer info: {e}")
            return None
    
    def unregister(self, username: str) -> bool:
        """Unregister this peer from STUN server"""
        try:
            response = requests.delete(
                f"{self.api_base}/unregister/{username}",
                timeout=5
            )
            
            if response.status_code == 200:
                console.print(f"[green]✓[/green] Unregistered from STUN server")
                return True
            else:
                console.print(f"[yellow]⚠[/yellow] Unregister warning: {response.status_code}")
                return False
                
        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Unregister error: {e}")
            return False
    
    def health_check(self) -> bool:
        """Check if STUN server is accessible"""
        try:
            response = requests.get(f"{self.stun_url}/health", timeout=3)
            return response.status_code == 200
        except:
            return False
