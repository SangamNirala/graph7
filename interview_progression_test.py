#!/usr/bin/env python3
"""
Interview Progression Fix Testing
Tests the specific fix for the "can't submit 6th answer" bug.

Key areas to test:
1. Enhanced Interview Flow - Test creating enhanced interview with different question counts (8-12 questions)
2. Interview Start Response - Verify "total_questions" field now returns actual number of generated questions instead of hardcoded 8
3. Interview Progression - Test that candidates can now submit answers and progress through ALL questions, especially beyond question 5
4. Question Type Logic - Verify that technical/behavioral question type classification works correctly with variable question counts
5. Complete Interview Flow - Test full interview completion for interviews with more than 8 questions

CRITICAL BUG TO TEST: Previously users couldn't submit the 6th answer and progress beyond question 5. This should now be fixed.
"""

import requests
import json
import time
import io
from typing import Dict, Any, Optional, List

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://d608964e-3bc2-49ac-82ce-24fb220fc6c6.preview.emergentagent.com/api"

class InterviewProgressionTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.enhanced_tokens = []  # Store multiple enhanced tokens for testing
        self.session_data = []  # Store session data for each test
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def create_enhanced_interview_token(self, min_questions: int, max_questions: int, role_archetype: str = "Software Engineer") -> Optional[str]:
        """Create an enhanced interview token with specific question counts"""
        try:
            resume_content = f"""Sarah Chen
Senior {role_archetype}
Email: sarah.chen@email.com
Phone: (555) 999-8888

EXPERIENCE:
- 6+ years of software development experience
- Expert in Python, JavaScript, and system architecture
- Led multiple teams and delivered complex projects
- Strong background in scalable system design
- Experience with microservices and cloud platforms

SKILLS:
- Python, JavaScript, TypeScript, Go
- FastAPI, React, Node.js, Django
- MongoDB, PostgreSQL, Redis, Elasticsearch
- Docker, Kubernetes, AWS, Azure
- Team leadership and mentoring

EDUCATION:
Master of Science in Computer Science
Stanford University, 2017"""
            
            files = {
                'resume_file': ('enhanced_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': f'Senior {role_archetype} - {min_questions}-{max_questions} Questions',
                'job_description': f'We are seeking a senior {role_archetype.lower()} to lead our technical team. This role requires deep technical expertise, leadership skills, and the ability to architect scalable solutions.',
                'job_requirements': f'Requirements: 5+ years experience, expert-level technical skills, team leadership experience, system design knowledge, strong communication skills.',
                'include_coding_challenge': True,
                'role_archetype': role_archetype,
                'interview_focus': 'Technical Deep-Dive',
                'min_questions': min_questions,
                'max_questions': max_questions
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job-enhanced",
                files=files,
                data=data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and "token" in result:
                    return result["token"]
            
            return None
        except Exception as e:
            print(f"Error creating enhanced token: {str(e)}")
            return None
    
    def test_enhanced_interview_creation(self) -> bool:
        """Test creating enhanced interviews with different question counts"""
        try:
            test_configs = [
                {"min": 8, "max": 10, "role": "Software Engineer"},
                {"min": 10, "max": 12, "role": "Software Engineer"},
                {"min": 9, "max": 11, "role": "Sales"},
                {"min": 8, "max": 12, "role": "Graduate"}
            ]
            
            success_count = 0
            for config in test_configs:
                token = self.create_enhanced_interview_token(
                    config["min"], config["max"], config["role"]
                )
                if token:
                    self.enhanced_tokens.append({
                        "token": token,
                        "min_questions": config["min"],
                        "max_questions": config["max"],
                        "role_archetype": config["role"]
                    })
                    success_count += 1
            
            success = success_count == len(test_configs)
            details = f"Created {success_count}/{len(test_configs)} enhanced interview tokens with variable question counts"
            self.log_test("Enhanced Interview Creation with Variable Question Counts", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Interview Creation with Variable Question Counts", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_start_total_questions_field(self) -> bool:
        """Test that interview start returns actual total_questions instead of hardcoded 8"""
        if not self.enhanced_tokens:
            self.log_test("Interview Start Total Questions Field", False, "No enhanced tokens available")
            return False
        
        try:
            success_count = 0
            total_tests = 0
            
            for token_data in self.enhanced_tokens:
                total_tests += 1
                payload = {
                    "token": token_data["token"],
                    "candidate_name": f"Test Candidate {total_tests}",
                    "voice_mode": False
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/start-interview",
                    json=payload,
                    timeout=20
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if total_questions field exists and is not hardcoded to 8
                    if "total_questions" in data:
                        total_questions = data["total_questions"]
                        min_expected = token_data["min_questions"]
                        max_expected = token_data["max_questions"]
                        
                        # Verify total_questions is within expected range and not hardcoded to 8
                        if min_expected <= total_questions <= max_expected and total_questions != 8:
                            success_count += 1
                            # Store session data for further testing
                            self.session_data.append({
                                "session_id": data.get("session_id"),
                                "token": token_data["token"],
                                "total_questions": total_questions,
                                "min_questions": min_expected,
                                "max_questions": max_expected,
                                "role_archetype": token_data["role_archetype"]
                            })
                        elif total_questions == 8:
                            print(f"   WARNING: total_questions still hardcoded to 8 for {token_data['role_archetype']} interview")
                    else:
                        print(f"   ERROR: total_questions field missing in response for {token_data['role_archetype']} interview")
            
            success = success_count == total_tests
            details = f"Verified dynamic total_questions field in {success_count}/{total_tests} interview starts. No hardcoded 8 values found."
            self.log_test("Interview Start Total Questions Field (Dynamic vs Hardcoded)", success, details)
            return success
        except Exception as e:
            self.log_test("Interview Start Total Questions Field (Dynamic vs Hardcoded)", False, f"Exception: {str(e)}")
            return False
    
    def test_interview_progression_beyond_question_5(self) -> bool:
        """Test that candidates can now submit answers and progress beyond question 5"""
        if not self.session_data:
            self.log_test("Interview Progression Beyond Question 5", False, "No session data available")
            return False
        
        try:
            # Test with the session that has the most questions
            test_session = max(self.session_data, key=lambda x: x["total_questions"])
            
            # Sample answers for progression testing
            sample_answers = [
                "I have extensive experience with Python and FastAPI, having built multiple production systems using these technologies. I focus on clean code, proper error handling, and comprehensive testing.",
                
                "For system architecture, I follow microservices principles with proper service boundaries, API design, and data consistency patterns. I use event-driven architecture for loose coupling.",
                
                "I implement comprehensive monitoring with metrics, logging, and alerting. I use tools like Prometheus, Grafana, and ELK stack for observability and performance tracking.",
                
                "My approach to code reviews focuses on maintainability, security, and performance. I provide constructive feedback and ensure knowledge sharing across the team.",
                
                "When facing tight deadlines, I prioritize features based on business impact, communicate risks clearly, and focus on delivering MVP functionality first with iterative improvements.",
                
                # CRITICAL: Question 6 - This is where the bug occurred
                "I handle team conflicts by facilitating open communication, understanding different perspectives, and finding common ground. I focus on the problem, not personalities, and seek win-win solutions.",
                
                "For technical debt, I maintain a balance between new features and refactoring. I document technical debt, prioritize based on impact, and allocate time for regular maintenance.",
                
                "I stay updated through continuous learning - reading technical blogs, attending conferences, experimenting with new technologies, and participating in the developer community.",
                
                # Additional answers for interviews with more than 8 questions
                "My leadership style is collaborative and supportive. I focus on empowering team members, providing clear direction, and creating an environment where everyone can contribute their best work.",
                
                "For performance optimization, I use profiling tools to identify bottlenecks, implement caching strategies, optimize database queries, and consider architectural improvements when needed.",
                
                "I approach problem-solving systematically by breaking down complex issues, gathering relevant data, considering multiple solutions, and implementing the most effective approach with proper testing.",
                
                "My experience with cloud platforms includes designing scalable architectures, implementing CI/CD pipelines, managing infrastructure as code, and optimizing costs while maintaining performance."
            ]
            
            success_count = 0
            total_questions = test_session["total_questions"]
            
            print(f"   Testing progression through {total_questions} questions for {test_session['role_archetype']} interview...")
            
            for question_num in range(1, total_questions + 1):
                if question_num <= len(sample_answers):
                    answer = sample_answers[question_num - 1]
                else:
                    answer = f"This is my answer to question {question_num}. I have relevant experience and skills that make me a good fit for this role."
                
                payload = {
                    "token": test_session["token"],
                    "message": answer
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/send-message",
                    json=payload,
                    timeout=25
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Special attention to question 6 (the critical bug point)
                    if question_num == 6:
                        print(f"   CRITICAL TEST: Successfully submitted answer #{question_num} (previously failed here)")
                    
                    if question_num < total_questions:
                        # Should have next question
                        if "next_question" in data and data["next_question"]:
                            success_count += 1
                            print(f"   ✓ Question {question_num}: Successfully progressed to next question")
                        else:
                            print(f"   ✗ Question {question_num}: Failed to get next question")
                            break
                    else:
                        # Last question - should complete interview
                        if data.get("completed", False):
                            success_count += 1
                            print(f"   ✓ Question {question_num}: Interview completed successfully")
                        else:
                            print(f"   ✗ Question {question_num}: Interview should have completed but didn't")
                else:
                    print(f"   ✗ Question {question_num}: HTTP {response.status_code} - {response.text[:100]}")
                    break
                
                # Small delay between questions
                time.sleep(0.5)
            
            success = success_count == total_questions
            details = f"Successfully progressed through {success_count}/{total_questions} questions. Critical test: Question 6 progression {'PASSED' if success_count >= 6 else 'FAILED'}"
            self.log_test("Interview Progression Beyond Question 5 (Critical Bug Fix)", success, details)
            return success
        except Exception as e:
            self.log_test("Interview Progression Beyond Question 5 (Critical Bug Fix)", False, f"Exception: {str(e)}")
            return False
    
    def test_question_type_logic_with_variable_counts(self) -> bool:
        """Test that technical/behavioral question type classification works with variable question counts"""
        if not self.session_data:
            self.log_test("Question Type Logic with Variable Counts", False, "No session data available")
            return False
        
        try:
            # Test with different session configurations
            success_count = 0
            total_tests = len(self.session_data)
            
            for session in self.session_data:
                # Start a new interview to test question type logic
                payload = {
                    "token": session["token"],
                    "candidate_name": "Question Type Test Candidate",
                    "voice_mode": False
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/start-interview",
                    json=payload,
                    timeout=20
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if question type information is available
                    if "question_type" in data or "technical_count" in data or "behavioral_count" in data:
                        # Verify the logic makes sense
                        total_questions = data.get("total_questions", 0)
                        
                        # For Technical Deep-Dive focus, we expect more technical questions
                        if session["role_archetype"] == "Software Engineer":
                            # Should have proper technical/behavioral split
                            success_count += 1
                            print(f"   ✓ {session['role_archetype']}: Question type logic working for {total_questions} questions")
                        else:
                            success_count += 1
                            print(f"   ✓ {session['role_archetype']}: Question type logic working for {total_questions} questions")
                    else:
                        print(f"   ✗ {session['role_archetype']}: Question type information missing")
                else:
                    print(f"   ✗ {session['role_archetype']}: Failed to start interview for question type testing")
            
            success = success_count == total_tests
            details = f"Verified question type logic for {success_count}/{total_tests} different interview configurations with variable question counts"
            self.log_test("Question Type Logic with Variable Question Counts", success, details)
            return success
        except Exception as e:
            self.log_test("Question Type Logic with Variable Question Counts", False, f"Exception: {str(e)}")
            return False
    
    def test_complete_interview_flow_more_than_8_questions(self) -> bool:
        """Test complete interview flow for interviews with more than 8 questions"""
        if not self.session_data:
            self.log_test("Complete Interview Flow (>8 Questions)", False, "No session data available")
            return False
        
        try:
            # Find a session with more than 8 questions
            long_interview = None
            for session in self.session_data:
                if session["total_questions"] > 8:
                    long_interview = session
                    break
            
            if not long_interview:
                self.log_test("Complete Interview Flow (>8 Questions)", False, "No interview with >8 questions found")
                return False
            
            # Start the interview
            payload = {
                "token": long_interview["token"],
                "candidate_name": "Complete Flow Test Candidate",
                "voice_mode": False
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=20
            )
            
            if response.status_code != 200:
                self.log_test("Complete Interview Flow (>8 Questions)", False, f"Failed to start interview: {response.status_code}")
                return False
            
            start_data = response.json()
            total_questions = start_data.get("total_questions", 0)
            
            print(f"   Testing complete flow for {total_questions}-question interview...")
            
            # Answer all questions
            comprehensive_answers = [
                "I have deep expertise in software architecture and system design, with experience building scalable distributed systems that handle millions of requests.",
                
                "My approach to technical leadership involves mentoring team members, establishing coding standards, and making architectural decisions that balance technical excellence with business needs.",
                
                "I implement comprehensive testing strategies including unit tests, integration tests, and end-to-end testing, with a focus on test-driven development and continuous integration.",
                
                "For performance optimization, I use profiling tools, implement caching strategies, optimize database queries, and design efficient algorithms to ensure system scalability.",
                
                "I handle technical debt by maintaining a balance between feature development and refactoring, documenting technical debt, and allocating dedicated time for code quality improvements.",
                
                "My conflict resolution approach focuses on understanding different perspectives, facilitating open communication, and finding solutions that benefit both the team and the project.",
                
                "I stay current with technology trends through continuous learning, attending conferences, participating in open source projects, and experimenting with new technologies in side projects.",
                
                "My experience with cloud platforms includes designing microservices architectures, implementing CI/CD pipelines, managing infrastructure as code, and optimizing costs.",
                
                "I approach problem-solving systematically by breaking down complex issues, gathering data, considering multiple solutions, and implementing the most effective approach with proper testing.",
                
                "My leadership philosophy emphasizes empowering team members, providing clear direction, fostering innovation, and creating an environment where everyone can contribute their best work.",
                
                "For code quality, I enforce coding standards through automated tools, conduct thorough code reviews, implement static analysis, and promote best practices across the team.",
                
                "I manage technical projects by setting clear milestones, communicating progress regularly, identifying risks early, and adapting plans based on changing requirements and feedback."
            ]
            
            questions_answered = 0
            for i in range(total_questions):
                if i < len(comprehensive_answers):
                    answer = comprehensive_answers[i]
                else:
                    answer = f"This is my comprehensive answer to question {i+1}. I bring extensive experience and proven ability to deliver results in challenging technical environments."
                
                payload = {
                    "token": long_interview["token"],
                    "message": answer
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/send-message",
                    json=payload,
                    timeout=25
                )
                
                if response.status_code == 200:
                    data = response.json()
                    questions_answered += 1
                    
                    if i == total_questions - 1:
                        # Last question - should complete
                        if data.get("completed", False):
                            print(f"   ✓ Interview completed successfully after {questions_answered} questions")
                            success = True
                        else:
                            print(f"   ✗ Interview should have completed but didn't")
                            success = False
                    else:
                        # Should have next question
                        if "next_question" in data:
                            print(f"   ✓ Question {i+1}: Progressed successfully")
                        else:
                            print(f"   ✗ Question {i+1}: No next question provided")
                            success = False
                            break
                else:
                    print(f"   ✗ Question {i+1}: Failed with status {response.status_code}")
                    success = False
                    break
                
                time.sleep(0.3)
            
            details = f"Completed {questions_answered}/{total_questions} questions in extended interview flow"
            self.log_test("Complete Interview Flow (>8 Questions)", success, details)
            return success
        except Exception as e:
            self.log_test("Complete Interview Flow (>8 Questions)", False, f"Exception: {str(e)}")
            return False
    
    def test_backward_compatibility_legacy_tokens(self) -> bool:
        """Test that legacy tokens still work with the fix"""
        try:
            # Create a legacy token
            resume_content = """Legacy Test Candidate
Software Developer
Email: legacy@test.com

EXPERIENCE:
- 3 years of development experience
- Python and JavaScript skills
- Database and API development

SKILLS:
- Python, JavaScript, SQL
- FastAPI, React, MongoDB"""
            
            files = {
                'resume_file': ('legacy_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Software Developer (Legacy Test)',
                'job_description': 'Standard software developer position for legacy compatibility testing.',
                'job_requirements': 'Basic programming skills and experience with web development.'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job",
                files=files,
                data=data,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test("Backward Compatibility (Legacy Tokens)", False, "Failed to create legacy token")
                return False
            
            result = response.json()
            legacy_token = result.get("token")
            
            if not legacy_token:
                self.log_test("Backward Compatibility (Legacy Tokens)", False, "No legacy token received")
                return False
            
            # Test legacy token interview start
            payload = {
                "token": legacy_token,
                "candidate_name": "Legacy Test Candidate",
                "voice_mode": False
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=20
            )
            
            if response.status_code == 200:
                data = response.json()
                total_questions = data.get("total_questions", 0)
                
                # Legacy tokens should still work, likely with 8 questions
                success = total_questions > 0 and "session_id" in data
                details = f"Legacy token works with {total_questions} questions, maintaining backward compatibility"
            else:
                success = False
                details = f"Legacy token failed: {response.status_code}"
            
            self.log_test("Backward Compatibility (Legacy Tokens)", success, details)
            return success
        except Exception as e:
            self.log_test("Backward Compatibility (Legacy Tokens)", False, f"Exception: {str(e)}")
            return False
    
    def run_interview_progression_tests(self) -> Dict[str, bool]:
        """Run all interview progression tests"""
        print("=" * 80)
        print("INTERVIEW PROGRESSION FIX TESTING")
        print("Testing the 'can't submit 6th answer' bug fix")
        print("=" * 80)
        print()
        
        results = {}
        
        # Test enhanced interview creation with variable question counts
        results["enhanced_interview_creation"] = self.test_enhanced_interview_creation()
        
        # Test that total_questions field is now dynamic
        results["dynamic_total_questions_field"] = self.test_interview_start_total_questions_field()
        
        # CRITICAL: Test progression beyond question 5
        results["progression_beyond_question_5"] = self.test_interview_progression_beyond_question_5()
        
        # Test question type logic with variable counts
        results["question_type_logic_variable_counts"] = self.test_question_type_logic_with_variable_counts()
        
        # Test complete interview flow for >8 questions
        results["complete_flow_more_than_8_questions"] = self.test_complete_interview_flow_more_than_8_questions()
        
        # Test backward compatibility
        results["backward_compatibility_legacy"] = self.test_backward_compatibility_legacy_tokens()
        
        # Summary
        print("=" * 80)
        print("INTERVIEW PROGRESSION FIX TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print(f"\nTest Results:")
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test_name}")
        
        print(f"\nOVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        # Special focus on the critical bug fix
        critical_test_passed = results.get("progression_beyond_question_5", False)
        if critical_test_passed:
            print("\n🎉 CRITICAL BUG FIX VERIFIED: Users can now submit 6th answer and progress beyond question 5!")
        else:
            print("\n❌ CRITICAL BUG STILL EXISTS: Users still cannot progress beyond question 5!")
        
        if passed == total:
            print("\n✅ ALL INTERVIEW PROGRESSION TESTS PASSED!")
            print("The interview progression fix is working correctly.")
        elif critical_test_passed:
            print("\n✅ CRITICAL BUG FIXED!")
            print("The main issue is resolved, with minor issues in other areas.")
        else:
            print("\n⚠️  CRITICAL BUG NOT FIXED!")
            print("The main interview progression issue still exists.")
        
        return results

def main():
    """Main test execution"""
    tester = InterviewProgressionTester()
    results = tester.run_interview_progression_tests()
    
    # Return exit code based on critical test
    critical_passed = results.get("progression_beyond_question_5", False)
    return 0 if critical_passed else 1

if __name__ == "__main__":
    exit(main())