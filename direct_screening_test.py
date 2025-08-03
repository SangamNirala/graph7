#!/usr/bin/env python3
"""
Direct Resume Screening Functionality Test
Tests the new /admin/screening/upload-and-analyze endpoint
"""

import requests
import json
import io
import tempfile
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://466a16b6-018f-40ef-a6a9-f50ebbf5d383.preview.emergentagent.com/api"

class DirectScreeningTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.job_requirements_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_admin_login(self) -> bool:
        """Test admin authentication first"""
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
            
            details = f"Status: {response.status_code}"
            if success:
                details += ", Admin authenticated successfully"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Admin Authentication", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_get_job_requirements(self) -> bool:
        """Test GET /admin/screening/job-requirements"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/screening/job-requirements",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("success", False)
                job_requirements = data.get("job_requirements", [])
                
                if job_requirements:
                    # Use the first available job requirement
                    self.job_requirements_id = job_requirements[0]["id"]
                    details = f"Status: {response.status_code}, Found {len(job_requirements)} job requirements, Using ID: {self.job_requirements_id[:8]}..."
                else:
                    details = f"Status: {response.status_code}, No job requirements found - will create one"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Get Job Requirements", success, details)
            return success
        except Exception as e:
            self.log_test("Get Job Requirements", False, f"Exception: {str(e)}")
            return False
    
    def test_create_job_requirements(self) -> bool:
        """Test POST /admin/screening/job-requirements to create sample job requirements"""
        try:
            payload = {
                "job_title": "Senior Python Developer",
                "job_description": "We are seeking an experienced Python developer to join our backend team. The ideal candidate will have strong experience with FastAPI, database design, and cloud technologies.",
                "required_skills": ["Python", "FastAPI", "MongoDB", "REST APIs", "Git"],
                "preferred_skills": ["Docker", "AWS", "React", "PostgreSQL", "Kubernetes"],
                "experience_level": "senior",
                "education_requirements": {
                    "minimum_degree": "Bachelor's",
                    "preferred_fields": ["Computer Science", "Software Engineering", "Information Technology"]
                },
                "industry_preferences": ["Technology", "Software Development", "Fintech"],
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
                data = response.json()
                success = data.get("success", False)
                if success:
                    self.job_requirements_id = data.get("job_requirements_id")
                    details = f"Status: {response.status_code}, Created job requirements ID: {self.job_requirements_id[:8]}..."
                else:
                    details = f"Status: {response.status_code}, Failed to create: {data}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            
            self.log_test("Create Job Requirements", success, details)
            return success
        except Exception as e:
            self.log_test("Create Job Requirements", False, f"Exception: {str(e)}")
            return False
    
    def test_upload_and_analyze_endpoint(self) -> bool:
        """Test the main /admin/screening/upload-and-analyze endpoint"""
        if not self.job_requirements_id:
            self.log_test("Upload and Analyze", False, "No job requirements ID available")
            return False
        
        try:
            # Create a sample resume file
            resume_content = """Jane Smith
Senior Software Engineer
Email: jane.smith@techcorp.com
Phone: (555) 987-6543

PROFESSIONAL SUMMARY:
Experienced Python developer with 6+ years of expertise in backend development, 
API design, and cloud technologies. Proven track record of leading development 
teams and delivering scalable solutions.

TECHNICAL SKILLS:
- Programming Languages: Python, JavaScript, TypeScript, SQL
- Frameworks: FastAPI, Django, React, Node.js
- Databases: MongoDB, PostgreSQL, Redis
- Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD
- Tools: Git, Jenkins, Terraform, Monitoring tools

PROFESSIONAL EXPERIENCE:

Senior Software Engineer | TechCorp Inc. | 2020 - Present
- Led backend development team of 5 engineers
- Designed and implemented RESTful APIs using FastAPI serving 1M+ requests/day
- Architected microservices infrastructure on AWS with 99.9% uptime
- Implemented automated testing and CI/CD pipelines reducing deployment time by 60%
- Mentored junior developers and conducted code reviews

Software Engineer | StartupXYZ | 2018 - 2020
- Developed scalable web applications using Python and React
- Designed database schemas and optimized queries for MongoDB
- Integrated third-party APIs and payment systems
- Collaborated with product team to deliver features on tight deadlines

EDUCATION:
Master of Science in Computer Science
Stanford University, 2018

Bachelor of Science in Software Engineering  
UC Berkeley, 2016

CERTIFICATIONS:
- AWS Certified Solutions Architect
- MongoDB Certified Developer
- Certified Kubernetes Administrator

ACHIEVEMENTS:
- Led migration of legacy system to microservices, improving performance by 40%
- Implemented real-time analytics system processing 100K events/second
- Open source contributor with 500+ GitHub stars across projects
"""
            
            # Create file-like object
            files = {
                'files': ('jane_smith_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_requirements_id': self.job_requirements_id,
                'batch_name': 'Testing Direct Screening'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/screening/upload-and-analyze",
                files=files,
                data=data,
                timeout=30  # AI analysis can take time
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = result.get("success", False)
                
                if success:
                    # Validate response structure
                    required_fields = [
                        "batch_id", "processing_summary", "screening_results", 
                        "processed_candidates", "top_candidates"
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in result]
                    if missing_fields:
                        success = False
                        details = f"Missing required fields: {missing_fields}"
                    else:
                        # Validate processing summary
                        processing = result["processing_summary"]
                        screening = result["screening_results"]
                        
                        details = f"""Status: {response.status_code}
   Batch ID: {result['batch_id'][:8]}...
   Processing: {processing['successfully_processed']}/{processing['total_files']} files ({processing['processing_rate']})
   Screening: {screening['candidates_screened']} candidates, avg score: {screening['average_score']}
   High quality matches: {screening['high_quality_matches']}
   Top candidates: {len(result['top_candidates'])}"""
                        
                        # Additional validation
                        if processing['successfully_processed'] == 0:
                            success = False
                            details += "\n   ERROR: No files were successfully processed"
                else:
                    details = f"Status: {response.status_code}, API returned success=false: {result}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:500]}"
            
            self.log_test("Upload and Analyze Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("Upload and Analyze Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_multiple_files_upload(self) -> bool:
        """Test uploading multiple resume files"""
        if not self.job_requirements_id:
            self.log_test("Multiple Files Upload", False, "No job requirements ID available")
            return False
        
        try:
            # Create multiple sample resumes
            resume1 = """John Doe
