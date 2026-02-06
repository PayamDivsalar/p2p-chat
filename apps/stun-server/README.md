# STUN Server - Refactored with Clean Architecture

## Project Structure

```
apps/stun-server/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Application entry point
│   │
│   ├── api/                     # API Layer
│   │   ├── __init__.py
│   │   ├── dependencies.py      # FastAPI dependencies (DI)
│   │   └── endpoints/           # API endpoints
│   │       ├── __init__.py
│   │       ├── peers.py         # Peer management endpoints
│   │       └── health.py        # Health check endpoints
│   │
│   ├── core/                    # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration management
│   │   └── redis_client.py      # Redis connection manager
│   │
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   └── peer.py              # Pydantic models for peers
│   │
│   └── services/                # Business logic layer
│       ├── __init__.py
│       └── peer_service.py      # Peer operations logic
│
├── .env                         # Environment configuration
├── .env.example                 # Example environment file
├── requirements.txt             # Python dependencies
├── project.json                 # Nx project configuration
└── README.md                    # This file
```

## Architecture Principles

### 1. **Separation of Concerns**
- **API Layer** (`api/`): Handles HTTP requests/responses, validation
- **Service Layer** (`services/`): Contains business logic
- **Core Layer** (`core/`): Configuration and infrastructure (Redis)
- **Models** (`models/`): Data structures and validation

### 2. **Dependency Injection**
- FastAPI's dependency injection system
- Loose coupling between layers
- Easy to test and mock

### 3. **Single Responsibility**
- Each module has one clear purpose
- Easy to maintain and extend

## Storage Backend

**Redis Only** - No in-memory option
- All peer data stored in Redis
- Persistent storage
- Production-ready

## Setup and Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Redis
```bash
# From project root
docker-compose up -d
```

### 3. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env if needed (defaults work with docker-compose)
```

### 4. Run Server
```bash
# From project root
npm run stun:serve

# Or directly from stun-server directory
cd apps/stun-server
python -m src.main
```

## API Documentation

Server runs on `http://localhost:8000`

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### Register Peer
```
POST /api/v1/register
Body: {"username": "alice", "ip": "192.168.1.10", "port": 5001}
```

#### Get All Peers
```
GET /api/v1/peers
```

#### Get Peer Info
```
GET /api/v1/peerinfo?username=alice
```

#### Unregister Peer
```
DELETE /api/v1/unregister/alice
```

#### Health Check
```
GET /health
```

## Configuration

Environment variables in `.env`:

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

## Development

### Running Tests
```bash
python apps/stun-server/test_api.py
```

### Code Structure Guidelines

1. **Models** (`models/peer.py`)
   - Pydantic models for validation
   - No business logic

2. **Services** (`services/peer_service.py`)
   - Business logic operations
   - Interacts with Redis
   - No HTTP/FastAPI code

3. **API Endpoints** (`api/endpoints/`)
   - HTTP request/response handling
   - Input validation
   - Calls service layer
   - Returns appropriate HTTP codes

4. **Dependencies** (`api/dependencies.py`)
   - FastAPI dependency injection
   - Provides service instances
   - Manages request-scoped resources

5. **Configuration** (`core/config.py`)
   - Pydantic Settings
   - Environment variable loading
   - Cached configuration

6. **Redis Client** (`core/redis_client.py`)
   - Connection management
   - Singleton pattern
   - Health checks

## Features

✅ Clean architecture with separation of concerns
✅ Redis-only storage (persistent, production-ready)
✅ Dependency injection pattern
✅ Comprehensive error handling
✅ Structured logging
✅ Type hints throughout
✅ Docker Compose for Redis
✅ Environment-based configuration
✅ API documentation (Swagger/ReDoc)
✅ Health check endpoint with Redis status

## Benefits of This Architecture

1. **Maintainability**: Clear structure, easy to find and modify code
2. **Testability**: Each layer can be tested independently
3. **Scalability**: Easy to add new endpoints and features
4. **Professional**: Follows industry best practices
5. **Type Safety**: Full type hints for better IDE support
6. **Configuration**: Environment-based, easy to deploy
7. **Reliability**: Redis persistence, proper error handling

## Migration from Old Structure

The old single-file `main.py` has been refactored into:
- Removed in-memory storage option (Redis only)
- Split into multiple modules by responsibility
- Added dependency injection
- Improved error handling
- Better configuration management
- Professional folder structure
