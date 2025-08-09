#!/usr/bin/env python3
"""
Placement Preparation Endpoints Testing
Tests the specific new placement preparation endpoints mentioned in the review request:
1. /api/admin/upload endpoint - PDF, TXT, DOCX file upload with parsing and preview
2. /api/admin/create-token endpoint - Token creation with job requirements and resume text
3. Workflow Integration Testing - End-to-end workflow
4. Error Handling - Various error scenarios

This addresses the user's 404 errors for these exact endpoints.
"""

import requests
import json
import time
import io
import tempfile
import os
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://e143a5dd-640d-4366-979e-f44e8b4324a2.preview.emergentagent.com/api"

class PlacementEndpointsTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.uploaded_files = []
        self.created_tokens = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def create_sample_pdf_content(self) -> bytes:
        """Create a simple PDF content for testing"""
        # This is a minimal PDF structure for testing
        pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 120
>>
stream
BT
/F1 12 Tf
72 720 Td
(Sarah Johnson - Senior Software Engineer) Tj
0 -20 Td
(5+ years Python, React, FastAPI experience) Tj
0 -20 Td
(Team leadership and project management skills) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000206 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
350
%%EOF"""
        return pdf_content
    
    def create_sample_txt_content(self) -> str:
        """Create sample TXT resume content"""
        return """Michael Chen
Senior Full Stack Developer
Email: michael.chen@email.com
Phone: (555) 234-5678

PROFESSIONAL SUMMARY:
Experienced full-stack developer with 6+ years of expertise in Python, JavaScript, and modern web technologies. Proven track record in leading development teams and delivering scalable applications.

TECHNICAL SKILLS:
- Programming Languages: Python, JavaScript, TypeScript, Java
- Frameworks: FastAPI, React, Node.js, Django, Express.js
- Databases: MongoDB, PostgreSQL, Redis, MySQL
- Cloud Platforms: AWS, Azure, Google Cloud Platform
- DevOps: Docker, Kubernetes, CI/CD, Jenkins
- Tools: Git, JIRA, Slack, VS Code

PROFESSIONAL EXPERIENCE:

Senior Full Stack Developer | TechCorp Inc. | 2020 - Present
- Led a team of 5 developers in building microservices architecture
- Implemented RESTful APIs using FastAPI and Python
- Developed responsive web applications using React and TypeScript
- Optimized database queries resulting in 40% performance improvement
- Mentored junior developers and conducted code reviews

Full Stack Developer | StartupXYZ | 2018 - 2020
- Built end-to-end web applications using Python and JavaScript
- Integrated third-party APIs and payment gateways
- Implemented automated testing and deployment pipelines
- Collaborated with product managers and designers on feature development

EDUCATION:
Master of Science in Computer Science
University of Technology, 2018

Bachelor of Science in Software Engineering
Tech Institute, 2016

CERTIFICATIONS:
- AWS Certified Solutions Architect
- MongoDB Certified Developer
- Scrum Master Certification

