#!/usr/bin/env python3
"""
Web Speech API Backend Integration Test
Testing the backend integration for Web Speech API functionality
"""

import requests
import json
import io
from typing import Dict, Any

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://ed1be7ee-3b3d-4ddb-a670-999d49a5f3da.preview.emergentagent.com/api"

class WebSpeechAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.generated_token = None
        self.session_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_admin_login(self) -> bool:
        """Test admin authentication first"""
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
            
            details = f"Status: {response.status_code}"
            self.log_test("Admin Authentication", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_token_creation(self) -> bool:
        """Test creating enhanced token for Web Speech API testing"""
        try:
            # Create sample resume content for Web Speech API testing
            resume_content = """Sarah Johnson
Web Speech API Developer
Email: sarah.johnson@email.com
Phone: (555) 999-8888

EXPERIENCE:
- 4+ years of frontend development with voice interfaces
- Experience with Web Speech API, SpeechRecognition, and SpeechSynthesis
- Built voice-controlled applications and accessibility features
- Strong background in JavaScript, React, and audio processing

SKILLS:
- JavaScript, TypeScript, React, HTML5
- Web Speech API, SpeechRecognition, SpeechSynthesis
- Audio processing, WebRTC, real-time applications
- Accessibility (WCAG), voice UI design
- Node.js, Express, MongoDB

EDUCATION:
Master of Science in Human-Computer Interaction
Tech University, 2019"""
            
            files = {
                'resume_file': ('web_speech_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Frontend Developer - Voice Interface Specialist',
                'job_description': 'We are seeking a frontend developer with expertise in Web Speech API and voice interfaces. The role involves implementing speech-to-text and text-to-speech functionality for our AI interview platform.',
                'job_requirements': 'Requirements: 3+ years frontend experience, Web Speech API expertise, JavaScript/React skills, voice interface design, accessibility knowledge.',
                'include_coding_challenge': 'false',
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
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.generated_token[:8]}..., Features: {result.get('features', {})}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Enhanced Token Creation", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Token Creation", False, f"Exception: {str(e)}")
            return False
    
    def test_token_validation(self) -> bool:
        """Test token validation for Web Speech API token"""
        if not self.generated_token:
            self.log_test("Token Validation", False, "No token available")
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
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Job: {data.get('job_title', 'N/A')[:50]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Token Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_camera_test_endpoint(self) -> bool:
        """Test camera test endpoint for Web Speech API features"""
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
                success = (data.get("success", False) and 
                          "features" in data and
                          data["features"].get("voice_mode") == True)
            
            details = f"Status: {response.status_code}"
            if success:
                features = data.get("features", {})
                details += f", Voice Mode: {features.get('voice_mode')}, Role: {features.get('role_archetype')}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Camera Test Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Camera Test Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_interview_start(self) -> bool:
        """Test starting voice interview with Web Speech API support"""
        if not self.generated_token:
            self.log_test("Voice Interview Start", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "candidate_name": "Sarah Johnson",
                "voice_mode": True
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
                          data.get("voice_mode") == True)
                if success:
                    self.session_id = data["session_id"]
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Session: {self.session_id[:8]}..., Voice Mode: {data.get('voice_mode')}"
                details += f", Question: {data.get('first_question', '')[:50]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Voice Interview Start", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Interview Start", False, f"Exception: {str(e)}")
            return False
    
    def test_text_cleaning_for_speech(self) -> bool:
        """Test text cleaning functionality for Web Speech API"""
        if not self.session_id:
            self.log_test("Text Cleaning for Speech", False, "No session available")
            return False
        
        try:
            # Test question rephrasing which uses text cleaning
            payload = {
                "session_id": self.session_id,
                "original_question": "Can you explain how `JavaScript` **closures** work and provide an example with `setTimeout`?"
            }
            response = self.session.post(
                f"{self.base_url}/candidate/rephrase-question",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("rephrased_question" in data and 
                          "question_text" in data)
                
                # Check if backticks and formatting are removed
                if success:
                    rephrased = data.get("rephrased_question", "")
                    question_text = data.get("question_text", "")
                    # Text should not contain backticks or markdown formatting
                    has_backticks = "`" in rephrased or "`" in question_text
                    has_bold = "**" in rephrased or "**" in question_text
                    success = not (has_backticks or has_bold)
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Cleaned text: {data.get('question_text', '')[:50]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Text Cleaning for Speech", success, details)
            return success
        except Exception as e:
            self.log_test("Text Cleaning for Speech", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_message_processing(self) -> bool:
        """Test voice message processing endpoints"""
        if not self.generated_token:
            self.log_test("Voice Message Processing", False, "No token available")
            return False
        
        try:
            # Test sending a text message (simulating Web Speech API transcription)
            payload = {
                "token": self.generated_token,
                "message": "I have extensive experience with Web Speech API, including both SpeechRecognition for speech-to-text and SpeechSynthesis for text-to-speech functionality. I've implemented voice-controlled interfaces and accessibility features."
            }
            response = self.session.post(
                f"{self.base_url}/candidate/send-message",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("next_question" in data or data.get("completed", False))
            
            details = f"Status: {response.status_code}"
            if success:
                if data.get("completed"):
                    details += ", Interview completed"
                else:
                    details += f", Next question: {data.get('next_question', '')[:50]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Voice Message Processing", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Message Processing", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all Web Speech API backend integration tests"""
        print("=" * 70)
        print("WEB SPEECH API BACKEND INTEGRATION TEST")
        print("Testing backend support for Web Speech API functionality")
        print("=" * 70)
        print()
        
        results = {}
        
        # Admin authentication
        results["admin_login"] = self.test_admin_login()
        
        # Enhanced token creation for Web Speech API
        results["enhanced_token_creation"] = self.test_enhanced_token_creation()
        
        # Token validation
        results["token_validation"] = self.test_token_validation()
        
        # Camera test endpoint
        results["camera_test_endpoint"] = self.test_camera_test_endpoint()
        
        # Voice interview start
        results["voice_interview_start"] = self.test_voice_interview_start()
        
        # Text cleaning for speech
        results["text_cleaning_for_speech"] = self.test_text_cleaning_for_speech()
        
        # Voice message processing
        results["voice_message_processing"] = self.test_voice_message_processing()
        
        # Summary
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print(f"\nWeb Speech API Backend Integration Results:")
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        # Analysis
        critical_tests = ["enhanced_token_creation", "voice_interview_start", "text_cleaning_for_speech"]
        critical_passed = sum(1 for test in critical_tests if results.get(test, False))
        
        if critical_passed == len(critical_tests):
            print("🎉 WEB SPEECH API BACKEND INTEGRATION WORKING! Backend properly supports Web Speech API functionality.")
        elif critical_passed >= len(critical_tests) * 0.7:
            print("✅ MOSTLY WORKING! Most Web Speech API backend features are functional.")
        else:
            print("⚠️  Web Speech API backend integration has issues.")
        
        return results

def main():
    """Main test execution"""
    tester = WebSpeechAPITester()
    results = tester.run_all_tests()
    
    # Return exit code based on critical tests
    critical_tests = ["enhanced_token_creation", "voice_interview_start", "text_cleaning_for_speech"]
    critical_passed = all(results.get(test, False) for test in critical_tests)
    
    return 0 if critical_passed else 1

if __name__ == "__main__":
    exit(main())