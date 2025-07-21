#!/usr/bin/env python3
"""
Comprehensive Backend Testing for AI-Powered Interview Agent
Tests the complete interview flow end-to-end including:
- Admin authentication and file upload
- Token validation and interview start
- Multi-turn interview conversation
- Assessment generation and reporting
"""

import requests
import json
import time
import io
from typing import Dict, Any, Optional

# Backend URL from frontend .env
BASE_URL = "https://d80e9782-6c10-4b64-ba91-296669c70895.preview.emergentagent.com/api"

class InterviewAgentTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.generated_token = None
        self.session_id = None
        self.assessment_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_health_check(self) -> bool:
        """Test basic API health check"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Response: {response.text[:100]}"
            self.log_test("Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login(self) -> bool:
        """Test admin authentication with correct password"""
        try:
            payload = {"password": "Game@123"}
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
            self.log_test("Admin Login", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_invalid(self) -> bool:
        """Test admin authentication with wrong password"""
        try:
            payload = {"password": "WrongPassword"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 401
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Admin Login (Invalid Password)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login (Invalid Password)", False, f"Exception: {str(e)}")
            return False
    
    def test_job_resume_upload(self) -> bool:
        """Test job description and resume upload with token generation"""
        try:
            # Create sample resume content
            resume_content = """John Doe
Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567

EXPERIENCE:
- 3+ years of Python development
- Experience with FastAPI and React
- Database design and optimization
- RESTful API development

SKILLS:
- Python, JavaScript, SQL
- FastAPI, React, MongoDB
- Git, Docker, AWS
- Problem-solving and teamwork

