# Peer Node - P2P Chat Application

## Overview
Peer-to-peer chat node that connects to STUN server and enables direct TCP communication between peers.

## Features
- ✅ TCP Server: Accept incoming peer connections
- ✅ TCP Client: Connect to other peers
- ✅ HTTP Client: Communicate with STUN server
- ✅ Real-time messaging
- ✅ File transfer support
- ✅ Connection management
- ✅ Error handling and notifications

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Configuration (.env)

```env
# Peer identity
PEER_USERNAME=user1
PEER_IP=0.0.0.0
PEER_PORT=9000

# STUN server connection
STUN_SERVER_URL=http://localhost:8000
```

## Usage

### Start Peer Node
```bash
python src/main.py
```

### Available Commands

- `peers` - List all registered peers
- `connect <username>` - Connect to a peer
- `send <username>` - Send text messages
- `file <username>` - Send a file
- `disconnect <username>` - Disconnect from peer
- `status` - Show connection status
- `help` - Show help
- `quit` - Exit application

## Example Workflow

1. **Start STUN server** (in separate terminal):
```bash
cd apps/stun-server
python src/main.py
```

2. **Start first peer** (user1):
```bash
cd apps/peer-node
# .env: PEER_USERNAME=user1, PEER_PORT=9000
python src/main.py
```

3. **Start second peer** (user2):
```bash
cd apps/peer-node
# .env: PEER_USERNAME=user2, PEER_PORT=9001
python src/main.py
```

4. **Connect and chat**:
```
# In user1 terminal:
> peers              # List available peers
> connect user2      # Connect to user2
> send user2         # Start chatting
You: Hello!
user2 → You: Hi there!
exit                 # Exit chat
> file user2         # Send a file
File path: document.pdf
```

## Architecture

```
src/
├── api/
│   └── stun_client.py      # HTTP client for STUN server
├── core/
│   ├── config.py           # Configuration from .env
│   └── tcp_server.py       # TCP server for incoming connections
├── models/
│   └── message.py          # Message data models
├── services/
│   ├── peer_manager.py     # Peer connection management
│   └── chat_service.py     # Chat and file transfer logic
└── main.py                 # Entry point and CLI
```

## Error Handling

- **Connection timeout**: Peer not responding (10 second timeout)
- **Connection refused**: Peer not accepting connections
- **Connection lost during send**: Automatic notification and cleanup
- **STUN server unreachable**: Cannot register/get peer list
- **File not found**: Validation before sending

## File Transfer

Files are received in the `downloads/` directory with automatic duplicate handling.

## Notes

- Each peer acts as both client and server
- Multiple peers can connect simultaneously
- Connections are managed per-peer with thread safety
- All errors are handled gracefully with user notifications
