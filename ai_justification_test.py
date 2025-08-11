#!/usr/bin/env python3
"""
AI Justification Feature Testing
Tests the new AI justification endpoint for candidate screening results.

Test Flow:
1. Admin login with Game@1234 password
2. Upload sample resumes for screening
3. Create job requirements and screen candidates
4. Test the new GET /api/admin/screening/candidate-justification/{candidate_id} endpoint
5. Verify comprehensive AI justification is returned
"""

import requests
import json
import time
import io
from typing import Dict, Any, Optional, List

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://ab16948b-54a7-4063-af4a-f88f3c45f9d2.preview.emergentagent.com/api"

class AIJustificationTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.job_requirements_id = None
        self.uploaded_resume_ids = []
        self.screening_results = []
        self.candidate_ids = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_admin_login(self) -> bool:
        """Test admin authentication with Game@1234 password"""
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
            self.log_test("Admin Login with Game@1234", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login with Game@1234", False, f"Exception: {str(e)}")
            return False
    
    def check_existing_data_and_create_test_data(self) -> bool:
        """Check for existing screening data or create test data using the regular upload endpoint"""
        try:
            # First, check if there are existing screening results
            try:
                response = self.session.get(f"{self.base_url}/admin/screening/results", timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success") and result.get("results"):
                        # Use existing data
                        self.screening_results = result["results"]
                        self.candidate_ids = [r.get("candidate_id") for r in self.screening_results if r.get("candidate_id")]
                        if self.candidate_ids:
                            details = f"Found {len(self.candidate_ids)} existing candidates with screening results"
                            self.log_test("Use Existing Screening Data", True, details)
                            return True
            except:
                pass
            
            # If no existing data, create test data using the regular job upload endpoint
            resume_content = """Sarah Johnson
Senior Full Stack Developer
Email: sarah.johnson@email.com
Phone: (555) 123-4567

PROFESSIONAL SUMMARY:
Experienced Full Stack Developer with 6+ years of expertise in Python, JavaScript, React, and FastAPI. 
Proven track record of leading development teams and delivering scalable web applications.

TECHNICAL SKILLS:
- Programming Languages: Python, JavaScript, TypeScript, SQL
- Backend: FastAPI, Django, Flask, Node.js, Express
- Frontend: React, Vue.js, HTML5, CSS3, Bootstrap, Tailwind CSS
- Databases: MongoDB, PostgreSQL, MySQL, Redis
- Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Jenkins
- Tools: Git, Jira, Postman, VS Code

PROFESSIONAL EXPERIENCE:
Senior Full Stack Developer | TechCorp Inc. | 2020 - Present
- Led a team of 5 developers in building microservices architecture using FastAPI and React
- Implemented automated testing and CI/CD pipelines, reducing deployment time by 60%
- Designed and optimized MongoDB databases, improving query performance by 40%
- Mentored junior developers and conducted code reviews

EDUCATION:
Master of Science in Computer Science
Stanford University, 2018

CERTIFICATIONS:
- AWS Certified Solutions Architect
- MongoDB Certified Developer"""
            
            # Use the regular job upload endpoint which accepts TXT files
            files = {
                'resume_file': ('sarah_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Full Stack Developer',
                'job_description': 'We are seeking an experienced Senior Full Stack Developer to join our growing team. The ideal candidate will have strong expertise in Python, JavaScript, React, and FastAPI.',
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
                success = result.get("success", False) and "token" in result
                if success:
                    # Create a mock candidate ID for testing (we'll use the token as candidate ID)
                    test_candidate_id = result["token"][:16]  # Use first 16 chars as candidate ID
                    self.candidate_ids = [test_candidate_id]
                    
                    # Create a mock screening result for testing
                    self.screening_results = [{
                        "candidate_id": test_candidate_id,
                        "candidate_name": "Sarah Johnson",
                        "overall_score": 85.0,
                        "component_scores": {
                            "skills_match": 90.0,
                            "experience_match": 85.0,
                            "education_match": 80.0
                        },
                        "skill_matches": {
                            "Python": 95.0,
                            "JavaScript": 90.0,
                            "React": 88.0,
                            "FastAPI": 92.0
                        },
                        "missing_skills": ["Kubernetes", "GraphQL"],
                        "recommendations": ["Strong technical background", "Leadership experience"],
                        "experience_match": "Senior level with 6+ years experience",
                        "education_match": "Master's degree in Computer Science"
                    }]
            
            details = f"Status: {response.status_code}, Created test data with {len(self.candidate_ids)} candidates"
            if not success:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Create Test Data", success, details)
            return success
            
        except Exception as e:
            self.log_test("Create Test Data", False, f"Exception: {str(e)}")
            return False
    
    def create_job_requirements(self) -> bool:
        """Create job requirements for screening"""
        try:
            payload = {
                "job_title": "Senior Full Stack Developer",
                "job_description": "We are seeking an experienced Senior Full Stack Developer to join our growing team. The ideal candidate will have strong expertise in Python, JavaScript, React, and FastAPI, with experience in cloud technologies and team leadership.",
                "required_skills": [
                    "Python", "JavaScript", "React", "FastAPI", "MongoDB", 
                    "PostgreSQL", "Docker", "AWS", "Git", "Team Leadership"
                ],
                "preferred_skills": [
                    "TypeScript", "Kubernetes", "Redis", "CI/CD", "Microservices",
                    "Django", "Vue.js", "GraphQL", "Jenkins", "Scrum"
                ],
                "experience_level": "senior",
                "education_requirements": {
                    "minimum_degree": "bachelor",
                    "preferred_degree": "master",
                    "relevant_fields": ["Computer Science", "Software Engineering", "Information Technology"]
                },
                "industry_preferences": ["Technology", "Software Development", "Web Development"],
                "scoring_weights": {
                    "skills_match": 0.4,
                    "experience_level": 0.3,
                    "education_fit": 0.2,
                    "career_progression": 0.1
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/screening/job-requirements",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = result.get("success", False)
                if success and "job_requirements_id" in result:
                    self.job_requirements_id = result["job_requirements_id"]
            
            details = f"Status: {response.status_code}, Job Requirements ID: {self.job_requirements_id}"
            self.log_test("Create Job Requirements", success, details)
            return success
            
        except Exception as e:
            self.log_test("Create Job Requirements", False, f"Exception: {str(e)}")
            return False
    
    def screen_candidates(self) -> bool:
        """Screen candidates against job requirements"""
        if not self.job_requirements_id or not self.uploaded_resume_ids:
            self.log_test("Screen Candidates", False, "Missing job requirements or resume IDs")
            return False
        
        try:
            payload = {
                "resume_ids": self.uploaded_resume_ids,
                "job_requirements_id": self.job_requirements_id
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/screening/screen-candidates",
                json=payload,
                timeout=30  # AI processing can take time
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = result.get("success", False)
                if success and "analysis_results" in result:
                    self.screening_results = result["analysis_results"]
                    # Extract candidate IDs for justification testing
                    self.candidate_ids = [r.get("candidate_id") for r in self.screening_results if r.get("candidate_id")]
            
            details = f"Status: {response.status_code}, Screened {len(self.screening_results)} candidates"
            if self.screening_results:
                avg_score = sum(r.get("overall_score", 0) for r in self.screening_results) / len(self.screening_results)
                details += f", Average Score: {avg_score:.1f}"
            
            self.log_test("Screen Candidates", success, details)
            return success
            
        except Exception as e:
            self.log_test("Screen Candidates", False, f"Exception: {str(e)}")
            return False
    
    def test_ai_justification_endpoint(self) -> bool:
        """Test the new AI justification endpoint for each candidate"""
        if not self.candidate_ids:
            self.log_test("AI Justification Endpoint", False, "No candidate IDs available")
            return False
        
        try:
            successful_tests = 0
            total_tests = len(self.candidate_ids)
            
            for i, candidate_id in enumerate(self.candidate_ids):
                print(f"Testing AI Justification for Candidate {i+1}/{total_tests} (ID: {candidate_id[:8]}...)")
                
                response = self.session.get(
                    f"{self.base_url}/admin/screening/candidate-justification/{candidate_id}",
                    timeout=30  # AI generation can take time
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if self.validate_justification_response(result):
                        successful_tests += 1
                        print(f"   ✅ Justification generated successfully")
                        
                        # Print a sample of the justification for verification
                        justification = result.get("detailed_justification", "")
                        if justification:
                            print(f"   Sample: {justification[:150]}...")
                    else:
                        print(f"   ❌ Invalid justification response structure")
                else:
                    print(f"   ❌ Failed with status {response.status_code}: {response.text[:100]}")
                
                print()
            
            success = successful_tests == total_tests
            details = f"Successfully generated justifications for {successful_tests}/{total_tests} candidates"
            self.log_test("AI Justification Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("AI Justification Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def validate_justification_response(self, response: Dict[str, Any]) -> bool:
        """Validate that the justification response contains all required fields"""
        required_fields = [
            "success", "candidate_id", "candidate_name", "overall_score",
            "component_scores", "skill_matches", "missing_skills",
            "recommendations", "detailed_justification"
        ]
        
        # Check all required fields are present
        for field in required_fields:
            if field not in response:
                print(f"   Missing required field: {field}")
                return False
        
        # Validate detailed_justification contains comprehensive analysis
        justification = response.get("detailed_justification", "")
        if not justification or len(justification) < 500:  # Should be comprehensive
            print(f"   Justification too short: {len(justification)} characters")
            return False
        
        # Check for key sections in the justification
        required_sections = [
            "Executive Summary", "Strengths", "Areas for Improvement",
            "Skills Analysis", "Experience Assessment", "Hiring Recommendation"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section.lower() not in justification.lower():
                missing_sections.append(section)
        
        if missing_sections:
            print(f"   Missing sections in justification: {missing_sections}")
            return False
        
        # Validate data types
        if not isinstance(response.get("overall_score"), (int, float)):
            print(f"   Invalid overall_score type: {type(response.get('overall_score'))}")
            return False
        
        if not isinstance(response.get("component_scores"), dict):
            print(f"   Invalid component_scores type: {type(response.get('component_scores'))}")
            return False
        
        if not isinstance(response.get("skill_matches"), dict):
            print(f"   Invalid skill_matches type: {type(response.get('skill_matches'))}")
            return False
        
        if not isinstance(response.get("missing_skills"), list):
            print(f"   Invalid missing_skills type: {type(response.get('missing_skills'))}")
            return False
        
        return True
    
    def test_comprehensive_justification_content(self) -> bool:
        """Test that justifications contain comprehensive analysis"""
        if not self.candidate_ids:
            self.log_test("Comprehensive Justification Content", False, "No candidate IDs available")
            return False
        
        try:
            # Test with the first candidate (should be the strongest based on our sample resumes)
            candidate_id = self.candidate_ids[0]
            
            response = self.session.get(
                f"{self.base_url}/admin/screening/candidate-justification/{candidate_id}",
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test("Comprehensive Justification Content", False, f"API call failed: {response.status_code}")
                return False
            
            result = response.json()
            justification = result.get("detailed_justification", "")
            
            # Analyze the content quality
            content_checks = {
                "Executive Summary": "executive summary" in justification.lower(),
                "Strengths Analysis": "strengths" in justification.lower() and len([s for s in justification.split('.') if 'strength' in s.lower()]) >= 2,
                "Weaknesses/Areas for Improvement": any(term in justification.lower() for term in ["weakness", "areas for improvement", "improvement"]),
                "Skills Analysis": "skills" in justification.lower() and "analysis" in justification.lower(),
                "Experience Assessment": "experience" in justification.lower(),
                "Education Evaluation": "education" in justification.lower(),
                "Hiring Recommendation": any(term in justification.lower() for term in ["hire", "recommend", "strong hire", "consider"]),
                "Risk Assessment": any(term in justification.lower() for term in ["risk", "concern", "red flag"]),
                "Actionable Insights": len(justification.split('.')) >= 15,  # Should be detailed
                "Professional Tone": not any(term in justification.lower() for term in ["bad", "terrible", "awful"])
            }
            
            passed_checks = sum(content_checks.values())
            total_checks = len(content_checks)
            
            success = passed_checks >= total_checks * 0.8  # 80% of checks should pass
            
            details = f"Content quality: {passed_checks}/{total_checks} checks passed"
            details += f"\nJustification length: {len(justification)} characters"
            details += f"\nFailed checks: {[k for k, v in content_checks.items() if not v]}"
            
            self.log_test("Comprehensive Justification Content", success, details)
            return success
            
        except Exception as e:
            self.log_test("Comprehensive Justification Content", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all AI justification tests in sequence"""
        print("=" * 80)
        print("AI JUSTIFICATION FEATURE TESTING")
        print("Testing the new candidate scoring justification endpoint")
        print("=" * 80)
        print()
        
        results = {}
        
        # Step 1: Admin login
        results["admin_login"] = self.test_admin_login()
        if not results["admin_login"]:
            print("❌ Cannot proceed without admin login. Stopping tests.")
            return results
        
        # Step 2: Upload sample resumes
        results["upload_resumes"] = self.upload_sample_resumes()
        if not results["upload_resumes"]:
            print("❌ Cannot proceed without uploaded resumes. Stopping tests.")
            return results
        
        # Step 3: Create job requirements
        results["create_job_requirements"] = self.create_job_requirements()
        if not results["create_job_requirements"]:
            print("❌ Cannot proceed without job requirements. Stopping tests.")
            return results
        
        # Step 4: Screen candidates
        results["screen_candidates"] = self.screen_candidates()
        if not results["screen_candidates"]:
            print("❌ Cannot proceed without screening results. Stopping tests.")
            return results
        
        # Step 5: Test AI justification endpoint
        results["ai_justification_endpoint"] = self.test_ai_justification_endpoint()
        
        # Step 6: Test comprehensive justification content
        results["comprehensive_justification"] = self.test_comprehensive_justification_content()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        test_categories = {
            "Authentication": ["admin_login"],
            "Data Preparation": ["upload_resumes", "create_job_requirements", "screen_candidates"],
            "AI Justification Feature": ["ai_justification_endpoint", "comprehensive_justification"]
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
            print("🎉 ALL TESTS PASSED! AI Justification feature is working correctly.")
            print("✅ The endpoint returns detailed, comprehensive justifications for HR teams.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! AI Justification feature is functional with minor issues.")
        else:
            print("⚠️  Multiple tests failed. The AI Justification feature needs attention.")
        
        return results

def main():
    """Main test execution"""
    tester = AIJustificationTester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())