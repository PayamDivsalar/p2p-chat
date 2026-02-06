"""
Peer Manager - Manages active peer connections
"""

import socket
import json
import threading
from typing import Dict, Optional
from rich.console import Console
from ..models.message import PeerInfo

console = Console()


class PeerConnection:
    """Represents a connection to a peer"""
    
    def __init__(self, peer_info: PeerInfo, sock: socket.socket):
        self.peer_info = peer_info
        self.socket = sock
        self.connected = True
        self.lock = threading.Lock()
    
    def send_message(self, message: dict) -> bool:
        """Send a message to this peer"""
        with self.lock:
            if not self.connected:
                console.print(f"[yellow]⚠[/yellow] Cannot send: not connected to {self.peer_info.username}")
                return False
            
            try:
                message_bytes = json.dumps(message).encode('utf-8')
                self.socket.sendall(message_bytes)
                return True
            except BrokenPipeError:
                console.print(f"[red]✗[/red] Connection broken: peer {self.peer_info.username} disconnected during send")
                self.connected = False
                return False
            except Exception as e:
                console.print(f"[red]✗[/red] Error sending to {self.peer_info.username}: {e}")
                self.connected = False
                return False
    
    def close(self):
        """Close this connection"""
        with self.lock:
            if self.connected:
                try:
                    self.socket.close()
                except:
                    pass
                self.connected = False


class PeerManager:
    """Manages connections to multiple peers"""
    
    def __init__(self):
        self.connections: Dict[str, PeerConnection] = {}
        self.lock = threading.Lock()
    
    def connect_to_peer(self, peer_info: PeerInfo, sender_username: str) -> bool:
        """Connect to a peer as a TCP client"""
        with self.lock:
            # Check if already connected
            if peer_info.username in self.connections:
                console.print(f"[yellow]⚠[/yellow] Already connected to {peer_info.username}")
                return True
        
        try:
            # Create TCP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            console.print(f"[cyan]→[/cyan] Connecting to {peer_info.username} at {peer_info.ip}:{peer_info.port}...")
            sock.connect((peer_info.ip, peer_info.port))
            
            # Send connection request
            connect_msg = {
                "type": "connect",
                "sender": sender_username,
                "message": f"Connection request from {sender_username}"
            }
            sock.sendall(json.dumps(connect_msg).encode('utf-8'))
            
            # Store connection
            with self.lock:
                self.connections[peer_info.username] = PeerConnection(peer_info, sock)
            
            console.print(f"[green]✓[/green] Connected to {peer_info.username}")
            return True
            
        except socket.timeout:
            console.print(f"[red]✗[/red] Connection timeout: {peer_info.username} is not responding")
            return False
        except ConnectionRefusedError:
            console.print(f"[red]✗[/red] Connection refused: {peer_info.username} is not accepting connections")
            return False
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to connect to {peer_info.username}: {e}")
            return False
    
    def send_to_peer(self, username: str, message: dict) -> bool:
        """Send a message to a connected peer"""
        with self.lock:
            connection = self.connections.get(username)
        
        if not connection:
            console.print(f"[yellow]⚠[/yellow] Not connected to {username}")
            return False
        
        success = connection.send_message(message)
        
        # Remove if connection failed
        if not success:
            with self.lock:
                if username in self.connections:
                    del self.connections[username]
        
        return success
    
    def disconnect_peer(self, username: str, sender_username: str):
        """Disconnect from a peer"""
        with self.lock:
            connection = self.connections.get(username)
            if connection:
                # Send disconnect message
                disconnect_msg = {
                    "type": "disconnect",
                    "sender": sender_username,
                    "message": f"{sender_username} has disconnected"
                }
                connection.send_message(disconnect_msg)
                connection.close()
                del self.connections[username]
                console.print(f"[yellow]←[/yellow] Disconnected from {username}")
            else:
                console.print(f"[yellow]⚠[/yellow] Not connected to {username}")
    
    def disconnect_all(self, sender_username: str):
        """Disconnect from all peers"""
        with self.lock:
            for username, connection in list(self.connections.items()):
                disconnect_msg = {
                    "type": "disconnect",
                    "sender": sender_username,
                    "message": f"{sender_username} has disconnected"
                }
                connection.send_message(disconnect_msg)
                connection.close()
            self.connections.clear()
            console.print("[yellow]←[/yellow] Disconnected from all peers")
    
    def get_connected_peers(self) -> list:
        """Get list of connected peer usernames"""
        with self.lock:
            return list(self.connections.keys())
    
    def is_connected(self, username: str) -> bool:
        """Check if connected to a peer"""
        with self.lock:
            return username in self.connections
