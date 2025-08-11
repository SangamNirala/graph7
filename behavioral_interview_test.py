#!/usr/bin/env python3
"""
Focused Testing for Behavioral Interview Questions Endpoints
Testing the specific endpoints that were reported as "not found" by previous testing agent
"""

import requests
import json
import time
import os
from datetime import datetime
import io

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://9111a607-ad7c-4aad-8586-9dca4be775f2.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class BehavioralInterviewTester:
    def __init__(self):
        self.session = requests.Session()
        self.analysis_id = None
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()

    def test_backend_connectivity(self):
        """Test basic backend connectivity"""
        try:
            response = self.session.get(f"{BACKEND_URL}/docs")
            
            if response.status_code == 200:
                self.log_test("Backend Connectivity", "PASS", 
                            f"Backend accessible at {BACKEND_URL}")
                return True
            else:
                self.log_test("Backend Connectivity", "FAIL", 
                            f"HTTP {response.status_code}: Backend not accessible")
                return False
                
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Exception: {str(e)}")
            return False

    def test_post_behavioral_interview_questions(self):
        """Test POST /api/placement-preparation/behavioral-interview-questions endpoint"""
        try:
            # Create sample resume content
            resume_content = """
            Sarah Johnson
            Senior Software Engineer
            
            PROFESSIONAL SUMMARY:
            Experienced software engineer with 8+ years in full-stack development, team leadership, and agile methodologies.
            
            EXPERIENCE:
            Senior Software Engineer | TechCorp Inc. | 2020-Present
            - Led a team of 5 developers on microservices architecture migration
            - Implemented CI/CD pipelines reducing deployment time by 60%
            - Mentored junior developers and conducted code reviews
            - Collaborated with product managers and designers on user experience improvements
            
            Software Engineer | StartupXYZ | 2018-2020
            - Developed React-based frontend applications serving 100K+ users
            - Built RESTful APIs using Node.js and Express
            - Worked in fast-paced agile environment with 2-week sprints
            - Participated in on-call rotation and incident response
            
            Junior Developer | WebSolutions | 2016-2018
            - Maintained legacy PHP applications
            - Learned modern JavaScript frameworks and best practices
            - Contributed to team knowledge sharing sessions
            
            EDUCATION:
            Bachelor of Science in Computer Science | State University | 2016
            
            SKILLS:
            JavaScript, React, Node.js, Python, MongoDB, AWS, Docker, Git, Agile, Team Leadership
            """
            
            # Prepare form data
            files = {
                'resume': ('sarah_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            form_data = {
                'job_title': 'Senior Software Engineer',
                'job_description': 'We are seeking a Senior Software Engineer to join our growing team. The ideal candidate will have 5+ years of experience in full-stack development, experience with React and Node.js, and proven leadership abilities. You will be responsible for architecting scalable solutions, mentoring junior developers, and collaborating with cross-functional teams to deliver high-quality software products.'
            }
            
            response = self.session.post(
                f"{BASE_URL}/placement-preparation/behavioral-interview-questions", 
                files=files, 
                data=form_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("analysis_id"):
                    self.analysis_id = data["analysis_id"]
                    analysis_length = len(data.get("interview_questions", ""))
                    self.log_test("POST Behavioral Interview Questions", "PASS", 
                                f"Analysis created successfully (ID: {self.analysis_id}, Length: {analysis_length} chars)")
                    return True
                else:
                    self.log_test("POST Behavioral Interview Questions", "FAIL", 
                                f"Unexpected response structure: {data}")
                    return False
            elif response.status_code == 404:
                self.log_test("POST Behavioral Interview Questions", "FAIL", 
                            f"Endpoint not found (404) - This confirms the routing issue reported")
                return False
            else:
                self.log_test("POST Behavioral Interview Questions", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("POST Behavioral Interview Questions", "FAIL", f"Exception: {str(e)}")
            return False

    def test_get_behavioral_interview_questions(self):
        """Test GET /api/placement-preparation/behavioral-interview-questions endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/placement-preparation/behavioral-interview-questions")
            
            if response.status_code == 200:
                data = response.json()
                if "analyses" in data:
                    analyses_count = len(data["analyses"])
                    self.log_test("GET Behavioral Interview Questions", "PASS", 
                                f"Retrieved {analyses_count} analyses successfully")
                    
                    # Check if our created analysis is in the list
                    if self.analysis_id:
                        found_analysis = any(analysis.get("id") == self.analysis_id for analysis in data["analyses"])
                        if found_analysis:
                            self.log_test("Analysis Retrieval Verification", "PASS", 
                                        f"Created analysis {self.analysis_id} found in list")
                        else:
                            self.log_test("Analysis Retrieval Verification", "FAIL", 
                                        f"Created analysis {self.analysis_id} not found in list")
                    
                    return True
                else:
                    self.log_test("GET Behavioral Interview Questions", "FAIL", 
                                f"Unexpected response structure: {data}")
                    return False
            elif response.status_code == 404:
                self.log_test("GET Behavioral Interview Questions", "FAIL", 
                            f"Endpoint not found (404) - This confirms the routing issue reported")
                return False
            else:
                self.log_test("GET Behavioral Interview Questions", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("GET Behavioral Interview Questions", "FAIL", f"Exception: {str(e)}")
            return False

    def test_download_behavioral_interview_pdf(self):
        """Test GET /api/placement-preparation/behavioral-interview-questions/{analysis_id}/download endpoint"""
        try:
            if not self.analysis_id:
                self.log_test("Download Behavioral Interview PDF", "FAIL", 
                            "No analysis ID available for download test")
                return False
            
            response = self.session.get(
                f"{BASE_URL}/placement-preparation/behavioral-interview-questions/{self.analysis_id}/download"
            )
            
            if response.status_code == 200:
                # Check if response is a PDF
                content_type = response.headers.get('content-type', '')
                content_length = len(response.content)
                
                if 'application/pdf' in content_type and content_length > 0:
                    self.log_test("Download Behavioral Interview PDF", "PASS", 
                                f"PDF downloaded successfully ({content_length} bytes, content-type: {content_type})")
                    return True
                else:
                    self.log_test("Download Behavioral Interview PDF", "FAIL", 
                                f"Invalid PDF response (content-type: {content_type}, size: {content_length})")
                    return False
            elif response.status_code == 404:
                self.log_test("Download Behavioral Interview PDF", "FAIL", 
                            f"Analysis or PDF not found (404) - Analysis ID: {self.analysis_id}")
                return False
            else:
                self.log_test("Download Behavioral Interview PDF", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Download Behavioral Interview PDF", "FAIL", f"Exception: {str(e)}")
            return False

    def test_endpoint_routing_investigation(self):
        """Investigate potential routing issues by testing similar endpoints"""
        try:
            # Test technical interview questions endpoint for comparison
            tech_response = self.session.get(f"{BASE_URL}/placement-preparation/technical-interview-questions")
            
            # Test other placement preparation endpoints
            ats_response = self.session.get(f"{BASE_URL}/placement-preparation/ats-score")
            
            routing_info = {
                "technical-interview-questions": tech_response.status_code,
                "ats-score": ats_response.status_code,
            }
            
            self.log_test("Endpoint Routing Investigation", "INFO", 
                        f"Related endpoint status codes: {routing_info}")
            
            # Check if there's a pattern in routing issues
            if tech_response.status_code == 404 and ats_response.status_code == 404:
                self.log_test("Routing Pattern Analysis", "FAIL", 
                            "Multiple placement-preparation endpoints returning 404 - possible routing configuration issue")
                return False
            elif tech_response.status_code == 200:
                self.log_test("Routing Pattern Analysis", "INFO", 
                            "Technical interview questions endpoint working - behavioral endpoint specific issue")
                return True
            else:
                self.log_test("Routing Pattern Analysis", "INFO", 
                            "Mixed results - need further investigation")
                return True
                
        except Exception as e:
            self.log_test("Endpoint Routing Investigation", "FAIL", f"Exception: {str(e)}")
            return False

    def run_focused_test(self):
        """Run focused tests for behavioral interview questions endpoints"""
        print("=" * 80)
        print("BEHAVIORAL INTERVIEW QUESTIONS ENDPOINTS FOCUSED TESTING")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Backend Connectivity
        test_results.append(self.test_backend_connectivity())
        
        # Test 2: Endpoint Routing Investigation
        test_results.append(self.test_endpoint_routing_investigation())
        
        # Test 3: POST Endpoint
        test_results.append(self.test_post_behavioral_interview_questions())
        
        # Test 4: GET Endpoint
        test_results.append(self.test_get_behavioral_interview_questions())
        
        # Test 5: Download PDF Endpoint (only if we have an analysis_id)
        if self.analysis_id:
            test_results.append(self.test_download_behavioral_interview_pdf())
        else:
            self.log_test("Download PDF Test", "SKIP", "No analysis ID available - POST endpoint failed")
        
        # Summary
        print("=" * 80)
        print("FOCUSED TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Specific findings
        print("\n🔍 KEY FINDINGS:")
        if self.analysis_id:
            print(f"✅ Behavioral interview questions can be generated (Analysis ID: {self.analysis_id})")
        else:
            print("❌ Behavioral interview questions generation failed")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Behavioral interview questions endpoints are working correctly.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Detailed investigation results above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = BehavioralInterviewTester()
    success = tester.run_focused_test()
    
    if success:
        print("\n✅ BEHAVIORAL INTERVIEW QUESTIONS TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ BEHAVIORAL INTERVIEW QUESTIONS TESTING COMPLETED WITH ISSUES")
        exit(1)

if __name__ == "__main__":
    main()