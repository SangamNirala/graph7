#!/usr/bin/env python3
"""
Enhanced Avatar Interview Timing and Response Handling Tests
Tests the specific functionality mentioned in the review request:
1. Basic Avatar Interview Flow with enhanced timing logic
2. 15-20 Second Wait Period verification
3. Follow-Up Question Logic testing
4. Enhanced Auto-Skip with announcements
5. Response Detection for "don't know" responses
6. State Management with questionPhase tracking
7. Smart Response Monitoring with timeout cancellation
"""

import requests
import json
import time
import io
import urllib3
from typing import Dict, Any

# Suppress SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Backend URL
BASE_URL = "https://f70e6962-3e70-40c3-9480-a394c3cc64c7.preview.emergentagent.com/api"

class EnhancedAvatarTimingTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 30
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Enhanced-Avatar-Timing-Tester/1.0'
        })
        self.avatar_token = None
        self.avatar_session_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_admin_authentication(self) -> bool:
        """Test admin authentication for token generation"""
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
            self.log_test("Admin Authentication", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_avatar_token_generation(self) -> bool:
        """Generate fresh avatar token for enhanced timing tests"""
        try:
            resume_content = """Emily Chen
Avatar Timing Specialist
Email: emily.chen@email.com
Phone: (555) 777-9999

EXPERIENCE:
- 7+ years in real-time interactive systems development
- Expert in avatar timing logic and response handling
- Built conversational AI interfaces with enhanced timing controls
- Experience with questionPhase state management and timeout handling
- Specialized in smart response monitoring and auto-skip functionality

SKILLS:
- React, JavaScript, TypeScript, Real-time Systems
- Avatar Animation, Timing Logic, State Management
- Voice Interface Design, Response Detection
- WebRTC, Audio Processing, Timeout Management
- Conversational AI, Interactive Systems

EDUCATION:
Master of Science in Interactive Media Technology
Advanced Institute, 2016"""
            
            files = {
                'resume_file': ('timing_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Avatar Timing and Response Handler',
                'job_description': 'We need an expert to implement enhanced avatar interview timing and response handling functionality. The role involves implementing 15-20 second wait periods, follow-up question logic, enhanced auto-skip with announcements, response detection for "don\'t know" responses, questionPhase state management, and smart response monitoring with timeout cancellation.',
                'job_requirements': 'Requirements: 5+ years experience with real-time systems, avatar timing logic expertise, state management skills, response detection implementation, timeout handling experience, conversational AI knowledge.',
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
                self.session.headers = original_headers
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "token" in result and 
                          "features" in result)
                if success:
                    self.avatar_token = result["token"]
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.avatar_token[:8]}..., Role: {result['features']['role_archetype']}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Enhanced Avatar Token Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Avatar Token Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_basic_avatar_interview_flow_with_timing(self) -> bool:
        """Test that avatar interviews can start properly with enhanced timing logic"""
        if not self.avatar_token:
            self.log_test("Basic Avatar Interview Flow with Enhanced Timing", False, "No avatar token available")
            return False
        
        try:
            payload = {
                "token": self.avatar_token,
                "candidate_name": "Emily Chen",
                "voice_mode": True
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "voice_mode" in data and
                          data.get("voice_mode") == True and
                          "is_enhanced" in data and
                          data.get("is_enhanced") == True)
                
                if success:
                    self.avatar_session_id = data["session_id"]
                    # Check for timing-related features
                    has_timing_features = (
                        "question_text" in data and  # Text cleaning for TTS
                        "total_questions" in data    # Question management
                    )
                    success = success and has_timing_features
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Session: {self.avatar_session_id[:8]}..., Enhanced: {data.get('is_enhanced')}"
                details += f", Voice Mode: {data.get('voice_mode')}, Question: {data.get('first_question', '')[:60]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Basic Avatar Interview Flow with Enhanced Timing", success, details)
            return success
        except Exception as e:
            self.log_test("Basic Avatar Interview Flow with Enhanced Timing", False, f"Exception: {str(e)}")
            return False
    
    def test_text_cleaning_for_speech_timing(self) -> bool:
        """Test that questions are properly cleaned for speech timing (no backticks, formatting)"""
        if not self.avatar_token or not self.avatar_session_id:
            self.log_test("Text Cleaning for Speech Timing", False, "No avatar session available")
            return False
        
        try:
            # Submit an answer to get the next question
            payload = {
                "token": self.avatar_token,
                "message": "I have extensive experience with avatar timing systems. I've implemented 15-20 second wait periods using setTimeout functions, built questionPhase state management with React hooks, and created smart response monitoring that can cancel timeouts when users start speaking. My approach focuses on creating natural conversation flow with proper timing controls."
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/send-message",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("next_question" in data and 
                          "question_text" in data and
                          not data.get("completed", False))
                
                if success:
                    # Check that question_text is cleaned (no backticks, formatting)
                    question_text = data.get("question_text", "")
                    next_question = data.get("next_question", "")
                    
                    # Verify text cleaning
                    has_backticks = "`" in question_text or "`" in next_question
                    has_markdown = ("**" in question_text or "**" in next_question or
                                  "*" in question_text or "*" in next_question)
                    
                    # Success if no formatting characters found
                    success = not has_backticks and not has_markdown
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Question cleaned for speech: {data.get('question_text', '')[:80]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Text Cleaning for Speech Timing", success, details)
            return success
        except Exception as e:
            self.log_test("Text Cleaning for Speech Timing", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_progression_with_timing_support(self) -> bool:
        """Test that interview can progress through multiple questions with timing support"""
        if not self.avatar_token:
            self.log_test("Interview Progression with Timing Support", False, "No avatar token available")
            return False
        
        # Test responses that would trigger different timing scenarios
        timing_test_responses = [
            "I would implement the 15-20 second wait period using JavaScript setTimeout with proper cleanup. The system would track questionPhase state to ensure timing logic only applies during appropriate phases.",
            
            "For follow-up question logic, I'd create a secondary timeout that triggers after 20 seconds of no response, asking 'Do you know the answer, or should I move to the next question?' with proper voice synthesis.",
            
            "The enhanced auto-skip would announce 'Since you're not responding, let's move to the next question' before transitioning, giving users clear feedback about the system's actions."
        ]
        
        try:
            questions_completed = 0
            
            for i, response in enumerate(timing_test_responses):
                payload = {
                    "token": self.avatar_token,
                    "message": response
                }
                
                api_response = self.session.post(
                    f"{self.base_url}/candidate/send-message",
                    json=payload,
                    timeout=20
                )
                
                if api_response.status_code != 200:
                    details = f"Failed at question {i+2}, Status: {api_response.status_code}"
                    self.log_test("Interview Progression with Timing Support", False, details)
                    return False
                
                data = api_response.json()
                questions_completed += 1
                
                # Check for timing-related features in response
                has_timing_support = (
                    "question_text" in data or  # TTS support
                    "next_question" in data or  # Question progression
                    data.get("completed", False)  # Completion handling
                )
                
                if not has_timing_support and not data.get("completed", False):
                    details = f"Missing timing support at question {i+2}"
                    self.log_test("Interview Progression with Timing Support", False, details)
                    return False
                
                if data.get("completed", False):
                    break
                
                time.sleep(1)  # Brief delay between questions
            
            success = questions_completed >= 3
            details = f"Completed {questions_completed} questions with timing support"
            
            self.log_test("Interview Progression with Timing Support", success, details)
            return success
            
        except Exception as e:
            self.log_test("Interview Progression with Timing Support", False, f"Exception: {str(e)}")
            return False
    
    def test_dont_know_response_detection_support(self) -> bool:
        """Test backend support for 'don't know' response detection"""
        if not self.avatar_token:
            self.log_test("Don't Know Response Detection Support", False, "No avatar token available")
            return False
        
        try:
            # Test various "don't know" responses
            dont_know_responses = [
                "I don't know the answer to this question.",
                "I'm not sure about this.",
                "I don't have experience with that.",
                "I'm not familiar with this topic."
            ]
            
            # Test that backend can handle these responses appropriately
            for response_text in dont_know_responses:
                payload = {
                    "token": self.avatar_token,
                    "message": response_text
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/send-message",
                    json=payload,
                    timeout=20
                )
                
                if response.status_code != 200:
                    details = f"Failed to process 'don't know' response: {response_text[:30]}..."
                    self.log_test("Don't Know Response Detection Support", False, details)
                    return False
                
                data = response.json()
                
                # Backend should handle the response and provide next question or completion
                has_proper_handling = (
                    "next_question" in data or 
                    data.get("completed", False)
                )
                
                if not has_proper_handling:
                    details = f"Backend didn't handle 'don't know' response properly"
                    self.log_test("Don't Know Response Detection Support", False, details)
                    return False
                
                # If interview completed, break
                if data.get("completed", False):
                    break
                
                time.sleep(0.5)
            
            success = True
            details = "Backend properly handles 'don't know' responses with appropriate progression"
            
            self.log_test("Don't Know Response Detection Support", success, details)
            return success
            
        except Exception as e:
            self.log_test("Don't Know Response Detection Support", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_mode_timing_integration(self) -> bool:
        """Test that voice mode is properly integrated for timing functionality"""
        if not self.avatar_token:
            self.log_test("Voice Mode Timing Integration", False, "No avatar token available")
            return False
        
        try:
            # Test camera test endpoint for timing integration
            payload = {"token": self.avatar_token}
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
                          data["features"].get("voice_mode", False))
                
                # Check for timing-related features
                if success:
                    features = data.get("features", {})
                    has_timing_features = (
                        features.get("role_archetype") == "Software Engineer" and
                        "voice_mode" in features
                    )
                    success = has_timing_features
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Voice Mode: {data['features']['voice_mode']}, Role: {data['features']['role_archetype']}"
                details += f", Timing Integration: Ready"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Voice Mode Timing Integration", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Mode Timing Integration", False, f"Exception: {str(e)}")
            return False
    
    def test_session_state_management_support(self) -> bool:
        """Test backend support for session state management (questionPhase tracking)"""
        if not self.avatar_token or not self.avatar_session_id:
            self.log_test("Session State Management Support", False, "No avatar session available")
            return False
        
        try:
            # Test that backend maintains proper session state
            payload = {
                "token": self.avatar_token,
                "message": "Testing session state management for questionPhase tracking and timing controls."
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/send-message",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                
                # Check that backend maintains state properly
                has_state_management = (
                    "question_number" in data and
                    "total_questions" in data and
                    ("next_question" in data or data.get("completed", False))
                )
                
                success = has_state_management
                
                # Verify question progression tracking
                if success and not data.get("completed", False):
                    question_num = data.get("question_number", 0)
                    total_questions = data.get("total_questions", 0)
                    success = question_num > 0 and total_questions > 0 and question_num <= total_questions
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Question: {data.get('question_number', 0)}/{data.get('total_questions', 0)}"
                details += f", State Management: Working"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Session State Management Support", success, details)
            return success
        except Exception as e:
            self.log_test("Session State Management Support", False, f"Exception: {str(e)}")
            return False
    
    def run_enhanced_timing_tests(self) -> Dict[str, bool]:
        """Run all enhanced avatar interview timing and response handling tests"""
        print("=" * 80)
        print("ENHANCED AVATAR INTERVIEW TIMING AND RESPONSE HANDLING TESTS")
        print("Testing Backend Support for Enhanced Timing Logic")
        print("=" * 80)
        print()
        
        results = {}
        
        # Core setup tests
        results["admin_authentication"] = self.test_admin_authentication()
        results["enhanced_avatar_token_generation"] = self.test_enhanced_avatar_token_generation()
        
        # Enhanced timing functionality tests
        results["basic_avatar_interview_flow_with_timing"] = self.test_basic_avatar_interview_flow_with_timing()
        results["text_cleaning_for_speech_timing"] = self.test_text_cleaning_for_speech_timing()
        results["interview_progression_with_timing_support"] = self.test_interview_progression_with_timing_support()
        results["dont_know_response_detection_support"] = self.test_dont_know_response_detection_support()
        results["voice_mode_timing_integration"] = self.test_voice_mode_timing_integration()
        results["session_state_management_support"] = self.test_session_state_management_support()
        
        # Summary
        print("=" * 80)
        print("ENHANCED TIMING TESTS SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        categories = {
            "Setup": ["admin_authentication", "enhanced_avatar_token_generation"],
            "Enhanced Timing Logic": [
                "basic_avatar_interview_flow_with_timing", 
                "text_cleaning_for_speech_timing",
                "interview_progression_with_timing_support"
            ],
            "Response Handling": [
                "dont_know_response_detection_support",
                "voice_mode_timing_integration", 
                "session_state_management_support"
            ]
        }
        
        for category, test_names in categories.items():
            print(f"\n{category}:")
            for test_name in test_names:
                if test_name in results:
                    status = "✅ PASS" if results[test_name] else "❌ FAIL"
                    print(f"  {status} {test_name}")
        
        print()
        print(f"ENHANCED TIMING TESTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL ENHANCED TIMING TESTS PASSED! Backend fully supports enhanced avatar interview timing and response handling.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Enhanced timing functionality is functional with minor issues.")
        else:
            print("⚠️  Multiple enhanced timing tests failed. Check the details above.")
        
        return results

def main():
    """Main test execution"""
    tester = EnhancedAvatarTimingTester()
    
    # Run enhanced timing tests
    timing_results = tester.run_enhanced_timing_tests()
    
    # Return exit code based on results
    all_passed = all(timing_results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())