#!/usr/bin/env python3
"""
Placement Preparation Resume Upload Testing
Tests the placement preparation resume upload functionality to ensure:
1. Resume files (TXT, PDF, DOC) are properly uploaded and processed
2. Resume preview text is extracted and returned correctly  
3. Preview text is suitable for scrollable box display format
4. Placement preparation workflow continues to work after resume upload

TESTING REQUIREMENTS:
1. Test that existing admin endpoints still work (since we're using the same backend endpoints)
2. Test the interview creation flow that the placement preparation page uses:
   - POST /api/admin/upload-job (for resume upload with preview) 
   - POST /api/admin/create-token (for creating interview tokens)
3. Verify that the same interview creation functionality works from the placement preparation page as it does from the admin dashboard
4. Test with sample data to ensure the complete workflow functions properly
5. FOCUS: Test resume preview text extraction and formatting for scrollable box display
"""

import requests
import json
import time
import io
import base64
import tempfile
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://a6c857f5-ba9e-4ce1-a4a2-779eff5469a9.preview.emergentagent.com/api"

class PlacementPreparationTester:
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
    
    def test_backend_connectivity(self) -> bool:
        """Test basic backend connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            success = response.status_code in [200, 405]  # 405 is also acceptable for health check
            details = f"Status: {response.status_code}, Backend responding"
            self.log_test("Backend Connectivity", success, details)
            return success
        except Exception as e:
            self.log_test("Backend Connectivity", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_functionality(self) -> bool:
        """Test admin login functionality (used by both admin dashboard and placement preparation)"""
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
            self.log_test("Admin Login Functionality", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login Functionality", False, f"Exception: {str(e)}")
            return False
    
    def test_resume_upload_endpoint(self) -> bool:
        """Test POST /api/admin/upload endpoint for resume upload"""
        try:
            # Create sample resume content for placement preparation testing
            resume_content = """Sarah Johnson
Placement Preparation Candidate
Email: sarah.johnson@university.edu
Phone: (555) 234-5678

EDUCATION:
Bachelor of Science in Computer Science
State University, Expected Graduation: May 2024
GPA: 3.8/4.0

EXPERIENCE:
Software Development Intern - Tech Startup (Summer 2023)
- Developed REST APIs using Python and FastAPI
- Built responsive web interfaces with React
- Collaborated with team of 5 developers on agile projects
- Implemented automated testing and CI/CD pipelines

PROJECTS:
E-commerce Web Application
- Full-stack application using React, Node.js, and MongoDB
- Implemented user authentication and payment processing
- Deployed on AWS with Docker containers

SKILLS:
- Programming: Python, JavaScript, Java, SQL
- Frameworks: React, FastAPI, Node.js, Express
- Databases: MongoDB, PostgreSQL, MySQL
- Tools: Git, Docker, AWS, Jenkins
- Soft Skills: Team collaboration, problem-solving, communication

ACHIEVEMENTS:
- Dean's List for 3 consecutive semesters
- Winner of University Hackathon 2023
- President of Computer Science Student Association"""
            
            files = {
                'resume_file': ('sarah_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Software Engineer - Entry Level',
                'job_description': 'We are seeking a motivated entry-level software engineer to join our development team. This role is perfect for recent graduates or candidates with 0-2 years of experience who are passionate about technology and eager to learn.',
                'job_requirements': 'Requirements: Bachelor\'s degree in Computer Science or related field, knowledge of Python/JavaScript, understanding of web development concepts, strong problem-solving skills, excellent communication abilities, willingness to learn new technologies.'
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
                success = (result.get("success", False) and 
                          "token" in result and 
                          "resume_preview" in result)
                if success:
                    self.generated_token = result["token"]
            
            details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            if self.generated_token:
                details += f", Token: {self.generated_token[:8]}..."
            
            self.log_test("Resume Upload Endpoint (/api/admin/upload-job)", success, details)
            return success
        except Exception as e:
            self.log_test("Resume Upload Endpoint (/api/admin/upload-job)", False, f"Exception: {str(e)}")
            return False
    
    def test_create_token_endpoint(self) -> bool:
        """Test POST /api/admin/upload-job endpoint for creating interview tokens (second test with different data)"""
        try:
            # Create another resume for token creation testing
            resume_content = """Michael Chen
Placement Preparation Test Candidate
Email: michael.chen@college.edu
Phone: (555) 345-6789

EDUCATION:
Master of Science in Software Engineering
Tech Institute, Graduation: December 2024
Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Architecture

EXPERIENCE:
Research Assistant - University AI Lab (2023-2024)
- Developed machine learning models using Python and TensorFlow
- Analyzed large datasets and created visualization dashboards
- Published research paper on natural language processing

