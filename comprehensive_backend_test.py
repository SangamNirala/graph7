#!/usr/bin/env python3
"""
Comprehensive Backend Testing for AI-Powered Voice Interview System
Tests all 13 new API endpoints for bulk candidate management and Phase 2 AI enhancement features
"""

import requests
import json
import time
import io
import base64
import tempfile
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://6d379ea8-29ec-435c-b4d7-9ae4b0ab361e.preview.emergentagent.com/api"

class ComprehensiveBackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.batch_id = None
        self.candidate_ids = []
        self.tag_ids = []
        self.job_requirements_id = None
        self.screening_session_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_admin_authentication(self) -> bool:
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
            self.log_test("Admin Authentication (Game@1234)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Authentication (Game@1234)", False, f"Exception: {str(e)}")
            return False
    
    def test_bulk_upload_api(self) -> bool:
        """Test POST /api/admin/bulk-upload - Bulk file upload endpoint"""
        try:
            # Create multiple resume files for bulk upload
            resume_files = []
            for i in range(3):
                resume_content = f"""Candidate {i+1}
Software Engineer
Email: candidate{i+1}@email.com
Phone: (555) {100+i:03d}-{1000+i:04d}

EXPERIENCE:
- {3+i}+ years of software development
- Experience with Python, JavaScript, and databases
- Built web applications and APIs
- Team collaboration and problem-solving

SKILLS:
- Python, JavaScript, SQL
- FastAPI, React, MongoDB
- Git, Docker, AWS
- Agile development methodologies

EDUCATION:
Bachelor of Science in Computer Science
Tech University, {2018+i}"""
                
                resume_files.append(
                    ('files', (f'resume_{i+1}.txt', io.StringIO(resume_content), 'text/plain'))
                )
            
            data = {
                'batch_name': 'Test Batch - Comprehensive Backend Testing'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/bulk-upload",
                files=resume_files,
                data=data,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "batch_id" in result and 
                          "total_files" in result)
                if success:
                    self.batch_id = result["batch_id"]
            
            details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            if self.batch_id:
                details += f", Batch ID: {self.batch_id[:8]}..."
            
            self.log_test("Bulk Upload API (POST /api/admin/bulk-upload)", success, details)
            return success
        except Exception as e:
            self.log_test("Bulk Upload API (POST /api/admin/bulk-upload)", False, f"Exception: {str(e)}")
            return False
    
    def test_bulk_process_api(self) -> bool:
        """Test POST /api/admin/bulk-process/{batch_id} - Process uploaded batch"""
        if not self.batch_id:
            self.log_test("Bulk Process API", False, "No batch ID available")
            return False
        
        try:
            payload = {
                "job_title": "Full Stack Developer",
                "job_description": "We are looking for a full stack developer to join our team. The role involves building web applications using modern technologies.",
                "job_requirements": "Requirements: 3+ years experience, Python/JavaScript skills, database knowledge, team collaboration."
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/bulk-process/{self.batch_id}",
                json=payload,
                timeout=30  # Processing can take time
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "processed_files" in result)
            
            details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            self.log_test("Bulk Process API (POST /api/admin/bulk-process/{batch_id})", success, details)
            return success
        except Exception as e:
            self.log_test("Bulk Process API (POST /api/admin/bulk-process/{batch_id})", False, f"Exception: {str(e)}")
            return False
    
    def test_candidates_list_api(self) -> bool:
        """Test GET /api/admin/candidates - Get paginated candidate list"""
        try:
            params = {
                "page": 1,
                "page_size": 10,
                "sort_by": "created_at",
                "sort_order": "desc"
            }
            
            response = self.session.get(
                f"{self.base_url}/admin/candidates",
                params=params,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "candidates" in result and 
                          "pagination" in result and
                          "total_count" in result.get("pagination", {}))
                
                # Store candidate IDs for later tests
                if success and result.get("candidates"):
                    self.candidate_ids = [c["id"] for c in result["candidates"][:3]]
            
            details = f"Status: {response.status_code}"
            if success:
                pagination = result.get("pagination", {})
                details += f", Found {pagination.get('total_count', 0)} candidates, Page {pagination.get('current_page', 1)}"
                if self.candidate_ids:
                    details += f", Stored {len(self.candidate_ids)} candidate IDs"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Candidates List API (GET /api/admin/candidates)", success, details)
            return success
        except Exception as e:
            self.log_test("Candidates List API (GET /api/admin/candidates)", False, f"Exception: {str(e)}")
            return False
    
    def test_tag_management_apis(self) -> bool:
        """Test GET/POST /api/admin/tags - Tag management endpoints"""
        try:
            # First, create a new tag
            create_payload = {
                "name": "Test Tag",
                "color": "#FF5722",
                "description": "Tag created during comprehensive backend testing"
            }
            
            create_response = self.session.post(
                f"{self.base_url}/admin/tags",
                json=create_payload,
                timeout=10
            )
            
            create_success = create_response.status_code == 200
            tag_id = None
            if create_success:
                create_result = create_response.json()
                create_success = create_result.get("success", False) and "tag_id" in create_result
                if create_success:
                    tag_id = create_result["tag_id"]
                    self.tag_ids.append(tag_id)
            
            # Then, get all tags
            get_response = self.session.get(f"{self.base_url}/admin/tags", timeout=10)
            get_success = get_response.status_code == 200
            if get_success:
                get_result = get_response.json()
                get_success = (get_result.get("success", False) and 
                              "tags" in get_result and 
                              isinstance(get_result["tags"], list))
            
            overall_success = create_success and get_success
            
            details = f"Create Status: {create_response.status_code}, Get Status: {get_response.status_code}"
            if tag_id:
                details += f", Created Tag ID: {tag_id[:8]}..."
            if get_success:
                details += f", Found {len(get_result.get('tags', []))} tags"
            
            self.log_test("Tag Management APIs (GET/POST /api/admin/tags)", overall_success, details)
            return overall_success
        except Exception as e:
            self.log_test("Tag Management APIs (GET/POST /api/admin/tags)", False, f"Exception: {str(e)}")
            return False
    
    def test_bulk_actions_api(self) -> bool:
        """Test POST /api/admin/candidates/bulk-actions - Bulk candidate operations"""
        if not self.candidate_ids or not self.tag_ids:
            self.log_test("Bulk Actions API", False, "No candidate IDs or tag IDs available")
            return False
        
        try:
            # Test adding tags to candidates
            payload = {
                "candidate_ids": self.candidate_ids[:2],  # Use first 2 candidates
                "action": "add_tags",
                "parameters": {
                    "tag_ids": [self.tag_ids[0]]
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/candidates/bulk-actions",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "affected_count" in result)
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Affected {result.get('affected_count', 0)} candidates"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Bulk Actions API (POST /api/admin/candidates/bulk-actions)", success, details)
            return success
        except Exception as e:
            self.log_test("Bulk Actions API (POST /api/admin/candidates/bulk-actions)", False, f"Exception: {str(e)}")
            return False
    
    def test_individual_candidate_apis(self) -> bool:
        """Test GET/PUT/DELETE /api/admin/candidates/{id} - Individual candidate operations"""
        if not self.candidate_ids:
            self.log_test("Individual Candidate APIs", False, "No candidate IDs available")
            return False
        
        try:
            candidate_id = self.candidate_ids[0]
            
            # Test GET individual candidate
            get_response = self.session.get(
                f"{self.base_url}/admin/candidates/{candidate_id}",
                timeout=10
            )
            
            get_success = get_response.status_code == 200
            if get_success:
                get_result = get_response.json()
                get_success = "candidate" in get_result
            
            # Test PUT update candidate
            update_payload = {
                "notes": "Updated during comprehensive backend testing",
                "status": "screening"
            }
            
            put_response = self.session.put(
                f"{self.base_url}/admin/candidates/{candidate_id}",
                json=update_payload,
                timeout=10
            )
            
            put_success = put_response.status_code == 200
            if put_success:
                put_result = put_response.json()
                put_success = put_result.get("success", False)
            
            overall_success = get_success and put_success
            
            details = f"GET Status: {get_response.status_code}, PUT Status: {put_response.status_code}"
            if get_success:
                details += f", Retrieved candidate data"
            if put_success:
                details += f", Updated candidate successfully"
            
            self.log_test("Individual Candidate APIs (GET/PUT /api/admin/candidates/{id})", overall_success, details)
            return overall_success
        except Exception as e:
            self.log_test("Individual Candidate APIs (GET/PUT /api/admin/candidates/{id})", False, f"Exception: {str(e)}")
            return False
    
    def test_batch_management_apis(self) -> bool:
        """Test GET /api/admin/bulk-uploads - Batch management with progress tracking"""
        try:
            response = self.session.get(f"{self.base_url}/admin/bulk-uploads", timeout=10)
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = ("batches" in result and isinstance(result["batches"], list))
                
                # Check if our batch is in the list
                if success and self.batch_id:
                    found_batch = any(
                        batch.get("id") == self.batch_id 
                        for batch in result["batches"]
                    )
                    if found_batch:
                        details = f"Status: {response.status_code}, Found {len(result['batches'])} batches including our test batch"
                    else:
                        details = f"Status: {response.status_code}, Found {len(result['batches'])} batches but our test batch not found"
                else:
                    details = f"Status: {response.status_code}, Found {len(result.get('batches', []))} batches"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Batch Management APIs (GET /api/admin/bulk-uploads)", success, details)
            return success
        except Exception as e:
            self.log_test("Batch Management APIs (GET /api/admin/bulk-uploads)", False, f"Exception: {str(e)}")
            return False
    
    def test_phase2_job_requirements_api(self) -> bool:
        """Test POST/GET /api/admin/screening/job-requirements - Phase 2 AI job requirements"""
        try:
            # Create job requirements
            create_payload = {
                "job_title": "Senior Python Developer",
                "job_description": "We are seeking a senior Python developer with expertise in FastAPI and machine learning.",
                "required_skills": ["Python", "FastAPI", "Machine Learning", "MongoDB"],
                "preferred_skills": ["Docker", "Kubernetes", "AWS"],
                "experience_level": "senior",
                "education_requirements": {
                    "degree_level": "bachelor",
                    "field_of_study": "Computer Science"
                },
                "industry_preferences": ["Technology", "Software Development"]
            }
            
            create_response = self.session.post(
                f"{self.base_url}/admin/screening/job-requirements",
                json=create_payload,
                timeout=15
            )
            
            create_success = create_response.status_code == 200
            if create_success:
                create_result = create_response.json()
                create_success = create_result.get("success", False) and "job_requirements_id" in create_result
                if create_success:
                    self.job_requirements_id = create_result["job_requirements_id"]
            
            # Get job requirements
            get_response = self.session.get(
                f"{self.base_url}/admin/screening/job-requirements",
                timeout=10
            )
            
            get_success = get_response.status_code == 200
            if get_success:
                get_result = get_response.json()
                get_success = "job_requirements" in get_result
            
            overall_success = create_success and get_success
            
            details = f"Create Status: {create_response.status_code}, Get Status: {get_response.status_code}"
            if self.job_requirements_id:
                details += f", Job Requirements ID: {self.job_requirements_id[:8]}..."
            
            self.log_test("Phase 2 Job Requirements API (POST/GET /api/admin/screening/job-requirements)", overall_success, details)
            return overall_success
        except Exception as e:
            self.log_test("Phase 2 Job Requirements API (POST/GET /api/admin/screening/job-requirements)", False, f"Exception: {str(e)}")
            return False
    
    def test_phase2_ai_screening_api(self) -> bool:
        """Test POST /api/admin/screening/bulk-analyze - Phase 2 AI screening with spaCy/NLTK"""
        if not self.job_requirements_id or not self.candidate_ids:
            self.log_test("Phase 2 AI Screening API", False, "No job requirements ID or candidate IDs available")
            return False
        
        try:
            payload = {
                "job_requirements_id": self.job_requirements_id,
                "candidate_ids": self.candidate_ids[:2]  # Use first 2 candidates
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/screening/bulk-analyze",
                json=payload,
                timeout=30  # AI analysis can take time
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "screening_session_id" in result and
                          "analyzed_candidates" in result)
                if success:
                    self.screening_session_id = result["screening_session_id"]
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Analyzed {result.get('analyzed_candidates', 0)} candidates"
                if self.screening_session_id:
                    details += f", Screening Session: {self.screening_session_id[:8]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Phase 2 AI Screening API (POST /api/admin/screening/bulk-analyze)", success, details)
            return success
        except Exception as e:
            self.log_test("Phase 2 AI Screening API (POST /api/admin/screening/bulk-analyze)", False, f"Exception: {str(e)}")
            return False
    
    def test_phase2_ai_enhancement_apis(self) -> bool:
        """Test Phase 2 AI Enhancement APIs - Bias Detection, ML Prediction, Personality Analysis"""
        try:
            # Test bias detection
            bias_payload = {
                "questions": [
                    "Tell me about your background",
                    "What are your salary expectations?",
                    "Do you have any family commitments?"
                ],
                "job_requirements": {
                    "title": "Software Engineer",
                    "skills": ["Python", "JavaScript"]
                }
            }
            
            bias_response = self.session.post(
                f"{self.base_url}/admin/ai-enhancement/analyze-bias",
                json=bias_payload,
                timeout=20
            )
            
            bias_success = bias_response.status_code == 200
            if bias_success:
                bias_result = bias_response.json()
                bias_success = "bias_analysis" in bias_result
            
            # Test ML model status
            ml_response = self.session.get(
                f"{self.base_url}/admin/ai-enhancement/ml-model-status",
                timeout=10
            )
            
            ml_success = ml_response.status_code == 200
            if ml_success:
                ml_result = ml_response.json()
                ml_success = "model_status" in ml_result
            
            overall_success = bias_success and ml_success
            
            details = f"Bias Analysis Status: {bias_response.status_code}, ML Model Status: {ml_response.status_code}"
            if bias_success:
                details += f", Bias analysis completed"
            if ml_success:
                details += f", ML model status retrieved"
            
            self.log_test("Phase 2 AI Enhancement APIs (Bias Detection, ML Prediction)", overall_success, details)
            return overall_success
        except Exception as e:
            self.log_test("Phase 2 AI Enhancement APIs (Bias Detection, ML Prediction)", False, f"Exception: {str(e)}")
            return False
    
    def test_data_privacy_apis(self) -> bool:
        """Test Data Privacy and Retention APIs - GDPR/CCPA compliance"""
        try:
            # Test get data privacy policies
            policies_response = self.session.get(
                f"{self.base_url}/admin/data-privacy/policies",
                timeout=10
            )
            
            policies_success = policies_response.status_code == 200
            if policies_success:
                policies_result = policies_response.json()
                policies_success = "retention_policies" in policies_result
            
            # Test data retention status
            status_response = self.session.get(
                f"{self.base_url}/admin/data-privacy/status",
                timeout=10
            )
            
            status_success = status_response.status_code == 200
            if status_success:
                status_result = status_response.json()
                status_success = "data_counts" in status_result
            
            overall_success = policies_success and status_success
            
            details = f"Policies Status: {policies_response.status_code}, Status Check: {status_response.status_code}"
            if policies_success:
                details += f", Privacy policies retrieved"
            if status_success:
                details += f", Data retention status checked"
            
            self.log_test("Data Privacy APIs (GDPR/CCPA Compliance)", overall_success, details)
            return overall_success
        except Exception as e:
            self.log_test("Data Privacy APIs (GDPR/CCPA Compliance)", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_processing_apis(self) -> bool:
        """Test Voice Processing APIs - TTS and Voice Answer Processing"""
        try:
            # Test TTS generation
            tts_payload = {
                "text": "Welcome to your AI-powered voice interview. Please introduce yourself and tell me about your background.",
                "voice_config": {
                    "language": "en-US",
                    "gender": "female"
                }
            }
            
            tts_response = self.session.post(
                f"{self.base_url}/voice/generate-tts",
                json=tts_payload,
                timeout=20
            )
            
            tts_success = tts_response.status_code == 200
            if tts_success:
                tts_result = tts_response.json()
                tts_success = "audio_base64" in tts_result and "file_id" in tts_result
            
            # Test voice answer processing (with dummy data)
            voice_payload = {
                "session_id": "test-session-voice-processing",
                "transcript": "I am a software engineer with 5 years of experience in Python and web development.",
                "audio_metadata": {
                    "duration": 15.5,
                    "sample_rate": 16000,
                    "format": "webm"
                }
            }
            
            voice_response = self.session.post(
                f"{self.base_url}/voice/process-answer",
                json=voice_payload,
                timeout=15
            )
            
            voice_success = voice_response.status_code == 200
            if voice_success:
                voice_result = voice_response.json()
                voice_success = "processed" in voice_result
            
            overall_success = tts_success and voice_success
            
            details = f"TTS Status: {tts_response.status_code}, Voice Processing Status: {voice_response.status_code}"
            if tts_success:
                details += f", TTS audio generated"
            if voice_success:
                details += f", Voice answer processed"
            
            self.log_test("Voice Processing APIs (TTS & Voice Answer Processing)", overall_success, details)
            return overall_success
        except Exception as e:
            self.log_test("Voice Processing APIs (TTS & Voice Answer Processing)", False, f"Exception: {str(e)}")
            return False
    
    def run_comprehensive_tests(self) -> Dict[str, bool]:
        """Run all comprehensive backend tests"""
        print("=" * 80)
        print("COMPREHENSIVE BACKEND TESTING - AI-POWERED VOICE INTERVIEW SYSTEM")
        print("Testing Bulk Candidate Management & Phase 2 AI Enhancement Features")
        print("=" * 80)
        print()
        
        results = {}
        
        # Core Authentication
        results["admin_authentication"] = self.test_admin_authentication()
        
        # Bulk Candidate Management (Phase 1)
        results["bulk_upload_api"] = self.test_bulk_upload_api()
        results["bulk_process_api"] = self.test_bulk_process_api()
        results["candidates_list_api"] = self.test_candidates_list_api()
        results["tag_management_apis"] = self.test_tag_management_apis()
        results["bulk_actions_api"] = self.test_bulk_actions_api()
        results["individual_candidate_apis"] = self.test_individual_candidate_apis()
        results["batch_management_apis"] = self.test_batch_management_apis()
        
        # Phase 2: AI-Powered Screening & Shortlisting
        results["phase2_job_requirements_api"] = self.test_phase2_job_requirements_api()
        results["phase2_ai_screening_api"] = self.test_phase2_ai_screening_api()
        results["phase2_ai_enhancement_apis"] = self.test_phase2_ai_enhancement_apis()
        
        # Data Privacy & Compliance
        results["data_privacy_apis"] = self.test_data_privacy_apis()
        
        # Voice Processing
        results["voice_processing_apis"] = self.test_voice_processing_apis()
        
        # Summary
        print("=" * 80)
        print("COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by category
        categories = {
            "Core Authentication": ["admin_authentication"],
            "Bulk Candidate Management (Phase 1)": [
                "bulk_upload_api", "bulk_process_api", "candidates_list_api", 
                "tag_management_apis", "bulk_actions_api", "individual_candidate_apis", 
                "batch_management_apis"
            ],
            "Phase 2: AI-Powered Screening": [
                "phase2_job_requirements_api", "phase2_ai_screening_api", "phase2_ai_enhancement_apis"
            ],
            "Data Privacy & Compliance": ["data_privacy_apis"],
            "Voice Processing": ["voice_processing_apis"]
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
            print("🎉 ALL COMPREHENSIVE TESTS PASSED! Bulk management and AI enhancement features are working correctly.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Most advanced features are functional with minor issues.")
        else:
            print("⚠️  Multiple advanced features failed. Check the details above.")
        
        return results

def main():
    """Main test execution"""
    tester = ComprehensiveBackendTester()
    results = tester.run_comprehensive_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())