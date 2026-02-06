"""
TCP Server - Listens for incoming peer connections
"""

import socket
import threading
import json
from typing import Callable, Optional
from rich.console import Console

console = Console()


class TCPServer:
    """TCP server to accept incoming peer connections"""
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket: Optional[socket.socket] = None
        self.running = False
        self.on_message_callback: Optional[Callable] = None
        self.on_connect_callback: Optional[Callable] = None
        self.on_disconnect_callback: Optional[Callable] = None
        
    def start(self):
        """Start the TCP server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            console.print(f"[green]✓[/green] TCP Server listening on {self.host}:{self.port}")
            
            # Start accepting connections in a separate thread
            accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
            accept_thread.start()
            
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to start TCP server: {e}")
            raise
    
    def _accept_connections(self):
        """Accept incoming connections"""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                console.print(f"[yellow]→[/yellow] Incoming connection from {client_address}")
                
                # Handle client in a separate thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_address),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    console.print(f"[red]✗[/red] Error accepting connection: {e}")
    
    def _handle_client(self, client_socket: socket.socket, client_address: tuple):
        """Handle individual client connection"""
        peer_username = None
        
        try:
            # Notify connection
            if self.on_connect_callback:
                self.on_connect_callback(client_address)
            
            while self.running:
                # Receive data
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    # Parse JSON message
                    message = json.loads(data.decode('utf-8'))
                    peer_username = message.get('sender', 'Unknown')
                    
                    # Call message callback
                    if self.on_message_callback:
                        self.on_message_callback(message, client_socket)
                        
                except json.JSONDecodeError:
                    console.print(f"[red]✗[/red] Invalid message format from {client_address}")
                    
        except ConnectionResetError:
            console.print(f"[yellow]⚠[/yellow] Connection reset by {peer_username or client_address}")
        except Exception as e:
            console.print(f"[red]✗[/red] Error handling client {peer_username or client_address}: {e}")
        finally:
            # Notify disconnection
            if self.on_disconnect_callback:
                self.on_disconnect_callback(peer_username or str(client_address))
            
            client_socket.close()
            console.print(f"[yellow]←[/yellow] Connection closed with {peer_username or client_address}")
    
    def stop(self):
        """Stop the TCP server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
            console.print("[yellow]⚠[/yellow] TCP Server stopped")
    
    def set_on_message(self, callback: Callable):
        """Set callback for incoming messages"""
        self.on_message_callback = callback
    
    def set_on_connect(self, callback: Callable):
        """Set callback for new connections"""
        self.on_connect_callback = callback
    
    def set_on_disconnect(self, callback: Callable):
        """Set callback for disconnections"""
        self.on_disconnect_callback = callback
