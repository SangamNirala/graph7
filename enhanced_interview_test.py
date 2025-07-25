#!/usr/bin/env python3
"""
Enhanced Interview Creation Functionality Test
Tests the specific functionality mentioned in the review request:
- /api/admin/upload-job-enhanced endpoint
- Enhanced parameters (job_title, job_description, job_requirements, include_coding_challenge, role_archetype, interview_focus, resume_file)
- Token generation with enhanced features
- Token validation for interview start
"""

import requests
import json
import io
from typing import Dict, Any

# Backend URL from frontend .env
BASE_URL = "https://0333f662-5e6b-4f4b-a6c5-ab4fc14b9c53.preview.emergentagent.com/api"

class EnhancedInterviewTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.enhanced_token = None
        self.session_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_enhanced_upload_endpoint(self) -> bool:
        """Test the /api/admin/upload-job-enhanced endpoint with enhanced parameters"""
        try:
            # Create sample resume content for testing
            resume_content = """Sarah Chen
Senior Software Engineer
Email: sarah.chen@email.com
Phone: (555) 987-6543

EXPERIENCE:
- 6+ years of full-stack development
- Expert in Python, JavaScript, and React
- Led development of microservices architecture
- Experience with coding challenges and technical interviews
- Strong problem-solving and algorithmic thinking

SKILLS:
- Python, JavaScript, TypeScript, Java
- React, FastAPI, Node.js, Spring Boot
- MongoDB, PostgreSQL, Redis
- Docker, Kubernetes, AWS, Azure
- Algorithm design and data structures
- System design and architecture

EDUCATION:
Master of Science in Computer Science
Stanford University, 2017

ACHIEVEMENTS:
- Led team of 8 developers on enterprise platform
- Optimized system performance by 40%
- Mentored 15+ junior developers
- Published 3 technical papers on distributed systems"""
            
            # Prepare multipart form data with enhanced parameters
            files = {
                'resume_file': ('enhanced_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Full-Stack Engineer',
                'job_description': 'We are seeking a highly skilled Senior Full-Stack Engineer to join our engineering team. The role involves designing and implementing scalable web applications, leading technical initiatives, and mentoring junior developers. You will work on cutting-edge projects using modern technologies and contribute to architectural decisions.',
                'job_requirements': 'Requirements: 5+ years of full-stack development experience, expertise in Python and JavaScript, experience with React and FastAPI, strong algorithmic and problem-solving skills, system design knowledge, leadership experience, excellent communication skills, ability to work in agile environments.',
                'include_coding_challenge': True,
                'role_archetype': 'Software Engineer',
                'interview_focus': 'Technical Deep-Dive'
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
                          "features" in result and
                          "estimated_duration" in result)
                
                if success:
                    self.enhanced_token = result["token"]
                    # Verify enhanced features are properly set
                    features = result.get("features", {})
                    success = (features.get("coding_challenge") == True and
                              features.get("role_archetype") == "Software Engineer" and
                              features.get("interview_focus") == "Technical Deep-Dive")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.enhanced_token[:8]}..., Features: {result.get('features', {})}, Duration: {result.get('estimated_duration')}min"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Enhanced Upload Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Upload Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_token_validation(self) -> bool:
        """Test that the enhanced token can be validated"""
        if not self.enhanced_token:
            self.log_test("Enhanced Token Validation", False, "No enhanced token available")
            return False
        
        try:
            payload = {"token": self.enhanced_token}
            response = self.session.post(
                f"{self.base_url}/candidate/validate-token",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("valid", False) and "job_title" in data
            
            details = f"Status: {response.status_code}, Valid: {data.get('valid') if success else 'N/A'}, Job: {data.get('job_title', 'N/A') if success else 'N/A'}"
            self.log_test("Enhanced Token Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Token Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_interview_start(self) -> bool:
        """Test starting an interview with enhanced token"""
        if not self.enhanced_token:
            self.log_test("Enhanced Interview Start", False, "No enhanced token available")
            return False
        
        try:
            payload = {
                "token": self.enhanced_token,
                "candidate_name": "Sarah Chen",
                "voice_mode": False
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
                          "is_enhanced" in data and
                          data.get("is_enhanced") == True and
                          "features" in data)
                
                if success:
                    self.session_id = data["session_id"]
                    # Verify enhanced features are present
                    features = data.get("features", {})
                    success = (features.get("coding_challenge") == True and
                              features.get("role_archetype") == "Software Engineer" and
                              features.get("interview_focus") == "Technical Deep-Dive")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Enhanced: {data.get('is_enhanced')}, Session: {self.session_id[:8]}..., Features: {data.get('features', {})}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Enhanced Interview Start", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Interview Start", False, f"Exception: {str(e)}")
            return False
    
    def test_coding_challenge_access(self) -> bool:
        """Test that coding challenge is accessible for enhanced interview"""
        if not self.session_id:
            self.log_test("Coding Challenge Access", False, "No session ID available")
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/modules/coding-challenge/{self.session_id}",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("challenge" in data and 
                          "problem_title" in data["challenge"] and
                          "problem_description" in data["challenge"] and
                          "initial_code" in data["challenge"])
            
            details = f"Status: {response.status_code}"
            if success:
                challenge = data["challenge"]
                details += f", Problem: {challenge.get('problem_title', 'N/A')}, Language: {challenge.get('language', 'N/A')}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Coding Challenge Access", success, details)
            return success
        except Exception as e:
            self.log_test("Coding Challenge Access", False, f"Exception: {str(e)}")
            return False
    
    def test_endpoint_accessibility(self) -> bool:
        """Test that the enhanced endpoint is accessible (basic connectivity)"""
        try:
            # Test with minimal data to check endpoint accessibility
            files = {
                'resume_file': ('test.txt', io.StringIO("Test resume content"), 'text/plain')
            }
            
            data = {
                'job_title': 'Test Job',
                'job_description': 'Test description',
                'job_requirements': 'Test requirements'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job-enhanced",
                files=files,
                data=data,
                timeout=10
            )
            
            # We expect either 200 (success) or 400 (validation error), but not 404 (not found)
            success = response.status_code in [200, 400, 422]  # 422 for validation errors
            
            details = f"Status: {response.status_code}, Endpoint accessible: {success}"
            if not success and response.status_code == 404:
                details += " - Endpoint not found!"
            
            self.log_test("Enhanced Endpoint Accessibility", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Endpoint Accessibility", False, f"Exception: {str(e)}")
            return False
    
    def test_different_role_archetypes(self) -> bool:
        """Test different role archetypes work correctly"""
        role_archetypes = ["Software Engineer", "Sales", "Graduate", "General"]
        
        for role in role_archetypes:
            try:
                resume_content = f"""Test Candidate for {role}
Email: test@email.com
Phone: (555) 123-4567

EXPERIENCE:
- Relevant experience for {role} position
- Strong background in required skills
- Proven track record of success

SKILLS:
- Role-specific skills for {role}
- Communication and teamwork
- Problem-solving abilities"""
                
                files = {
                    'resume_file': (f'{role.lower()}_resume.txt', io.StringIO(resume_content), 'text/plain')
                }
                
                data = {
                    'job_title': f'{role} Position',
                    'job_description': f'Job description for {role} role',
                    'job_requirements': f'Requirements for {role} position',
                    'role_archetype': role,
                    'interview_focus': 'Balanced'
                }
                
                response = self.session.post(
                    f"{self.base_url}/admin/upload-job-enhanced",
                    files=files,
                    data=data,
                    timeout=15
                )
                
                if response.status_code != 200:
                    self.log_test(f"Role Archetype: {role}", False, f"Status: {response.status_code}")
                    return False
                
                result = response.json()
                if not (result.get("success") and result.get("features", {}).get("role_archetype") == role):
                    self.log_test(f"Role Archetype: {role}", False, f"Features not set correctly: {result.get('features', {})}")
                    return False
                
            except Exception as e:
                self.log_test(f"Role Archetype: {role}", False, f"Exception: {str(e)}")
                return False
        
        self.log_test("Different Role Archetypes", True, f"All {len(role_archetypes)} role archetypes working correctly")
        return True
    
    def run_enhanced_tests(self) -> Dict[str, bool]:
        """Run all enhanced interview creation tests"""
        print("=" * 80)
        print("ENHANCED INTERVIEW CREATION FUNCTIONALITY TEST")
        print("Testing /api/admin/upload-job-enhanced endpoint and token generation")
        print("=" * 80)
        print()
        
        results = {}
        
        # Test endpoint accessibility first
        results["endpoint_accessibility"] = self.test_endpoint_accessibility()
        
        # Test enhanced upload with all parameters
        results["enhanced_upload"] = self.test_enhanced_upload_endpoint()
        
        # Test token validation
        results["enhanced_token_validation"] = self.test_enhanced_token_validation()
        
        # Test interview start with enhanced features
        results["enhanced_interview_start"] = self.test_enhanced_interview_start()
        
        # Test coding challenge access
        results["coding_challenge_access"] = self.test_coding_challenge_access()
        
        # Test different role archetypes
        results["role_archetypes"] = self.test_different_role_archetypes()
        
        # Summary
        print("=" * 80)
        print("ENHANCED INTERVIEW CREATION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL ENHANCED INTERVIEW CREATION TESTS PASSED!")
            print("✅ The enhanced interview creation functionality is working correctly.")
            print("✅ Token generation with enhanced features is functional.")
            print("✅ Enhanced tokens can be validated and used for interview start.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Enhanced functionality is largely functional.")
        else:
            print("⚠️  Multiple tests failed. Enhanced interview creation needs attention.")
        
        return results

def main():
    """Main test execution"""
    tester = EnhancedInterviewTester()
    results = tester.run_enhanced_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())