PROJECTS:
- E-commerce Platform: Built scalable platform handling 10k+ daily users
- Real-time Chat Application: Implemented WebSocket-based messaging system
- Data Analytics Dashboard: Created interactive dashboards using React and D3.js"""
    
    def create_sample_docx_content(self) -> bytes:
        """Create sample DOCX content (simplified binary representation)"""
        # This is a simplified representation - in real testing, you'd use python-docx
        # For now, we'll simulate DOCX content
        docx_content = b"PK\x03\x04\x14\x00\x00\x00\x08\x00" + b"DOCX_PLACEHOLDER_CONTENT" * 50
        return docx_content
    
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
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Admin Login Authentication", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login Authentication", False, f"Exception: {str(e)}")
            return False
    
    def test_upload_pdf_file(self) -> bool:
        """Test /api/admin/upload endpoint with PDF file"""
        try:
            pdf_content = self.create_sample_pdf_content()
            
            files = {
                'resume': ('resume.pdf', io.BytesIO(pdf_content), 'application/pdf')
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload",
                files=files,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                expected_fields = ['success', 'preview', 'full_text', 'filename']
                success = all(field in data for field in expected_fields)
                
                if success and data.get('success'):
                    self.uploaded_files.append({
                        'type': 'pdf',
                        'filename': data.get('filename'),
                        'preview': data.get('preview'),
                        'full_text': data.get('full_text')
                    })
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Preview length: {len(data.get('preview', ''))}, Full text length: {len(data.get('full_text', ''))}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("PDF File Upload (/api/admin/upload)", success, details)
            return success
        except Exception as e:
            self.log_test("PDF File Upload (/api/admin/upload)", False, f"Exception: {str(e)}")
            return False
    
    def test_upload_txt_file(self) -> bool:
        """Test /api/admin/upload endpoint with TXT file"""
        try:
            txt_content = self.create_sample_txt_content()
            
            files = {
                'resume': ('resume.txt', io.StringIO(txt_content), 'text/plain')
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload",
                files=files,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                expected_fields = ['success', 'preview', 'full_text', 'filename']
                success = all(field in data for field in expected_fields)
                
                if success and data.get('success'):
                    self.uploaded_files.append({
                        'type': 'txt',
                        'filename': data.get('filename'),
                        'preview': data.get('preview'),
                        'full_text': data.get('full_text')
                    })
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Preview length: {len(data.get('preview', ''))}, Full text length: {len(data.get('full_text', ''))}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("TXT File Upload (/api/admin/upload)", success, details)
            return success
        except Exception as e:
            self.log_test("TXT File Upload (/api/admin/upload)", False, f"Exception: {str(e)}")
            return False
    
    def test_upload_docx_file(self) -> bool:
        """Test /api/admin/upload endpoint with DOCX file"""
        try:
            docx_content = self.create_sample_docx_content()
            
            files = {
                'resume': ('resume.docx', io.BytesIO(docx_content), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload",
                files=files,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                expected_fields = ['success', 'preview', 'full_text', 'filename']
                success = all(field in data for field in expected_fields)
                
                if success and data.get('success'):
                    self.uploaded_files.append({
                        'type': 'docx',
                        'filename': data.get('filename'),
                        'preview': data.get('preview'),
                        'full_text': data.get('full_text')
                    })
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Preview length: {len(data.get('preview', ''))}, Full text length: {len(data.get('full_text', ''))}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("DOCX File Upload (/api/admin/upload)", success, details)
            return success
        except Exception as e:
            self.log_test("DOCX File Upload (/api/admin/upload)", False, f"Exception: {str(e)}")
            return False
    
    def test_upload_invalid_file_type(self) -> bool:
        """Test /api/admin/upload endpoint with invalid file type (should be rejected)"""
        try:
            # Create a fake image file
            invalid_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            
            files = {
                'resume': ('image.png', io.BytesIO(invalid_content), 'image/png')
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload",
                files=files,
                timeout=15
            )
            
            # Should return 400 or similar error for invalid file type
            success = response.status_code in [400, 422, 415]  # Bad Request, Unprocessable Entity, or Unsupported Media Type
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Invalid File Type Rejection (/api/admin/upload)", success, details)
            return success
        except Exception as e:
            self.log_test("Invalid File Type Rejection (/api/admin/upload)", False, f"Exception: {str(e)}")
            return False
    
    def test_create_token_complete_payload(self) -> bool:
        """Test /api/admin/create-token endpoint with complete payload"""
        try:
            # Use text from uploaded file if available
            resume_text = "Default resume text for testing"
            if self.uploaded_files:
                resume_text = self.uploaded_files[0]['full_text']
            
            payload = {
                "job_title": "Senior Full Stack Developer",
                "job_description": "We are seeking an experienced full-stack developer to join our dynamic team. The ideal candidate will have strong expertise in Python, JavaScript, and modern web frameworks. You will be responsible for designing and implementing scalable web applications, collaborating with cross-functional teams, and mentoring junior developers.",
                "job_requirements": "Required: 5+ years of full-stack development experience, proficiency in Python and JavaScript, experience with React and FastAPI, strong database skills (MongoDB/PostgreSQL), cloud platform experience (AWS/Azure), excellent problem-solving abilities. Preferred: Team leadership experience, DevOps knowledge, microservices architecture experience.",
                "resume_text": resume_text,
                "role_archetype": "Software Engineer",
                "interview_focus": "Technical Deep-Dive",
                "include_coding_challenge": True,
                "min_questions": 10,
                "max_questions": 15
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/create-token",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                expected_fields = ['success', 'token', 'job_title', 'token_features']
                success = all(field in data for field in expected_fields)
                
                if success and data.get('success'):
                    self.created_tokens.append({
                        'token': data.get('token'),
                        'job_title': data.get('job_title'),
                        'features': data.get('token_features', {})
                    })
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {data.get('token', '')[:8]}..., Job: {data.get('job_title', '')}"
                if 'token_features' in data:
                    features = data['token_features']
                    details += f", Features: coding_challenge={features.get('coding_challenge')}, archetype={features.get('role_archetype')}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Complete Token Creation (/api/admin/create-token)", success, details)
            return success
        except Exception as e:
            self.log_test("Complete Token Creation (/api/admin/create-token)", False, f"Exception: {str(e)}")
            return False
    
    def test_create_token_missing_fields(self) -> bool:
        """Test /api/admin/create-token endpoint with missing required fields"""
        try:
            # Missing job_requirements and resume_text
            payload = {
                "job_title": "Developer",
                "job_description": "A developer position"
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/create-token",
                json=payload,
                timeout=15
            )
            
            # Should return 400 or 422 for missing required fields
            success = response.status_code in [400, 422]
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Missing Required Fields (/api/admin/create-token)", success, details)
            return success
        except Exception as e:
            self.log_test("Missing Required Fields (/api/admin/create-token)", False, f"Exception: {str(e)}")
            return False
    
    def test_create_token_enhanced_features(self) -> bool:
        """Test /api/admin/create-token endpoint with enhanced features"""
        try:
            payload = {
                "job_title": "Graduate Software Engineer",
                "job_description": "Entry-level position for recent graduates with strong programming fundamentals and eagerness to learn.",
                "job_requirements": "Required: Computer Science degree, programming experience in any language, problem-solving skills, good communication. Preferred: Internship experience, knowledge of web technologies, familiarity with version control.",
                "resume_text": "Recent Computer Science graduate with internship experience in web development. Strong foundation in programming and eager to start career in software development.",
                "role_archetype": "Graduate",
                "interview_focus": "Graduate Screening",
                "include_coding_challenge": False,
                "min_questions": 6,
                "max_questions": 10
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/create-token",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                expected_fields = ['success', 'token', 'job_title', 'token_features']
                success = all(field in data for field in expected_fields)
                
                if success and data.get('success'):
                    token_features = data.get('token_features', {})
                    # Verify enhanced features are stored
                    enhanced_features_present = (
                        token_features.get('role_archetype') == 'Graduate' and
                        token_features.get('interview_focus') == 'Graduate Screening' and
                        token_features.get('enhanced_features') == True
                    )
                    success = enhanced_features_present
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {data.get('token', '')[:8]}..., Enhanced features verified"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Enhanced Features Token (/api/admin/create-token)", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Features Token (/api/admin/create-token)", False, f"Exception: {str(e)}")
            return False
    
    def test_token_storage_verification(self) -> bool:
        """Verify token is generated and stored in enhanced_tokens collection"""
        if not self.created_tokens:
            self.log_test("Token Storage Verification", False, "No tokens created to verify")
            return False
        
        try:
            # Test token validation to verify it's stored
            token = self.created_tokens[0]['token']
            payload = {"token": token}
            
            response = self.session.post(
                f"{self.base_url}/candidate/validate-token",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("valid", False) and "job_title" in data
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token validated successfully, Job: {data.get('job_title', '')}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Token Storage Verification", success, details)
            return success
        except Exception as e:
            self.log_test("Token Storage Verification", False, f"Exception: {str(e)}")
            return False
    
    def test_workflow_integration(self) -> bool:
        """Test complete workflow: Upload document -> Create token -> Verify workflow"""
        try:
            # Step 1: Upload a document
            txt_content = """Alex Rodriguez
