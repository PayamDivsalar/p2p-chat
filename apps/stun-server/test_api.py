"""
STUN Server API Test Script
Use this script to test the STUN server
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"


def print_response(response: requests.Response, title: str):
    """Pretty print response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*60}\n")


def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Root Endpoint")


def test_register(username: str, ip: str, port: int):
    """Test peer registration"""
    data = {
        "username": username,
        "ip": ip,
        "port": port
    }
    response = requests.post(f"{BASE_URL}/register", json=data)
    print_response(response, f"Register Peer: {username}")
    return response.status_code == 201


def test_get_peers():
    """Test get peers list"""
    response = requests.get(f"{BASE_URL}/peers")
    print_response(response, "Peers List")
    return response.json() if response.status_code == 200 else None


def test_get_peer_info(username: str):
    """Test get peer info"""
    response = requests.get(f"{BASE_URL}/peerinfo", params={"username": username})
    print_response(response, f"Peer Info: {username}")
    return response.json() if response.status_code == 200 else None


def test_unregister(username: str):
    """Test unregister peer"""
    response = requests.delete(f"{BASE_URL}/unregister/{username}")
    print_response(response, f"Unregister Peer: {username}")
    return response.status_code == 200


def test_health():
    """Test server health"""
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Server Health Check")


def test_duplicate_registration():
    """Test duplicate registration"""
    username = "duplicate_test"
    test_register(username, "192.168.1.50", 5050)
    # Try to register again
    response = requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "ip": "192.168.1.51",
        "port": 5051
    })
    print_response(response, "Test Duplicate Registration (should fail)")
    test_unregister(username)


def test_nonexistent_peer():
    """Test getting info for non-existent peer"""
    response = requests.get(f"{BASE_URL}/peerinfo", params={"username": "nonexistent_user"})
    print_response(response, "Test Non-existent Peer (should fail)")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  Starting STUN Server Tests")
    print("="*60)
    
    try:
        # Initial tests
        test_root()
        test_health()
        
        # Register multiple peers
        print("\n--- Registering Peers ---")
        test_register("alice", "192.168.1.10", 5001)
        test_register("bob", "192.168.1.11", 5002)
        test_register("charlie", "192.168.1.12", 5003)
        
        # Get peers list
        print("\n--- Getting Peers List ---")
        test_get_peers()
        
        # Get peer info
        print("\n--- Getting Peer Information ---")
        test_get_peer_info("alice")
        test_get_peer_info("bob")
        
        # Test errors
        print("\n--- Testing Error Cases ---")
        test_duplicate_registration()
        test_nonexistent_peer()
        
        # Unregister peers
        print("\n--- Unregistering Peers ---")
        test_unregister("alice")
        test_unregister("bob")
        test_unregister("charlie")
        
        # Final state
        print("\n--- Final State ---")
        test_get_peers()
        test_health()
        
        print("\n" + "="*60)
        print("  All tests completed successfully!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: STUN server is not accessible!")
        print("Please start the server first: npm run stun:serve\n")
    except Exception as e:
        print(f"\n❌ Error running tests: {e}\n")


if __name__ == "__main__":
    run_all_tests()
