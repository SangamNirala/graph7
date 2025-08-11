#!/usr/bin/env python3
"""
AI Question Generation Test for Voice Mode
Tests if the AI generates clean text without backticks for voice mode
"""

import requests
import json
import time
import io

# Backend URL from frontend .env
BASE_URL = "https://00a8e650-3105-4677-9117-76e2639bccac.preview.emergentagent.com/api"

class AIQuestionTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_token = None
        self.voice_session_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def setup_voice_interview_token(self) -> bool:
        """Create a token for voice interview testing with technical content"""
        try:
            # Create resume with technical content that would normally have backticks
            resume_content = """Sarah Tech
Senior Frontend Developer
Email: sarah.tech@email.com
Phone: (555) 999-8888

EXPERIENCE:
- 6+ years of JavaScript and React development
- Expert in CSS, HTML, and modern web technologies
- Built responsive web applications using CSS Grid and Flexbox
- Implemented state management with Redux and Context API
- Experience with REST APIs and GraphQL integration

TECHNICAL SKILLS:
- Languages: JavaScript, TypeScript, Python, HTML, CSS
- Frameworks: React, Vue.js, Angular, Express.js
- Tools: Webpack, Babel, ESLint, Jest, Cypress
- CSS: Sass, Less, Tailwind CSS, Bootstrap
- Databases: MongoDB, PostgreSQL, Firebase

PROJECTS:
- E-commerce platform with React and Node.js
- Real-time chat application using WebSocket
- Progressive Web App with service workers
- Component library with Storybook documentation"""
            
            files = {
                'resume_file': ('tech_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Frontend Developer',
                'job_description': 'We are seeking a senior frontend developer with expertise in modern web technologies. The role involves working with React, CSS, HTML, and various JavaScript frameworks to build responsive web applications.',
                'job_requirements': 'Requirements: 5+ years JavaScript experience, React expertise, CSS and HTML proficiency, experience with modern build tools, knowledge of responsive design principles.'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job",
                files=files,
                data=data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success") and "token" in result:
                    self.test_token = result["token"]
                    return True
            
            return False
        except Exception as e:
            print(f"Setup failed: {str(e)}")
            return False
    
    def test_ai_generates_clean_questions(self) -> bool:
        """Test that AI generates questions without backticks for voice mode"""
        if not self.test_token:
            if not self.setup_voice_interview_token():
                self.log_test("AI Generates Clean Questions", False, "Failed to setup test token")
                return False
        
        try:
            # Start voice interview to get AI-generated questions
            payload = {
                "token": self.test_token,
                "candidate_name": "Sarah Tech",
                "voice_mode": True
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "voice_mode" in data and
                          data.get("voice_mode") == True)
                
                if success:
                    self.voice_session_id = data["session_id"]
                    first_question = data.get("first_question", "")
                    
                    # Check if the first question contains backticks
                    has_backticks = "`" in first_question
                    
                    # Check for other markdown formatting
                    has_bold = "**" in first_question
                    has_italic = "*" in first_question and not has_bold
                    has_strikethrough = "~~" in first_question
                    
                    # Success if no formatting is present
                    success = not (has_backticks or has_bold or has_italic or has_strikethrough)
                    
                    details = f"Question: '{first_question}' | "
                    details += f"Backticks: {has_backticks}, Bold: {has_bold}, Italic: {has_italic}, Strikethrough: {has_strikethrough}"
                else:
                    details = f"Missing required fields in response: {response.text[:200]}"
            else:
                details = f"HTTP {response.status_code}: {response.text[:200]}"
            
            self.log_test("AI Generates Clean Questions", success, details)
            return success
            
        except Exception as e:
            self.log_test("AI Generates Clean Questions", False, f"Exception: {str(e)}")
            return False
    
    def test_follow_up_questions_clean(self) -> bool:
        """Test that follow-up questions are also clean"""
        if not self.test_token or not self.voice_session_id:
            self.log_test("Follow-up Questions Clean", False, "No active voice session")
            return False
        
        try:
            # Send a technical answer that might prompt a technical follow-up
            technical_answer = "I have extensive experience with React hooks, particularly useState for state management and useEffect for side effects. I've built many components using these hooks and understand their lifecycle and optimization patterns."
            
            payload = {
                "token": self.test_token,
                "message": technical_answer
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/send-message",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                
                if not data.get("completed", False):
                    next_question = data.get("next_question", "")
                    
                    # Check for formatting in the follow-up question
                    has_backticks = "`" in next_question
                    has_bold = "**" in next_question
                    has_italic = "*" in next_question and not has_bold
                    has_strikethrough = "~~" in next_question
                    
                    success = not (has_backticks or has_bold or has_italic or has_strikethrough)
                    
                    details = f"Follow-up: '{next_question[:100]}...' | "
                    details += f"Backticks: {has_backticks}, Bold: {has_bold}, Italic: {has_italic}, Strikethrough: {has_strikethrough}"
                else:
                    # Interview completed - that's also valid
                    success = True
                    details = "Interview completed successfully"
            else:
                details = f"HTTP {response.status_code}: {response.text[:200]}"
            
            self.log_test("Follow-up Questions Clean", success, details)
            return success
            
        except Exception as e:
            self.log_test("Follow-up Questions Clean", False, f"Exception: {str(e)}")
            return False
    
    def test_multiple_questions_for_patterns(self) -> bool:
        """Test multiple questions to check for consistent clean text generation"""
        if not self.test_token:
            if not self.setup_voice_interview_token():
                self.log_test("Multiple Questions Pattern Test", False, "Failed to setup test token")
                return False
        
        # Create multiple interview sessions to get different questions
        question_samples = []
        
        for i in range(3):  # Test 3 different sessions
            try:
                # Create a new token for each test
                resume_content = f"""Test Candidate {i+1}
Frontend Developer
Email: test{i+1}@email.com

EXPERIENCE:
- {3+i}+ years of JavaScript development
- Experience with React, Vue, and Angular
- Built web applications with modern frameworks
- Knowledge of CSS, HTML, and responsive design

SKILLS:
- JavaScript, TypeScript, HTML, CSS
- React, Vue.js, Angular, Node.js
- Webpack, Babel, Git, Docker
- Testing with Jest and Cypress"""
                
                files = {
                    'resume_file': (f'test_resume_{i}.txt', io.StringIO(resume_content), 'text/plain')
                }
                
                data = {
                    'job_title': f'Frontend Developer {i+1}',
                    'job_description': f'Frontend development role {i+1} focusing on modern web technologies and user experience.',
                    'job_requirements': f'Requirements: {3+i}+ years experience, JavaScript expertise, framework knowledge.'
                }
                
                response = self.session.post(
                    f"{self.base_url}/admin/upload-job",
                    files=files,
                    data=data,
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    token = result.get("token")
                    
                    if token:
                        # Start interview to get questions
                        payload = {
                            "token": token,
                            "candidate_name": f"Test Candidate {i+1}",
                            "voice_mode": True
                        }
                        
                        response = self.session.post(
                            f"{self.base_url}/candidate/start-interview",
                            json=payload,
                            timeout=25
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            first_question = data.get("first_question", "")
                            question_samples.append(first_question)
                
                # Small delay between requests
                time.sleep(2)
                
            except Exception as e:
                print(f"   Error in sample {i+1}: {str(e)}")
        
        # Analyze all collected questions
        all_clean = True
        formatting_found = []
        
        for i, question in enumerate(question_samples):
            has_backticks = "`" in question
            has_bold = "**" in question
            has_italic = "*" in question and not has_bold
            has_strikethrough = "~~" in question
            
            if has_backticks:
                formatting_found.append(f"Sample {i+1}: backticks")
                all_clean = False
            if has_bold:
                formatting_found.append(f"Sample {i+1}: bold")
                all_clean = False
            if has_italic:
                formatting_found.append(f"Sample {i+1}: italic")
                all_clean = False
            if has_strikethrough:
                formatting_found.append(f"Sample {i+1}: strikethrough")
                all_clean = False
        
        details = f"Tested {len(question_samples)} question samples. "
        if all_clean:
            details += "All questions generated without markdown formatting."
        else:
            details += f"Formatting found: {', '.join(formatting_found)}"
        
        self.log_test("Multiple Questions Pattern Test", all_clean, details)
        return all_clean
    
    def run_ai_question_tests(self) -> dict:
        """Run all AI question generation tests"""
        print("=" * 70)
        print("AI QUESTION GENERATION TEST FOR VOICE MODE")
        print("Testing if AI generates clean text without backticks")
        print("=" * 70)
        print()
        
        results = {}
        
        # Test AI generates clean questions
        results["ai_clean_questions"] = self.test_ai_generates_clean_questions()
        
        # Test follow-up questions are clean
        results["follow_up_clean"] = self.test_follow_up_questions_clean()
        
        # Test multiple questions for patterns
        results["multiple_questions_pattern"] = self.test_multiple_questions_for_patterns()
        
        # Summary
        print("=" * 70)
        print("AI QUESTION GENERATION TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        test_categories = {
            "Initial Question Generation": ["ai_clean_questions"],
            "Follow-up Questions": ["follow_up_clean"],
            "Pattern Consistency": ["multiple_questions_pattern"]
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
            print("🎉 ALL AI QUESTION TESTS PASSED!")
            print("✅ AI generates clean text without backticks for voice mode")
            print("✅ Follow-up questions are consistently clean")
            print("✅ Pattern is consistent across multiple question generations")
        elif passed >= total * 0.7:
            print("✅ MOSTLY WORKING! AI question generation is mostly clean.")
        else:
            print("⚠️  AI question generation needs improvement for voice mode.")
        
        return results

def main():
    """Main test execution for AI question generation"""
    tester = AIQuestionTester()
    results = tester.run_ai_question_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())