"""
P2P Chat Peer Node - Main Entry Point
"""

import sys
import signal
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.core.config import get_settings
from src.core.tcp_server import TCPServer
from src.api.stun_client import STUNClient
from src.services.peer_manager import PeerManager
from src.services.chat_service import ChatService

console = Console()


class PeerNode:
    """Main peer node application"""
    
    def __init__(self):
        self.settings = get_settings()
        self.tcp_server = None
        self.stun_client = None
        self.peer_manager = None
        self.chat_service = None
        self.running = False
    
    def start(self):
        """Start the peer node"""
        console.print(Panel.fit(
            f"[bold cyan]P2P Chat Peer Node[/bold cyan]\n"
            f"Username: [yellow]{self.settings.peer_username}[/yellow]\n"
            f"Listening on: [yellow]{self.settings.peer_ip}:{self.settings.peer_port}[/yellow]",
            border_style="cyan"
        ))
        
        # Initialize components
        self.stun_client = STUNClient(self.settings.stun_server_url)
        self.peer_manager = PeerManager()
        self.chat_service = ChatService(self.peer_manager, self.settings.peer_username)
        
        # Check STUN server connectivity
        if not self.stun_client.health_check():
            console.print(f"[red]✗[/red] Cannot reach STUN server at {self.settings.stun_server_url}")
            console.print("[yellow]⚠[/yellow] Make sure STUN server is running")
            return False
        
        # Start TCP server
        self.tcp_server = TCPServer(self.settings.peer_ip, self.settings.peer_port)
        self.tcp_server.set_on_message(self.chat_service.handle_incoming_message)
        
        try:
            self.tcp_server.start()
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to start TCP server: {e}")
            return False
        
        # Register with STUN server
        success = self.stun_client.register(
            self.settings.peer_username,
            self.settings.peer_ip,
            self.settings.peer_port
        )
        
        if not success:
            console.print("[yellow]⚠[/yellow] Failed to register with STUN server")
            self.tcp_server.stop()
            return False
        
        self.running = True
        console.print("\n[green]✓[/green] Peer node is ready!")
        self.show_help()
        
        return True
    
    def stop(self):
        """Stop the peer node"""
        if not self.running:
            return
        
        console.print("\n[yellow]Shutting down...[/yellow]")
        
        # Disconnect from all peers
        if self.peer_manager:
            self.peer_manager.disconnect_all(self.settings.peer_username)
        
        # Unregister from STUN server
        if self.stun_client:
            self.stun_client.unregister(self.settings.peer_username)
        
        # Stop TCP server
        if self.tcp_server:
            self.tcp_server.stop()
        
        self.running = False
        console.print("[green]✓[/green] Peer node stopped")
    
    def show_help(self):
        """Display available commands"""
        console.print("\n[bold]Available Commands:[/bold]")
        console.print("  [cyan]peers[/cyan]              - List all registered peers")
        console.print("  [cyan]connect <username>[/cyan] - Connect to a peer")
        console.print("  [cyan]send <username>[/cyan]    - Send text message to a peer")
        console.print("  [cyan]file <username>[/cyan]    - Send file to a peer")
        console.print("  [cyan]disconnect <username>[/cyan] - Disconnect from a peer")
        console.print("  [cyan]status[/cyan]             - Show connection status")
        console.print("  [cyan]help[/cyan]               - Show this help")
        console.print("  [cyan]quit[/cyan]               - Exit the application\n")
    
    def list_peers(self):
        """List all registered peers from STUN server"""
        peers = self.stun_client.get_peers()
        
        if not peers:
            console.print("[yellow]⚠[/yellow] No peers found")
            return
        
        table = Table(title="Registered Peers")
        table.add_column("Username", style="cyan")
        table.add_column("IP Address", style="yellow")
        table.add_column("Port", style="yellow")
        table.add_column("Status", style="green")
        
        for peer in peers:
            if peer.username == self.settings.peer_username:
                continue  # Skip self
            
            status = "Connected" if self.peer_manager.is_connected(peer.username) else "Available"
            table.add_row(peer.username, peer.ip, str(peer.port), status)
        
        console.print(table)
    
    def connect_to_peer(self, username: str):
        """Connect to a peer"""
        if username == self.settings.peer_username:
            console.print("[yellow]⚠[/yellow] Cannot connect to yourself")
            return
        
        # Get peer info from STUN server
        peer_info = self.stun_client.get_peer_info(username)
        if not peer_info:
            return
        
        # Connect
        self.peer_manager.connect_to_peer(peer_info, self.settings.peer_username)
    
    def send_message(self, username: str):
        """Send a message to a peer"""
        if not self.peer_manager.is_connected(username):
            console.print(f"[yellow]⚠[/yellow] Not connected to {username}. Use 'connect {username}' first.")
            return
        
        console.print(f"[cyan]Chatting with {username}[/cyan] (type 'exit' to stop)")
        
        while True:
            try:
                message = console.input("[bold cyan]You:[/bold cyan] ")
                
                if message.lower() == 'exit':
                    break
                
                if not message.strip():
                    continue
                
                success = self.chat_service.send_text_message(username, message)
                if not success:
                    console.print(f"[red]✗[/red] Failed to send message. Connection may be lost.")
                    break
                    
            except KeyboardInterrupt:
                break
    
    def send_file(self, username: str):
        """Send a file to a peer"""
        if not self.peer_manager.is_connected(username):
            console.print(f"[yellow]⚠[/yellow] Not connected to {username}. Use 'connect {username}' first.")
            return
        
        filepath = console.input("[cyan]File path:[/cyan] ").strip()
        self.chat_service.send_file(username, filepath)
    
    def disconnect_from_peer(self, username: str):
        """Disconnect from a peer"""
        self.peer_manager.disconnect_peer(username, self.settings.peer_username)
    
    def show_status(self):
        """Show current connection status"""
        connected = self.peer_manager.get_connected_peers()
        
        if not connected:
            console.print("[yellow]⚠[/yellow] Not connected to any peers")
        else:
            console.print(f"[green]✓[/green] Connected to {len(connected)} peer(s):")
            for username in connected:
                console.print(f"  • [cyan]{username}[/cyan]")
    
    def run(self):
        """Main CLI loop"""
        if not self.start():
            return
        
        # Setup signal handler for graceful shutdown
        def signal_handler(sig, frame):
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Main command loop
        while self.running:
            try:
                command = console.input("\n[bold green]>[/bold green] ").strip().lower()
                
                if not command:
                    continue
                
                parts = command.split(maxsplit=1)
                cmd = parts[0]
                arg = parts[1] if len(parts) > 1 else None
                
                if cmd == 'peers':
                    self.list_peers()
                
                elif cmd == 'connect':
                    if not arg:
                        console.print("[yellow]⚠[/yellow] Usage: connect <username>")
                    else:
                        self.connect_to_peer(arg)
                
                elif cmd == 'send':
                    if not arg:
                        console.print("[yellow]⚠[/yellow] Usage: send <username>")
                    else:
                        self.send_message(arg)
                
                elif cmd == 'file':
                    if not arg:
                        console.print("[yellow]⚠[/yellow] Usage: file <username>")
                    else:
                        self.send_file(arg)
                
                elif cmd == 'disconnect':
                    if not arg:
                        console.print("[yellow]⚠[/yellow] Usage: disconnect <username>")
                    else:
                        self.disconnect_from_peer(arg)
                
                elif cmd == 'status':
                    self.show_status()
                
                elif cmd == 'help':
                    self.show_help()
                
                elif cmd in ['quit', 'exit']:
                    self.stop()
                    break
                
                else:
                    console.print(f"[yellow]⚠[/yellow] Unknown command: {cmd}")
                    console.print("Type 'help' for available commands")
            
            except EOFError:
                self.stop()
                break
            except Exception as e:
                console.print(f"[red]✗[/red] Error: {e}")


if __name__ == "__main__":
    node = PeerNode()
    node.run()
