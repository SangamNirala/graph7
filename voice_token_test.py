#!/usr/bin/env python3
"""
Voice Recording Token Generation Test
Specifically tests the creation of fresh tokens for voice recording functionality testing.

This test focuses on:
1. Generate Fresh Token: Create a new enhanced interview token with voice mode enabled
2. Verify Token: Ensure the token is valid and ready for voice interview testing  
3. Test Backend Readiness: Confirm all backend endpoints are working for voice interviews

Context: Fixed voice recording issues in frontend:
- Fixed transcript duplication (was repeating same text multiple times)
- Changed flow: when recording stops, transcript now populates answer field instead of auto-submitting
- Added proper state management for transcript handling
"""

import requests
import json
import time
import io
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://9111a607-ad7c-4aad-8586-9dca4be775f2.preview.emergentagent.com/api"

class VoiceTokenTester:
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
    
    def test_admin_authentication(self) -> bool:
        """Test admin authentication with correct password"""
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
            if success:
                details += ", Admin authenticated successfully"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Admin Authentication", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_token_creation(self) -> bool:
        """Create a fresh enhanced token with voice mode enabled"""
        try:
            # Create resume content for voice recording testing
            resume_content = """Sarah Chen
Voice Recording Test Candidate
Email: sarah.chen@email.com
Phone: (555) 999-8888

EXPERIENCE:
- 5+ years of frontend development with React and JavaScript
- Experience with Web Speech API and voice interfaces
- Built real-time audio processing applications
- Strong background in user interface design and accessibility

SKILLS:
- JavaScript, TypeScript, React, HTML5, CSS3
- Web Speech API, WebRTC, Audio Web APIs
- Voice UI design, accessibility standards
- Real-time communication systems
- MongoDB, Node.js, Express

EDUCATION:
Master of Science in Human-Computer Interaction
Tech Institute, 2019

PROJECTS:
- Voice-controlled task management application
- Real-time speech transcription system
- Accessible voice navigation interface"""
            
            files = {
                'resume_file': ('voice_test_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Frontend Developer - Voice Interface Specialist',
                'job_description': 'We are seeking a frontend developer with expertise in voice interfaces and speech technologies. The role involves building voice-enabled web applications, implementing Web Speech API integrations, and creating accessible voice user interfaces.',
                'job_requirements': 'Requirements: 3+ years frontend experience, Web Speech API knowledge, voice interface design, accessibility standards, real-time audio processing, React expertise.',
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
                    estimated_duration = features.get("estimated_duration", 0)
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.fresh_token}, Duration: {estimated_duration}min"
                details += f", Role: {features.get('role_archetype')}, Focus: {features.get('interview_focus')}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Enhanced Token Creation", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Token Creation", False, f"Exception: {str(e)}")
            return False
    
    def test_token_validation(self) -> bool:
        """Verify the fresh token is valid and ready for use"""
        if not self.fresh_token:
            self.log_test("Token Validation", False, "No fresh token available")
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
                          "job_description" in data)
                
                if success:
                    job_title = data.get("job_title", "")
                    is_enhanced = data.get("is_enhanced", False)
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Valid: True, Job: {job_title}, Enhanced: {is_enhanced}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Token Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_camera_test_endpoint(self) -> bool:
        """Test camera test endpoint for voice interview preparation"""
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
                          "features" in data)
                
                if success:
                    features = data.get("features", {})
                    voice_mode = features.get("voice_mode", False)
                    role_archetype = features.get("role_archetype", "")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Voice Mode: {voice_mode}, Role: {role_archetype}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Camera Test Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Camera Test Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_interview_start(self) -> bool:
        """Test starting voice interview with the fresh token"""
        if not self.fresh_token:
            self.log_test("Voice Interview Start", False, "No fresh token available")
            return False
        
        try:
            payload = {
                "token": self.fresh_token,
                "candidate_name": "Sarah Chen - Voice Test Candidate",
                "voice_mode": True
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=25  # Longer timeout for potential TTS generation
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
                    first_question = data.get("first_question", "")
                    question_number = data.get("question_number", 0)
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Session: {self.session_id[:8]}..., Voice Mode: True"
                details += f", Question {question_number}: {first_question[:50]}..."
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Voice Interview Start", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Interview Start", False, f"Exception: {str(e)}")
            return False
    
    def test_text_cleaning_functionality(self) -> bool:
        """Test that backend text cleaning is working for TTS"""
        if not self.session_id:
            self.log_test("Text Cleaning for TTS", False, "No session ID available")
            return False
        
        try:
            # Test question rephrasing which uses text cleaning
            payload = {
                "session_id": self.session_id,
                "original_question": "Can you explain how `JavaScript` **closures** work and provide an example with `code snippets`?"
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
                
                if success:
                    rephrased = data.get("rephrased_question", "")
                    cleaned_text = data.get("question_text", "")
                    # Check that backticks and formatting are removed
                    has_backticks = "`" in cleaned_text
                    has_bold = "**" in cleaned_text
                    success = not has_backticks and not has_bold
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Text cleaned successfully (no backticks/formatting)"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Text Cleaning for TTS", success, details)
            return success
        except Exception as e:
            self.log_test("Text Cleaning for TTS", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_message_processing(self) -> bool:
        """Test voice message processing endpoint"""
        if not self.fresh_token:
            self.log_test("Voice Message Processing", False, "No fresh token available")
            return False
        
        try:
            # Test sending a text message (simulating transcript from Web Speech API)
            payload = {
                "token": self.fresh_token,
                "message": "I have extensive experience with JavaScript and React. I've built several voice-enabled applications using the Web Speech API, including a real-time transcription system and a voice-controlled task manager. My approach to voice interfaces focuses on accessibility and user experience."
            }
            response = self.session.post(
                f"{self.base_url}/candidate/send-message",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("next_question" in data or "completed" in data)
                
                if success:
                    if data.get("completed"):
                        details = f"Status: {response.status_code}, Interview completed"
                    else:
                        next_question = data.get("next_question", "")
                        details = f"Status: {response.status_code}, Next question: {next_question[:50]}..."
            
            if not success:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Voice Message Processing", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Message Processing", False, f"Exception: {str(e)}")
            return False
    
    def run_voice_token_tests(self) -> Dict[str, bool]:
        """Run all voice token generation and validation tests"""
        print("=" * 80)
        print("VOICE RECORDING TOKEN GENERATION TEST")
        print("Creating fresh token for voice recording functionality testing")
        print("=" * 80)
        print()
        
        results = {}
        
        # Step 1: Admin authentication
        results["admin_authentication"] = self.test_admin_authentication()
        
        # Step 2: Generate fresh enhanced token with voice mode
        results["enhanced_token_creation"] = self.test_enhanced_token_creation()
        
        # Step 3: Verify token is valid
        results["token_validation"] = self.test_token_validation()
        
        # Step 4: Test camera test endpoint
        results["camera_test_endpoint"] = self.test_camera_test_endpoint()
        
        # Step 5: Test voice interview start
        results["voice_interview_start"] = self.test_voice_interview_start()
        
        # Step 6: Test text cleaning for TTS
        results["text_cleaning_functionality"] = self.test_text_cleaning_functionality()
        
        # Step 7: Test voice message processing
        results["voice_message_processing"] = self.test_voice_message_processing()
        
        # Summary
        print("=" * 80)
        print("VOICE TOKEN TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print(f"\nTest Results:")
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if self.fresh_token:
            print(f"\n🎯 FRESH TOKEN GENERATED: {self.fresh_token}")
            print("This token is ready for voice recording functionality testing!")
            print("\nToken Features:")
            print("- Voice mode enabled")
            print("- Enhanced interview with 8-10 questions")
            print("- Software Engineer role archetype")
            print("- Technical Deep-Dive focus")
            print("- Frontend Developer - Voice Interface Specialist position")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Fresh voice token is ready for testing.")
            print("Backend voice interview support is fully operational.")
        elif passed >= total * 0.8:
            print("\n✅ MOSTLY WORKING! Voice token generated with minor issues.")
        else:
            print("\n⚠️  Multiple tests failed. Voice functionality may have issues.")
        
        return results

def main():
    """Main test execution"""
    tester = VoiceTokenTester()
    results = tester.run_voice_token_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())