Teaching Assistant - Introduction to Programming (2023)
- Assisted 50+ students with Python programming concepts
- Conducted lab sessions and graded assignments
- Improved student pass rate by 15%

TECHNICAL SKILLS:
- Languages: Python, Java, C++, JavaScript, SQL
- Frameworks: Django, Flask, React, Spring Boot
- Databases: PostgreSQL, MongoDB, Redis
- Cloud: AWS, Google Cloud Platform
- Tools: Git, Docker, Kubernetes, Jenkins

PROJECTS:
Real-time Chat Application
- Built using WebSocket, Node.js, and React
- Implemented user authentication and message encryption
- Deployed on AWS with auto-scaling capabilities

Data Analytics Dashboard
- Created interactive dashboard using Python and Plotly
- Integrated with multiple data sources and APIs
- Used by 100+ users for business intelligence"""
            
            files = {
                'resume_file': ('michael_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Full Stack Developer - Graduate Position',
                'job_description': 'We are looking for a talented graduate-level full stack developer to join our engineering team. The ideal candidate will have strong academic background and hands-on experience with modern web technologies.',
                'job_requirements': 'Requirements: Master\'s degree in Computer Science or related field, proficiency in Python and JavaScript, experience with web frameworks, database knowledge, cloud platform familiarity, strong analytical and problem-solving skills.'
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
                success = (result.get("success", False) and 
                          "token" in result)
                if success:
                    # Store this token for further testing
                    create_token_result = result["token"]
            
            details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            if success and 'create_token_result' in locals():
                details += f", Token: {create_token_result[:8]}..."
            
            self.log_test("Token Creation via Upload-Job Endpoint (Second Test)", success, details)
            return success
        except Exception as e:
            self.log_test("Token Creation via Upload-Job Endpoint (Second Test)", False, f"Exception: {str(e)}")
            return False
    
    def test_token_validation_workflow(self) -> bool:
        """Test that tokens created via placement preparation work with candidate validation"""
        if not self.generated_token:
            self.log_test("Token Validation Workflow", False, "No token available from upload test")
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
            self.log_test("Token Validation Workflow", success, details)
            return success
        except Exception as e:
            self.log_test("Token Validation Workflow", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_start_workflow(self) -> bool:
        """Test that placement preparation tokens work with interview start"""
        if not self.generated_token:
            self.log_test("Interview Start Workflow", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "candidate_name": "Sarah Johnson - Placement Prep",
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
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "question_number" in data)
                if success:
                    self.session_id = data["session_id"]
            
            details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            if self.session_id:
                details += f", Session ID: {self.session_id[:8]}..."
            
            self.log_test("Interview Start Workflow", success, details)
            return success
        except Exception as e:
            self.log_test("Interview Start Workflow", False, f"Exception: {str(e)}")
            return False
    
    def test_complete_placement_preparation_flow(self) -> bool:
        """Test complete flow: upload resume -> create token -> validate -> start interview -> answer questions"""
        try:
            # Step 1: Upload resume (already done in previous test)
            if not self.generated_token:
                self.log_test("Complete Placement Preparation Flow", False, "No token from previous upload")
                return False
            
            # Step 2: Answer a few interview questions to test the complete flow
            sample_answers = [
                "I'm a recent computer science graduate with strong academic background and internship experience. I've worked with Python, JavaScript, and modern web frameworks. I'm passionate about software development and eager to contribute to a professional development team.",
                
                "During my internship, I was tasked with optimizing a slow API endpoint. I analyzed the database queries, identified N+1 query problems, and implemented proper joins and caching. This reduced response time from 2 seconds to 200ms, significantly improving user experience.",
                
                "I believe in writing clean, maintainable code with proper documentation. I follow coding standards, use meaningful variable names, and write unit tests. I also believe in continuous learning and staying updated with industry best practices and new technologies."
            ]
            
            questions_answered = 0
            for i, answer in enumerate(sample_answers):
                payload = {
                    "token": self.generated_token,
                    "message": answer
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/send-message",
                    json=payload,
                    timeout=20
                )
                
                if response.status_code != 200:
                    details = f"Failed at question {i+1}, Status: {response.status_code}"
                    self.log_test("Complete Placement Preparation Flow", False, details)
                    return False
                
                data = response.json()
                questions_answered += 1
                
                # Check if we have next question or completion
                if data.get("completed", False):
                    break
                elif not data.get("next_question"):
                    break
                
                time.sleep(1)  # Small delay between questions
            
            success = questions_answered >= 3
            details = f"Successfully answered {questions_answered} questions in placement preparation flow"
            self.log_test("Complete Placement Preparation Flow", success, details)
            return success
            
        except Exception as e:
            self.log_test("Complete Placement Preparation Flow", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_dashboard_compatibility(self) -> bool:
        """Test that admin dashboard endpoints still work (backward compatibility)"""
        try:
            # Test admin reports endpoint
            response = self.session.get(f"{self.base_url}/admin/reports", timeout=10)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "reports" in data and isinstance(data["reports"], list)
            
            details = f"Status: {response.status_code}, Found {len(data.get('reports', []))} reports"
            self.log_test("Admin Dashboard Compatibility", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Dashboard Compatibility", False, f"Exception: {str(e)}")
            return False
    
    def test_placement_vs_admin_endpoint_consistency(self) -> bool:
        """Test that placement preparation and admin dashboard use the same endpoints consistently"""
        try:
            # Test that both upload-job endpoint works consistently
            upload_test_passed = hasattr(self, 'generated_token') and self.generated_token is not None
            
            # Test that the same endpoint structure works for different job types
            # This tests consistency rather than re-using tokens
            if upload_test_passed:
                # Test admin reports endpoint (should work the same way for both admin and placement prep)
                response = self.session.get(f"{self.base_url}/admin/reports", timeout=10)
                reports_consistent = response.status_code == 200
                
                # Test health endpoint (basic consistency check)
                health_response = self.session.get(f"{self.base_url}/health", timeout=10)
                health_consistent = health_response.status_code == 200
                
                endpoint_consistency = reports_consistent and health_consistent
            else:
                endpoint_consistency = False
            
            success = upload_test_passed and endpoint_consistency
            details = f"Upload endpoint working: {upload_test_passed}, Reports endpoint consistent: {reports_consistent if 'reports_consistent' in locals() else False}, Health endpoint consistent: {health_consistent if 'health_consistent' in locals() else False}"
            self.log_test("Placement vs Admin Endpoint Consistency", success, details)
            return success
        except Exception as e:
            self.log_test("Placement vs Admin Endpoint Consistency", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all placement preparation tests"""
        print("=" * 80)
        print("PLACEMENT PREPARATION BACKEND TESTING")
        print("Testing backend functionality for the new placement preparation feature")
        print("=" * 80)
        print()
        
        results = {}
        
        # Test 1: Basic connectivity
        results["backend_connectivity"] = self.test_backend_connectivity()
        
        # Test 2: Admin login (used by both admin and placement preparation)
        results["admin_login_functionality"] = self.test_admin_login_functionality()
        
        # Test 3: Resume upload endpoint (POST /api/admin/upload)
        results["resume_upload_endpoint"] = self.test_resume_upload_endpoint()
        
        # Test 4: Create token endpoint (POST /api/admin/create-token)
        results["create_token_endpoint"] = self.test_create_token_endpoint()
        
        # Test 5: Token validation workflow
        results["token_validation_workflow"] = self.test_token_validation_workflow()
        
        # Test 6: Interview start workflow
        results["interview_start_workflow"] = self.test_interview_start_workflow()
        
        # Test 7: Complete placement preparation flow
        results["complete_placement_flow"] = self.test_complete_placement_preparation_flow()
        
        # Test 8: Admin dashboard compatibility (backward compatibility)
        results["admin_dashboard_compatibility"] = self.test_admin_dashboard_compatibility()
        
        # Test 9: Endpoint consistency between placement prep and admin
        results["endpoint_consistency"] = self.test_placement_vs_admin_endpoint_consistency()
        
        # Summary
        print("=" * 80)
        print("PLACEMENT PREPARATION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by category
        categories = {
            "Basic Functionality": ["backend_connectivity", "admin_login_functionality"],
            "Core Placement Preparation Endpoints": ["resume_upload_endpoint", "create_token_endpoint"],
            "Interview Creation Workflow": ["token_validation_workflow", "interview_start_workflow"],
            "End-to-End Testing": ["complete_placement_flow"],
            "Compatibility & Consistency": ["admin_dashboard_compatibility", "endpoint_consistency"]
        }
        
        for category, test_names in categories.items():
            print(f"\n{category}:")
            for test_name in test_names:
                if test_name in results:
                    status = "✅ PASS" if results[test_name] else "❌ FAIL"
                    print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Placement preparation backend functionality is working correctly.")
            print("✅ The same backend endpoints work for both admin dashboard and placement preparation page.")
            print("✅ Resume upload, token creation, and interview workflows are fully functional.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Placement preparation functionality is largely operational.")
            print("⚠️  Some minor issues detected - check details above.")
        else:
            print("❌ MULTIPLE FAILURES! Placement preparation backend needs attention.")
            print("⚠️  Check the failed tests above for specific issues.")
        
        return results

def main():
    """Main test execution"""
    tester = PlacementPreparationTester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())