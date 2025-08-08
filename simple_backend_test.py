#!/usr/bin/env python3
"""
Simple Backend Testing for AI Interview Platform
Tests core backend functionality without complex dependencies
"""

import requests
import json
import time
import io
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://6d379ea8-29ec-435c-b4d7-9ae4b0ab361e.preview.emergentagent.com/api"

class SimpleBackendTester:
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
    
    def test_health_check(self) -> bool:
        """Test basic API connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            success = response.status_code in [200, 404, 405]  # 404/405 means server is responding
            details = f"Status: {response.status_code}"
            self.log_test("Backend Connectivity", success, details)
            return success
        except Exception as e:
            self.log_test("Backend Connectivity", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login(self) -> bool:
        """Test admin authentication"""
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
    
    def test_resume_upload(self) -> bool:
        """Test resume upload and token generation"""
        try:
            resume_content = """John Smith
Senior Software Engineer
Email: john.smith@email.com
Phone: (555) 123-4567

EXPERIENCE:
- 5+ years of Python and JavaScript development
- Expert in FastAPI, React, and MongoDB
- Led team of 4 developers on microservices project
- Implemented CI/CD pipelines and cloud deployments

SKILLS:
- Python, JavaScript, TypeScript, SQL
- FastAPI, React, Node.js, MongoDB, PostgreSQL
- Docker, Kubernetes, AWS, Azure
- Team leadership and project management

EDUCATION:
Master of Science in Computer Science
Tech University, 2018"""
            
            files = {
                'resume_file': ('resume.txt', resume_content, 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Python Developer - Backend Testing',
                'job_description': 'We are seeking a senior Python developer to lead our backend team. The role involves architecting scalable systems, mentoring junior developers, and driving technical decisions.',
                'job_requirements': 'Requirements: 5+ years Python experience, FastAPI expertise, team leadership experience, cloud platform knowledge, strong communication skills.'
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
                success = (result.get("success", False) and "token" in result)
                if success:
                    self.generated_token = result["token"]
            
            details = f"Status: {response.status_code}, Token: {self.generated_token[:8] if self.generated_token else 'None'}..."
            self.log_test("Resume Upload & Token Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Resume Upload & Token Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_token_validation(self) -> bool:
        """Test token validation"""
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
            
            details = f"Status: {response.status_code}, Valid: {data.get('valid', False) if success else 'N/A'}"
            self.log_test("Token Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_start(self) -> bool:
        """Test interview start"""
        if not self.generated_token:
            self.log_test("Interview Start", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "candidate_name": "John Smith",
                "voice_mode": False
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and "first_question" in data)
                if success:
                    self.session_id = data["session_id"]
            
            details = f"Status: {response.status_code}, Session: {self.session_id[:8] if self.session_id else 'None'}..."
            self.log_test("Interview Start", success, details)
            return success
        except Exception as e:
            self.log_test("Interview Start", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_interview_start(self) -> bool:
        """Test voice interview start"""
        if not self.generated_token:
            self.log_test("Voice Interview Start", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "candidate_name": "John Smith Voice Test",
                "voice_mode": True
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=25  # Longer timeout for TTS
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and "voice_mode" in data and data.get("voice_mode") == True)
            
            details = f"Status: {response.status_code}, Voice Mode: {data.get('voice_mode', False) if success else 'N/A'}"
            self.log_test("Voice Interview Start", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Interview Start", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_message(self) -> bool:
        """Test sending interview message"""
        if not self.generated_token:
            self.log_test("Interview Message", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "message": "I have 5+ years of Python experience, working extensively with FastAPI for building REST APIs. I've built several microservices using FastAPI, implemented authentication, database integration, and API documentation. I'm comfortable with async programming and have used Pydantic for data validation."
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
            
            details = f"Status: {response.status_code}, Has Next Question: {'next_question' in data if success else 'N/A'}"
            self.log_test("Interview Message", success, details)
            return success
        except Exception as e:
            self.log_test("Interview Message", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_reports(self) -> bool:
        """Test admin reports"""
        try:
            response = self.session.get(f"{self.base_url}/admin/reports", timeout=10)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "reports" in data and isinstance(data["reports"], list)
            
            details = f"Status: {response.status_code}, Reports Count: {len(data.get('reports', [])) if success else 'N/A'}"
            self.log_test("Admin Reports", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Reports", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests"""
        print("=" * 70)
        print("AI-POWERED INTERVIEW AGENT - SIMPLE BACKEND TESTING")
        print("Testing Core Backend Functionality")
        print("=" * 70)
        print()
        
        results = {}
        
        # Core functionality tests
        results["backend_connectivity"] = self.test_health_check()
        results["admin_authentication"] = self.test_admin_login()
        results["resume_upload"] = self.test_resume_upload()
        results["token_validation"] = self.test_token_validation()
        results["interview_start"] = self.test_interview_start()
        results["voice_interview_start"] = self.test_voice_interview_start()
        results["interview_message"] = self.test_interview_message()
        results["admin_reports"] = self.test_admin_reports()
        
        # Summary
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Backend is working correctly.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Most features are functional.")
        else:
            print("⚠️  Multiple tests failed. Backend needs attention.")
        
        return results

def main():
    """Main test execution"""
    tester = SimpleBackendTester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())