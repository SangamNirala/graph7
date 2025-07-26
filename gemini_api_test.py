#!/usr/bin/env python3
"""
Direct Gemini API Key Testing
Tests the specific Gemini API key to confirm it's the root cause
"""

import requests
import json

def test_gemini_api_key():
    """Test the Gemini API key directly"""
    api_key = "AIzaSyCFYX2-5r3oZH_Z53rl-5-xNaotmBtBhbc"
    
    # Test with Google AI Studio API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Hello, this is a test message."
            }]
        }]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Gemini API key is VALID")
            return True
        elif response.status_code == 400:
            response_data = response.json()
            if "API key not valid" in response_data.get("error", {}).get("message", ""):
                print("❌ Gemini API key is INVALID")
                return False
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception testing Gemini API: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("GEMINI API KEY VALIDATION TEST")
    print("=" * 60)
    test_gemini_api_key()