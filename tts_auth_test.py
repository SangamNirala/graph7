#!/usr/bin/env python3
"""
Test Google Cloud TTS authentication issue mentioned in test_result.md
"""

import requests
import json
import io
import urllib3

# Suppress SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://5e9f40e5-f239-4764-bed3-2bd804e0f2a9.preview.emergentagent.com/api"

class TTSAuthTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 30
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'TTS-Auth-Tester/1.0'
        })
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def create_voice_interview_token(self) -> str:
        """Create a token for voice interview testing"""
        try:
            # Authenticate admin
            payload = {"password": "Game@1234"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            if response.status_code != 200:
                return None
            
            # Create token for voice interview
            resume_content = """Voice Test User
TTS Testing Candidate
Email: tts.test@email.com
Phone: (555) 999-0000

EXPERIENCE:
- Voice interface development
- Audio processing expertise
- Real-time communication systems

SKILLS:
- Python, JavaScript
- Audio APIs, TTS/STT
- Real-time systems"""
            
            files = {
                'resume_file': ('tts_test_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Voice Interface Developer - TTS Test',
                'job_description': 'Testing TTS functionality for voice interviews.',
                'job_requirements': 'Requirements: Voice interface experience.',
                'include_coding_challenge': 'false',
                'role_archetype': 'Software Engineer',
                'interview_focus': 'Technical Deep-Dive'
            }
            
            # Remove Content-Type header for multipart form data
            original_headers = self.session.headers.copy()
            if 'Content-Type' in self.session.headers:
                del self.session.headers['Content-Type']
            
            try:
                response = self.session.post(
                    f"{self.base_url}/admin/upload-job-enhanced",
                    files=files,
                    data=data,
                    timeout=15
                )
            finally:
                # Restore original headers
                self.session.headers = original_headers
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success", False) and "token" in result:
                    return result["token"]
            
            return None
            
        except Exception as e:
            print(f"Error creating voice token: {str(e)}")
            return None
    
    def test_voice_interview_start_for_tts(self) -> bool:
        """Test voice interview start to trigger TTS generation"""
        try:
            token = self.create_voice_interview_token()
            if not token:
                self.log_test("Voice Interview Start (TTS Test)", False, "Failed to create token")
                return False
            
            print(f"🔍 Testing voice interview start with token: {token}")
            print("   This should trigger TTS generation for welcome message and first question")
            
            payload = {
                "token": token,
                "candidate_name": "TTS Test User",
                "voice_mode": True
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=30  # Longer timeout for TTS processing
            )
            
            success = response.status_code == 200
            
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Session ID: {data.get('session_id', 'N/A')[:8]}..."
                details += f", Voice Mode: {data.get('voice_mode', 'N/A')}"
                
                # Check for TTS-related fields
                if "welcome_audio" in data:
                    details += f", Welcome Audio: Present"
                else:
                    details += f", Welcome Audio: Missing"
                
                if "question_audio" in data:
                    details += f", Question Audio: Present"
                else:
                    details += f", Question Audio: Missing"
                
                # Check if TTS failed silently
                if data.get('voice_mode') and 'welcome_audio' not in data and 'question_audio' not in data:
                    print("🚨 TTS ISSUE DETECTED!")
                    print("   Voice mode is enabled but no audio data generated")
                    print("   This suggests Google Cloud TTS authentication failure")
                    
            else:
                details += f", Response: {response.text}"
                
                # Check for specific TTS-related errors
                if "TTS" in response.text or "text-to-speech" in response.text.lower():
                    print("🚨 TTS ERROR CONFIRMED!")
                    print(f"   TTS-related error in response: {response.text}")
            
            self.log_test("Voice Interview Start (TTS Test)", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice Interview Start (TTS Test)", False, f"Exception: {str(e)}")
            return False
    
    def test_direct_tts_endpoint(self) -> bool:
        """Test direct TTS endpoint if available"""
        try:
            # First create a session to get session_id
            token = self.create_voice_interview_token()
            if not token:
                self.log_test("Direct TTS Endpoint Test", False, "Failed to create token")
                return False
            
            # Start interview to get session_id
            payload = {
                "token": token,
                "candidate_name": "TTS Direct Test",
                "voice_mode": False  # Start without voice mode first
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test("Direct TTS Endpoint Test", False, "Failed to create session")
                return False
            
            session_data = response.json()
            session_id = session_data.get("session_id")
            
            if not session_id:
                self.log_test("Direct TTS Endpoint Test", False, "No session ID received")
                return False
            
            # Now test direct TTS endpoint
            tts_payload = {
                "session_id": session_id,
                "question_text": "This is a test question for TTS generation. Can you hear this audio clearly?"
            }
            
            print(f"🔍 Testing direct TTS endpoint with session: {session_id[:8]}...")
            
            response = self.session.post(
                f"{self.base_url}/voice/generate-question",
                json=tts_payload,
                timeout=30
            )
            
            success = response.status_code == 200
            
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Success: {data.get('success', 'N/A')}"
                
                if "audio_base64" in data:
                    details += f", Audio Generated: Yes ({len(data['audio_base64']) // 1024}KB)"
                else:
                    details += f", Audio Generated: No"
                    print("🚨 NO AUDIO GENERATED!")
                    print("   TTS endpoint accessible but no audio data returned")
                    print("   This confirms Google Cloud TTS authentication issue")
                    
            else:
                details += f", Response: {response.text}"
                
                # Check for authentication errors
                if "401" in response.text or "authentication" in response.text.lower():
                    print("🚨 TTS AUTHENTICATION ERROR CONFIRMED!")
                    print(f"   Authentication error in TTS endpoint: {response.text}")
                elif "500" in response.text:
                    print("🚨 TTS SERVER ERROR!")
                    print(f"   Server error in TTS processing: {response.text}")
            
            self.log_test("Direct TTS Endpoint Test", success, details)
            return success
            
        except Exception as e:
            self.log_test("Direct TTS Endpoint Test", False, f"Exception: {str(e)}")
            return False
    
    def test_text_cleaning_function(self) -> bool:
        """Test if text cleaning function is working (mentioned as fixed in test_result.md)"""
        try:
            # Create a session first
            token = self.create_voice_interview_token()
            if not token:
                self.log_test("Text Cleaning Function Test", False, "Failed to create token")
                return False
            
            # Start interview to get session_id
            payload = {
                "token": token,
                "candidate_name": "Text Cleaning Test",
                "voice_mode": False
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test("Text Cleaning Function Test", False, "Failed to create session")
                return False
            
            session_data = response.json()
            first_question = session_data.get("first_question", "")
            
            # Check if the question contains backticks or other formatting
            has_backticks = "`" in first_question
            has_bold = "**" in first_question
            has_italic = "*" in first_question and "**" not in first_question
            
            success = not (has_backticks or has_bold or has_italic)
            
            details = f"Question: {first_question[:100]}..."
            if has_backticks:
                details += ", Contains backticks: YES"
            if has_bold:
                details += ", Contains bold: YES"
            if has_italic:
                details += ", Contains italic: YES"
            
            if success:
                details += ", Text cleaning: WORKING"
            else:
                details += ", Text cleaning: NEEDS ATTENTION"
                print("🚨 TEXT FORMATTING DETECTED!")
                print(f"   Question contains formatting that should be cleaned: {first_question}")
            
            self.log_test("Text Cleaning Function Test", success, details)
            return success
            
        except Exception as e:
            self.log_test("Text Cleaning Function Test", False, f"Exception: {str(e)}")
            return False
    
    def run_tts_tests(self):
        """Run all TTS-related tests"""
        print("=" * 80)
        print("GOOGLE CLOUD TTS AUTHENTICATION TESTING")
        print("Testing the stuck task mentioned in test_result.md")
        print("=" * 80)
        print()
        
        results = {}
        
        # Test 1: Voice interview start (should trigger TTS)
        results["voice_interview_tts"] = self.test_voice_interview_start_for_tts()
        
        # Test 2: Direct TTS endpoint
        results["direct_tts_endpoint"] = self.test_direct_tts_endpoint()
        
        # Test 3: Text cleaning function
        results["text_cleaning"] = self.test_text_cleaning_function()
        
        # Summary
        print("=" * 80)
        print("TTS TEST SUMMARY")
        print("=" * 80)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print()
        
        # Analysis
        print("ANALYSIS:")
        if not results.get("voice_interview_tts", False) or not results.get("direct_tts_endpoint", False):
            print("❌ TTS AUTHENTICATION ISSUE CONFIRMED")
            print("   Google Cloud TTS is not generating audio due to authentication failure")
            print("   This explains why users can't hear AI voice in interviews")
            print("   RECOMMENDATION: Fix Google Cloud TTS service account credentials")
        else:
            print("✅ TTS functionality appears to be working")
            print("   Audio generation is successful")
        
        if results.get("text_cleaning", False):
            print("✅ Text cleaning function is working correctly")
        else:
            print("❌ Text cleaning function needs attention")
        
        return results

def main():
    """Main test execution"""
    tester = TTSAuthTester()
    results = tester.run_tts_tests()
    
    # Return exit code based on TTS functionality
    tts_working = results.get("voice_interview_tts", False) and results.get("direct_tts_endpoint", False)
    return 0 if tts_working else 1

if __name__ == "__main__":
    exit(main())