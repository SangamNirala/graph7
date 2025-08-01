#!/usr/bin/env python3
"""
Webcam Token Generation Test
This script tests admin login and creates a simple interview token 
for testing webcam functionality in the interview session.
"""

import requests
import json
import io
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://4c07abd9-00f3-4bb2-a1a6-832745c054f9.preview.emergentagent.com/api"

class WebcamTokenTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.generated_token = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_admin_login(self) -> bool:
        """Test admin authentication with password Game@1234"""
        try:
            payload = {"password": "Game@1234"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("success", False)
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Admin Login with Game@1234", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login with Game@1234", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_token_creation(self) -> bool:
        """Create an enhanced interview token for webcam testing"""
        try:
            # Create sample resume content for webcam testing
            resume_content = """Sarah Wilson
Webcam Test Candidate
Email: sarah.wilson@email.com
Phone: (555) 999-8888

EXPERIENCE:
- 4+ years of frontend development
- Experience with React and modern web technologies
- Built video conferencing applications
- Strong background in user interface design

SKILLS:
- React, JavaScript, TypeScript, HTML5, CSS3
- WebRTC, Media APIs, Camera/Microphone integration
- Responsive design, accessibility
- User experience optimization

EDUCATION:
Bachelor of Science in Computer Science
Tech University, 2019"""
            
            # Prepare multipart form data for enhanced upload
            files = {
                'resume_file': ('webcam_test_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Frontend Developer - Video Interface Specialist',
                'job_description': 'We are seeking a frontend developer with experience in video interfaces and webcam integration. The role involves building user-friendly video applications and ensuring smooth camera/microphone functionality.',
                'job_requirements': 'Requirements: 3+ years frontend experience, React expertise, WebRTC knowledge, camera/microphone API experience, strong UI/UX skills.',
                'include_coding_challenge': 'false',  # Keep it simple for webcam testing
                'role_archetype': 'Software Engineer',
                'interview_focus': 'Technical Deep-Dive',
                'min_questions': '8',
                'max_questions': '10'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job-enhanced",
                files=files,
                data=data,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "token" in result and 
                          "features" in result)
                if success:
                    self.generated_token = result["token"]
                    print(f"🎯 GENERATED TOKEN FOR WEBCAM TESTING: {self.generated_token}")
                    print(f"📋 Resume Preview: {result.get('resume_preview', 'N/A')[:100]}...")
                    print(f"⏱️  Estimated Duration: {result.get('estimated_duration', 'N/A')} minutes")
                    print(f"🔧 Features: {json.dumps(result.get('features', {}), indent=2)}")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.generated_token}, Features: {result.get('features', {})}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Enhanced Token Creation for Webcam Testing", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Token Creation for Webcam Testing", False, f"Exception: {str(e)}")
            return False
    
    def test_token_validation(self) -> bool:
        """Validate the generated token"""
        if not self.generated_token:
            self.log_test("Token Validation", False, "No token available from creation test")
            return False
        
        try:
            payload = {"token": self.generated_token}
            response = self.session.post(
                f"{self.base_url}/candidate/validate-token",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("valid", False) and "job_title" in data
                if success:
                    print(f"✅ Token is valid for job: {data.get('job_title')}")
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Token Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_camera_test_endpoint(self) -> bool:
        """Test the camera test endpoint with the generated token"""
        if not self.generated_token:
            self.log_test("Camera Test Endpoint", False, "No token available")
            return False
        
        try:
            payload = {"token": self.generated_token}
            response = self.session.post(
                f"{self.base_url}/candidate/camera-test",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("success", False)
                if success:
                    print(f"📹 Camera test endpoint ready")
                    print(f"🎥 Features available: {data.get('features', {})}")
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Camera Test Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Camera Test Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_start_with_voice(self) -> bool:
        """Test starting interview with voice mode for webcam functionality"""
        if not self.generated_token:
            self.log_test("Interview Start with Voice Mode", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "candidate_name": "Sarah Wilson",
                "voice_mode": True  # Enable voice mode for webcam testing
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "voice_mode" in data)
                if success:
                    session_id = data["session_id"]
                    print(f"🎤 Interview session started with voice mode")
                    print(f"📝 Session ID: {session_id}")
                    print(f"❓ First Question: {data.get('first_question', 'N/A')[:100]}...")
                    print(f"🔊 Voice Mode: {data.get('voice_mode', False)}")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Session: {session_id[:8]}..., Voice Mode: {data.get('voice_mode')}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Interview Start with Voice Mode", success, details)
            return success
        except Exception as e:
            self.log_test("Interview Start with Voice Mode", False, f"Exception: {str(e)}")
            return False
    
    def run_webcam_token_test(self) -> Dict[str, bool]:
        """Run webcam token generation test sequence"""
        print("=" * 70)
        print("WEBCAM FUNCTIONALITY TOKEN GENERATION TEST")
        print("Testing admin login and token creation for webcam testing")
        print("=" * 70)
        print()
        
        results = {}
        
        # Test admin login
        results["admin_login"] = self.test_admin_login()
        
        if results["admin_login"]:
            # Create enhanced token for webcam testing
            results["token_creation"] = self.test_enhanced_token_creation()
            
            if results["token_creation"]:
                # Validate the token
                results["token_validation"] = self.test_token_validation()
                
                # Test camera endpoint
                results["camera_test"] = self.test_camera_test_endpoint()
                
                # Test interview start with voice mode
                results["interview_start_voice"] = self.test_interview_start_with_voice()
        else:
            print("❌ Admin login failed - skipping token creation tests")
            results["token_creation"] = False
            results["token_validation"] = False
            results["camera_test"] = False
            results["interview_start_voice"] = False
        
        # Summary
        print("=" * 70)
        print("WEBCAM TOKEN TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if self.generated_token and results.get("token_validation", False):
            print()
            print("🎯 SUCCESS! Token ready for webcam testing:")
            print(f"   TOKEN: {self.generated_token}")
            print()
            print("📋 Instructions for webcam testing:")
            print("1. Go to the candidate portal")
            print("2. Enter the token above")
            print("3. Click 'Start Interview'")
            print("4. Test the webcam functionality when prompted")
            print("5. Verify that the 'Start Interview' button activates the webcam")
        else:
            print("❌ Token generation failed - webcam testing not possible")
        
        return results

def main():
    """Main test execution"""
    tester = WebcamTokenTester()
    results = tester.run_webcam_token_test()
    
    # Return exit code based on results
    token_ready = results.get("token_validation", False)
    return 0 if token_ready else 1

if __name__ == "__main__":
    exit(main())