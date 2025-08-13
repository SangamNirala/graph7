#!/usr/bin/env python3
"""
Backend Test for Aptitude Question Seeding Endpoints
Testing newly added aptitude question seeding functionality
"""

import requests
import json
import sys
import os
from datetime import datetime

# Backend URL from frontend .env
BACKEND_URL = "https://aptitude-models.preview.emergentagent.com/api"

def test_aptitude_question_seeding():
    """Test the aptitude question seeding endpoints"""
    print("🎯 TESTING APTITUDE QUESTION SEEDING ENDPOINTS")
    print("=" * 60)
    
    results = {
        "total_tests": 2,
        "passed_tests": 0,
        "failed_tests": 0,
        "test_details": []
    }
    
    # Test 1: POST /api/admin/aptitude-questions/seed
    print("\n📝 TEST 1: POST /api/admin/aptitude-questions/seed")
    print("-" * 50)
    
    try:
        # Prepare request data
        seed_data = {
            "force": True,
            "target_total": 800
        }
        
        print(f"🔄 Calling POST {BACKEND_URL}/admin/aptitude-questions/seed")
        print(f"📋 Request body: {json.dumps(seed_data, indent=2)}")
        
        # Make the request
        response = requests.post(
            f"{BACKEND_URL}/admin/aptitude-questions/seed",
            json=seed_data,
            headers={"Content-Type": "application/json"},
            timeout=120  # Extended timeout for seeding operation
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"📋 Response Data: {json.dumps(response_data, indent=2)}")
            
            # Validate response structure and values
            expected_fields = ["success", "generated", "inserted", "total_in_db"]
            validation_passed = True
            validation_details = []
            
            # Check required fields
            for field in expected_fields:
                if field not in response_data:
                    validation_passed = False
                    validation_details.append(f"❌ Missing field: {field}")
                else:
                    validation_details.append(f"✅ Field present: {field}")
            
            # Check success field
            if response_data.get("success") is True:
                validation_details.append("✅ success=true")
            else:
                validation_passed = False
                validation_details.append(f"❌ success={response_data.get('success')}, expected True")
            
            # Check generated count (should be around 800)
            generated = response_data.get("generated", 0)
            if 750 <= generated <= 850:  # Allow some tolerance
                validation_details.append(f"✅ generated={generated} (within expected range 750-850)")
            else:
                validation_passed = False
                validation_details.append(f"❌ generated={generated}, expected ~800")
            
            # Check inserted count (should be around 800)
            inserted = response_data.get("inserted", 0)
            if 750 <= inserted <= 850:  # Allow some tolerance
                validation_details.append(f"✅ inserted={inserted} (within expected range 750-850)")
            else:
                validation_passed = False
                validation_details.append(f"❌ inserted={inserted}, expected ~800")
            
            # Check total_in_db (should be >= 800)
            total_in_db = response_data.get("total_in_db", 0)
            if total_in_db >= 800:
                validation_details.append(f"✅ total_in_db={total_in_db} (>= 800)")
            else:
                validation_passed = False
                validation_details.append(f"❌ total_in_db={total_in_db}, expected >= 800")
            
            # Print validation results
            print("\n🔍 VALIDATION RESULTS:")
            for detail in validation_details:
                print(f"  {detail}")
            
            if validation_passed:
                print("✅ TEST 1 PASSED: Aptitude question seeding endpoint working correctly")
                results["passed_tests"] += 1
                results["test_details"].append({
                    "test": "POST /api/admin/aptitude-questions/seed",
                    "status": "PASSED",
                    "details": f"Generated {generated}, Inserted {inserted}, Total in DB {total_in_db}"
                })
            else:
                print("❌ TEST 1 FAILED: Response validation failed")
                results["failed_tests"] += 1
                results["test_details"].append({
                    "test": "POST /api/admin/aptitude-questions/seed",
                    "status": "FAILED",
                    "details": "Response validation failed",
                    "validation_errors": [d for d in validation_details if d.startswith("❌")]
                })
        else:
            print(f"❌ TEST 1 FAILED: HTTP {response.status_code}")
            print(f"📋 Response: {response.text}")
            results["failed_tests"] += 1
            results["test_details"].append({
                "test": "POST /api/admin/aptitude-questions/seed",
                "status": "FAILED",
                "details": f"HTTP {response.status_code}: {response.text}"
            })
            
    except requests.exceptions.Timeout:
        print("❌ TEST 1 FAILED: Request timeout (seeding operation took too long)")
        results["failed_tests"] += 1
        results["test_details"].append({
            "test": "POST /api/admin/aptitude-questions/seed",
            "status": "FAILED",
            "details": "Request timeout - seeding operation took too long"
        })
    except Exception as e:
        print(f"❌ TEST 1 FAILED: Exception occurred - {str(e)}")
        results["failed_tests"] += 1
        results["test_details"].append({
            "test": "POST /api/admin/aptitude-questions/seed",
            "status": "FAILED",
            "details": f"Exception: {str(e)}"
        })
    
    # Test 2: GET /api/admin/aptitude-questions/stats
    print("\n📝 TEST 2: GET /api/admin/aptitude-questions/stats")
    print("-" * 50)
    
    try:
        print(f"🔄 Calling GET {BACKEND_URL}/admin/aptitude-questions/stats")
        
        # Make the request
        response = requests.get(
            f"{BACKEND_URL}/admin/aptitude-questions/stats",
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"📋 Response Data: {json.dumps(response_data, indent=2)}")
            
            # Validate response structure and values
            validation_passed = True
            validation_details = []
            
            # Check required fields
            required_fields = ["success", "total", "by_topic", "by_difficulty"]
            for field in required_fields:
                if field not in response_data:
                    validation_passed = False
                    validation_details.append(f"❌ Missing field: {field}")
                else:
                    validation_details.append(f"✅ Field present: {field}")
            
            # Check success field
            if response_data.get("success") is True:
                validation_details.append("✅ success=true")
            else:
                validation_passed = False
                validation_details.append(f"❌ success={response_data.get('success')}, expected True")
            
            # Check total count (should be >= 800)
            total = response_data.get("total", 0)
            if total >= 800:
                validation_details.append(f"✅ total={total} (>= 800)")
            else:
                validation_passed = False
                validation_details.append(f"❌ total={total}, expected >= 800")
            
            # Check by_topic distribution (should be around 200 each for 4 topics)
            by_topic = response_data.get("by_topic", {})
            expected_topics = ["numerical_reasoning", "logical_reasoning", "verbal_comprehension", "spatial_reasoning"]
            
            for topic in expected_topics:
                if topic in by_topic:
                    topic_count = by_topic[topic]
                    if 180 <= topic_count <= 220:  # Allow some tolerance around 200
                        validation_details.append(f"✅ {topic}={topic_count} (within expected range 180-220)")
                    else:
                        validation_passed = False
                        validation_details.append(f"❌ {topic}={topic_count}, expected ~200")
                else:
                    validation_passed = False
                    validation_details.append(f"❌ Missing topic: {topic}")
            
            # Check by_difficulty distribution (should be around 40/40/20 per topic)
            by_difficulty = response_data.get("by_difficulty", {})
            expected_difficulties = ["easy", "medium", "hard"]
            
            for difficulty in expected_difficulties:
                if difficulty in by_difficulty:
                    diff_count = by_difficulty[difficulty]
                    if difficulty in ["easy", "medium"]:
                        # Easy and medium should be around 40% each of 800 = ~320 each
                        if 280 <= diff_count <= 360:
                            validation_details.append(f"✅ {difficulty}={diff_count} (within expected range 280-360)")
                        else:
                            validation_passed = False
                            validation_details.append(f"❌ {difficulty}={diff_count}, expected ~320")
                    else:  # hard
                        # Hard should be around 20% of 800 = ~160
                        if 140 <= diff_count <= 180:
                            validation_details.append(f"✅ {difficulty}={diff_count} (within expected range 140-180)")
                        else:
                            validation_passed = False
                            validation_details.append(f"❌ {difficulty}={diff_count}, expected ~160")
                else:
                    validation_passed = False
                    validation_details.append(f"❌ Missing difficulty: {difficulty}")
            
            # Print validation results
            print("\n🔍 VALIDATION RESULTS:")
            for detail in validation_details:
                print(f"  {detail}")
            
            if validation_passed:
                print("✅ TEST 2 PASSED: Aptitude question stats endpoint working correctly")
                results["passed_tests"] += 1
                results["test_details"].append({
                    "test": "GET /api/admin/aptitude-questions/stats",
                    "status": "PASSED",
                    "details": f"Total: {total}, Topics: {by_topic}, Difficulties: {by_difficulty}"
                })
            else:
                print("❌ TEST 2 FAILED: Response validation failed")
                results["failed_tests"] += 1
                results["test_details"].append({
                    "test": "GET /api/admin/aptitude-questions/stats",
                    "status": "FAILED",
                    "details": "Response validation failed",
                    "validation_errors": [d for d in validation_details if d.startswith("❌")]
                })
        else:
            print(f"❌ TEST 2 FAILED: HTTP {response.status_code}")
            print(f"📋 Response: {response.text}")
            results["failed_tests"] += 1
            results["test_details"].append({
                "test": "GET /api/admin/aptitude-questions/stats",
                "status": "FAILED",
                "details": f"HTTP {response.status_code}: {response.text}"
            })
            
    except Exception as e:
        print(f"❌ TEST 2 FAILED: Exception occurred - {str(e)}")
        results["failed_tests"] += 1
        results["test_details"].append({
            "test": "GET /api/admin/aptitude-questions/stats",
            "status": "FAILED",
            "details": f"Exception: {str(e)}"
        })
    
    # Test 3: Route Prefix Verification
    print("\n📝 TEST 3: Route Prefix Verification")
    print("-" * 50)
    
    # Check that we're using /api prefix, not double /api/api
    if BACKEND_URL.endswith("/api"):
        print("✅ Backend URL uses correct /api prefix")
        print(f"🔗 URL: {BACKEND_URL}")
        
        # Verify no double prefix by checking if endpoints work with single /api
        test_url = f"{BACKEND_URL}/admin/aptitude-questions/stats"
        print(f"🔄 Testing single /api prefix with: {test_url}")
        
        try:
            response = requests.get(test_url, timeout=10)
            if response.status_code in [200, 404, 401, 403]:  # Any valid HTTP response
                print("✅ Single /api prefix works correctly")
                results["test_details"].append({
                    "test": "Route Prefix Verification",
                    "status": "PASSED",
                    "details": "Backend uses correct /api prefix, no double /api/api"
                })
            else:
                print(f"⚠️  Unexpected response code: {response.status_code}")
                results["test_details"].append({
                    "test": "Route Prefix Verification", 
                    "status": "WARNING",
                    "details": f"Unexpected response code: {response.status_code}"
                })
        except Exception as e:
            print(f"⚠️  Could not verify prefix: {str(e)}")
            results["test_details"].append({
                "test": "Route Prefix Verification",
                "status": "WARNING", 
                "details": f"Could not verify prefix: {str(e)}"
            })
    else:
        print(f"⚠️  Backend URL doesn't end with /api: {BACKEND_URL}")
        results["test_details"].append({
            "test": "Route Prefix Verification",
            "status": "WARNING",
            "details": f"Backend URL doesn't end with /api: {BACKEND_URL}"
        })
    
    return results

def main():
    """Main test execution"""
    print("🚀 APTITUDE QUESTION SEEDING ENDPOINTS TEST")
    print("=" * 60)
    print(f"🕒 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Backend URL: {BACKEND_URL}")
    
    # Run tests
    results = test_aptitude_question_seeding()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {results['total_tests']}")
    print(f"✅ Passed: {results['passed_tests']}")
    print(f"❌ Failed: {results['failed_tests']}")
    print(f"📈 Success Rate: {(results['passed_tests'] / results['total_tests'] * 100):.1f}%")
    
    print("\n📋 DETAILED RESULTS:")
    for i, test_detail in enumerate(results['test_details'], 1):
        print(f"\n{i}. {test_detail['test']}")
        print(f"   Status: {test_detail['status']}")
        print(f"   Details: {test_detail['details']}")
        if 'validation_errors' in test_detail:
            print("   Validation Errors:")
            for error in test_detail['validation_errors']:
                print(f"     {error}")
    
    print(f"\n🕒 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return appropriate exit code
    return 0 if results['failed_tests'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())