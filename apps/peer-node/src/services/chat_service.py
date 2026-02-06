"""
Chat Service - Handles messaging and file transfer
"""

import os
from pathlib import Path
from typing import Optional
from rich.console import Console
from ..services.peer_manager import PeerManager
from ..models.message import TextMessage, FileMessage

console = Console()


class ChatService:
    """Service for handling chat messages and file transfers"""
    
    def __init__(self, peer_manager: PeerManager, username: str):
        self.peer_manager = peer_manager
        self.username = username
        self.download_dir = Path("downloads")
        self.download_dir.mkdir(exist_ok=True)
    
    def send_text_message(self, target_username: str, content: str) -> bool:
        """Send a text message to a peer"""
        if not self.peer_manager.is_connected(target_username):
            console.print(f"[yellow]⚠[/yellow] Not connected to {target_username}")
            return False
        
        message = TextMessage(
            sender=self.username,
            content=content
        )
        
        success = self.peer_manager.send_to_peer(
            target_username,
            message.model_dump()
        )
        
        if success:
            console.print(f"[cyan]You → {target_username}:[/cyan] {content}")
        else:
            console.print(f"[red]✗[/red] Failed to send message to {target_username}")
            console.print(f"[yellow]⚠[/yellow] Connection may have been lost. Try reconnecting.")
        
        return success
    
    def send_file(self, target_username: str, filepath: str) -> bool:
        """Send a file to a peer"""
        if not self.peer_manager.is_connected(target_username):
            console.print(f"[yellow]⚠[/yellow] Not connected to {target_username}")
            return False
        
        try:
            file_path = Path(filepath)
            if not file_path.exists():
                console.print(f"[red]✗[/red] File not found: {filepath}")
                return False
            
            # Read file
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            message = FileMessage(
                sender=self.username,
                filename=file_path.name,
                filesize=len(file_data),
                content=file_data
            )
            
            # Convert to dict (bytes will be base64 encoded by pydantic)
            message_dict = message.model_dump()
            
            console.print(f"[cyan]→[/cyan] Sending file '{file_path.name}' ({len(file_data)} bytes) to {target_username}...")
            
            success = self.peer_manager.send_to_peer(target_username, message_dict)
            
            if success:
                console.print(f"[green]✓[/green] File sent successfully to {target_username}")
            else:
                console.print(f"[red]✗[/red] Failed to send file to {target_username}")
                console.print(f"[yellow]⚠[/yellow] Connection may have been lost during transfer.")
            
            return success
            
        except Exception as e:
            console.print(f"[red]✗[/red] Error sending file: {e}")
            return False
    
    def handle_incoming_message(self, message: dict, client_socket=None):
        """Handle incoming message from a peer"""
        msg_type = message.get('type')
        sender = message.get('sender', 'Unknown')
        
        if msg_type == 'text':
            # Text message
            content = message.get('content', '')
            console.print(f"[green]{sender} → You:[/green] {content}")
        
        elif msg_type == 'file':
            # File transfer
            filename = message.get('filename', 'unknown')
            filesize = message.get('filesize', 0)
            file_content = message.get('content', b'')
            
            try:
                # Save file
                save_path = self.download_dir / filename
                
                # Handle duplicate names
                counter = 1
                while save_path.exists():
                    name_parts = filename.rsplit('.', 1)
                    if len(name_parts) == 2:
                        save_path = self.download_dir / f"{name_parts[0]}_{counter}.{name_parts[1]}"
                    else:
                        save_path = self.download_dir / f"{filename}_{counter}"
                    counter += 1
                
                with open(save_path, 'wb') as f:
                    f.write(file_content)
                
                console.print(f"[green]✓[/green] Received file '{filename}' ({filesize} bytes) from {sender}")
                console.print(f"[cyan]→[/cyan] Saved to: {save_path}")
                
            except Exception as e:
                console.print(f"[red]✗[/red] Error saving file from {sender}: {e}")
        
        elif msg_type == 'connect':
            # Connection request
            msg = message.get('message', '')
            console.print(f"[yellow]→[/yellow] {sender} connected: {msg}")
        
        elif msg_type == 'disconnect':
            # Disconnect notification
            msg = message.get('message', '')
            console.print(f"[yellow]←[/yellow] {sender} disconnected: {msg}")
        
        else:
            console.print(f"[yellow]⚠[/yellow] Unknown message type from {sender}: {msg_type}")
