#!/usr/bin/env python3
"""
Focused Testing for Candidate Interview Start Functionality
Tests the specific issue: "Failed to start interview: TypeError: Failed to fetch at handleStartInterview"

This test focuses on:
1. Testing if the /api/candidate/start-interview endpoint is accessible and working
2. Check if this is a Gemini API key issue or other backend error
3. Verify if a valid token is needed for the start-interview endpoint
4. Test the complete flow from token generation to interview start
"""

import requests
import json
import time
import io
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://aptitude-models.preview.emergentagent.com/api"

class CandidateInterviewStartTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.generated_token = None
        self.enhanced_token = None
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
            # Test a simple endpoint first
            response = self.session.get(f"{self.base_url}/admin/reports", timeout=10)
            success = response.status_code in [200, 401, 403]  # Any response means backend is reachable
            details = f"Status: {response.status_code} - Backend is {'reachable' if success else 'unreachable'}"
            self.log_test("Backend Connectivity", success, details)
            return success
        except Exception as e:
            self.log_test("Backend Connectivity", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_authentication(self) -> bool:
        """Test admin authentication to ensure backend is working"""
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
    
    def test_token_generation(self) -> bool:
        """Generate a valid token for testing interview start"""
        try:
            # Create sample resume content
            resume_content = """Sarah Wilson
Frontend Developer - Voice Interface Specialist
Email: sarah.wilson@email.com
Phone: (555) 987-6543

EXPERIENCE:
- 4+ years of React and JavaScript development
- Experience with WebRTC and voice interfaces
- Built real-time communication applications
- Strong background in frontend architecture

SKILLS:
- React, JavaScript, TypeScript, HTML5, CSS3
- WebRTC, Web Speech API, audio processing
- FastAPI integration, REST APIs
- Voice UI design and accessibility

EDUCATION:
Bachelor of Science in Computer Science
Tech University, 2019"""
            
            files = {
                'resume_file': ('resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Frontend Developer - Voice Interface Specialist',
                'job_description': 'We are seeking a frontend developer with expertise in voice interfaces and real-time communication. The role involves building voice-enabled web applications and integrating speech technologies.',
                'job_requirements': 'Requirements: 3+ years React experience, WebRTC knowledge, voice interface experience, strong JavaScript skills, real-time application development.'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job",
                files=files,
                data=data,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = result.get("success", False) and "token" in result
                if success:
                    self.generated_token = result["token"]
            
            details = f"Status: {response.status_code}"
            if self.generated_token:
                details += f", Token: {self.generated_token}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Token Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Token Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_token_generation(self) -> bool:
        """Generate an enhanced token for testing voice interview start"""
        try:
            # Create sample resume content
            resume_content = """Michael Chen
Senior Software Engineer
Email: michael.chen@email.com
Phone: (555) 456-7890

EXPERIENCE:
- 6+ years of full-stack development
- Team lead experience with 5+ developers
- Microservices architecture and cloud deployment
- Strong problem-solving and communication skills

SKILLS:
- Python, JavaScript, TypeScript, Java
- FastAPI, React, Node.js, Spring Boot
- Docker, Kubernetes, AWS, Azure
- Team leadership and mentoring

EDUCATION:
Master of Science in Computer Science
University of Technology, 2017"""
            
            files = {
                'resume_file': ('enhanced_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Software Engineer - Team Lead',
                'job_description': 'We are looking for a senior software engineer to lead our development team. The role involves technical leadership, architecture decisions, and mentoring junior developers.',
                'job_requirements': 'Requirements: 5+ years experience, team leadership, microservices knowledge, cloud platforms, strong communication skills.',
                'include_coding_challenge': 'true',
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
                success = result.get("success", False) and "token" in result
                if success:
                    self.enhanced_token = result["token"]
            
            details = f"Status: {response.status_code}"
            if self.enhanced_token:
                details += f", Enhanced Token: {self.enhanced_token}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Enhanced Token Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Token Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_token_validation(self) -> bool:
        """Test token validation before interview start"""
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
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Token Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_start_text_mode(self) -> bool:
        """Test starting interview in text mode"""
        if not self.generated_token:
            self.log_test("Interview Start (Text Mode)", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "candidate_name": "Sarah Wilson",
                "voice_mode": False
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=20  # Longer timeout for AI processing
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "question_number" in data)
                if success:
                    self.session_id = data["session_id"]
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Session ID: {self.session_id[:8] if self.session_id else 'None'}..."
                details += f", Question: {data.get('first_question', '')[:50]}..."
            else:
                details += f", Response: {response.text[:400]}"
            
            self.log_test("Interview Start (Text Mode)", success, details)
            return success
        except Exception as e:
            self.log_test("Interview Start (Text Mode)", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_start_voice_mode(self) -> bool:
        """Test starting interview in voice mode - this is the main issue"""
        if not self.generated_token:
            self.log_test("Interview Start (Voice Mode)", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "candidate_name": "Sarah Wilson",
                "voice_mode": True
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=30  # Longer timeout for TTS generation
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "voice_mode" in data and
                          data.get("voice_mode") == True)
                
                if success:
                    voice_session_id = data["session_id"]
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Voice Mode: {data.get('voice_mode')}"
                details += f", Session: {voice_session_id[:8] if 'voice_session_id' in locals() else 'None'}..."
                details += f", Question: {data.get('first_question', '')[:50]}..."
                if "welcome_audio" in data:
                    details += f", Welcome Audio: Present"
                if "question_audio" in data:
                    details += f", Question Audio: Present"
            else:
                details += f", Response: {response.text[:500]}"
            
            self.log_test("Interview Start (Voice Mode)", success, details)
            return success
        except Exception as e:
            self.log_test("Interview Start (Voice Mode)", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_interview_start(self) -> bool:
        """Test starting enhanced interview with voice mode"""
        if not self.enhanced_token:
            self.log_test("Enhanced Interview Start (Voice Mode)", False, "No enhanced token available")
            return False
        
        try:
            payload = {
                "token": self.enhanced_token,
                "candidate_name": "Michael Chen",
                "voice_mode": True
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=30  # Longer timeout for AI processing
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "voice_mode" in data and
                          data.get("voice_mode") == True)
                
                # Check for enhanced features
                if success and "is_enhanced" in data:
                    enhanced_session_id = data["session_id"]
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Enhanced: {data.get('is_enhanced', False)}"
                details += f", Voice Mode: {data.get('voice_mode')}"
                details += f", Session: {enhanced_session_id[:8] if 'enhanced_session_id' in locals() else 'None'}..."
                details += f", Question: {data.get('first_question', '')[:50]}..."
            else:
                details += f", Response: {response.text[:500]}"
            
            self.log_test("Enhanced Interview Start (Voice Mode)", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Interview Start (Voice Mode)", False, f"Exception: {str(e)}")
            return False
    
    def test_gemini_api_key_validation(self) -> bool:
        """Test if Gemini API key is working by trying to generate questions"""
        if not self.generated_token:
            self.log_test("Gemini API Key Validation", False, "No token available")
            return False
        
        try:
            # Try to start an interview which requires Gemini API for question generation
            payload = {
                "token": self.generated_token,
                "candidate_name": "Test Candidate",
                "voice_mode": False
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=25
            )
            
            # Check if the error is specifically related to Gemini API
            success = response.status_code == 200
            gemini_error = False
            
            if not success:
                response_text = response.text.lower()
                if any(keyword in response_text for keyword in ['api key not valid', 'gemini', 'authentication', 'invalid api key']):
                    gemini_error = True
            
            details = f"Status: {response.status_code}"
            if success:
                details += ", Gemini API working correctly"
            elif gemini_error:
                details += ", GEMINI API KEY ERROR DETECTED"
            else:
                details += f", Other error: {response.text[:300]}"
            
            self.log_test("Gemini API Key Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Gemini API Key Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_camera_test_endpoint(self) -> bool:
        """Test camera test endpoint which is part of the interview flow"""
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
                success = data.get("success", False) and "features" in data
            
            details = f"Status: {response.status_code}"
            if success:
                features = data.get("features", {})
                details += f", Voice Mode: {features.get('voice_mode', False)}"
                details += f", Coding Challenge: {features.get('coding_challenge', False)}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Camera Test Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Camera Test Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_cors_configuration(self) -> bool:
        """Test CORS configuration by checking response headers"""
        try:
            # Make a preflight request to check CORS
            headers = {
                'Origin': 'https://aptitude-models.preview.emergentagent.com',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
            
            response = self.session.options(
                f"{self.base_url}/candidate/start-interview",
                headers=headers,
                timeout=10
            )
            
            success = response.status_code in [200, 204]
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            details = f"Status: {response.status_code}, CORS Headers: {cors_headers}"
            self.log_test("CORS Configuration", success, details)
            return success
        except Exception as e:
            self.log_test("CORS Configuration", False, f"Exception: {str(e)}")
            return False
    
    def run_focused_tests(self) -> Dict[str, bool]:
        """Run focused tests for candidate interview start functionality"""
        print("=" * 80)
        print("CANDIDATE INTERVIEW START FUNCTIONALITY - FOCUSED TESTING")
        print("Testing the specific issue: 'Failed to start interview: TypeError: Failed to fetch'")
        print("=" * 80)
        print()
        
        results = {}
        
        # Basic connectivity and authentication
        results["backend_connectivity"] = self.test_backend_connectivity()
        results["admin_authentication"] = self.test_admin_authentication()
        
        # Token generation and validation
        results["token_generation"] = self.test_token_generation()
        results["enhanced_token_generation"] = self.test_enhanced_token_generation()
        results["token_validation"] = self.test_token_validation()
        
        # Core interview start functionality
        results["interview_start_text_mode"] = self.test_interview_start_text_mode()
        results["interview_start_voice_mode"] = self.test_interview_start_voice_mode()
        results["enhanced_interview_start"] = self.test_enhanced_interview_start()
        
        # API and configuration tests
        results["gemini_api_key_validation"] = self.test_gemini_api_key_validation()
        results["camera_test_endpoint"] = self.test_camera_test_endpoint()
        results["cors_configuration"] = self.test_cors_configuration()
        
        # Summary
        print("=" * 80)
        print("FOCUSED TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by category
        categories = {
            "Basic Infrastructure": ["backend_connectivity", "admin_authentication", "cors_configuration"],
            "Token Management": ["token_generation", "enhanced_token_generation", "token_validation"],
            "Interview Start (CORE ISSUE)": ["interview_start_text_mode", "interview_start_voice_mode", "enhanced_interview_start"],
            "API Dependencies": ["gemini_api_key_validation", "camera_test_endpoint"]
        }
        
        for category, test_names in categories.items():
            print(f"\n{category}:")
            for test_name in test_names:
                if test_name in results:
                    status = "✅ PASS" if results[test_name] else "❌ FAIL"
                    print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        # Specific analysis for the main issue
        print("\n" + "=" * 80)
        print("ROOT CAUSE ANALYSIS")
        print("=" * 80)
        
        if not results.get("backend_connectivity", False):
            print("❌ CRITICAL: Backend is not reachable - this explains the 'Failed to fetch' error")
        elif not results.get("cors_configuration", False):
            print("❌ CRITICAL: CORS configuration issue - this could cause 'Failed to fetch' error")
        elif not results.get("gemini_api_key_validation", False):
            print("❌ CRITICAL: Gemini API key issue - this causes 500 errors in interview start")
        elif not results.get("interview_start_voice_mode", False):
            print("❌ ISSUE CONFIRMED: Voice interview start is failing - this matches the reported issue")
        elif results.get("interview_start_text_mode", False) and not results.get("interview_start_voice_mode", False):
            print("⚠️  PARTIAL ISSUE: Text mode works but voice mode fails - voice-specific problem")
        else:
            print("✅ All core functionality appears to be working")
        
        return results

def main():
    """Main test execution"""
    tester = CandidateInterviewStartTester()
    results = tester.run_focused_tests()
    
    # Return exit code based on critical tests
    critical_tests = ["backend_connectivity", "interview_start_voice_mode", "gemini_api_key_validation"]
    critical_passed = all(results.get(test, False) for test in critical_tests)
    
    return 0 if critical_passed else 1

if __name__ == "__main__":
    exit(main())