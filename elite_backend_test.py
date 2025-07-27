#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Elite AI Interview Platform
Tests the enhanced backend features including:
- Enhanced Admin APIs with role archetypes and coding challenges
- Interactive Modules (Coding Challenges, SJT Tests)
- Enhanced Interview Flow with practice rounds and question rephrasing
- Advanced AI Features with bias mitigation and multi-vector scoring
- Candidate Pipeline Management and Comparison Tools
- Backward Compatibility with legacy endpoints
"""

import requests
import json
import time
import io
import base64
from typing import Dict, Any, Optional, List

# Backend URL from frontend .env
BASE_URL = "https://8efc00c9-cb7f-48ab-a6b5-ecb4f59517b3.preview.emergentagent.com/api"

class EliteInterviewPlatformTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.legacy_token = None
        self.enhanced_token = None
        self.session_id = None
        self.assessment_id = None
        self.coding_challenge_id = None
        self.sjt_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_health_check(self) -> bool:
        """Test basic API health check"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Response: {response.text[:100]}"
            self.log_test("Health Check", success, details)
            return success
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login(self) -> bool:
        """Test admin authentication with correct password"""
        try:
            payload = {"password": "Game@123"}
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
            self.log_test("Admin Login", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_admin_upload(self) -> bool:
        """Test enhanced admin upload with new parameters"""
        try:
            resume_content = """Sarah Chen
Senior Software Engineer
Email: sarah.chen@email.com
Phone: (555) 123-4567

EXPERIENCE:
- 6+ years of full-stack development
- Expert in Python, JavaScript, React, and FastAPI
- Led development of microservices architecture
- Experience with coding challenges and technical interviews
- Strong problem-solving and algorithmic thinking

SKILLS:
- Python, JavaScript, TypeScript, Java
- FastAPI, React, Node.js, Spring Boot
- MongoDB, PostgreSQL, Redis
- Docker, Kubernetes, AWS, Azure
- Data structures and algorithms
- System design and architecture

EDUCATION:
Master of Science in Computer Science
Stanford University, 2017"""
            
            files = {
                'resume_file': ('enhanced_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Software Engineer',
                'job_description': 'We are seeking a senior software engineer to join our elite development team. The role involves complex problem-solving, system design, and technical leadership.',
                'job_requirements': 'Requirements: 5+ years experience, strong algorithmic skills, system design knowledge, coding challenge proficiency, leadership experience.',
                'include_coding_challenge': 'true',
                'role_archetype': 'Software Engineer',
                'interview_focus': 'Technical Deep-Dive'
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
                          "features" in result)
                if success:
                    self.enhanced_token = result["token"]
                    features = result.get("features", {})
                    success = (features.get("coding_challenge") == True and
                              features.get("role_archetype") == "Software Engineer" and
                              features.get("interview_focus") == "Technical Deep-Dive")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.enhanced_token[:8]}..., Features: {result.get('features', {})}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Enhanced Admin Upload with New Parameters", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Admin Upload with New Parameters", False, f"Exception: {str(e)}")
            return False
    
    def test_legacy_admin_upload(self) -> bool:
        """Test backward compatibility with legacy admin upload"""
        try:
            resume_content = """John Smith
Software Developer
Email: john.smith@email.com
Phone: (555) 987-6543

EXPERIENCE:
- 3+ years of Python development
- Experience with web frameworks and databases
- RESTful API development
- Team collaboration and agile methodologies

SKILLS:
- Python, JavaScript, SQL
- FastAPI, React, MongoDB
- Git, Docker, basic AWS
- Problem-solving and debugging

EDUCATION:
Bachelor of Science in Computer Science
Tech University, 2020"""
            
            files = {
                'resume_file': ('legacy_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Python Developer',
                'job_description': 'We are looking for a Python developer to join our team. Standard interview process with technical and behavioral questions.',
                'job_requirements': 'Requirements: 2+ years Python experience, web development knowledge, database skills, team collaboration.'
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
                success = (result.get("success", False) and "token" in result)
                if success:
                    self.legacy_token = result["token"]
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.legacy_token[:8]}..."
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Legacy Admin Upload (Backward Compatibility)", success, details)
            return success
        except Exception as e:
            self.log_test("Legacy Admin Upload (Backward Compatibility)", False, f"Exception: {str(e)}")
            return False
    
    def test_candidate_pipeline(self) -> bool:
        """Test candidate pipeline management endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/admin/candidate-pipeline", timeout=10)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "pipeline" in data and isinstance(data["pipeline"], list)
                
                # Check if our tokens are in the pipeline
                if success:
                    pipeline = data["pipeline"]
                    enhanced_found = any(
                        candidate.get("token") == self.enhanced_token 
                        for candidate in pipeline
                    ) if self.enhanced_token else False
                    
                    legacy_found = any(
                        candidate.get("token") == self.legacy_token 
                        for candidate in pipeline
                    ) if self.legacy_token else False
                    
                    details = f"Status: {response.status_code}, Pipeline size: {len(pipeline)}"
                    if enhanced_found:
                        details += ", Enhanced token found"
                    if legacy_found:
                        details += ", Legacy token found"
                else:
                    details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Candidate Pipeline Management", success, details)
            return success
        except Exception as e:
            self.log_test("Candidate Pipeline Management", False, f"Exception: {str(e)}")
            return False
    
    def test_compare_candidates(self) -> bool:
        """Test candidate comparison endpoint"""
        try:
            # We need at least one token to test comparison
            if not (self.enhanced_token or self.legacy_token):
                self.log_test("Candidate Comparison", False, "No tokens available for comparison")
                return False
            
            candidate_tokens = []
            if self.enhanced_token:
                candidate_tokens.append(self.enhanced_token)
            if self.legacy_token:
                candidate_tokens.append(self.legacy_token)
            
            response = self.session.post(
                f"{self.base_url}/admin/compare-candidates",
                json=candidate_tokens,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "comparisons" in data and isinstance(data["comparisons"], list)
            
            details = f"Status: {response.status_code}, Tokens tested: {len(candidate_tokens)}"
            if success:
                details += f", Comparisons returned: {len(data.get('comparisons', []))}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Candidate Comparison", success, details)
            return success
        except Exception as e:
            self.log_test("Candidate Comparison", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_interview_start(self) -> bool:
        """Test enhanced interview start with new features"""
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
                timeout=15
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
                    features = data.get("features", {})
                    success = features.get("coding_challenge") == True
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Session: {self.session_id[:8]}..., Enhanced: {data.get('is_enhanced')}, Features: {data.get('features', {})}"
            else:
                details += f", Response: {response.text[:300]}"
            
            self.log_test("Enhanced Interview Start with New Features", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Interview Start with New Features", False, f"Exception: {str(e)}")
            return False
    
    def test_practice_round(self) -> bool:
        """Test practice round functionality"""
        if not self.enhanced_token:
            self.log_test("Practice Round", False, "No enhanced token available")
            return False
        
        try:
            payload = {
                "token": self.enhanced_token,
                "candidate_name": "Sarah Chen"
            }
            response = self.session.post(
                f"{self.base_url}/candidate/practice-round",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "practice_question" in data and
                          "message" in data)
                
                # Check if practice question is the expected one
                if success:
                    expected_question = "Tell me about a hobby you're passionate about."
                    success = data.get("practice_question") == expected_question
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Practice Session: {data.get('session_id', '')[:8]}..., Question: {data.get('practice_question', '')[:50]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Practice Round Functionality", success, details)
            return success
        except Exception as e:
            self.log_test("Practice Round Functionality", False, f"Exception: {str(e)}")
            return False
    
    def test_question_rephrasing(self) -> bool:
        """Test question rephrasing functionality"""
        if not self.session_id:
            self.log_test("Question Rephrasing", False, "No session ID available")
            return False
        
        try:
            payload = {
                "session_id": self.session_id,
                "original_question": "Explain the concept of polymorphism in object-oriented programming and provide examples."
            }
            response = self.session.post(
                f"{self.base_url}/candidate/rephrase-question",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "rephrased_question" in data
                
                # Verify the rephrased question is different and meaningful
                if success:
                    original = payload["original_question"]
                    rephrased = data.get("rephrased_question", "")
                    success = len(rephrased) > 20 and rephrased != original
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Rephrased: {data.get('rephrased_question', '')[:100]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Question Rephrasing", success, details)
            return success
        except Exception as e:
            self.log_test("Question Rephrasing", False, f"Exception: {str(e)}")
            return False
    
    def test_coding_challenge_generation(self) -> bool:
        """Test coding challenge generation"""
        if not self.session_id:
            self.log_test("Coding Challenge Generation", False, "No session ID available")
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
                if success:
                    self.coding_challenge_id = data["challenge"].get("id")
            
            details = f"Status: {response.status_code}"
            if success:
                challenge = data["challenge"]
                details += f", Title: {challenge.get('problem_title', '')}, Language: {challenge.get('language', '')}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Coding Challenge Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Coding Challenge Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_coding_challenge_submission(self) -> bool:
        """Test coding challenge solution submission"""
        if not self.session_id:
            self.log_test("Coding Challenge Submission", False, "No session ID available")
            return False
        
        try:
            # Submit a sample solution
            sample_code = """
function findTwoSum(numbers, target) {
    const map = new Map();
    for (let i = 0; i < numbers.length; i++) {
        const complement = target - numbers[i];
        if (map.has(complement)) {
            return [map.get(complement), i];
        }
        map.set(numbers[i], i);
    }
    return [];
}
"""
            
            payload = {
                "session_id": self.session_id,
                "submitted_code": sample_code.strip()
            }
            response = self.session.post(
                f"{self.base_url}/modules/coding-challenge/submit",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("success" in data and 
                          "score" in data and 
                          "analysis" in data)
                
                # Verify score is reasonable
                if success:
                    score = data.get("score", 0)
                    success = 0 <= score <= 100
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Score: {data.get('score', 0)}/100, Analysis length: {len(data.get('analysis', ''))}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Coding Challenge Submission", success, details)
            return success
        except Exception as e:
            self.log_test("Coding Challenge Submission", False, f"Exception: {str(e)}")
            return False
    
    def test_sjt_generation(self) -> bool:
        """Test Situational Judgment Test generation"""
        if not self.session_id:
            self.log_test("SJT Generation", False, "No session ID available")
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/modules/sjt/{self.session_id}",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("sjt" in data and 
                          "scenario" in data["sjt"] and
                          "question" in data["sjt"] and
                          "options" in data["sjt"] and
                          len(data["sjt"]["options"]) >= 3)
                if success:
                    self.sjt_id = data["sjt"].get("id")
            
            details = f"Status: {response.status_code}"
            if success:
                sjt = data["sjt"]
                details += f", Scenario length: {len(sjt.get('scenario', ''))}, Options: {len(sjt.get('options', []))}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("SJT Generation", success, details)
            return success
        except Exception as e:
            self.log_test("SJT Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_sjt_submission(self) -> bool:
        """Test SJT answer submission"""
        if not self.session_id or not self.sjt_id:
            self.log_test("SJT Submission", False, "No session ID or SJT ID available")
            return False
        
        try:
            payload = {
                "session_id": self.session_id,
                "sjt_id": self.sjt_id,
                "selected_answer": "b"  # Assuming option 'b' exists
            }
            response = self.session.post(
                f"{self.base_url}/modules/sjt/submit",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("success" in data and 
                          "is_correct" in data and 
                          "score" in data and
                          "explanation" in data)
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Correct: {data.get('is_correct')}, Score: {data.get('score')}, Explanation length: {len(data.get('explanation', ''))}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("SJT Submission", success, details)
            return success
        except Exception as e:
            self.log_test("SJT Submission", False, f"Exception: {str(e)}")
            return False
    
    def test_text_cleaning_for_tts(self) -> bool:
        """Test text cleaning function for TTS (backtick fix)"""
        try:
            # Start an interview to get a question that might contain backticks
            if not self.enhanced_token:
                self.log_test("Text Cleaning for TTS", False, "No enhanced token available")
                return False
            
            payload = {
                "token": self.enhanced_token,
                "candidate_name": "Test Candidate",
                "voice_mode": True  # Enable voice mode to trigger TTS
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                first_question = data.get("first_question", "")
                
                # Check if the question contains backticks (it shouldn't after cleaning)
                success = "`" not in first_question
                
                # Also check if TTS audio was generated (indicates cleaning worked)
                if "question_audio" in data:
                    try:
                        audio_bytes = base64.b64decode(data["question_audio"])
                        success = success and len(audio_bytes) > 0
                    except Exception:
                        success = False
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Question clean: {'✓' if '`' not in first_question else '✗'}, Audio generated: {'✓' if 'question_audio' in data else '✗'}"
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Text Cleaning for TTS (Backtick Fix)", success, details)
            return success
        except Exception as e:
            self.log_test("Text Cleaning for TTS (Backtick Fix)", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all enhanced backend tests"""
        print("=" * 80)
        print("ELITE AI INTERVIEW PLATFORM - COMPREHENSIVE BACKEND TESTING")
        print("Testing Enhanced Features & New Capabilities")
        print("=" * 80)
        print()
        
        results = {}
        
        # Basic connectivity
        results["health_check"] = self.test_health_check()
        
        # Admin authentication
        results["admin_login"] = self.test_admin_login()
        
        # Enhanced Admin APIs
        results["enhanced_admin_upload"] = self.test_enhanced_admin_upload()
        results["legacy_admin_upload"] = self.test_legacy_admin_upload()
        results["candidate_pipeline"] = self.test_candidate_pipeline()
        results["compare_candidates"] = self.test_compare_candidates()
        
        # Enhanced Interview Flow
        results["enhanced_interview_start"] = self.test_enhanced_interview_start()
        results["practice_round"] = self.test_practice_round()
        results["question_rephrasing"] = self.test_question_rephrasing()
        
        # Interactive Modules
        results["coding_challenge_generation"] = self.test_coding_challenge_generation()
        results["coding_challenge_submission"] = self.test_coding_challenge_submission()
        results["sjt_generation"] = self.test_sjt_generation()
        results["sjt_submission"] = self.test_sjt_submission()
        
        # Advanced AI Features
        results["text_cleaning_for_tts"] = self.test_text_cleaning_for_tts()
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by category
        categories = {
            "Basic Connectivity": ["health_check"],
            "Admin Authentication": ["admin_login"],
            "Enhanced Admin APIs": ["enhanced_admin_upload", "legacy_admin_upload", "candidate_pipeline", "compare_candidates"],
            "Enhanced Interview Flow": ["enhanced_interview_start", "practice_round", "question_rephrasing"],
            "Interactive Modules": ["coding_challenge_generation", "coding_challenge_submission", "sjt_generation", "sjt_submission"],
            "Advanced AI Features": ["text_cleaning_for_tts"]
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
            print("🎉 ALL TESTS PASSED! Elite AI Interview Platform backend is fully functional.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Most enhanced features are functional with minor issues.")
        else:
            print("⚠️  Multiple tests failed. Check the details above.")
        
        return results

def main():
    """Main test execution"""
    tester = EliteInterviewPlatformTester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())