Product Manager
Email: alex.rodriguez@email.com

EXPERIENCE:
- 4+ years in product management
- Led cross-functional teams of 8+ members
- Launched 3 major product features
- Strong analytical and communication skills

SKILLS:
- Product strategy and roadmap planning
- User research and data analysis
- Agile/Scrum methodologies
- Stakeholder management"""
            
            files = {
                'resume': ('product_manager_resume.txt', io.StringIO(txt_content), 'text/plain')
            }
            
            upload_response = self.session.post(
                f"{self.base_url}/admin/upload",
                files=files,
                timeout=15
            )
            
            if upload_response.status_code != 200:
                self.log_test("Workflow Integration", False, f"Upload failed: {upload_response.status_code}")
                return False
            
            upload_data = upload_response.json()
            if not upload_data.get('success'):
                self.log_test("Workflow Integration", False, "Upload not successful")
                return False
            
            # Step 2: Use the returned text to create token
            resume_text = upload_data.get('full_text', '')
            
            token_payload = {
                "job_title": "Senior Product Manager",
                "job_description": "We are looking for an experienced product manager to drive product strategy and execution. The role involves working with engineering, design, and business teams to deliver impactful products.",
                "job_requirements": "Required: 3+ years product management experience, strong analytical skills, experience with agile methodologies, excellent communication skills. Preferred: Technical background, B2B product experience, data-driven decision making.",
                "resume_text": resume_text,
                "role_archetype": "Product Manager",
                "interview_focus": "Cultural Fit",
                "include_coding_challenge": False
            }
            
            token_response = self.session.post(
                f"{self.base_url}/admin/create-token",
                json=token_payload,
                timeout=20
            )
            
            if token_response.status_code != 200:
                self.log_test("Workflow Integration", False, f"Token creation failed: {token_response.status_code}")
                return False
            
            token_data = token_response.json()
            if not token_data.get('success'):
                self.log_test("Workflow Integration", False, "Token creation not successful")
                return False
            
            # Step 3: Verify the complete workflow works
            created_token = token_data.get('token')
            job_title = token_data.get('job_title')
            
            success = (
                created_token and 
                job_title == "Senior Product Manager" and
                len(resume_text) > 100  # Ensure resume text was properly extracted
            )
            
            details = f"Upload successful, Token created: {created_token[:8]}..., Job: {job_title}, Resume length: {len(resume_text)}"
            self.log_test("Workflow Integration", success, details)
            return success
            
        except Exception as e:
            self.log_test("Workflow Integration", False, f"Exception: {str(e)}")
            return False
    
    def test_upload_corrupted_file(self) -> bool:
        """Test upload with corrupted/empty files"""
        try:
            # Test with empty file
            files = {
                'resume': ('empty.txt', io.StringIO(''), 'text/plain')
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload",
                files=files,
                timeout=15
            )
            
            # Should handle empty file gracefully (either success with empty content or appropriate error)
            success = response.status_code in [200, 400, 422]
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Corrupted/Empty File Handling", success, details)
            return success
        except Exception as e:
            self.log_test("Corrupted/Empty File Handling", False, f"Exception: {str(e)}")
            return False
    
    def test_invalid_json_payload(self) -> bool:
        """Test token creation with invalid JSON payload"""
        try:
            # Send malformed JSON
            response = self.session.post(
                f"{self.base_url}/admin/create-token",
                data="invalid json data",
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            # Should return 400 or 422 for invalid JSON
            success = response.status_code in [400, 422]
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Invalid JSON Payload Handling", success, details)
            return success
        except Exception as e:
            self.log_test("Invalid JSON Payload Handling", False, f"Exception: {str(e)}")
            return False
    
    def test_proper_error_messages(self) -> bool:
        """Verify proper error messages are returned"""
        try:
            # Test with missing file in upload
            response = self.session.post(
                f"{self.base_url}/admin/upload",
                files={},
                timeout=15
            )
            
            success = response.status_code in [400, 422]
            if success:
                # Check if response contains meaningful error message
                response_text = response.text.lower()
                success = any(keyword in response_text for keyword in ['file', 'required', 'missing', 'error'])
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Proper Error Messages", success, details)
            return success
        except Exception as e:
            self.log_test("Proper Error Messages", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all placement preparation endpoint tests"""
        print("=" * 80)
        print("PLACEMENT PREPARATION ENDPOINTS TESTING")
        print("Testing specific /api/admin/upload and /api/admin/create-token endpoints")
        print("Addressing user's 404 errors for these exact endpoints")
        print("=" * 80)
        print()
        
        results = {}
        
        # Admin authentication first
        results["admin_login"] = self.test_admin_login()
        
        # Test /api/admin/upload endpoint
        results["upload_pdf"] = self.test_upload_pdf_file()
        results["upload_txt"] = self.test_upload_txt_file()
        results["upload_docx"] = self.test_upload_docx_file()
        results["upload_invalid_type"] = self.test_upload_invalid_file_type()
        
        # Test /api/admin/create-token endpoint
        results["create_token_complete"] = self.test_create_token_complete_payload()
        results["create_token_missing_fields"] = self.test_create_token_missing_fields()
        results["create_token_enhanced"] = self.test_create_token_enhanced_features()
        results["token_storage"] = self.test_token_storage_verification()
        
        # Workflow Integration Testing
        results["workflow_integration"] = self.test_workflow_integration()
        
        # Error Handling
        results["corrupted_file"] = self.test_upload_corrupted_file()
        results["invalid_json"] = self.test_invalid_json_payload()
        results["error_messages"] = self.test_proper_error_messages()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by category
        categories = {
            "Authentication": ["admin_login"],
            "/api/admin/upload Endpoint": [
                "upload_pdf", "upload_txt", "upload_docx", "upload_invalid_type"
            ],
            "/api/admin/create-token Endpoint": [
                "create_token_complete", "create_token_missing_fields", 
                "create_token_enhanced", "token_storage"
            ],
            "Workflow Integration": ["workflow_integration"],
            "Error Handling": ["corrupted_file", "invalid_json", "error_messages"]
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
            print("🎉 ALL TESTS PASSED! Placement preparation endpoints are working correctly.")
            print("✅ The user's 404 errors have been resolved - endpoints are accessible.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Most endpoints are functional with minor issues.")
        else:
            print("⚠️  Multiple tests failed. Check the details above.")
        
        return results

def main():
    """Main test execution"""
    tester = PlacementEndpointsTester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())