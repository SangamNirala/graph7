#!/usr/bin/env python3
"""
API Endpoint Investigation Test
Testing the specific endpoints mentioned in the user's issue:
1. GET /api/placement-preparation/resume-analyses - returning 404
2. GET /api/placement-preparation/rejection-reasons - should work
"""

import requests
import json
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://00a8e650-3105-4677-9117-76e2639bccac.preview.emergentagent.com')

def test_api_endpoints():
    """Test the specific API endpoints mentioned in the user's issue"""
    
    print("🔍 API ENDPOINT INVESTIGATION")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now()}")
    print()
    
    # Test 1: GET /api/placement-preparation/resume-analyses
    print("📋 TEST 1: GET /api/placement-preparation/resume-analyses")
    print("-" * 50)
    
    try:
        url = f"{BACKEND_URL}/api/placement-preparation/resume-analyses"
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Response received")
            print(f"Data structure: {type(data)}")
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
                if 'analyses' in data:
                    analyses = data['analyses']
                    print(f"Number of analyses: {len(analyses)}")
                    if analyses:
                        print(f"Sample analysis keys: {list(analyses[0].keys())}")
                    else:
                        print("No analyses found in database")
            print(f"Response preview: {str(data)[:500]}...")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response text: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    print()
    
    # Test 2: GET /api/placement-preparation/rejection-reasons
    print("📋 TEST 2: GET /api/placement-preparation/rejection-reasons")
    print("-" * 50)
    
    try:
        url = f"{BACKEND_URL}/api/placement-preparation/rejection-reasons"
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Response received")
            print(f"Data structure: {type(data)}")
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
                if 'analyses' in data:
                    analyses = data['analyses']
                    print(f"Number of rejection analyses: {len(analyses)}")
                    if analyses:
                        print(f"Sample analysis keys: {list(analyses[0].keys())}")
                        # Check for PDF download links
                        sample = analyses[0]
                        if 'id' in sample:
                            print(f"Sample analysis ID: {sample['id']}")
                        if 'pdf_path' in sample:
                            print(f"PDF path present: {sample['pdf_path']}")
                        if 'pdf_filename' in sample:
                            print(f"PDF filename: {sample['pdf_filename']}")
                    else:
                        print("No rejection analyses found in database")
            print(f"Response preview: {str(data)[:500]}...")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response text: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    print()
    
    # Test 3: Check backend connectivity
    print("📋 TEST 3: Backend Connectivity Check")
    print("-" * 50)
    
    try:
        # Try a simple endpoint first
        url = f"{BACKEND_URL}/api/admin/login"
        print(f"Testing basic connectivity with: {url}")
        
        response = requests.post(url, 
                               json={"password": "Game@1234"}, 
                               timeout=30)
        print(f"Admin login status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Backend is accessible and responding")
        else:
            print(f"⚠️  Backend responding but login failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Backend connectivity error: {str(e)}")
    
    print()
    
    # Test 4: Check if routes are properly registered
    print("📋 TEST 4: Route Registration Check")
    print("-" * 50)
    
    # Test various placement-preparation endpoints to see which ones work
    endpoints_to_test = [
        "/api/placement-preparation/ats-score-calculate",
        "/api/placement-preparation/resume-analyses", 
        "/api/placement-preparation/rejection-reasons",
        "/api/placement-preparation/acceptance-reasons",
        "/api/placement-preparation/ats-optimized-resume",
        "/api/placement-preparation/technical-questions",
        "/api/placement-preparation/behavioral-questions"
    ]
    
    for endpoint in endpoints_to_test:
        try:
            url = f"{BACKEND_URL}{endpoint}"
            if "calculate" in endpoint or "reasons" in endpoint or "questions" in endpoint:
                # These are POST endpoints, expect 405 Method Not Allowed for GET
                response = requests.get(url, timeout=10)
                if response.status_code == 405:
                    print(f"✅ {endpoint} - Route exists (405 Method Not Allowed)")
                elif response.status_code == 200:
                    print(f"✅ {endpoint} - Route exists and responds to GET")
                else:
                    print(f"❓ {endpoint} - Status: {response.status_code}")
            else:
                # These should be GET endpoints
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"✅ {endpoint} - Working")
                elif response.status_code == 404:
                    print(f"❌ {endpoint} - Not Found (404)")
                else:
                    print(f"❓ {endpoint} - Status: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ {endpoint} - Error: {str(e)}")
    
    print()
    print("🔍 INVESTIGATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_api_endpoints()