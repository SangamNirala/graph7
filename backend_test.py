#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Placement Preparation Assessment Reports and Token-Based Visibility Logic
Testing the complete end-to-end workflow for placement preparation vs admin token separation
"""

import requests
import json
import time
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://350119d5-292b-44b0-a739-5efd46504bc2.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class PlacementPreparationTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_authenticated = False
        self.placement_prep_token = None
        self.admin_token = None
        self.placement_prep_session_id = None
        self.admin_session_id = None
        self.placement_prep_assessment_id = None
        self.admin_assessment_id = None
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()

    def test_admin_authentication(self):
        """Test admin authentication with Game@1234 password"""
        try:
            response = self.session.post(f"{BASE_URL}/admin/login", 
                                       json={"password": "Game@1234"})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.admin_authenticated = True
                    self.log_test("Admin Authentication", "PASS", 
                                f"Successfully authenticated with Game@1234 password")
                    return True
                else:
                    self.log_test("Admin Authentication", "FAIL", 
                                f"Authentication failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Admin Authentication", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", "FAIL", f"Exception: {str(e)}")
            return False

    def create_placement_preparation_token(self):
        """Create a token via placement preparation endpoint"""
        try:
            # Create sample resume content
            resume_content = """
            John Smith
            Senior Software Engineer
            
            EXPERIENCE:
            - 5+ years Python development
            - 3+ years React/JavaScript
            - Experience with FastAPI, MongoDB
            - Team leadership experience
            - AWS cloud deployment
            
            EDUCATION:
            - Bachelor's in Computer Science
            - Master's in Software Engineering
            
            SKILLS:
            Python, JavaScript, React, FastAPI, MongoDB, Docker, AWS, Team Leadership
            """
            
            token_request = {
                "job_title": "Senior Full Stack Developer - Placement Prep",
                "job_description": "We are looking for a senior full stack developer with expertise in Python and React.",
                "job_requirements": "5+ years experience, Python, React, FastAPI, MongoDB, leadership skills",
                "resume_text": resume_content.strip(),
                "role_archetype": "Software Engineer",
                "interview_focus": "Technical Deep-Dive",
                "include_coding_challenge": True,
                "min_questions": 8,
                "max_questions": 12
            }
            
            response = self.session.post(f"{BASE_URL}/admin/create-token", 
                                       json=token_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("token"):
                    self.placement_prep_token = data["token"]
                    self.log_test("Placement Preparation Token Creation", "PASS", 
                                f"Token created: {self.placement_prep_token[:8]}... via placement preparation")
                    return True
                else:
                    self.log_test("Placement Preparation Token Creation", "FAIL", 
                                f"Token creation failed: {data}")
                    return False
            else:
                self.log_test("Placement Preparation Token Creation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Placement Preparation Token Creation", "FAIL", f"Exception: {str(e)}")
            return False

    def create_admin_token(self):
        """Create a token via admin dashboard endpoint"""
        try:
            # Create sample resume file content
            resume_content = """
            Jane Doe
            Senior Backend Developer
            
            EXPERIENCE:
            - 6+ years Python development
            - 4+ years Django/FastAPI
            - Database design and optimization
            - Microservices architecture
            - DevOps and CI/CD
            
            EDUCATION:
            - Bachelor's in Computer Engineering
            - AWS Certified Solutions Architect
            
            SKILLS:
            Python, Django, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, AWS
            """
            
            # Prepare form data for admin upload
            files = {
                'resume_file': ('jane_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            form_data = {
                'job_title': 'Senior Backend Developer - Admin',
                'job_description': 'We are seeking a senior backend developer with strong Python skills.',
                'job_requirements': '6+ years experience, Python, Django/FastAPI, database design, microservices'
            }
            
            response = self.session.post(f"{BASE_URL}/admin/upload-job", 
                                       files=files, data=form_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("token"):
                    self.admin_token = data["token"]
                    self.log_test("Admin Token Creation", "PASS", 
                                f"Token created: {self.admin_token[:8]}... via admin dashboard")
                    return True
                else:
                    self.log_test("Admin Token Creation", "FAIL", 
                                f"Token creation failed: {data}")
                    return False
            else:
                self.log_test("Admin Token Creation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Admin Token Creation", "FAIL", f"Exception: {str(e)}")
            return False

    def verify_token_source_marking(self):
        """Verify that tokens are marked with correct created_via field"""
        try:
            # Check placement preparation token in database
            # We'll validate this by starting interviews and checking the assessment created_via field
            # since we can't directly query the database from the test
            
            # Validate placement prep token
            pp_response = self.session.post(f"{BASE_URL}/candidate/validate-token", 
                                          json={"token": self.placement_prep_token})
            
            # Validate admin token  
            admin_response = self.session.post(f"{BASE_URL}/candidate/validate-token", 
                                             json={"token": self.admin_token})
            
            if pp_response.status_code == 200 and admin_response.status_code == 200:
                pp_data = pp_response.json()
                admin_data = admin_response.json()
                
                self.log_test("Token Source Marking Validation", "PASS", 
                            f"Both tokens validated successfully - PP: {pp_data.get('job_title')}, Admin: {admin_data.get('job_title')}")
                return True
            else:
                self.log_test("Token Source Marking Validation", "FAIL", 
                            f"Token validation failed - PP: {pp_response.status_code}, Admin: {admin_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Token Source Marking Validation", "FAIL", f"Exception: {str(e)}")
            return False

    def complete_placement_preparation_interview(self):
        """Complete a full interview using placement preparation token"""
        try:
            # Start interview
            start_response = self.session.post(f"{BASE_URL}/candidate/start-interview", 
                                             json={
                                                 "token": self.placement_prep_token,
                                                 "candidate_name": "John Smith",
                                                 "voice_mode": False
                                             })
            
            if start_response.status_code != 200:
                self.log_test("Placement Prep Interview Start", "FAIL", 
                            f"Failed to start interview: {start_response.status_code}")
                return False
            
            start_data = start_response.json()
            self.placement_prep_session_id = start_data.get("session_id")
            
            if not self.placement_prep_session_id:
                self.log_test("Placement Prep Interview Start", "FAIL", 
                            "No session ID returned")
                return False
            
            self.log_test("Placement Prep Interview Start", "PASS", 
                        f"Interview started with session ID: {self.placement_prep_session_id}")
            
            # Answer questions to complete the interview
            questions_answered = 0
            max_questions = 8
            
            sample_answers = [
                "I have 5+ years of experience in Python development, working on web applications and APIs.",
                "I've led a team of 4 developers on a microservices project using FastAPI and MongoDB.",
                "My approach to debugging involves systematic logging, unit testing, and using debugging tools.",
                "I stay updated through tech blogs, conferences, and contributing to open source projects.",
                "I handled a critical production issue by implementing proper monitoring and rollback procedures.",
                "I believe in collaborative leadership, clear communication, and mentoring team members.",
                "I prioritize tasks based on business impact, technical complexity, and dependencies.",
                "I've worked with AWS services including EC2, RDS, Lambda, and implemented CI/CD pipelines."
            ]
            
            while questions_answered < max_questions:
                # Send answer
                answer_response = self.session.post(f"{BASE_URL}/candidate/send-message", 
                                                  json={
                                                      "token": self.placement_prep_token,
                                                      "message": sample_answers[questions_answered % len(sample_answers)]
                                                  })
                
                if answer_response.status_code != 200:
                    self.log_test("Placement Prep Interview Answer", "FAIL", 
                                f"Failed to submit answer {questions_answered + 1}: {answer_response.status_code}")
                    return False
                
                answer_data = answer_response.json()
                questions_answered += 1
                
                # Check if interview is complete
                if answer_data.get("interview_complete"):
                    self.log_test("Placement Prep Interview Completion", "PASS", 
                                f"Interview completed after {questions_answered} questions")
                    break
                
                # Small delay between questions
                time.sleep(0.5)
            
            return True
            
        except Exception as e:
            self.log_test("Placement Prep Interview Completion", "FAIL", f"Exception: {str(e)}")
            return False

    def complete_admin_interview(self):
        """Complete a full interview using admin token"""
        try:
            # Start interview
            start_response = self.session.post(f"{BASE_URL}/candidate/start-interview", 
                                             json={
                                                 "token": self.admin_token,
                                                 "candidate_name": "Jane Doe",
                                                 "voice_mode": False
                                             })
            
            if start_response.status_code != 200:
                self.log_test("Admin Interview Start", "FAIL", 
                            f"Failed to start interview: {start_response.status_code}")
                return False
            
            start_data = start_response.json()
            self.admin_session_id = start_data.get("session_id")
            
            if not self.admin_session_id:
                self.log_test("Admin Interview Start", "FAIL", 
                            "No session ID returned")
                return False
            
            self.log_test("Admin Interview Start", "PASS", 
                        f"Interview started with session ID: {self.admin_session_id}")
            
            # Answer questions to complete the interview
            questions_answered = 0
            max_questions = 8
            
            sample_answers = [
                "I have 6+ years of backend development experience with Python and Django/FastAPI.",
                "I've designed and implemented microservices architectures for high-traffic applications.",
                "I use profiling tools, database query optimization, and caching strategies for performance.",
                "I follow TDD practices, write comprehensive unit tests, and use CI/CD for quality assurance.",
                "I've implemented OAuth2, JWT tokens, and proper input validation for security.",
                "I use monitoring tools like Prometheus, implement proper logging, and set up alerts.",
                "I've mentored junior developers and led technical architecture discussions.",
                "I've worked with Docker, Kubernetes, AWS services, and implemented infrastructure as code."
            ]
            
            while questions_answered < max_questions:
                # Send answer
                answer_response = self.session.post(f"{BASE_URL}/candidate/send-message", 
                                                  json={
                                                      "token": self.admin_token,
                                                      "message": sample_answers[questions_answered % len(sample_answers)]
                                                  })
                
                if answer_response.status_code != 200:
                    self.log_test("Admin Interview Answer", "FAIL", 
                                f"Failed to submit answer {questions_answered + 1}: {answer_response.status_code}")
                    return False
                
                answer_data = answer_response.json()
                questions_answered += 1
                
                # Check if interview is complete
                if answer_data.get("interview_complete"):
                    self.log_test("Admin Interview Completion", "PASS", 
                                f"Interview completed after {questions_answered} questions")
                    break
                
                # Small delay between questions
                time.sleep(0.5)
            
            return True
            
        except Exception as e:
            self.log_test("Admin Interview Completion", "FAIL", f"Exception: {str(e)}")
            return False

    def test_placement_preparation_reports_visibility(self):
        """Test that placement preparation reports endpoint only shows placement preparation assessments"""
        try:
            response = self.session.get(f"{BASE_URL}/placement-preparation/reports")
            
            if response.status_code != 200:
                self.log_test("Placement Preparation Reports Visibility", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            reports = data.get("reports", [])
            
            # Verify all reports are from placement preparation
            placement_prep_count = 0
            admin_count = 0
            
            for report in reports:
                created_via = report.get("created_via", "unknown")
                if created_via == "placement_preparation":
                    placement_prep_count += 1
                elif created_via == "admin":
                    admin_count += 1
                    
                # Check if our placement prep session is in the results
                if report.get("session_id") == self.placement_prep_session_id:
                    self.placement_prep_assessment_id = report.get("id")
            
            if admin_count > 0:
                self.log_test("Placement Preparation Reports Visibility", "FAIL", 
                            f"Found {admin_count} admin reports in placement preparation endpoint")
                return False
            
            self.log_test("Placement Preparation Reports Visibility", "PASS", 
                        f"Found {placement_prep_count} placement preparation reports, 0 admin reports (correct separation)")
            return True
            
        except Exception as e:
            self.log_test("Placement Preparation Reports Visibility", "FAIL", f"Exception: {str(e)}")
            return False

    def test_admin_reports_visibility(self):
        """Test that admin reports endpoint only shows admin and legacy assessments"""
        try:
            response = self.session.get(f"{BASE_URL}/admin/reports")
            
            if response.status_code != 200:
                self.log_test("Admin Reports Visibility", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            reports = data.get("reports", [])
            
            # Verify no placement preparation reports are shown
            placement_prep_count = 0
            admin_count = 0
            legacy_count = 0
            
            for report in reports:
                created_via = report.get("created_via")
                if created_via == "placement_preparation":
                    placement_prep_count += 1
                elif created_via == "admin":
                    admin_count += 1
                elif created_via is None:  # Legacy reports
                    legacy_count += 1
                    
                # Check if our admin session is in the results
                if report.get("session_id") == self.admin_session_id:
                    self.admin_assessment_id = report.get("id")
            
            if placement_prep_count > 0:
                self.log_test("Admin Reports Visibility", "FAIL", 
                            f"Found {placement_prep_count} placement preparation reports in admin endpoint")
                return False
            
            self.log_test("Admin Reports Visibility", "PASS", 
                        f"Found {admin_count} admin reports, {legacy_count} legacy reports, 0 placement prep reports (correct separation)")
            return True
            
        except Exception as e:
            self.log_test("Admin Reports Visibility", "FAIL", f"Exception: {str(e)}")
            return False

    def test_placement_preparation_detailed_report(self):
        """Test placement preparation detailed report endpoint"""
        try:
            if not self.placement_prep_session_id:
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            "No placement preparation session ID available")
                return False
            
            response = self.session.get(f"{BASE_URL}/placement-preparation/reports/{self.placement_prep_session_id}")
            
            if response.status_code == 404:
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            "Report not found - assessment may not have been created yet")
                return False
            elif response.status_code != 200:
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            report = data.get("report", {})
            
            # Verify report structure and content
            required_fields = ["session_id", "candidate_name", "job_title", "technical_score", 
                             "behavioral_score", "overall_score", "created_via"]
            
            missing_fields = [field for field in required_fields if field not in report]
            if missing_fields:
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            f"Missing required fields: {missing_fields}")
                return False
            
            # Verify it's marked as placement preparation
            if report.get("created_via") != "placement_preparation":
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            f"Report has incorrect created_via: {report.get('created_via')}")
                return False
            
            self.log_test("Placement Preparation Detailed Report", "PASS", 
                        f"Retrieved detailed report for {report.get('candidate_name')} - {report.get('job_title')}")
            return True
            
        except Exception as e:
            self.log_test("Placement Preparation Detailed Report", "FAIL", f"Exception: {str(e)}")
            return False

    def test_admin_detailed_report(self):
        """Test admin detailed report endpoint"""
        try:
            if not self.admin_session_id:
                self.log_test("Admin Detailed Report", "FAIL", 
                            "No admin session ID available")
                return False
            
            response = self.session.get(f"{BASE_URL}/admin/reports/{self.admin_session_id}")
            
            if response.status_code == 404:
                self.log_test("Admin Detailed Report", "FAIL", 
                            "Report not found - assessment may not have been created yet")
                return False
            elif response.status_code != 200:
                self.log_test("Admin Detailed Report", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            report = data.get("report", {})
            
            # Verify report structure and content
            required_fields = ["session_id", "candidate_name", "job_title", "technical_score", 
                             "behavioral_score", "overall_score", "created_via"]
            
            missing_fields = [field for field in required_fields if field not in report]
            if missing_fields:
                self.log_test("Admin Detailed Report", "FAIL", 
                            f"Missing required fields: {missing_fields}")
                return False
            
            # Verify it's marked as admin
            if report.get("created_via") != "admin":
                self.log_test("Admin Detailed Report", "FAIL", 
                            f"Report has incorrect created_via: {report.get('created_via')}")
                return False
            
            self.log_test("Admin Detailed Report", "PASS", 
                        f"Retrieved detailed report for {report.get('candidate_name')} - {report.get('job_title')}")
            return True
            
        except Exception as e:
            self.log_test("Admin Detailed Report", "FAIL", f"Exception: {str(e)}")
            return False

    def test_cross_endpoint_isolation(self):
        """Test that placement preparation reports are not accessible via admin endpoint and vice versa"""
        try:
            # Try to access placement preparation report via admin endpoint
            if self.placement_prep_session_id:
                admin_access_response = self.session.get(f"{BASE_URL}/admin/reports/{self.placement_prep_session_id}")
                if admin_access_response.status_code != 404:
                    self.log_test("Cross-Endpoint Isolation", "FAIL", 
                                f"Placement prep report accessible via admin endpoint (should be 404)")
                    return False
            
            # Try to access admin report via placement preparation endpoint
            if self.admin_session_id:
                pp_access_response = self.session.get(f"{BASE_URL}/placement-preparation/reports/{self.admin_session_id}")
                if pp_access_response.status_code != 404:
                    self.log_test("Cross-Endpoint Isolation", "FAIL", 
                                f"Admin report accessible via placement prep endpoint (should be 404)")
                    return False
            
            self.log_test("Cross-Endpoint Isolation", "PASS", 
                        "Reports are properly isolated - placement prep reports not accessible via admin endpoint and vice versa")
            return True
            
        except Exception as e:
            self.log_test("Cross-Endpoint Isolation", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("=" * 80)
        print("PLACEMENT PREPARATION ASSESSMENT REPORTS & TOKEN-BASED VISIBILITY TESTING")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Admin Authentication
        test_results.append(self.test_admin_authentication())
        
        if not self.admin_authenticated:
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Test 2: Token Creation & Source Marking
        test_results.append(self.create_placement_preparation_token())
        test_results.append(self.create_admin_token())
        test_results.append(self.verify_token_source_marking())
        
        # Test 3: Complete Interview Workflows
        test_results.append(self.complete_placement_preparation_interview())
        test_results.append(self.complete_admin_interview())
        
        # Wait a moment for assessments to be generated
        print("⏳ Waiting for assessments to be generated...")
        time.sleep(3)
        
        # Test 4: Assessment Reports Visibility
        test_results.append(self.test_placement_preparation_reports_visibility())
        test_results.append(self.test_admin_reports_visibility())
        
        # Test 5: Detailed Report Functionality
        test_results.append(self.test_placement_preparation_detailed_report())
        test_results.append(self.test_admin_detailed_report())
        
        # Test 6: Cross-Endpoint Isolation
        test_results.append(self.test_cross_endpoint_isolation())
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Placement preparation assessment reports and token-based visibility logic is working correctly.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = PlacementPreparationTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ PLACEMENT PREPARATION TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ PLACEMENT PREPARATION TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()