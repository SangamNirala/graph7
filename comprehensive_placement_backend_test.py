#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Placement Preparation Application
Testing all major backend functionality as requested in the review:
1. Enhanced ATS Score Calculation System
2. Resume Management
3. AI Screening Workflow
4. Interview System
5. Voice Integration
6. Data Management
"""

import requests
import json
import time
import os
import base64
from datetime import datetime
from typing import Dict, List, Any

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://aptiscore-engine.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class ComprehensivePlacementTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_authenticated = False
        self.test_results = []
        self.ats_score_id = None
        self.uploaded_resume_ids = []
        self.job_requirements_id = None
        self.screening_session_id = None
        self.interview_token = None
        self.interview_session_id = None
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "timestamp": timestamp
        }
        self.test_results.append(result)
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()

    # ===== AUTHENTICATION TESTS =====
    
    def test_admin_authentication(self) -> bool:
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

    # ===== ENHANCED ATS SCORE CALCULATION TESTS =====
    
    def test_ats_score_calculation(self) -> bool:
        """Test Enhanced ATS Score Calculation System with Multi-Phase Analysis"""
        try:
            # Prepare comprehensive test resume content
            resume_content = """
            John Smith
            Senior Software Engineer
            Email: john.smith@email.com
            Phone: (555) 123-4567
            
            PROFESSIONAL SUMMARY:
            Experienced Senior Software Engineer with 7+ years of expertise in full-stack development.
            Proven track record of leading development teams and delivering scalable web applications.
            Strong background in Python, JavaScript, React, and cloud technologies.
            
            TECHNICAL SKILLS:
            • Programming Languages: Python, JavaScript, TypeScript, Java
            • Frontend: React, Vue.js, HTML5, CSS3, Bootstrap, Tailwind CSS
            • Backend: FastAPI, Django, Node.js, Express.js
            • Databases: PostgreSQL, MongoDB, Redis
            • Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
            • Tools: Git, Jenkins, JIRA, Agile methodologies
            
            PROFESSIONAL EXPERIENCE:
            Senior Software Engineer | TechCorp Inc. | 2020 - Present
            • Led a team of 5 developers in building microservices architecture
            • Improved application performance by 40% through optimization
            • Implemented CI/CD pipelines reducing deployment time by 60%
            • Mentored junior developers and conducted code reviews
            
            Software Engineer | StartupXYZ | 2018 - 2020
            • Developed full-stack web applications using React and Python
            • Collaborated with product team to define technical requirements
            • Implemented automated testing increasing code coverage to 85%
            
            Junior Developer | DevCompany | 2017 - 2018
            • Built responsive web interfaces using modern JavaScript frameworks
            • Participated in agile development processes
            • Contributed to open-source projects
            
            EDUCATION:
            Bachelor of Science in Computer Science
            University of Technology | 2017
            
            CERTIFICATIONS:
            • AWS Certified Solutions Architect
            • Certified Scrum Master
            
            ACHIEVEMENTS:
            • Led successful migration of legacy system serving 100K+ users
            • Reduced system downtime by 75% through improved monitoring
            • Published 3 technical articles on software architecture
            """
            
            # Prepare form data with file upload
            files = {
                'resume': ('john_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            form_data = {
                'job_title': 'Senior Full Stack Developer',
                'job_description': 'We are seeking a Senior Full Stack Developer to join our dynamic team. The ideal candidate will have extensive experience in both frontend and backend development, with a strong focus on modern web technologies and scalable architecture design.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=form_data)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["ats_score", "ats_id", "analysis_text", "pdf_filename"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("ATS Score Calculation", "FAIL", 
                                f"Missing required fields: {missing_fields}")
                    return False
                
                # Verify score is reasonable
                ats_score = data.get("ats_score", 0)
                if not isinstance(ats_score, (int, float)) or ats_score < 0 or ats_score > 100:
                    self.log_test("ATS Score Calculation", "FAIL", 
                                f"Invalid ATS score: {ats_score}")
                    return False
                
                # Verify analysis text is comprehensive
                analysis_text = data.get("analysis_text", "")
                if len(analysis_text) < 1000:  # Should be comprehensive
                    self.log_test("ATS Score Calculation", "FAIL", 
                                f"Analysis text too short: {len(analysis_text)} characters")
                    return False
                
                # Store ATS ID for PDF download test
                self.ats_score_id = data.get("ats_id")
                
                self.log_test("ATS Score Calculation", "PASS", 
                            f"ATS Score: {ats_score}/100, Analysis: {len(analysis_text)} chars, ID: {self.ats_score_id}")
                return True
            else:
                self.log_test("ATS Score Calculation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("ATS Score Calculation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_ats_pdf_generation(self) -> bool:
        """Test ATS Score PDF Generation and Download"""
        try:
            if not self.ats_score_id:
                self.log_test("ATS PDF Generation", "FAIL", 
                            "No ATS score ID available for PDF download")
                return False
            
            response = self.session.get(f"{BASE_URL}/placement-preparation/ats-score/{self.ats_score_id}/download")
            
            if response.status_code == 200:
                # Verify PDF content
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' not in content_type:
                    self.log_test("ATS PDF Generation", "FAIL", 
                                f"Invalid content type: {content_type}")
                    return False
                
                # Verify PDF size is reasonable
                pdf_size = len(response.content)
                if pdf_size < 1000:  # Should be substantial
                    self.log_test("ATS PDF Generation", "FAIL", 
                                f"PDF too small: {pdf_size} bytes")
                    return False
                
                self.log_test("ATS PDF Generation", "PASS", 
                            f"PDF downloaded successfully: {pdf_size} bytes")
                return True
            else:
                self.log_test("ATS PDF Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("ATS PDF Generation", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== RESUME MANAGEMENT TESTS =====
    
    def test_resume_upload(self) -> bool:
        """Test Resume Upload with Multi-Format Support"""
        try:
            # Test TXT format
            resume_content = """
            Jane Doe
            Data Scientist
            Email: jane.doe@email.com
            
            EXPERIENCE:
            • 5+ years in data science and machine learning
            • Expert in Python, R, SQL, and statistical analysis
            • Experience with TensorFlow, PyTorch, and scikit-learn
            • Led data science projects for Fortune 500 companies
            
            EDUCATION:
            • PhD in Statistics, Stanford University
            • MS in Computer Science, MIT
            
            SKILLS:
            Python, R, SQL, Machine Learning, Deep Learning, Statistics, Data Visualization
            """
            
            files = {
                'resume': ('jane_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            response = self.session.post(f"{BASE_URL}/admin/upload", files=files)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["success", "preview", "full_text", "filename", "message"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Resume Upload", "FAIL", 
                                f"Missing required fields: {missing_fields}")
                    return False
                
                # Verify content preservation
                full_text = data.get("full_text", "")
                preview = data.get("preview", "")
                
                if len(full_text) < 100:
                    self.log_test("Resume Upload", "FAIL", 
                                f"Full text too short: {len(full_text)} characters")
                    return False
                
                if len(preview) < 50:
                    self.log_test("Resume Upload", "FAIL", 
                                f"Preview too short: {len(preview)} characters")
                    return False
                
                self.log_test("Resume Upload", "PASS", 
                            f"Resume uploaded: {len(full_text)} chars full text, {len(preview)} chars preview")
                return True
            else:
                self.log_test("Resume Upload", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Resume Upload", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== AI SCREENING WORKFLOW TESTS =====
    
    def test_bulk_resume_upload(self) -> bool:
        """Test Bulk Resume Upload for AI Screening"""
        try:
            # Create multiple test resumes
            resumes = [
                {
                    'filename': 'candidate1.txt',
                    'content': """
                    Alice Johnson
                    Software Engineer
                    
                    EXPERIENCE:
                    • 3+ years Python development
                    • React and JavaScript expertise
                    • AWS cloud experience
                    
                    SKILLS: Python, React, JavaScript, AWS, Docker
                    """
                },
                {
                    'filename': 'candidate2.txt', 
                    'content': """
                    Bob Wilson
                    Senior Developer
                    
                    EXPERIENCE:
                    • 6+ years full-stack development
                    • Team leadership experience
                    • Microservices architecture
                    
                    SKILLS: Java, Spring Boot, Angular, PostgreSQL, Kubernetes
                    """
                }
            ]
            
            # Upload resumes
            files = []
            for resume in resumes:
                files.append(('resume_files', (resume['filename'], resume['content'].encode(), 'text/plain')))
            
            data = {'batch_name': 'Test Batch for AI Screening'}
            
            response = self.session.post(f"{BASE_URL}/admin/bulk-upload", 
                                       files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("success"):
                    batch_id = result.get("batch_id")
                    uploaded_count = result.get("uploaded_count", 0)
                    
                    if uploaded_count != len(resumes):
                        self.log_test("Bulk Resume Upload", "FAIL", 
                                    f"Expected {len(resumes)} uploads, got {uploaded_count}")
                        return False
                    
                    self.log_test("Bulk Resume Upload", "PASS", 
                                f"Uploaded {uploaded_count} resumes, batch ID: {batch_id}")
                    return True
                else:
                    self.log_test("Bulk Resume Upload", "FAIL", 
                                f"Upload failed: {result.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Bulk Resume Upload", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Bulk Resume Upload", "FAIL", f"Exception: {str(e)}")
            return False

    def test_job_requirements_setup(self) -> bool:
        """Test Job Requirements Setup for AI Screening"""
        try:
            job_requirements = {
                "job_title": "Senior Full Stack Developer",
                "job_description": "We are looking for a senior full stack developer with expertise in modern web technologies.",
                "required_skills": ["Python", "JavaScript", "React", "FastAPI", "MongoDB"],
                "preferred_skills": ["AWS", "Docker", "Kubernetes", "TypeScript"],
                "experience_level": "senior",
                "education_requirements": {
                    "minimum_degree": "Bachelor's",
                    "preferred_fields": ["Computer Science", "Software Engineering"]
                },
                "industry_preferences": ["Technology", "Software Development"]
            }
            
            response = self.session.post(f"{BASE_URL}/admin/job-requirements", 
                                       json=job_requirements)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    self.job_requirements_id = data.get("job_requirements_id")
                    
                    self.log_test("Job Requirements Setup", "PASS", 
                                f"Job requirements created: {self.job_requirements_id}")
                    return True
                else:
                    self.log_test("Job Requirements Setup", "FAIL", 
                                f"Setup failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Job Requirements Setup", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Job Requirements Setup", "FAIL", f"Exception: {str(e)}")
            return False

    def test_candidate_screening(self) -> bool:
        """Test AI-Powered Candidate Screening"""
        try:
            if not self.job_requirements_id:
                self.log_test("Candidate Screening", "FAIL", 
                            "No job requirements ID available")
                return False
            
            screening_request = {
                "job_requirements_id": self.job_requirements_id,
                "candidate_ids": None  # Screen all candidates
            }
            
            response = self.session.post(f"{BASE_URL}/admin/bulk-screening", 
                                       json=screening_request)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    self.screening_session_id = data.get("screening_session_id")
                    candidates_screened = data.get("candidates_screened", 0)
                    
                    self.log_test("Candidate Screening", "PASS", 
                                f"Screened {candidates_screened} candidates, session: {self.screening_session_id}")
                    return True
                else:
                    self.log_test("Candidate Screening", "FAIL", 
                                f"Screening failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Candidate Screening", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Candidate Screening", "FAIL", f"Exception: {str(e)}")
            return False

    def test_screening_results(self) -> bool:
        """Test Screening Results Retrieval"""
        try:
            response = self.session.get(f"{BASE_URL}/admin/candidates")
            
            if response.status_code == 200:
                data = response.json()
                
                candidates = data.get("candidates", [])
                total_count = data.get("total_count", 0)
                
                if total_count == 0:
                    self.log_test("Screening Results", "FAIL", 
                                "No candidates found in results")
                    return False
                
                # Verify candidate data structure
                if candidates:
                    candidate = candidates[0]
                    required_fields = ["id", "name", "filename", "status", "score"]
                    missing_fields = [field for field in required_fields if field not in candidate]
                    
                    if missing_fields:
                        self.log_test("Screening Results", "FAIL", 
                                    f"Missing candidate fields: {missing_fields}")
                        return False
                
                self.log_test("Screening Results", "PASS", 
                            f"Retrieved {total_count} candidates with screening results")
                return True
            else:
                self.log_test("Screening Results", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Screening Results", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== INTERVIEW SYSTEM TESTS =====
    
    def test_interview_token_generation(self) -> bool:
        """Test Interview Token Generation"""
        try:
            token_request = {
                "job_title": "Senior Software Engineer",
                "job_description": "We are looking for a senior software engineer with strong technical skills.",
                "job_requirements": "5+ years experience, Python, JavaScript, system design",
                "resume_text": """
                Test Candidate
                Senior Software Engineer
                
                EXPERIENCE:
                • 5+ years software development
                • Python and JavaScript expertise
                • System design experience
                
                SKILLS: Python, JavaScript, React, FastAPI, System Design
                """,
                "role_archetype": "Software Engineer",
                "interview_focus": "Technical Deep-Dive",
                "include_coding_challenge": False,
                "min_questions": 6,
                "max_questions": 10
            }
            
            response = self.session.post(f"{BASE_URL}/admin/create-token", 
                                       json=token_request)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success") and data.get("token"):
                    self.interview_token = data["token"]
                    
                    self.log_test("Interview Token Generation", "PASS", 
                                f"Token generated: {self.interview_token[:8]}...")
                    return True
                else:
                    self.log_test("Interview Token Generation", "FAIL", 
                                f"Token generation failed: {data}")
                    return False
            else:
                self.log_test("Interview Token Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Interview Token Generation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_interview_session_start(self) -> bool:
        """Test Interview Session Start"""
        try:
            if not self.interview_token:
                self.log_test("Interview Session Start", "FAIL", 
                            "No interview token available")
                return False
            
            start_request = {
                "token": self.interview_token,
                "candidate_name": "Test Candidate",
                "voice_mode": False
            }
            
            response = self.session.post(f"{BASE_URL}/candidate/start-interview", 
                                       json=start_request)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for session_id and either question or first_question
                session_id = data.get("session_id")
                question = data.get("question") or data.get("first_question")
                
                if session_id and question:
                    self.interview_session_id = session_id
                    
                    self.log_test("Interview Session Start", "PASS", 
                                f"Session started: {self.interview_session_id}, First question: {question[:50]}...")
                    return True
                else:
                    self.log_test("Interview Session Start", "FAIL", 
                                f"Session start failed: missing session_id or question in response: {data}")
                    return False
            else:
                self.log_test("Interview Session Start", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Interview Session Start", "FAIL", f"Exception: {str(e)}")
            return False

    def test_interview_conversation(self) -> bool:
        """Test Interview Conversation Flow"""
        try:
            if not self.interview_token:
                self.log_test("Interview Conversation", "FAIL", 
                            "No interview token available")
                return False
            
            # Send a few answers to test conversation flow
            sample_answers = [
                "I have 5+ years of experience in software development, primarily working with Python and JavaScript.",
                "I approach problem-solving by breaking down complex issues into smaller components and using systematic debugging.",
                "I stay updated with technology through tech blogs, conferences, and hands-on experimentation with new tools."
            ]
            
            for i, answer in enumerate(sample_answers):
                response = self.session.post(f"{BASE_URL}/candidate/send-message", 
                                           json={
                                               "token": self.interview_token,
                                               "message": answer
                                           })
                
                if response.status_code != 200:
                    self.log_test("Interview Conversation", "FAIL", 
                                f"Failed to send answer {i+1}: {response.status_code}")
                    return False
                
                data = response.json()
                
                # Check if we got a next question or completion
                if data.get("interview_complete"):
                    self.log_test("Interview Conversation", "PASS", 
                                f"Interview completed after {i+1} answers")
                    return True
                elif not data.get("question"):
                    self.log_test("Interview Conversation", "FAIL", 
                                f"No next question received after answer {i+1}")
                    return False
                
                # Small delay between answers
                time.sleep(0.5)
            
            self.log_test("Interview Conversation", "PASS", 
                        f"Successfully exchanged {len(sample_answers)} Q&A pairs")
            return True
                
        except Exception as e:
            self.log_test("Interview Conversation", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== VOICE INTEGRATION TESTS =====
    
    def test_voice_interview_support(self) -> bool:
        """Test Voice Interview Support (TTS Integration)"""
        try:
            # Test TTS endpoint
            tts_request = {
                "text": "Hello, welcome to your voice interview. Please introduce yourself.",
                "voice_config": {
                    "language_code": "en-US",
                    "name": "en-US-Wavenet-F",
                    "ssml_gender": "FEMALE"
                }
            }
            
            response = self.session.post(f"{BASE_URL}/voice/generate-speech", 
                                       json=tts_request)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success") and data.get("audio_base64"):
                    audio_data = data["audio_base64"]
                    file_id = data.get("file_id")
                    
                    # Verify audio data is valid base64
                    try:
                        base64.b64decode(audio_data)
                        audio_valid = True
                    except:
                        audio_valid = False
                    
                    if not audio_valid:
                        self.log_test("Voice Interview Support", "FAIL", 
                                    "Invalid base64 audio data")
                        return False
                    
                    self.log_test("Voice Interview Support", "PASS", 
                                f"TTS generated audio: {len(audio_data)} chars base64, file ID: {file_id}")
                    return True
                else:
                    self.log_test("Voice Interview Support", "FAIL", 
                                f"TTS generation failed: {data}")
                    return False
            else:
                self.log_test("Voice Interview Support", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Voice Interview Support", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== DATA MANAGEMENT TESTS =====
    
    def test_data_privacy_compliance(self) -> bool:
        """Test Data Privacy and GDPR Compliance Features"""
        try:
            # Test data retention status
            response = self.session.get(f"{BASE_URL}/admin/data-privacy/status")
            
            if response.status_code == 200:
                data = response.json()
                
                required_fields = ["current_time", "retention_policies", "data_counts"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Data Privacy Compliance", "FAIL", 
                                f"Missing required fields: {missing_fields}")
                    return False
                
                retention_policies = data.get("retention_policies", {})
                data_counts = data.get("data_counts", {})
                
                self.log_test("Data Privacy Compliance", "PASS", 
                            f"Data retention policies: {retention_policies}, Current counts: {len(data_counts)} categories")
                return True
            else:
                self.log_test("Data Privacy Compliance", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Data Privacy Compliance", "FAIL", f"Exception: {str(e)}")
            return False

    def test_mongodb_operations(self) -> bool:
        """Test MongoDB Data Operations"""
        try:
            # Test by checking if we can retrieve some data (candidates list)
            response = self.session.get(f"{BASE_URL}/admin/candidates?page=1&page_size=5")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                if "candidates" in data and "total_count" in data:
                    total_count = data.get("total_count", 0)
                    candidates = data.get("candidates", [])
                    
                    self.log_test("MongoDB Operations", "PASS", 
                                f"Successfully retrieved {len(candidates)} candidates from {total_count} total")
                    return True
                else:
                    self.log_test("MongoDB Operations", "FAIL", 
                                "Invalid response structure from candidates endpoint")
                    return False
            else:
                self.log_test("MongoDB Operations", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("MongoDB Operations", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== MAIN TEST EXECUTION =====
    
    def run_comprehensive_test(self) -> bool:
        """Run all comprehensive backend tests"""
        print("=" * 100)
        print("COMPREHENSIVE PLACEMENT PREPARATION BACKEND TESTING")
        print("=" * 100)
        print()
        
        test_methods = [
            # Authentication
            ("Admin Authentication", self.test_admin_authentication),
            
            # Enhanced ATS Score Calculation System
            ("ATS Score Calculation", self.test_ats_score_calculation),
            ("ATS PDF Generation", self.test_ats_pdf_generation),
            
            # Resume Management
            ("Resume Upload", self.test_resume_upload),
            
            # AI Screening Workflow
            ("Bulk Resume Upload", self.test_bulk_resume_upload),
            ("Job Requirements Setup", self.test_job_requirements_setup),
            ("Candidate Screening", self.test_candidate_screening),
            ("Screening Results", self.test_screening_results),
            
            # Interview System
            ("Interview Token Generation", self.test_interview_token_generation),
            ("Interview Session Start", self.test_interview_session_start),
            ("Interview Conversation", self.test_interview_conversation),
            
            # Voice Integration
            ("Voice Interview Support", self.test_voice_interview_support),
            
            # Data Management
            ("Data Privacy Compliance", self.test_data_privacy_compliance),
            ("MongoDB Operations", self.test_mongodb_operations),
        ]
        
        results = []
        
        for test_name, test_method in test_methods:
            try:
                result = test_method()
                results.append(result)
                
                # Stop if admin authentication fails
                if test_name == "Admin Authentication" and not result:
                    print("❌ Cannot proceed without admin authentication")
                    break
                    
            except Exception as e:
                self.log_test(test_name, "FAIL", f"Unexpected exception: {str(e)}")
                results.append(False)
        
        # Summary
        print("=" * 100)
        print("COMPREHENSIVE TEST SUMMARY")
        print("=" * 100)
        
        passed_tests = sum(results)
        total_tests = len(results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Detailed results by category
        categories = {
            "Authentication": results[0:1],
            "ATS Score System": results[1:3],
            "Resume Management": results[3:4],
            "AI Screening": results[4:8],
            "Interview System": results[8:11],
            "Voice Integration": results[11:12],
            "Data Management": results[12:14]
        }
        
        print("\n📋 Results by Category:")
        for category, category_results in categories.items():
            if category_results:
                passed = sum(category_results)
                total = len(category_results)
                status = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
                print(f"  {status} {category}: {passed}/{total}")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Placement Preparation backend is fully functional.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = ComprehensivePlacementTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ COMPREHENSIVE BACKEND TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ COMPREHENSIVE BACKEND TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()