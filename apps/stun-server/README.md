# STUN Server - Peer Address Management Server

This HTTP server manages peer (user) information for the P2P chat system.

## Installation and Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Server
```bash
# From project root
npm run stun:serve

# Or directly
python apps/stun-server/src/main.py
```

Server runs on port `8000`.

## API Endpoints

### 1. Register Peer
**POST** `/register`

Register a new peer in the system.

**Request Body:**
```json
{
  "username": "user1",
  "ip": "192.168.1.100",
  "port": 5000
}
```

**Response (201 Created):**
```json
{
  "message": "Peer 'user1' registered successfully",
  "details": {
    "username": "user1",
    "ip": "192.168.1.100",
    "port": 5000
  }
}
```

**Errors:**
- `409 Conflict`: Username already exists
- `422 Validation Error`: Invalid input data

---

### 2. Get Peers List
**GET** `/peers`

Get list of all registered peers.

**Response (200 OK):**
```json
{
  "count": 3,
  "peers": ["user1", "user2", "user3"]
}
```

---

### 3. Get Peer Info
**GET** `/peerinfo?username=user1`

Get information about a specific peer.

**Query Parameters:**
- `username` (required): Username

**Response (200 OK):**
```json
{
  "username": "user1",
  "ip": "192.168.1.100",
  "port": 5000
}
```

**Errors:**
- `404 Not Found`: Peer not found

---

### 4. Unregister Peer (Optional)
**DELETE** `/unregister/{username}`

Remove a peer from the system.

**Response (200 OK):**
```json
{
  "message": "Peer 'user1' unregistered successfully"
}
```

---

### 5. Health Check
**GET** `/health`

Check server status.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "peers_count": 5
}
```

## Usage Examples

### With curl
```bash
# Register
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","ip":"192.168.1.10","port":5001}'

# Get list
curl http://localhost:8000/peers

# Get info
curl "http://localhost:8000/peerinfo?username=alice"
```

### With Python requests
```python
import requests

# Register
response = requests.post('http://localhost:8000/register', json={
    'username': 'alice',
    'ip': '192.168.1.10',
    'port': 5001
})
print(response.json())

# Get peers list
response = requests.get('http://localhost:8000/peers')
print(response.json())

# Get peer info
response = requests.get('http://localhost:8000/peerinfo', params={'username': 'alice'})
print(response.json())
```

## API Documentation

When server is running, you can access interactive Swagger documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Implemented Features

✅ Peer registration with full validation
✅ Get list of all peers
✅ Get specific peer information
✅ Remove peer from system
✅ Server health check
✅ Event logging
✅ Standard HTTP error handling
✅ In-memory storage

## Future Enhancements

🔲 Redis support for persistent storage
🔲 Authentication and security
🔲 Rate limiting
🔲 Heartbeat mechanism to check peer online status
