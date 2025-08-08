#!/usr/bin/env python3
"""
Admin Login and Fresh Token Generation Testing
Specifically tests:
1. Admin authentication with Game@1234 password
2. Generate a new fresh token for voice recording testing
3. Verify token validation and voice interview capabilities
"""

import requests
import json
import time
import io
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://204317b8-4340-425d-9217-c13cabdf4c95.preview.emergentagent.com/api"

class AdminLoginTokenTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.fresh_token = None
        self.session_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_backend_connectivity(self) -> bool:
        """Test basic backend connectivity"""
        try:
            # Test a simple endpoint to verify backend is responding
            response = self.session.get(f"{self.base_url.replace('/api', '')}", timeout=10)
            success = response.status_code in [200, 404, 405]  # Any response means server is up
            details = f"Status: {response.status_code} - Backend server is responding"
            self.log_test("Backend Connectivity", success, details)
            return success
        except Exception as e:
            self.log_test("Backend Connectivity", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_correct_password(self) -> bool:
        """Test admin authentication with correct password Game@1234"""
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
                success = data.get("success", False) and data.get("message") == "Admin authenticated successfully"
            
            details = f"Status: {response.status_code}, Response: {response.json() if response.status_code == 200 else response.text[:200]}"
            self.log_test("Admin Login (Game@1234)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login (Game@1234)", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_invalid_password(self) -> bool:
        """Test admin authentication with invalid password for security verification"""
        try:
            payload = {"password": "WrongPassword123"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 401
            details = f"Status: {response.status_code} - Security validation working correctly"
            self.log_test("Admin Login Security (Invalid Password)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login Security (Invalid Password)", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_empty_password(self) -> bool:
        """Test admin authentication with empty password"""
        try:
            payload = {"password": ""}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 401
            details = f"Status: {response.status_code} - Empty password properly rejected"
            self.log_test("Admin Login Security (Empty Password)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login Security (Empty Password)", False, f"Exception: {str(e)}")
            return False
    
    def generate_fresh_token_enhanced(self) -> bool:
        """Generate a fresh enhanced token for voice recording testing"""
        try:
            # Create resume content specifically for voice recording testing
            resume_content = """Sarah Chen
Senior Voice Technology Specialist
Email: sarah.chen@voicetech.com
Phone: (555) 999-8888

EXPERIENCE:
- 6+ years in voice interface development and audio processing
- Expert in Web Speech API, Google Cloud Speech-to-Text, and TTS systems
- Led development of voice-enabled applications with real-time transcription
- Experience with voice biometrics and speech recognition optimization
- Built voice recording systems with start/stop functionality and transcript processing

TECHNICAL SKILLS:
- Voice Technologies: Web Speech API, Google Cloud Speech, Amazon Polly
- Programming: JavaScript, Python, React, FastAPI, Node.js
- Audio Processing: WebRTC, MediaRecorder API, audio format conversion
- Real-time Systems: WebSocket, streaming audio, low-latency processing
- Databases: MongoDB, PostgreSQL, audio metadata storage

PROJECTS:
- Voice Interview Platform: Built complete voice recording system with transcript generation
- Real-time Voice Assistant: Implemented speech recognition with 95% accuracy
- Audio Analytics Dashboard: Created voice sentiment analysis and emotional intelligence scoring
- Multi-language Voice System: Developed voice interfaces supporting 12 languages

EDUCATION:
Master of Science in Computer Science (Audio Processing Specialization)
Voice Technology Institute, 2018"""
            
            files = {
                'resume_file': ('voice_specialist_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Voice Recording Engineer - Interview Platform',
                'job_description': 'We are seeking a senior voice recording engineer to enhance our AI-powered interview platform. The role involves optimizing voice recording functionality, implementing advanced speech-to-text features, and ensuring seamless voice interview experiences. You will work on cutting-edge voice technologies including Web Speech API integration, real-time transcription, and voice analytics.',
                'job_requirements': 'Requirements: 5+ years voice technology experience, Web Speech API expertise, real-time audio processing, JavaScript/Python proficiency, experience with interview platforms, knowledge of speech recognition optimization, familiarity with voice UI/UX design.',
                'include_coding_challenge': True,
                'role_archetype': 'Software Engineer',
                'interview_focus': 'Technical Deep-Dive',
                'min_questions': 8,
                'max_questions': 10
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job-enhanced",
                files=files,
                data=data,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "token" in result and 
                          "features" in result)
                if success:
                    self.fresh_token = result["token"]
                    features = result.get("features", {})
                    details = f"Status: {response.status_code}, Token: {self.fresh_token}, Features: coding_challenge={features.get('coding_challenge')}, role_archetype={features.get('role_archetype')}, interview_focus={features.get('interview_focus')}, estimated_duration={features.get('estimated_duration')}min"
                else:
                    details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            
            self.log_test("Fresh Enhanced Token Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Fresh Enhanced Token Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_token_validation(self) -> bool:
        """Test validation of the freshly generated token"""
        if not self.fresh_token:
            self.log_test("Fresh Token Validation", False, "No fresh token available")
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
                success = (data.get("valid", False) and 
                          "job_title" in data and
                          "is_enhanced" in data)
                
                if success:
                    details = f"Status: {response.status_code}, Valid: {data.get('valid')}, Job: {data.get('job_title')}, Enhanced: {data.get('is_enhanced')}, Features: {data.get('features', {})}"
                else:
                    details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Fresh Token Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Fresh Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_camera_test_endpoint(self) -> bool:
        """Test camera test endpoint with fresh token"""
        if not self.fresh_token:
            self.log_test("Camera Test Endpoint", False, "No fresh token available")
            return False
        
        try:
            payload = {"token": self.fresh_token}
            response = self.session.post(
                f"{self.base_url}/candidate/camera-test",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "features" in data and
                          data.get("features", {}).get("voice_mode") == True)
                
                if success:
                    features = data.get("features", {})
                    details = f"Status: {response.status_code}, Voice Mode: {features.get('voice_mode')}, Coding Challenge: {features.get('coding_challenge')}, Role: {features.get('role_archetype')}"
                else:
                    details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Camera Test Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Camera Test Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_interview_start(self) -> bool:
        """Test starting voice interview with fresh token"""
        if not self.fresh_token:
            self.log_test("Voice Interview Start", False, "No fresh token available")
            return False
        
        try:
            payload = {
                "token": self.fresh_token,
                "candidate_name": "Sarah Chen - Voice Recording Test",
                "voice_mode": True
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=25  # Longer timeout for voice processing
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "voice_mode" in data and
                          data.get("voice_mode") == True)
                
                if success:
                    self.session_id = data["session_id"]
                    details = f"Status: {response.status_code}, Session ID: {self.session_id[:12]}..., Voice Mode: {data.get('voice_mode')}, Question: {data.get('first_question', '')[:50]}..."
                else:
                    details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            
            self.log_test("Voice Interview Start", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Interview Start", False, f"Exception: {str(e)}")
            return False
    
    def test_text_cleaning_for_tts(self) -> bool:
        """Test text cleaning functionality for TTS (backtick removal)"""
        if not self.session_id:
            self.log_test("Text Cleaning for TTS", False, "No session ID available")
            return False
        
        try:
            # Test the voice message processing endpoint which should clean text
            payload = {
                "session_id": self.session_id,
                "message": "I have experience with `JavaScript` and `Python` programming languages, including `FastAPI` and `React` frameworks."
            }
            response = self.session.post(
                f"{self.base_url}/voice/process-message",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("next_question" in data and 
                          "question_text" in data)
                
                # Check if backticks are removed from the question text
                question_text = data.get("question_text", "")
                has_backticks = "`" in question_text
                success = success and not has_backticks
                
                if success:
                    details = f"Status: {response.status_code}, Text cleaning working - no backticks in TTS text, Question length: {len(question_text)} chars"
                else:
                    details = f"Status: {response.status_code}, Backticks found in TTS text: {has_backticks}, Response: {response.text[:200]}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Text Cleaning for TTS", success, details)
            return success
        except Exception as e:
            self.log_test("Text Cleaning for TTS", False, f"Exception: {str(e)}")
            return False
    
    def run_comprehensive_test(self) -> Dict[str, bool]:
        """Run comprehensive admin login and token generation tests"""
        print("=" * 80)
        print("ADMIN LOGIN & FRESH TOKEN GENERATION TESTING")
        print("Testing admin authentication and voice recording token generation")
        print("=" * 80)
        print()
        
        results = {}
        
        # Test backend connectivity
        results["backend_connectivity"] = self.test_backend_connectivity()
        
        # Test admin login functionality
        results["admin_login_correct"] = self.test_admin_login_correct_password()
        results["admin_login_invalid"] = self.test_admin_login_invalid_password()
        results["admin_login_empty"] = self.test_admin_login_empty_password()
        
        # Test fresh token generation
        results["fresh_token_generation"] = self.generate_fresh_token_enhanced()
        
        # Test token validation and voice capabilities
        results["token_validation"] = self.test_token_validation()
        results["camera_test"] = self.test_camera_test_endpoint()
        results["voice_interview_start"] = self.test_voice_interview_start()
        results["text_cleaning_tts"] = self.test_text_cleaning_for_tts()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by category
        categories = {
            "Backend Infrastructure": ["backend_connectivity"],
            "Admin Authentication": ["admin_login_correct", "admin_login_invalid", "admin_login_empty"],
            "Fresh Token Generation": ["fresh_token_generation", "token_validation"],
            "Voice Interview Capabilities": ["camera_test", "voice_interview_start", "text_cleaning_tts"]
        }
        
        for category, test_names in categories.items():
            print(f"\n{category}:")
            for test_name in test_names:
                if test_name in results:
                    status = "✅ PASS" if results[test_name] else "❌ FAIL"
                    print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        # Display fresh token information
        if self.fresh_token:
            print(f"\n🎯 FRESH TOKEN GENERATED FOR VOICE RECORDING TESTING:")
            print(f"   Token: {self.fresh_token}")
            print(f"   Purpose: Voice recording functionality testing")
            print(f"   Features: Enhanced interview with voice mode, coding challenge, technical focus")
            print(f"   Status: {'✅ Ready for use' if results.get('token_validation', False) else '❌ Validation failed'}")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Admin login and fresh token generation working perfectly.")
        elif passed >= total * 0.8:
            print("\n✅ MOSTLY WORKING! Admin functionality operational with minor issues.")
        else:
            print("\n⚠️  Multiple tests failed. Check the details above.")
        
        return results

def main():
    """Main test execution"""
    tester = AdminLoginTokenTester()
    results = tester.run_comprehensive_test()
    
    # Return exit code based on results
    critical_tests = ["admin_login_correct", "fresh_token_generation", "token_validation"]
    critical_passed = all(results.get(test, False) for test in critical_tests)
    
    return 0 if critical_passed else 1

if __name__ == "__main__":
    exit(main())