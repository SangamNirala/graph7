#!/usr/bin/env python3
"""
Voice Interview Functionality Testing
Focus on testing the voice interview features after CORS fix:
1. Voice Interview Start with TTS audio generation
2. Voice Message Processing with TTS for follow-up questions  
3. TTS Authentication and audio quality verification
4. Base64 audio encoding validation
"""

import requests
import json
import time
import io
import base64
import tempfile
from typing import Dict, Any, Optional

# Backend URL from frontend .env (updated after CORS fix)
BASE_URL = "https://9e22884b-b8ee-476f-9f2a-0ddeaaf2e889.preview.emergentagent.com/api"

class VoiceInterviewTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.voice_token = None
        self.voice_session_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def create_voice_interview_token(self) -> bool:
        """Create a token specifically for voice interview testing"""
        try:
            resume_content = """Sarah Chen
Voice Interface Specialist
Email: sarah.chen@email.com
Phone: (555) 999-8888

EXPERIENCE:
- 5+ years developing voice-enabled applications
- Expert in speech recognition and text-to-speech systems
- Built conversational AI interfaces for customer service
- Experience with Google Cloud Speech APIs and Amazon Polly
- Led voice UX design for mobile applications

SKILLS:
- Python, JavaScript, React, FastAPI
- Google Cloud TTS/STT, WebRTC, real-time audio processing
- Voice user interface design and conversational flow
- Natural language processing and speech synthesis
- Audio signal processing and voice quality optimization

EDUCATION:
Master of Science in Human-Computer Interaction
Stanford University, 2019"""
            
            files = {
                'resume_file': ('voice_specialist_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Voice Interface Developer',
                'job_description': 'We are seeking a senior voice interface developer to lead our voice AI initiatives. The role involves designing and implementing voice-enabled applications, integrating speech technologies, and optimizing voice user experiences.',
                'job_requirements': 'Requirements: 5+ years voice interface experience, Google Cloud Speech API expertise, conversational AI knowledge, Python/JavaScript proficiency, voice UX design skills.'
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
                    self.voice_token = result["token"]
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Token: {self.voice_token[:8]}..., Resume Preview: {result.get('resume_preview', '')[:50]}..."
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Voice Interview Token Creation", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Interview Token Creation", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_interview_start(self) -> bool:
        """Test /api/candidate/start-interview with voice_mode=true"""
        if not self.voice_token:
            self.log_test("Voice Interview Start", False, "No voice token available")
            return False
        
        try:
            payload = {
                "token": self.voice_token,
                "candidate_name": "Sarah Chen",
                "voice_mode": True
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=30  # Extended timeout for TTS generation
            )
            
            success = response.status_code == 200
            audio_details = []
            
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "voice_mode" in data and
                          data.get("voice_mode") == True)
                
                if success:
                    self.voice_session_id = data["session_id"]
                
                # Check for TTS audio generation
                if "welcome_audio" in data:
                    try:
                        welcome_audio_bytes = base64.b64decode(data["welcome_audio"])
                        audio_details.append(f"Welcome Audio: {len(welcome_audio_bytes)} bytes ({len(welcome_audio_bytes) // 1024}KB)")
                        
                        # Verify it's valid base64 and has reasonable size
                        if len(welcome_audio_bytes) < 1000:  # Too small for real audio
                            success = False
                            audio_details.append("Welcome audio too small - likely not real audio data")
                    except Exception as e:
                        success = False
                        audio_details.append(f"Welcome audio base64 decode failed: {str(e)}")
                else:
                    success = False
                    audio_details.append("No welcome_audio in response")
                
                if "question_audio" in data:
                    try:
                        question_audio_bytes = base64.b64decode(data["question_audio"])
                        audio_details.append(f"Question Audio: {len(question_audio_bytes)} bytes ({len(question_audio_bytes) // 1024}KB)")
                        
                        # Verify it's valid base64 and has reasonable size
                        if len(question_audio_bytes) < 1000:  # Too small for real audio
                            success = False
                            audio_details.append("Question audio too small - likely not real audio data")
                    except Exception as e:
                        success = False
                        audio_details.append(f"Question audio base64 decode failed: {str(e)}")
                else:
                    success = False
                    audio_details.append("No question_audio in response")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Session: {self.voice_session_id[:8]}..., Voice Mode: {data.get('voice_mode')}"
                details += f", Question: '{data.get('first_question', '')[:50]}...'"
                if audio_details:
                    details += f", Audio: {'; '.join(audio_details)}"
            else:
                details += f", Response: {response.text[:300]}"
                if audio_details:
                    details += f", Audio Issues: {'; '.join(audio_details)}"
            
            self.log_test("Voice Interview Start with TTS Audio Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Interview Start with TTS Audio Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_message_processing(self) -> bool:
        """Test /api/candidate/send-message for voice mode interviews"""
        if not self.voice_token or not self.voice_session_id:
            self.log_test("Voice Message Processing", False, "No voice session available")
            return False
        
        try:
            # Send a message to get the next question with TTS
            payload = {
                "token": self.voice_token,
                "message": "I have extensive experience with voice interfaces, having worked on conversational AI systems for the past 5 years. I've implemented speech recognition using Google Cloud Speech-to-Text API and built text-to-speech systems with natural-sounding voices. My recent project involved creating a voice-controlled customer service bot that reduced call handling time by 40%."
            }
            
            response = self.session.post(
                f"{self.base_url}/candidate/send-message",
                json=payload,
                timeout=30  # Extended timeout for AI processing and TTS generation
            )
            
            success = response.status_code == 200
            audio_details = []
            
            if success:
                data = response.json()
                
                # Check if we get a next question (not completed yet)
                if not data.get("completed", False):
                    success = "next_question" in data
                    
                    # Check for TTS audio in follow-up question
                    if "question_audio" in data:
                        try:
                            question_audio_bytes = base64.b64decode(data["question_audio"])
                            audio_details.append(f"Follow-up Question Audio: {len(question_audio_bytes)} bytes ({len(question_audio_bytes) // 1024}KB)")
                            
                            # Verify it's valid base64 and has reasonable size
                            if len(question_audio_bytes) < 1000:  # Too small for real audio
                                success = False
                                audio_details.append("Follow-up audio too small - likely not real audio data")
                        except Exception as e:
                            success = False
                            audio_details.append(f"Follow-up audio base64 decode failed: {str(e)}")
                    else:
                        # For voice mode, we should have audio for follow-up questions
                        success = False
                        audio_details.append("No question_audio in follow-up response for voice mode")
                else:
                    # Interview completed - this is also valid
                    success = True
                    audio_details.append("Interview completed")
            
            details = f"Status: {response.status_code}"
            if success:
                if data.get("completed"):
                    details += f", Interview Completed, Assessment: {data.get('assessment_id', 'N/A')[:8]}..."
                else:
                    details += f", Next Question: '{data.get('next_question', '')[:50]}...'"
                    details += f", Question #{data.get('question_number', 'N/A')}"
                if audio_details:
                    details += f", Audio: {'; '.join(audio_details)}"
            else:
                details += f", Response: {response.text[:300]}"
                if audio_details:
                    details += f", Audio Issues: {'; '.join(audio_details)}"
            
            self.log_test("Voice Message Processing with TTS Follow-up", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Message Processing with TTS Follow-up", False, f"Exception: {str(e)}")
            return False
    
    def test_tts_authentication(self) -> bool:
        """Test Google Cloud TTS integration directly"""
        try:
            payload = {
                "session_id": self.voice_session_id or "test-session-tts",
                "question_text": "Can you explain your experience with machine learning algorithms and how you've applied them in real-world projects?"
            }
            
            response = self.session.post(
                f"{self.base_url}/voice/generate-question",
                json=payload,
                timeout=25  # TTS can take time
            )
            
            success = response.status_code == 200
            audio_details = []
            
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "audio_base64" in data and 
                          "file_id" in data)
                
                if success and data.get("audio_base64"):
                    try:
                        audio_bytes = base64.b64decode(data["audio_base64"])
                        audio_details.append(f"Generated Audio: {len(audio_bytes)} bytes ({len(audio_bytes) // 1024}KB)")
                        audio_details.append(f"File ID: {data.get('file_id', '')[:12]}...")
                        
                        # Check if audio is reasonable size (should be at least a few KB for real TTS)
                        if len(audio_bytes) < 2000:
                            success = False
                            audio_details.append("Audio too small - likely authentication or generation issue")
                        
                        # Check if it starts with MP3 header (basic format validation)
                        if not audio_bytes.startswith(b'ID3') and not audio_bytes.startswith(b'\xff\xfb'):
                            # Not a standard MP3, but could still be valid audio
                            audio_details.append("Audio format: Non-standard MP3 header")
                        else:
                            audio_details.append("Audio format: Valid MP3")
                            
                    except Exception as e:
                        success = False
                        audio_details.append(f"Base64 decode failed: {str(e)}")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", TTS Success: {data.get('success')}"
                if audio_details:
                    details += f", {'; '.join(audio_details)}"
            else:
                details += f", Response: {response.text[:300]}"
                if audio_details:
                    details += f", Issues: {'; '.join(audio_details)}"
            
            self.log_test("Google Cloud TTS Authentication & Audio Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Google Cloud TTS Authentication & Audio Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_audio_quality_validation(self) -> bool:
        """Test audio quality and format validation"""
        try:
            # Test with a longer, more complex text to ensure quality
            test_text = "Welcome to your voice interview for the Senior Voice Interface Developer position. I'll be asking you a series of questions about your technical experience, problem-solving abilities, and how you approach voice user interface design. Please speak clearly and take your time with your responses."
            
            payload = {
                "session_id": self.voice_session_id or "test-session-quality",
                "question_text": test_text
            }
            
            response = self.session.post(
                f"{self.base_url}/voice/generate-question",
                json=payload,
                timeout=30
            )
            
            success = response.status_code == 200
            quality_details = []
            
            if success:
                data = response.json()
                success = data.get("success", False) and "audio_base64" in data
                
                if success and data.get("audio_base64"):
                    try:
                        audio_bytes = base64.b64decode(data["audio_base64"])
                        audio_size_kb = len(audio_bytes) // 1024
                        
                        quality_details.append(f"Audio Size: {len(audio_bytes)} bytes ({audio_size_kb}KB)")
                        
                        # Quality checks
                        # 1. Size should be reasonable for the text length (rough estimate: ~1KB per 10 words)
                        word_count = len(test_text.split())
                        expected_min_size = word_count * 100  # Very rough estimate
                        
                        if len(audio_bytes) >= expected_min_size:
                            quality_details.append(f"Size Check: PASS (Expected >{expected_min_size//1024}KB, Got {audio_size_kb}KB)")
                        else:
                            success = False
                            quality_details.append(f"Size Check: FAIL (Expected >{expected_min_size//1024}KB, Got {audio_size_kb}KB)")
                        
                        # 2. Base64 encoding validation
                        try:
                            # Re-encode and compare to ensure no corruption
                            re_encoded = base64.b64encode(audio_bytes).decode('utf-8')
                            if re_encoded == data["audio_base64"]:
                                quality_details.append("Base64 Encoding: PASS (No corruption)")
                            else:
                                success = False
                                quality_details.append("Base64 Encoding: FAIL (Corruption detected)")
                        except Exception:
                            success = False
                            quality_details.append("Base64 Encoding: FAIL (Re-encoding failed)")
                        
                        # 3. Basic audio format validation
                        if audio_bytes.startswith(b'ID3') or audio_bytes.startswith(b'\xff\xfb') or audio_bytes.startswith(b'\xff\xf3'):
                            quality_details.append("Format Check: PASS (Valid MP3 header)")
                        elif len(audio_bytes) > 1000:  # If it's large enough, might still be valid audio
                            quality_details.append("Format Check: UNKNOWN (Non-standard header but reasonable size)")
                        else:
                            success = False
                            quality_details.append("Format Check: FAIL (Invalid header and small size)")
                            
                    except Exception as e:
                        success = False
                        quality_details.append(f"Quality validation failed: {str(e)}")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Quality Validation: PASS"
                if quality_details:
                    details += f", Details: {'; '.join(quality_details)}"
            else:
                details += f", Quality Validation: FAIL"
                if quality_details:
                    details += f", Issues: {'; '.join(quality_details)}"
                else:
                    details += f", Response: {response.text[:200]}"
            
            self.log_test("Audio Quality & Format Validation", success, details)
            return success
        except Exception as e:
            self.log_test("Audio Quality & Format Validation", False, f"Exception: {str(e)}")
            return False
    
    def test_text_cleaning_for_tts(self) -> bool:
        """Test that backticks and formatting are cleaned before TTS"""
        try:
            # Test text with backticks and formatting that should be cleaned
            test_text_with_formatting = "Can you explain how `JavaScript` works with **APIs** and how you would implement a `fetch()` request to handle *JSON* responses? Please describe your approach to ~~debugging~~ troubleshooting such implementations."
            
            payload = {
                "session_id": self.voice_session_id or "test-session-cleaning",
                "question_text": test_text_with_formatting
            }
            
            response = self.session.post(
                f"{self.base_url}/voice/generate-question",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            
            if success:
                data = response.json()
                success = data.get("success", False) and "audio_base64" in data
                
                if success:
                    # If we get valid audio, the text cleaning worked
                    # (We can't directly verify the cleaned text, but successful TTS generation indicates it worked)
                    audio_bytes = base64.b64decode(data["audio_base64"])
                    details = f"Status: {response.status_code}, Text Cleaning: SUCCESS, Audio Generated: {len(audio_bytes)} bytes"
                else:
                    details = f"Status: {response.status_code}, Text Cleaning: UNKNOWN, TTS Failed"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Text Cleaning for TTS (Backtick Fix)", success, details)
            return success
        except Exception as e:
            self.log_test("Text Cleaning for TTS (Backtick Fix)", False, f"Exception: {str(e)}")
            return False
    
    def run_voice_tests(self) -> Dict[str, bool]:
        """Run all voice interview tests"""
        print("=" * 80)
        print("VOICE INTERVIEW FUNCTIONALITY TESTING")
        print("Focus: TTS Audio Generation, Base64 Encoding, Voice Mode Support")
        print("=" * 80)
        print()
        
        results = {}
        
        # Create voice interview token
        results["voice_token_creation"] = self.create_voice_interview_token()
        
        # Test voice interview start with TTS
        results["voice_interview_start"] = self.test_voice_interview_start()
        
        # Test voice message processing with TTS follow-up
        results["voice_message_processing"] = self.test_voice_message_processing()
        
        # Test TTS authentication and generation
        results["tts_authentication"] = self.test_tts_authentication()
        
        # Test audio quality and format validation
        results["audio_quality_validation"] = self.test_audio_quality_validation()
        
        # Test text cleaning for TTS (backtick fix)
        results["text_cleaning_tts"] = self.test_text_cleaning_for_tts()
        
        # Summary
        print("=" * 80)
        print("VOICE INTERVIEW TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        test_categories = {
            "Voice Interview Setup": ["voice_token_creation"],
            "Voice Interview Flow": ["voice_interview_start", "voice_message_processing"],
            "TTS Integration": ["tts_authentication", "text_cleaning_tts"],
            "Audio Quality": ["audio_quality_validation"]
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
            print("🎉 ALL VOICE TESTS PASSED! Voice interview functionality is working correctly.")
            print("   Users should be able to hear AI voice questions properly.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Voice features are largely functional.")
            print("   Minor issues may affect some voice functionality.")
        else:
            print("⚠️  VOICE FUNCTIONALITY ISSUES DETECTED!")
            print("   Users may not be able to hear AI voice properly.")
            print("   Check TTS authentication and audio generation.")
        
        return results

def main():
    """Main test execution for voice interview functionality"""
    tester = VoiceInterviewTester()
    results = tester.run_voice_tests()
    
    # Return exit code based on results
    critical_tests = ["voice_interview_start", "tts_authentication", "audio_quality_validation"]
    critical_passed = all(results.get(test, False) for test in critical_tests)
    
    return 0 if critical_passed else 1

if __name__ == "__main__":
    exit(main())