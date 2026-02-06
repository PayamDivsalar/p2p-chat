# p2p-chat

P2P chat system implementation with two services:
1. **STUN Server**: Peer address management server (HTTP + Redis) ✅ Fully Implemented
2. **Peer Node**: Direct TCP communication peer ⏳ In Development

## Project Structure
```
apps/
  stun-server/                   ✅ Production-Ready Architecture
    src/
      api/                        # API Layer
        endpoints/
          peers.py                # Peer management endpoints  
          health.py               # Health check endpoints
        dependencies.py           # FastAPI DI
      core/                       # Core functionality
        config.py                 # Configuration management
        redis_client.py           # Redis connection manager
      models/                     # Data models
        peer.py                   # Pydantic models
      services/                   # Business logic
        peer_service.py           # Peer operations
      main.py                     # Application entry point
    .env                          # Environment configuration
    .env.example                  # Example configuration
    requirements.txt              # Python dependencies
    project.json                  # Nx configuration
    README.md                     # Complete documentation
    test_api.py                   # API tests
    
  peer-node/                      ⏳ Next Phase
    src/
      main.py
    requirements.txt
    
docker-compose.yml                # Redis container
.gitignore
package.json
nx.json
README.md                         # This file
```

## Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (for Redis)
- Node.js (for Nx scripts)

### 1. Start Redis
```bash
docker-compose up -d
```

### 2. Install STUN Server Dependencies
```bash
pip install -r apps/stun-server/requirements.txt
```

### 3. Run STUN Server
```bash
npm run stun:serve
```

Server runs on `http://localhost:8000`

### 4. Test APIs
```bash
python apps/stun-server/test_api.py
```

### 5. View API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## STUN Server Architecture

### Clean Architecture Implementation

✅ **Separation of Concerns**
- API Layer: HTTP handling, validation
- Service Layer: Business logic
- Core Layer: Infrastructure (Redis, config)
- Models: Data structures

✅ **Design Patterns**
- Dependency Injection (FastAPI)
- Repository Pattern (PeerService)
- Singleton (RedisClient)
- Settings management (Pydantic Settings)

✅ **Redis-Only Storage**
- Persistent data storage
- Production-ready
- No in-memory fallback
- Docker Compose integration

### API Endpoints

All endpoints under `/api/v1/` prefix:

- `POST /api/v1/register` - Register new peer
- `GET /api/v1/peers` - Get all peers list  
- `GET /api/v1/peerinfo?username=alice` - Get peer info
- `DELETE /api/v1/unregister/{username}` - Remove peer
- `GET /health` - Health check + Redis status
- `GET /` - Server information

## Implementation Roadmap (3 Phases)

### ✅ Phase 1: STUN Server (COMPLETED)
- [x] Clean architecture implementation
- [x] API layer with proper endpoints
- [x] Service layer with business logic
- [x] Redis integration (exclusive storage)
- [x] Configuration management with .env
- [x] Docker Compose for Redis
- [x] Dependency injection pattern
- [x] Comprehensive error handling
- [x] Structured logging
- [x] Type hints throughout
- [x] API documentation (Swagger/ReDoc)
- [x] Health check with Redis status
- [x] Automated tests updated

**Architecture Highlights:**
- ✨ Professional folder structure
- ✨ Separation of concerns (API/Service/Core/Models)
- ✨ FastAPI dependency injection
- ✨ Pydantic Settings for configuration
- ✨ Redis client with connection management
- ✨ Comprehensive documentation

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

## Configuration

### Environment Variables (.env)

```env
# Application
APP_NAME=P2P Chat STUN Server
APP_VERSION=1.0.0
DEBUG=false

# Server
HOST=0.0.0.0
PORT=8000

# Redis (Required)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
REDIS_DECODE_RESPONSES=true
REDIS_PEER_PREFIX=peer:
```

### Docker Compose

Redis container configured in `docker-compose.yml`:
- Image: redis:7-alpine
- Port: 6379
- Persistent volume: redis_data
- Health checks enabled
- Auto-restart

## Usage Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Register peer
requests.post(f"{BASE_URL}/register", json={
    'username': 'alice',
    'ip': '192.168.1.10',
    'port': 5001
})

# Get all peers
peers = requests.get(f"{BASE_URL}/peers").json()
print(peers)  # {"count": 1, "peers": ["alice"]}

# Get peer info
info = requests.get(f"{BASE_URL}/peerinfo?username=alice").json()
print(info)  # {"username": "alice", "ip": "192.168.1.10", "port": 5001}

# Unregister
requests.delete(f"{BASE_URL}/unregister/alice")
```

## Development Commands

```bash
# Start Redis
docker-compose up -d

# Stop Redis
docker-compose down

# View Redis logs
docker-compose logs -f redis

# Run STUN server
npm run stun:serve

# Run tests
python apps/stun-server/test_api.py

# Install dependencies
pip install -r apps/stun-server/requirements.txt
```

## Technical Stack

### STUN Server
- **Framework**: FastAPI 0.115
- **Server**: Uvicorn 0.32
- **Validation**: Pydantic 2.9
- **Storage**: Redis 5.0.8
- **Configuration**: Pydantic Settings 2.5
- **Environment**: python-dotenv 1.0

### Infrastructure
- **Container**: Docker Compose
- **Database**: Redis 7 (Alpine)
- **Build Tool**: Nx

## Features

✅ **Production-Ready Architecture**
- Clean separation of concerns
- Professional folder structure
- Type-safe with full type hints
- Environment-based configuration
- Dependency injection

✅ **Robust Storage**
- Redis-only (persistent)
- Connection health monitoring
- Automatic reconnection handling
- Proper error management

✅ **Developer Experience**
- Comprehensive API documentation
- Automated tests
- Clear code organization
- Detailed README files
- Example configurations

✅ **Operational Excellence**
- Structured logging
- Health check endpoint
- Docker Compose setup
- Environment variables
- Error handling

---

