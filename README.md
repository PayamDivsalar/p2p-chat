# p2p-chat

P2P chat system implementation with two services:
1. **STUN Server**: Peer address management server (HTTP) ✅ Implemented
2. **Peer Node**: Direct TCP communication peer ⏳ In Development

## Project Structure
```
apps/
  stun-server/           ✅ Fully Implemented
    src/
      main.py           # HTTP server with FastAPI
    requirements.txt
    README.md           # Complete documentation
    test_api.py         # API tests
  peer-node/            ⏳ Next
    src/
      main.py
    requirements.txt
libs/
```

## Installation and Setup

### Install Python Dependencies (STUN Server)
```bash
pip install -r apps/stun-server/requirements.txt
```

### Run Services

#### STUN Server
```bash
npm run stun:serve
# or
python apps/stun-server/src/main.py
```

Server runs on `http://localhost:8000`.

#### Test APIs
```bash
python apps/stun-server/test_api.py
```

#### Interactive API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Peer Node (In Development)
```bash
npm run peer:serve
```

## Implementation Roadmap (3 Phases)

### ✅ Phase 1: STUN Server (Completed)
- [x] HTTP server implementation with FastAPI
- [x] Peer registration endpoint (POST /register)
- [x] Peers list endpoint (GET /peers)
- [x] Peer info endpoint (GET /peerinfo)
- [x] In-memory storage
- [x] Data validation (Pydantic)
- [x] Error handling and proper HTTP status codes
- [x] Logging
- [x] API documentation
- [x] Automated tests

**Bonus Features Implemented:**
- ✨ Peer removal endpoint (DELETE /unregister)
- ✨ Health check endpoint (GET /health)
- ✨ Interactive Swagger UI
- ✨ Complete test script

### ⏳ Phase 2: Peer Node Implementation
- [ ] Register with STUN server via HTTP
- [ ] Get peers list from server
- [ ] TCP server implementation for receiving connections
- [ ] TCP client implementation for initiating connections
- [ ] Connection request handling (accept/reject)

### 🔲 Phase 3: Chat and Connection Management
- [ ] Real-time text message sending/receiving
- [ ] Connection drop and error handling
- [ ] Simple CLI interface
- [ ] [Bonus] File transfer
- [ ] [Bonus] Graphical interface

## Current STUN Server Features

✅ **Peer Registration**: POST /register
- Unique username validation (letters/numbers/_/- only)
- IP validation
- Port validation (1024-65535)
- 409 error for duplicate username

✅ **Peers List**: GET /peers
- Total peer count
- Username array

✅ **Peer Info**: GET /peerinfo?username=xxx
- Peer IP and port
- 404 error for non-existent peer

✅ **Peer Removal**: DELETE /unregister/{username}
- Remove from memory
- 404 error for non-existent peer

✅ **Health Check**: GET /health
- Server status
- Active peers count

## Usage Example

```python
import requests

# Register
requests.post('http://localhost:8000/register', json={
    'username': 'alice',
    'ip': '192.168.1.10',
    'port': 5001
})

# Get list
peers = requests.get('http://localhost:8000/peers').json()
print(peers)  # {"count": 1, "peers": ["alice"]}

# Get info
info = requests.get('http://localhost:8000/peerinfo?username=alice').json()
print(info)  # {"username": "alice", "ip": "192.168.1.10", "port": 5001}
```

## Quick Test

```bash
# Run server
npm run stun:serve

# In another terminal - run tests
python apps/stun-server/test_api.py
```

## Future Enhancements

### STUN Server
- 🔲 Redis support
- 🔲 Authentication
- 🔲 Heartbeat mechanism (check peer online status)

### Peer Node
- 🔲 Complete TCP implementation
- 🔲 Concurrent connection management
- 🔲 Message encryption

---

**Project Status**: Phase 1 Complete ✅ | Current: Phase 2 ⏳