EDUCATION:
Bachelor of Science in Computer Science
University of Technology, 2020"""
            
            # Prepare multipart form data
            files = {
                'resume_file': ('resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Python Developer',
                'job_description': 'We are looking for an experienced Python developer to join our team. The ideal candidate will have strong experience with FastAPI, database design, and modern web development practices.',
                'job_requirements': 'Requirements: 3+ years Python experience, FastAPI knowledge, database skills, strong problem-solving abilities, team collaboration skills.'
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
            
            details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            if self.generated_token:
                details += f", Token: {self.generated_token[:8]}..."
            
            self.log_test("Job & Resume Upload", success, details)
            return success
        except Exception as e:
            self.log_test("Job & Resume Upload", False, f"Exception: {str(e)}")
            return False
    
    def test_token_validation(self) -> bool:
        """Test candidate token validation"""
        if not self.generated_token:
            self.log_test("Token Validation", False, "No token available from upload test")
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
    
    def test_token_validation_invalid(self) -> bool:
        """Test token validation with invalid token"""
        try:
            payload = {"token": "INVALID_TOKEN_123"}
            response = self.session.post(
                f"{self.base_url}/candidate/validate-token",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 401
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Token Validation (Invalid Token)", success, details)
            return success
        except Exception as e:
            self.log_test("Token Validation (Invalid Token)", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_start(self) -> bool:
        """Test starting an interview session"""
        if not self.generated_token:
            self.log_test("Interview Start", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "candidate_name": "John Doe"
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "question_number" in data)
                if success:
                    self.session_id = data["session_id"]
            
            details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            if self.session_id:
                details += f", Session ID: {self.session_id[:8]}..."
            
            self.log_test("Interview Start", success, details)
            return success
        except Exception as e:
            self.log_test("Interview Start", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_conversation(self) -> bool:
        """Test complete 8-question interview conversation"""
        if not self.generated_token:
            self.log_test("Interview Conversation", False, "No token available")
            return False
        
        # Sample answers for the 8 questions (4 technical, 4 behavioral)
        sample_answers = [
            # Technical answers
            "I have 3+ years of Python experience, working extensively with FastAPI for building REST APIs. I've built several microservices using FastAPI, implemented authentication, database integration, and API documentation. I'm comfortable with async programming and have used Pydantic for data validation.",
            
            "For database optimization, I focus on proper indexing, query optimization, and connection pooling. I've worked with MongoDB and PostgreSQL, implementing efficient schemas and using aggregation pipelines. I also monitor query performance and use database profiling tools to identify bottlenecks.",
            
            "I follow RESTful principles with proper HTTP methods, status codes, and resource naming. I implement comprehensive error handling, input validation, and API versioning. I use tools like Swagger/OpenAPI for documentation and ensure consistent response formats across endpoints.",
            
            "I use Git for version control with feature branches and pull requests. For deployment, I've worked with Docker containers and CI/CD pipelines. I'm familiar with cloud platforms like AWS and have experience with monitoring tools and logging systems for production applications.",
            
            # Behavioral answers
            "In my previous role, I had to implement a complex feature with a tight deadline. I broke down the requirements, prioritized core functionality, and communicated regularly with stakeholders about progress. I delivered the MVP on time and added enhancements in subsequent iterations.",
            
            "I once disagreed with a senior developer about the architecture approach for a new service. I prepared a detailed comparison of both approaches, highlighting pros and cons. We had a constructive discussion, and we ended up combining the best aspects of both solutions, which resulted in a better outcome.",
            
            "I encountered a production bug that was causing intermittent failures. I systematically analyzed logs, reproduced the issue in a test environment, and traced it to a race condition in concurrent requests. I implemented proper locking mechanisms and added comprehensive logging for future debugging.",
            
            "I regularly attend tech meetups, follow industry blogs, and take online courses. I recently completed a course on microservices architecture and have been experimenting with new Python libraries. I also contribute to open-source projects and participate in code reviews to learn from peers."
        ]
        
        try:
            for i, answer in enumerate(sample_answers):
                payload = {
                    "token": self.generated_token,
                    "message": answer
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/send-message",
                    json=payload,
                    timeout=20  # Longer timeout for AI processing
                )
                
                if response.status_code != 200:
                    details = f"Failed at question {i+1}, Status: {response.status_code}, Response: {response.text[:200]}"
                    self.log_test("Interview Conversation", False, details)
                    return False
                
                data = response.json()
                
                # Check if interview is completed
                if data.get("completed", False):
                    if "assessment_id" in data:
                        self.assessment_id = data["assessment_id"]
                    success = i == len(sample_answers) - 1  # Should complete on last question
                    details = f"Interview completed after {i+1} questions, Assessment ID: {self.assessment_id[:8] if self.assessment_id else 'None'}..."
                    self.log_test("Interview Conversation", success, details)
                    return success
                
                # Verify next question is provided
                if not data.get("next_question"):
                    details = f"No next question provided at step {i+1}"
                    self.log_test("Interview Conversation", False, details)
                    return False
                
                # Small delay between questions
                time.sleep(1)
            
            # If we reach here, interview didn't complete as expected
            self.log_test("Interview Conversation", False, "Interview didn't complete after 8 questions")
            return False
            
        except Exception as e:
            self.log_test("Interview Conversation", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_reports(self) -> bool:
        """Test admin reports endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/admin/reports", timeout=10)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "reports" in data and isinstance(data["reports"], list)
                
                # Check if our assessment is in the reports
                if success and self.assessment_id:
                    found_assessment = any(
                        report.get("id") == self.assessment_id 
                        for report in data["reports"]
                    )
                    if found_assessment:
                        details = f"Status: {response.status_code}, Found {len(data['reports'])} reports including our assessment"
                    else:
                        details = f"Status: {response.status_code}, Found {len(data['reports'])} reports but our assessment not found"
                else:
                    details = f"Status: {response.status_code}, Found {len(data.get('reports', []))} reports"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Admin Reports", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Reports", False, f"Exception: {str(e)}")
            return False
    
    def test_specific_report(self) -> bool:
        """Test getting a specific report by session ID"""
        if not self.session_id:
            self.log_test("Specific Report", False, "No session ID available")
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/admin/reports/{self.session_id}",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("report" in data and 
                          "technical_score" in data["report"] and 
                          "behavioral_score" in data["report"])
            
            details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            self.log_test("Specific Report", success, details)
            return success
        except Exception as e:
            self.log_test("Specific Report", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests in sequence"""
        print("=" * 60)
        print("AI-POWERED INTERVIEW AGENT - BACKEND TESTING")
        print("=" * 60)
        print()
        
        results = {}
        
        # Basic connectivity
        results["health_check"] = self.test_health_check()
        
        # Admin authentication
        results["admin_login"] = self.test_admin_login()
        results["admin_login_invalid"] = self.test_admin_login_invalid()
        
        # Job and resume upload
        results["job_resume_upload"] = self.test_job_resume_upload()
        
        # Token validation
        results["token_validation"] = self.test_token_validation()
        results["token_validation_invalid"] = self.test_token_validation_invalid()
        
        # Interview flow
        results["interview_start"] = self.test_interview_start()
        results["interview_conversation"] = self.test_interview_conversation()
        
        # Admin reporting
        results["admin_reports"] = self.test_admin_reports()
        results["specific_report"] = self.test_specific_report()
        
        # Summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Backend is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the details above.")
        
        return results

def main():
    """Main test execution"""
    tester = InterviewAgentTester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())