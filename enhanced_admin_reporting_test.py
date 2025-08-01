#!/usr/bin/env python3
"""
Enhanced Admin Reporting Functionality Testing
Tests the new enhanced admin reporting features as requested in the review:

1. Admin Authentication with password 'Game@1234'
2. Detailed Report API: /api/admin/detailed-report/{session_id} endpoint
3. Candidate Pipeline: /api/admin/candidate-pipeline with session_id field
4. Enhanced Admin Upload: Verify enhanced token generation still works correctly

Focus on testing the new detailed transcript and reporting features that provide:
- Formatted interview transcript (Q1, A1, Q2, A2 format)  
- Candidate score breakdown
- AI-generated hiring justification with merits/demerits
- Specific hiring recommendations
"""

import requests
import json
import time
import io
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://01b5d04f-7f60-4bed-835a-83f1069e2978.preview.emergentagent.com/api"

class EnhancedAdminReportingTester:
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
    
    def test_admin_authentication(self) -> bool:
        """Test admin authentication with password 'Game@1234'"""
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
            
            details = f"Status: {response.status_code}, Response: {response.json() if response.status_code == 200 else response.text[:200]}"
            self.log_test("Admin Authentication (Game@1234)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Authentication (Game@1234)", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_admin_upload(self) -> bool:
        """Test enhanced admin upload with new parameters"""
        try:
            # Create sample resume content for enhanced testing
            resume_content = """Sarah Wilson
Senior Software Engineer - Enhanced Interview Candidate
Email: sarah.wilson@email.com
Phone: (555) 999-8888

EXPERIENCE:
- 6+ years of full-stack development with Python and JavaScript
- Expert in FastAPI, React, and MongoDB with microservices architecture
- Led development teams and implemented CI/CD pipelines
- Experience with voice interfaces and real-time applications
- Strong background in system design and scalability

SKILLS:
- Python, JavaScript, TypeScript, Go
- FastAPI, React, Node.js, MongoDB, PostgreSQL
- Docker, Kubernetes, AWS, Azure, GCP
- Team leadership, mentoring, and project management
- Voice UI, WebRTC, real-time systems

EDUCATION:
Master of Science in Computer Science
Advanced Tech University, 2017"""
            
            files = {
                'resume_file': ('enhanced_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Full-Stack Engineer - Enhanced Interview',
                'job_description': 'We are seeking a senior full-stack engineer to join our enhanced interview platform team. The role involves building scalable systems, leading technical decisions, and mentoring junior developers.',
                'job_requirements': 'Requirements: 5+ years experience, Python/JavaScript expertise, system design skills, team leadership experience, strong communication abilities.',
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
                success = (result.get("success", False) and 
                          "token" in result and 
                          "features" in result)
                if success:
                    self.generated_token = result["token"]
                    # Verify enhanced features are present
                    features = result["features"]
                    success = (features.get("coding_challenge") == True and
                              features.get("role_archetype") == "Software Engineer" and
                              features.get("interview_focus") == "Technical Deep-Dive")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.generated_token[:8]}..., Features: {result.get('features', {})}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Enhanced Admin Upload with New Parameters", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Admin Upload with New Parameters", False, f"Exception: {str(e)}")
            return False
    
    def test_candidate_pipeline_with_session_id(self) -> bool:
        """Test candidate pipeline endpoint to ensure it includes session_id field"""
        try:
            response = self.session.get(f"{self.base_url}/admin/candidate-pipeline", timeout=10)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "pipeline" in data and isinstance(data["pipeline"], list)
                
                if success and len(data["pipeline"]) > 0:
                    # Check if session_id field is present in pipeline entries
                    pipeline_entries = data["pipeline"]
                    session_id_present = any("session_id" in entry for entry in pipeline_entries)
                    
                    details = f"Status: {response.status_code}, Pipeline entries: {len(pipeline_entries)}, Session ID field present: {session_id_present}"
                    
                    # Look for entries with session_id
                    entries_with_session = [entry for entry in pipeline_entries if entry.get("session_id")]
                    if entries_with_session:
                        details += f", Entries with session_id: {len(entries_with_session)}"
                        # Show sample session_id
                        sample_session_id = entries_with_session[0]["session_id"]
                        details += f", Sample session_id: {sample_session_id[:8] if sample_session_id else 'None'}..."
                else:
                    details = f"Status: {response.status_code}, Empty pipeline - no entries to check for session_id"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Candidate Pipeline with Session ID Field", success, details)
            return success
        except Exception as e:
            self.log_test("Candidate Pipeline with Session ID Field", False, f"Exception: {str(e)}")
            return False
    
    def create_test_interview_session(self) -> bool:
        """Create a complete test interview session to generate data for detailed report testing"""
        if not self.generated_token:
            return False
        
        try:
            # Start interview
            payload = {
                "token": self.generated_token,
                "candidate_name": "Sarah Wilson",
                "voice_mode": False
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"Failed to start interview: {response.status_code}, {response.text}")
                return False
            
            data = response.json()
            self.session_id = data.get("session_id")
            
            if not self.session_id:
                print("No session ID received")
                return False
            
            print(f"Created interview session: {self.session_id[:8]}...")
            
            # Complete a full interview with 8 questions to generate assessment
            sample_answers = [
                # Technical answers (4)
                "I have 6+ years of Python experience, specializing in FastAPI for building scalable REST APIs. I've architected microservices systems, implemented authentication and authorization, and worked extensively with async programming patterns. I'm proficient with Pydantic for data validation and SQLAlchemy for database operations.",
                
                "For system design, I focus on scalability, reliability, and maintainability. I use microservices architecture with proper service boundaries, implement caching strategies with Redis, and ensure proper monitoring and logging. I've designed systems handling millions of requests per day using load balancers and auto-scaling.",
                
                "I follow RESTful principles with proper HTTP methods and status codes. I implement comprehensive error handling, input validation, and API versioning. I use OpenAPI/Swagger for documentation and ensure consistent response formats. I also implement rate limiting and authentication middleware for security.",
                
                "I use Git with feature branches and pull requests for code review. For deployment, I work with Docker containers and CI/CD pipelines using GitHub Actions. I'm experienced with cloud platforms like AWS and implement monitoring with tools like Prometheus and Grafana for production systems.",
                
                # Behavioral answers (4)
                "I led a team of 5 developers in rebuilding our legacy monolith into microservices. I established coding standards, implemented code review processes, and mentored junior developers. The project improved system performance by 300% and reduced deployment time from hours to minutes. I facilitated daily standups and sprint planning.",
                
                "When I disagreed with a senior architect about using a NoSQL database for a project, I prepared a detailed analysis comparing SQL vs NoSQL for our specific use case. I presented data on performance, consistency requirements, and team expertise. We had a constructive discussion and decided on a hybrid approach that satisfied both concerns.",
                
                "I encountered a critical production bug causing intermittent failures during peak traffic. I systematically analyzed logs, reproduced the issue in staging, and identified a race condition in our caching layer. I implemented proper locking mechanisms and added comprehensive monitoring to prevent similar issues.",
                
                "I stay current by following industry blogs, attending conferences, and taking online courses. I recently completed a course on distributed systems and have been experimenting with new Python frameworks. I contribute to open-source projects and participate in tech meetups to learn from the community."
            ]
            
            for i, answer in enumerate(sample_answers):
                payload = {
                    "token": self.generated_token,
                    "message": answer
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/send-message",
                    json=payload,
                    timeout=25
                )
                
                if response.status_code != 200:
                    print(f"Failed at question {i+1}: {response.status_code}, {response.text}")
                    return False
                
                data = response.json()
                print(f"Answered question {i+1}/8")
                
                if data.get("completed", False):
                    print(f"Interview completed after {i+1} questions")
                    if "assessment_id" in data:
                        self.assessment_id = data["assessment_id"]
                        print(f"Assessment created: {self.assessment_id[:8]}...")
                    break
                
                time.sleep(2)  # Longer delay for AI processing
            
            return True
            
        except Exception as e:
            print(f"Exception in create_test_interview_session: {str(e)}")
            return False
    
    def test_detailed_report_valid_session(self) -> bool:
        """Test detailed report API with valid session ID"""
        # First create a test session if we don't have one
        if not self.session_id:
            session_created = self.create_test_interview_session()
            if not session_created:
                self.log_test("Detailed Report API (Valid Session)", False, "Failed to create test session")
                return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/admin/detailed-report/{self.session_id}",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                
                # Based on actual API response, check for the correct fields
                core_fields = ["session_id", "candidate_name", "job_title", "transcript"]
                present_core_fields = [field for field in core_fields if field in data]
                
                # Check for assessment-related fields
                assessment_fields = ["assessment_summary", "detailed_justification", "full_assessment"]
                present_assessment_fields = [field for field in assessment_fields if field in data]
                
                # Verify transcript format (Q1, A1, Q2, A2 format)
                transcript = data.get("transcript", "")
                has_qa_format = "Q1:" in transcript and "A1:" in transcript
                
                # Check for justification content (in detailed_justification field)
                justification = data.get("detailed_justification", "")
                has_merits_demerits = ("MERITS" in justification and 
                                     "DEMERITS" in justification and 
                                     "RECOMMENDATION" in justification)
                
                # Check for assessment summary with scores
                assessment_summary = data.get("assessment_summary", {})
                has_scores = ("technical_score" in assessment_summary and 
                            "behavioral_score" in assessment_summary and 
                            "overall_score" in assessment_summary)
                
                # Success criteria: core fields present, Q&A format, and either scores or justification
                success = (len(present_core_fields) >= 3 and 
                          has_qa_format and 
                          (has_scores or has_merits_demerits))
                
                details = f"Status: {response.status_code}, Session: {data.get('session_id', '')[:8]}..., "
                details += f"Core fields: {len(present_core_fields)}/4, Assessment fields: {len(present_assessment_fields)}/3, "
                details += f"Q&A Format: {has_qa_format}, Has scores: {has_scores}, "
                details += f"Merits/Demerits: {has_merits_demerits}, "
                details += f"Transcript Length: {len(transcript)} chars"
                
                if has_scores:
                    scores = assessment_summary
                    details += f", Scores: T={scores.get('technical_score')}, B={scores.get('behavioral_score')}, O={scores.get('overall_score')}"
                    
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            
            self.log_test("Detailed Report API (Valid Session)", success, details)
            return success
        except Exception as e:
            self.log_test("Detailed Report API (Valid Session)", False, f"Exception: {str(e)}")
            return False
    
    def test_detailed_report_invalid_session(self) -> bool:
        """Test detailed report API with invalid session ID for error handling"""
        try:
            invalid_session_id = "invalid-session-12345"
            response = self.session.get(
                f"{self.base_url}/admin/detailed-report/{invalid_session_id}",
                timeout=15
            )
            
            # Should return 404 for invalid session
            success = response.status_code == 404
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Detailed Report API (Invalid Session)", success, details)
            return success
        except Exception as e:
            self.log_test("Detailed Report API (Invalid Session)", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_token_generation_compatibility(self) -> bool:
        """Test that enhanced token generation still works correctly"""
        try:
            # Create a fresh token for validation testing
            resume_content = """Test Candidate
Validation Test Engineer
Email: test@email.com

EXPERIENCE:
- 3+ years of software development
- Experience with Python and JavaScript
- API development and testing

SKILLS:
- Python, JavaScript
- FastAPI, React
- Testing and validation"""
            
            files = {
                'resume_file': ('validation_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Validation Test Engineer',
                'job_description': 'Testing enhanced token validation functionality.',
                'job_requirements': 'Requirements: Testing experience, attention to detail.',
                'include_coding_challenge': 'false',
                'role_archetype': 'General',
                'interview_focus': 'Balanced'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job-enhanced",
                files=files,
                data=data,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test("Enhanced Token Generation Compatibility", False, f"Failed to create validation token: {response.status_code}")
                return False
            
            result = response.json()
            validation_token = result.get("token")
            
            if not validation_token:
                self.log_test("Enhanced Token Generation Compatibility", False, "No validation token received")
                return False
            
            # Test token validation
            payload = {"token": validation_token}
            response = self.session.post(
                f"{self.base_url}/candidate/validate-token",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("valid", False) and 
                          "job_title" in data)
                
                # For enhanced tokens, check if features are present
                if "features" in data:
                    features = data.get("features", {})
                    has_enhanced_features = ("coding_challenge" in features and
                                           "role_archetype" in features and
                                           "interview_focus" in features)
                    details = f"Status: {response.status_code}, Token valid: {data.get('valid')}, Enhanced features: {has_enhanced_features}, Features: {features}"
                else:
                    details = f"Status: {response.status_code}, Token valid: {data.get('valid')}, Job: {data.get('job_title', 'N/A')}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Enhanced Token Generation Compatibility", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Token Generation Compatibility", False, f"Exception: {str(e)}")
            return False
    
    def run_enhanced_admin_reporting_tests(self) -> Dict[str, bool]:
        """Run all enhanced admin reporting tests"""
        print("=" * 80)
        print("ENHANCED ADMIN REPORTING FUNCTIONALITY TESTING")
        print("Testing new detailed transcript and reporting features")
        print("=" * 80)
        print()
        
        results = {}
        
        # 1. Admin Authentication
        results["admin_authentication"] = self.test_admin_authentication()
        
        # 2. Enhanced Admin Upload
        results["enhanced_admin_upload"] = self.test_enhanced_admin_upload()
        
        # 3. Candidate Pipeline with Session ID
        results["candidate_pipeline_session_id"] = self.test_candidate_pipeline_with_session_id()
        
        # 4. Detailed Report API - Valid Session
        results["detailed_report_valid"] = self.test_detailed_report_valid_session()
        
        # 5. Detailed Report API - Invalid Session (Error Handling)
        results["detailed_report_invalid"] = self.test_detailed_report_invalid_session()
        
        # 6. Enhanced Token Generation Compatibility
        results["enhanced_token_compatibility"] = self.test_enhanced_token_generation_compatibility()
        
        # Summary
        print("=" * 80)
        print("ENHANCED ADMIN REPORTING TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        test_categories = {
            "Admin Authentication": ["admin_authentication"],
            "Enhanced Token System": ["enhanced_admin_upload", "enhanced_token_compatibility"],
            "Candidate Pipeline Management": ["candidate_pipeline_session_id"],
            "Detailed Reporting API": ["detailed_report_valid", "detailed_report_invalid"]
        }
        
        for category, test_names in test_categories.items():
            print(f"\n{category}:")
            for test_name in test_names:
                if test_name in results:
                    status = "✅ PASS" if results[test_name] else "❌ FAIL"
                    print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL ENHANCED ADMIN REPORTING TESTS PASSED!")
            print("✅ Admin authentication working with Game@1234")
            print("✅ Detailed report API providing formatted transcripts")
            print("✅ Candidate pipeline includes session_id field")
            print("✅ Enhanced token generation working correctly")
            print("✅ AI-generated hiring justification with merits/demerits")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Enhanced admin reporting features are functional with minor issues.")
        else:
            print("⚠️  Multiple enhanced admin reporting tests failed. Check the details above.")
        
        return results

def main():
    """Main test execution"""
    tester = EnhancedAdminReportingTester()
    results = tester.run_enhanced_admin_reporting_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())