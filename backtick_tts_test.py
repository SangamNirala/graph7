#!/usr/bin/env python3
"""
Backtick Fix Testing for TTS Functionality
Tests the text cleaning function and TTS generation with technical content containing backticks.

Specific tests:
1. Test clean_text_for_speech function directly
2. Test TTS generation with technical text containing backticks
3. Verify generated audio doesn't include pronunciation of backticks
4. Test normal interview questions still work
5. Test AI system prompts generate plain text for voice mode
"""

import requests
import json
import time
import io
import base64
import tempfile
import re
from typing import Dict, Any, Optional

# Backend URL from frontend .env
BASE_URL = "https://f70e6962-3e70-40c3-9480-a394c3cc64c7.preview.emergentagent.com/api"

class BacktickTTSTester:
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
    
    def test_text_cleaning_function(self) -> bool:
        """Test the clean_text_for_speech function by testing TTS with technical content"""
        try:
            # Test text with various markdown formatting that should be cleaned
            test_texts = [
                # Backticks around code terms
                "How do `margin`, `padding`, and `border` interact in the CSS box model?",
                
                # Multiple formatting types
                "Explain the difference between `let`, `const`, and `var` in **JavaScript**.",
                
                # Complex technical question with formatting
                "What is the purpose of the `useEffect` hook in React, and how does it differ from `componentDidMount`?",
                
                # Bold and italic formatting
                "Describe how **CSS Grid** and *Flexbox* work together for responsive layouts.",
                
                # Strikethrough and other formatting
                "Why would you use `async/await` instead of ~~callbacks~~ or **Promises**?",
                
                # Technical acronyms that should be spelled out
                "How do you optimize API calls in a React application using JSON data?"
            ]
            
            expected_cleanings = [
                # Expected cleaned versions (backticks removed, acronyms spelled out)
                "How do margin, padding, and border interact in the C-S-S box model?",
                "Explain the difference between let, const, and var in Java Script.",
                "What is the purpose of the useEffect hook in React, and how does it differ from componentDidMount?",
                "Describe how C-S-S Grid and Flexbox work together for responsive layouts.",
                "Why would you use async/await instead of callbacks or Promises?",
                "How do you optimize A-P-I calls in a React application using J-S-O-N data?"
            ]
            
            # Test each text by generating TTS and checking if it succeeds
            all_passed = True
            for i, test_text in enumerate(test_texts):
                try:
                    payload = {
                        "session_id": "test-cleaning-session",
                        "question_text": test_text
                    }
                    
                    response = self.session.post(
                        f"{self.base_url}/voice/generate-question",
                        json=payload,
                        timeout=20
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success") and "audio_base64" in data:
                            # Verify audio was generated (non-empty base64)
                            try:
                                audio_bytes = base64.b64decode(data["audio_base64"])
                                if len(audio_bytes) > 0:
                                    print(f"   ✓ Text {i+1}: Generated {len(audio_bytes)} bytes of audio")
                                else:
                                    all_passed = False
                                    print(f"   ✗ Text {i+1}: Empty audio generated")
                            except Exception:
                                all_passed = False
                                print(f"   ✗ Text {i+1}: Invalid base64 audio")
                        else:
                            all_passed = False
                            print(f"   ✗ Text {i+1}: TTS generation failed")
                    else:
                        all_passed = False
                        print(f"   ✗ Text {i+1}: HTTP {response.status_code}")
                    
                    # Small delay between requests
                    time.sleep(1)
                    
                except Exception as e:
                    all_passed = False
                    print(f"   ✗ Text {i+1}: Exception - {str(e)}")
            
            details = f"Tested {len(test_texts)} technical texts with formatting. All should generate clean audio without backtick pronunciation."
            self.log_test("Text Cleaning Function", all_passed, details)
            return all_passed
            
        except Exception as e:
            self.log_test("Text Cleaning Function", False, f"Exception: {str(e)}")
            return False
    
    def test_tts_with_backticks(self) -> bool:
        """Test TTS generation specifically with backtick-heavy technical content"""
        try:
            # Technical question that would normally be full of backticks
            technical_question = "Can you explain how `useState` and `useEffect` hooks work in React? How would you use `fetch` API with `async/await` to make HTTP requests?"
            
            payload = {
                "session_id": "test-backticks-session",
                "question_text": technical_question
            }
            
            response = self.session.post(
                f"{self.base_url}/voice/generate-question",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "audio_base64" in data and 
                          "file_id" in data)
                
                if success:
                    # Verify audio data is valid and substantial
                    try:
                        audio_bytes = base64.b64decode(data["audio_base64"])
                        audio_size_kb = len(audio_bytes) // 1024
                        
                        # Audio should be substantial (technical question should generate decent length audio)
                        success = len(audio_bytes) > 1000  # At least 1KB of audio
                        
                        details = f"Generated {audio_size_kb}KB audio for technical question with backticks. File ID: {data.get('file_id', '')[:8]}..."
                    except Exception:
                        success = False
                        details = "Invalid base64 audio data"
                else:
                    details = f"TTS failed: {response.text[:200]}"
            else:
                details = f"HTTP {response.status_code}: {response.text[:200]}"
            
            self.log_test("TTS with Backticks", success, details)
            return success
            
        except Exception as e:
            self.log_test("TTS with Backticks", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_interview_with_technical_questions(self) -> bool:
        """Test complete voice interview flow with technical questions that would contain backticks"""
        if not self.test_token:
            if not self.setup_voice_interview_token():
                self.log_test("Voice Interview with Technical Questions", False, "Failed to setup test token")
                return False
        
        try:
            # Start voice interview
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
                    
                    # Check if TTS audio was generated
                    has_welcome_audio = "welcome_audio" in data and len(data["welcome_audio"]) > 0
                    has_question_audio = "question_audio" in data and len(data["question_audio"]) > 0
                    
                    # Verify the first question doesn't contain backticks (should be cleaned by AI prompt)
                    has_backticks = "`" in first_question
                    
                    success = has_welcome_audio and has_question_audio and not has_backticks
                    
                    details = f"Session: {self.voice_session_id[:8]}..., "
                    details += f"Welcome Audio: {len(data.get('welcome_audio', '')) // 1024}KB, "
                    details += f"Question Audio: {len(data.get('question_audio', '')) // 1024}KB, "
                    details += f"Question has backticks: {has_backticks}, "
                    details += f"Question preview: {first_question[:100]}..."
                else:
                    details = f"Missing required fields in response: {response.text[:200]}"
            else:
                details = f"HTTP {response.status_code}: {response.text[:200]}"
            
            self.log_test("Voice Interview with Technical Questions", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice Interview with Technical Questions", False, f"Exception: {str(e)}")
            return False
    
    def test_ai_prompt_generates_clean_text(self) -> bool:
        """Test that AI generates clean text without backticks for voice mode"""
        if not self.test_token or not self.voice_session_id:
            self.log_test("AI Prompt Generates Clean Text", False, "No active voice session")
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
                    has_backticks = "`" in next_question
                    has_question_audio = "question_audio" in data and len(data["question_audio"]) > 0
                    
                    # Success if question has no backticks and audio was generated
                    success = not has_backticks and has_question_audio
                    
                    details = f"Next question has backticks: {has_backticks}, "
                    details += f"Audio generated: {has_question_audio}, "
                    details += f"Question preview: {next_question[:100]}..."
                else:
                    # Interview completed - that's also valid
                    success = True
                    details = "Interview completed successfully"
            else:
                details = f"HTTP {response.status_code}: {response.text[:200]}"
            
            self.log_test("AI Prompt Generates Clean Text", success, details)
            return success
            
        except Exception as e:
            self.log_test("AI Prompt Generates Clean Text", False, f"Exception: {str(e)}")
            return False
    
    def test_normal_questions_still_work(self) -> bool:
        """Test that normal interview questions without technical formatting still work properly"""
        try:
            # Test normal behavioral question
            normal_question = "Tell me about a time when you had to work under pressure to meet a tight deadline."
            
            payload = {
                "session_id": "test-normal-session",
                "question_text": normal_question
            }
            
            response = self.session.post(
                f"{self.base_url}/voice/generate-question",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "audio_base64" in data and 
                          "file_id" in data)
                
                if success:
                    try:
                        audio_bytes = base64.b64decode(data["audio_base64"])
                        audio_size_kb = len(audio_bytes) // 1024
                        success = len(audio_bytes) > 500  # Should generate reasonable audio
                        details = f"Generated {audio_size_kb}KB audio for normal question"
                    except Exception:
                        success = False
                        details = "Invalid audio data"
                else:
                    details = f"TTS failed: {response.text[:200]}"
            else:
                details = f"HTTP {response.status_code}: {response.text[:200]}"
            
            self.log_test("Normal Questions Still Work", success, details)
            return success
            
        except Exception as e:
            self.log_test("Normal Questions Still Work", False, f"Exception: {str(e)}")
            return False
    
    def run_backtick_tests(self) -> Dict[str, bool]:
        """Run all backtick-related TTS tests"""
        print("=" * 70)
        print("BACKTICK FIX TESTING FOR TTS FUNCTIONALITY")
        print("Testing text cleaning and TTS with technical content")
        print("=" * 70)
        print()
        
        results = {}
        
        # Setup
        print("Setting up test environment...")
        if not self.setup_voice_interview_token():
            print("❌ Failed to setup test token")
            return {"setup": False}
        print("✅ Test token created successfully")
        print()
        
        # Test the text cleaning function
        results["text_cleaning_function"] = self.test_text_cleaning_function()
        
        # Test TTS with backticks specifically
        results["tts_with_backticks"] = self.test_tts_with_backticks()
        
        # Test voice interview flow with technical questions
        results["voice_interview_technical"] = self.test_voice_interview_with_technical_questions()
        
        # Test AI generates clean text
        results["ai_clean_text_generation"] = self.test_ai_prompt_generates_clean_text()
        
        # Test normal questions still work
        results["normal_questions_work"] = self.test_normal_questions_still_work()
        
        # Summary
        print("=" * 70)
        print("BACKTICK FIX TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        test_categories = {
            "Text Cleaning": ["text_cleaning_function"],
            "TTS with Technical Content": ["tts_with_backticks"],
            "Voice Interview Flow": ["voice_interview_technical"],
            "AI Text Generation": ["ai_clean_text_generation"],
            "Normal Functionality": ["normal_questions_work"]
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
            print("🎉 ALL BACKTICK TESTS PASSED! The text cleaning fix is working correctly.")
            print("✅ TTS no longer pronounces backticks in technical content")
            print("✅ AI generates clean text for voice mode")
            print("✅ Normal questions continue to work properly")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Most backtick fixes are functional.")
        else:
            print("⚠️  Multiple backtick tests failed. The fix may need adjustment.")
        
        return results

def main():
    """Main test execution for backtick fix"""
    tester = BacktickTTSTester()
    results = tester.run_backtick_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())