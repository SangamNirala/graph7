#!/usr/bin/env python3
"""
Debug test for 401 authentication error in avatar interview functionality
Specifically testing the /api/candidate/start-interview endpoint with proper request format
"""

import requests
import json
import io
import urllib3

# Suppress SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://925addbc-2681-4d59-bfd4-4de0b3e3b55d.preview.emergentagent.com/api"

class Avatar401DebugTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 30
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Avatar-401-Debug-Tester/1.0'
        })
        self.fresh_token = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def generate_fresh_enhanced_token(self) -> bool:
        """Generate a fresh enhanced token through admin portal"""
        try:
            # First authenticate admin
            payload = {"password": "Game@1234"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            if response.status_code != 200:
                self.log_test("Admin Authentication", False, f"Status: {response.status_code}")
                return False
            
            # Create enhanced token for avatar interview
            resume_content = """Test User
Avatar Interview Candidate
Email: testuser@email.com
Phone: (555) 123-4567

EXPERIENCE:
- 5+ years of frontend development
- Expert in React and JavaScript
- Experience with avatar interfaces and voice technologies
- Built real-time interactive applications

SKILLS:
- React, JavaScript, TypeScript
- SVG animations, Web APIs
- Voice interfaces, WebRTC
- Real-time systems"""
            
            files = {
                'resume_file': ('test_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Avatar Interface Developer',
                'job_description': 'We need a developer to work on avatar interview functionality with voice-driven interactions and realistic female avatar implementation.',
                'job_requirements': 'Requirements: React expertise, voice interface experience, SVG animation skills, real-time audio processing knowledge.',
                'include_coding_challenge': 'false',
                'role_archetype': 'Software Engineer',
                'interview_focus': 'Technical Deep-Dive'
            }
            
            # Remove Content-Type header for multipart form data
            original_headers = self.session.headers.copy()
            if 'Content-Type' in self.session.headers:
                del self.session.headers['Content-Type']
            
            try:
                response = self.session.post(
                    f"{self.base_url}/admin/upload-job-enhanced",
                    files=files,
                    data=data,
                    timeout=15
                )
            finally:
                # Restore original headers
                self.session.headers = original_headers
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = result.get("success", False) and "token" in result
                if success:
                    self.fresh_token = result["token"]
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.fresh_token}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Generate Fresh Enhanced Token", success, details)
            return success
            
        except Exception as e:
            self.log_test("Generate Fresh Enhanced Token", False, f"Exception: {str(e)}")
            return False
    
    def test_start_interview_with_candidate_name(self) -> bool:
        """Test /api/candidate/start-interview with proper request format including candidate_name field"""
        if not self.fresh_token:
            self.log_test("Start Interview with candidate_name", False, "No fresh token available")
            return False
        
        try:
            # Test the exact format mentioned in the review request
            payload = {
                "token": self.fresh_token,
                "candidate_name": "Test User",
                "voice_mode": True
            }
            
            print(f"🔍 Testing /api/candidate/start-interview with payload:")
            print(f"   Token: {self.fresh_token}")
            print(f"   Candidate Name: Test User")
            print(f"   Voice Mode: true")
            print()
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Session ID: {data.get('session_id', 'N/A')[:8]}..."
                details += f", Voice Mode: {data.get('voice_mode', 'N/A')}"
                details += f", First Question: {data.get('first_question', 'N/A')[:50]}..."
            else:
                details += f", Response: {response.text}"
                
                # Check if it's the 401 error mentioned
                if response.status_code == 401:
                    print("🚨 FOUND THE 401 ERROR!")
                    print(f"   Error Response: {response.text}")
                    try:
                        error_data = response.json()
                        print(f"   Error Detail: {error_data.get('detail', 'No detail provided')}")
                    except:
                        pass
            
            self.log_test("Start Interview with candidate_name", success, details)
            return success
            
        except Exception as e:
            self.log_test("Start Interview with candidate_name", False, f"Exception: {str(e)}")
            return False
    
    def test_token_validation_first(self) -> bool:
        """Test token validation before starting interview"""
        if not self.fresh_token:
            self.log_test("Token Validation First", False, "No fresh token available")
            return False
        
        try:
            payload = {"token": self.fresh_token}
            response = self.session.post(
                f"{self.base_url}/candidate/validate-token",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("valid", False)
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Valid: {data.get('valid')}, Job: {data.get('job_title')}"
            else:
                details += f", Response: {response.text}"
            
            self.log_test("Token Validation First", success, details)
            return success
            
        except Exception as e:
            self.log_test("Token Validation First", False, f"Exception: {str(e)}")
            return False
    
    def test_regular_interview_flow(self) -> bool:
        """Test regular interview flow (non-avatar) for comparison"""
        if not self.fresh_token:
            self.log_test("Regular Interview Flow", False, "No fresh token available")
            return False
        
        try:
            # Test regular interview start (voice_mode=false)
            payload = {
                "token": self.fresh_token,
                "candidate_name": "Test User",
                "voice_mode": False
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Session ID: {data.get('session_id', 'N/A')[:8]}..."
                details += f", Voice Mode: {data.get('voice_mode', 'N/A')}"
            else:
                details += f", Response: {response.text}"
            
            self.log_test("Regular Interview Flow", success, details)
            return success
            
        except Exception as e:
            self.log_test("Regular Interview Flow", False, f"Exception: {str(e)}")
            return False
    
    def test_missing_candidate_name(self) -> bool:
        """Test what happens when candidate_name is missing (as mentioned in error logs)"""
        if not self.fresh_token:
            self.log_test("Missing candidate_name Test", False, "No fresh token available")
            return False
        
        try:
            # Test without candidate_name field
            payload = {
                "token": self.fresh_token,
                "voice_mode": True
                # Missing candidate_name intentionally
            }
            
            print(f"🔍 Testing without candidate_name field:")
            print(f"   Token: {self.fresh_token}")
            print(f"   Voice Mode: true")
            print(f"   candidate_name: MISSING")
            print()
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=15
            )
            
            # We expect this to fail
            success = response.status_code in [400, 422]  # Bad request or validation error
            
            details = f"Status: {response.status_code}"
            details += f", Response: {response.text}"
            
            if response.status_code == 401:
                print("🚨 401 ERROR WHEN candidate_name IS MISSING!")
                print(f"   This might be the root cause mentioned in the review request")
            
            self.log_test("Missing candidate_name Test", success, details)
            return success
            
        except Exception as e:
            self.log_test("Missing candidate_name Test", False, f"Exception: {str(e)}")
            return False
    
    def run_debug_tests(self):
        """Run all debug tests to identify the 401 error"""
        print("=" * 80)
        print("AVATAR INTERVIEW 401 ERROR DEBUG TESTING")
        print("Reproducing the 401 authentication error mentioned in review request")
        print("=" * 80)
        print()
        
        results = {}
        
        # Step 1: Generate fresh enhanced token
        results["generate_token"] = self.generate_fresh_enhanced_token()
        
        # Step 2: Validate token first
        results["validate_token"] = self.test_token_validation_first()
        
        # Step 3: Test regular interview flow for comparison
        results["regular_flow"] = self.test_regular_interview_flow()
        
        # Step 4: Test avatar interview with proper candidate_name
        results["avatar_with_name"] = self.test_start_interview_with_candidate_name()
        
        # Step 5: Test what happens without candidate_name (potential root cause)
        results["missing_name"] = self.test_missing_candidate_name()
        
        # Summary
        print("=" * 80)
        print("DEBUG TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print()
        print(f"DEBUG TESTS: {passed}/{total} tests passed")
        
        # Analysis
        print("\n" + "=" * 80)
        print("ANALYSIS")
        print("=" * 80)
        
        if results.get("avatar_with_name", False):
            print("✅ Avatar interview with candidate_name field is WORKING")
            print("   The 401 error is NOT occurring with proper request format")
        else:
            print("❌ Avatar interview with candidate_name field is FAILING")
            print("   This confirms the 401 error mentioned in the review request")
        
        if not results.get("missing_name", False) and results.get("avatar_with_name", False):
            print("✅ The issue appears to be related to missing candidate_name field")
        
        return results

def main():
    """Main debug test execution"""
    tester = Avatar401DebugTester()
    results = tester.run_debug_tests()
    
    # Return exit code based on critical tests
    critical_passed = results.get("avatar_with_name", False)
    return 0 if critical_passed else 1

if __name__ == "__main__":
    exit(main())