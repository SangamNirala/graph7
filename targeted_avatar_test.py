#!/usr/bin/env python3
"""
Targeted test for avatar interview 401 error - using separate tokens for each test
"""

import requests
import json
import io
import urllib3

# Suppress SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://925addbc-2681-4d59-bfd4-4de0b3e3b55d.preview.emergentagent.com/api"

class AvatarInterviewTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 30
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Avatar-Interview-Tester/1.0'
        })
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def authenticate_admin(self) -> bool:
        """Authenticate admin with password Game@1234"""
        try:
            payload = {"password": "Game@1234"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
    
    def create_fresh_avatar_token(self, job_suffix: str = "") -> str:
        """Create a fresh enhanced token for avatar testing"""
        try:
            if not self.authenticate_admin():
                return None
            
            resume_content = f"""Avatar Test User {job_suffix}
Avatar Interview Candidate
Email: avatar.test{job_suffix}@email.com
Phone: (555) 123-456{len(job_suffix)}

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
                'resume_file': (f'avatar_resume{job_suffix}.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': f'Avatar Interface Developer {job_suffix}',
                'job_description': f'Avatar interview functionality with voice-driven interactions {job_suffix}.',
                'job_requirements': 'Requirements: React expertise, voice interface experience, SVG animation skills.',
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
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success", False) and "token" in result:
                    return result["token"]
            
            return None
            
        except Exception as e:
            print(f"Error creating token: {str(e)}")
            return None
    
    def test_avatar_interview_direct(self) -> bool:
        """Test avatar interview directly with fresh token"""
        try:
            # Create fresh token specifically for this test
            token = self.create_fresh_avatar_token("_direct")
            if not token:
                self.log_test("Avatar Interview Direct Test", False, "Failed to create fresh token")
                return False
            
            print(f"🔍 Testing avatar interview with fresh token: {token}")
            
            # Test avatar interview start with voice_mode=true and candidate_name
            payload = {
                "token": token,
                "candidate_name": "Test User",
                "voice_mode": True
            }
            
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
                details += f", Enhanced: {data.get('is_enhanced', 'N/A')}"
                details += f", Question: {data.get('first_question', 'N/A')[:50]}..."
            else:
                details += f", Response: {response.text}"
                
                if response.status_code == 401:
                    print("🚨 401 ERROR CONFIRMED!")
                    try:
                        error_data = response.json()
                        print(f"   Error Detail: {error_data.get('detail', 'No detail')}")
                    except:
                        pass
            
            self.log_test("Avatar Interview Direct Test", success, details)
            return success
            
        except Exception as e:
            self.log_test("Avatar Interview Direct Test", False, f"Exception: {str(e)}")
            return False
    
    def test_regular_interview_direct(self) -> bool:
        """Test regular interview directly with fresh token for comparison"""
        try:
            # Create fresh token specifically for this test
            token = self.create_fresh_avatar_token("_regular")
            if not token:
                self.log_test("Regular Interview Direct Test", False, "Failed to create fresh token")
                return False
            
            print(f"🔍 Testing regular interview with fresh token: {token}")
            
            # Test regular interview start with voice_mode=false
            payload = {
                "token": token,
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
            
            self.log_test("Regular Interview Direct Test", success, details)
            return success
            
        except Exception as e:
            self.log_test("Regular Interview Direct Test", False, f"Exception: {str(e)}")
            return False
    
    def test_token_reuse_issue(self) -> bool:
        """Test if tokens are being marked as used incorrectly"""
        try:
            # Create fresh token
            token = self.create_fresh_avatar_token("_reuse")
            if not token:
                self.log_test("Token Reuse Issue Test", False, "Failed to create fresh token")
                return False
            
            print(f"🔍 Testing token reuse with token: {token}")
            
            # First, validate the token
            payload = {"token": token}
            response = self.session.post(
                f"{self.base_url}/candidate/validate-token",
                json=payload,
                timeout=10
            )
            
            if response.status_code != 200:
                self.log_test("Token Reuse Issue Test", False, f"Token validation failed: {response.status_code}")
                return False
            
            print("   ✅ Token validation successful")
            
            # Now try to start interview
            payload = {
                "token": token,
                "candidate_name": "Test User",
                "voice_mode": True
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Session created successfully"
            else:
                details += f", Response: {response.text}"
                
                if response.status_code == 401:
                    print("🚨 TOKEN MARKED AS USED INCORRECTLY!")
                    print("   Token was valid during validation but invalid during interview start")
            
            self.log_test("Token Reuse Issue Test", success, details)
            return success
            
        except Exception as e:
            self.log_test("Token Reuse Issue Test", False, f"Exception: {str(e)}")
            return False
    
    def run_targeted_tests(self):
        """Run targeted tests to identify the exact issue"""
        print("=" * 80)
        print("TARGETED AVATAR INTERVIEW TESTING")
        print("Identifying the root cause of 401 authentication errors")
        print("=" * 80)
        print()
        
        results = {}
        
        # Test 1: Regular interview (should work)
        results["regular_interview"] = self.test_regular_interview_direct()
        
        # Test 2: Avatar interview (may fail with 401)
        results["avatar_interview"] = self.test_avatar_interview_direct()
        
        # Test 3: Token reuse issue investigation
        results["token_reuse"] = self.test_token_reuse_issue()
        
        # Summary
        print("=" * 80)
        print("TARGETED TEST SUMMARY")
        print("=" * 80)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print()
        
        # Analysis
        print("ANALYSIS:")
        if results.get("regular_interview", False) and not results.get("avatar_interview", False):
            print("❌ ISSUE CONFIRMED: Avatar interview fails while regular interview works")
            print("   This suggests a specific issue with voice_mode=true or enhanced token handling")
        elif results.get("avatar_interview", False):
            print("✅ Avatar interview is working correctly")
            print("   The 401 error may be intermittent or related to specific conditions")
        else:
            print("❌ Both interview types are failing - broader authentication issue")
        
        return results

def main():
    """Main test execution"""
    tester = AvatarInterviewTester()
    results = tester.run_targeted_tests()
    
    # Return exit code based on avatar interview test
    avatar_passed = results.get("avatar_interview", False)
    return 0 if avatar_passed else 1

if __name__ == "__main__":
    exit(main())