Python Developer
Email: john.doe@email.com

SKILLS: Python, FastAPI, MongoDB, Docker
EXPERIENCE: 3 years of Python development
EDUCATION: BS Computer Science"""

            resume2 = """Alice Johnson  
Senior Backend Engineer
Email: alice.johnson@company.com

SKILLS: Python, Django, PostgreSQL, AWS, Kubernetes
EXPERIENCE: 5 years backend development, team lead experience
EDUCATION: MS Software Engineering"""

            resume3 = """Bob Wilson
Full Stack Developer  
Email: bob.wilson@startup.com

SKILLS: JavaScript, React, Node.js, Python, MongoDB
EXPERIENCE: 4 years full stack development
EDUCATION: BS Information Technology"""
            
            # Create multiple files
            files = [
                ('files', ('john_doe.txt', io.StringIO(resume1), 'text/plain')),
                ('files', ('alice_johnson.txt', io.StringIO(resume2), 'text/plain')),
                ('files', ('bob_wilson.txt', io.StringIO(resume3), 'text/plain'))
            ]
            
            data = {
                'job_requirements_id': self.job_requirements_id,
                'batch_name': 'Multi-File Test Batch'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/screening/upload-and-analyze",
                files=files,
                data=data,
                timeout=45  # More time for multiple files
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = result.get("success", False)
                
                if success:
                    processing = result["processing_summary"]
                    screening = result["screening_results"]
                    
                    details = f"""Status: {response.status_code}
   Files processed: {processing['successfully_processed']}/{processing['total_files']}
   Processing rate: {processing['processing_rate']}
   Candidates screened: {screening['candidates_screened']}
   Average score: {screening['average_score']}
   Score distribution: {screening['score_distribution']}"""
                    
                    # Validate that multiple candidates were processed
                    if screening['candidates_screened'] < 2:
                        success = False
                        details += f"\n   ERROR: Expected multiple candidates, got {screening['candidates_screened']}"
                else:
                    details = f"Status: {response.status_code}, Failed: {result}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:400]}"
            
            self.log_test("Multiple Files Upload", success, details)
            return success
        except Exception as e:
            self.log_test("Multiple Files Upload", False, f"Exception: {str(e)}")
            return False
    
    def test_invalid_file_handling(self) -> bool:
        """Test handling of invalid file types"""
        if not self.job_requirements_id:
            self.log_test("Invalid File Handling", False, "No job requirements ID available")
            return False
        
        try:
            # Create an invalid file (not PDF/DOC/DOCX/TXT)
            invalid_content = "This is not a valid resume file"
            
            files = {
                'files': ('invalid_file.xyz', io.StringIO(invalid_content), 'application/octet-stream')
            }
            
            data = {
                'job_requirements_id': self.job_requirements_id,
                'batch_name': 'Invalid File Test'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/screening/upload-and-analyze",
                files=files,
                data=data,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = result.get("success", False)
                
                if success:
                    # Should have failed files due to invalid type
                    failed_files = result.get("failed_files", [])
                    processing = result["processing_summary"]
                    
                    if len(failed_files) > 0 and processing['successfully_processed'] == 0:
                        details = f"Status: {response.status_code}, Correctly rejected invalid file: {failed_files[0]['error']}"
                    else:
                        success = False
                        details = f"Status: {response.status_code}, Should have rejected invalid file but didn't"
                else:
                    details = f"Status: {response.status_code}, Failed: {result}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            
            self.log_test("Invalid File Handling", success, details)
            return success
        except Exception as e:
            self.log_test("Invalid File Handling", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all direct screening tests"""
        print("🚀 Starting Direct Resume Screening Functionality Tests")
        print("=" * 60)
        
        tests = [
            ("Admin Authentication", self.test_admin_login),
            ("Get Job Requirements", self.test_get_job_requirements),
        ]
        
        # If no job requirements found, create one
        if not self.job_requirements_id:
            tests.append(("Create Job Requirements", self.test_create_job_requirements))
        
        # Main functionality tests
        tests.extend([
            ("Upload and Analyze Endpoint", self.test_upload_and_analyze_endpoint),
            ("Multiple Files Upload", self.test_multiple_files_upload),
            ("Invalid File Handling", self.test_invalid_file_handling),
        ])
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            if test_func():
                passed += 1
        
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! Direct resume screening functionality is working correctly.")
        else:
            print(f"⚠️  {total - passed} test(s) failed. Please check the implementation.")
        
        return passed == total

if __name__ == "__main__":
    tester = DirectScreeningTester()
    tester.run_all_tests()