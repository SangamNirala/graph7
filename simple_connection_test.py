#!/usr/bin/env python3
"""
Simple connectivity test for personalized interview functionality
"""

import requests
import json

# Backend URL
BASE_URL = "https://b7e7e359-045b-441d-b7aa-cfd28adfed5e.preview.emergentagent.com/api"

def test_simple_connection():
    """Test basic connection to backend"""
    try:
        print("Testing basic connectivity...")
        
        # Test admin login
        payload = {"password": "Game@1234"}
        response = requests.post(
            f"{BASE_URL}/admin/login",
            json=payload,
            timeout=30,
            verify=False  # Disable SSL verification for testing
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Admin login successful!")
                return True
            else:
                print("❌ Admin login failed - incorrect response")
                return False
        else:
            print(f"❌ Admin login failed - status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_simple_connection()