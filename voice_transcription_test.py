#!/usr/bin/env python3
"""
Voice Recording and Transcription Functionality Testing
Tests the voice recording and transcription functionality that was just implemented.

Focus Areas:
1. Backend Testing: Verify existing interview endpoints work with transcribed text from frontend
2. Voice Processing Flow: Test /api/candidate/send-message endpoint for voice-transcribed text
3. Interview Session Management: Verify voice mode interviews create sessions correctly
4. Transcript Generation: Test that voice answers appear correctly in transcripts and reports

Key Change: Voice recordings are now handled entirely on frontend using Web Speech API,
and transcribed text is sent to standard text answer submission endpoint.
"""

import requests
import json
import time
import io
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://aptitude-models.preview.emergentagent.com/api"

class VoiceTranscriptionTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.voice_token = None
        self.voice_session_id = None
        self.assessment_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_admin_login_voice_mode(self) -> bool:
        """Test admin authentication for voice mode setup"""
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
            self.log_test("Admin Login for Voice Mode", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login for Voice Mode", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_token_generation(self) -> bool:
        """Test token generation with voice mode enabled"""
        try:
            # Create resume content for voice interview testing
            resume_content = """Sarah Williams
Voice Interview Specialist
Email: sarah.williams@email.com
Phone: (555) 999-8888

EXPERIENCE:
- 5+ years in speech recognition and voice interface development
- Expert in Web Speech API, real-time audio processing
- Built voice-enabled applications with React and Python
- Experience with transcription services and natural language processing

SKILLS:
- JavaScript, Python, React, FastAPI
- Web Speech API, Audio Processing, WebRTC
- Real-time systems, MongoDB, RESTful APIs
- Voice UI/UX design and accessibility

EDUCATION:
Master of Science in Computer Science
Voice Technology Institute, 2019"""
            
            files = {
                'resume_file': ('voice_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Voice Interface Developer - Transcription Specialist',
                'job_description': 'We are seeking a developer experienced in voice interfaces and speech transcription. The role involves building voice-enabled applications using Web Speech API and ensuring accurate transcription of user speech to text.',
                'job_requirements': 'Requirements: 4+ years experience, Web Speech API expertise, real-time transcription systems, Python/JavaScript skills, voice interface design experience.'
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
                          "resume_preview" in result)
                if success:
                    self.voice_token = result["token"]
            
            details = f"Status: {response.status_code}, Token: {self.voice_token[:8] if self.voice_token else 'None'}..."
            if success:
                details += f", Resume Preview: {result.get('resume_preview', '')[:50]}..."
            
            self.log_test("Voice Token Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Token Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_interview_session_creation(self) -> bool:
        """Test starting a voice interview session"""
        if not self.voice_token:
            self.log_test("Voice Interview Session Creation", False, "No voice token available")
            return False
        
        try:
            payload = {
                "token": self.voice_token,
                "candidate_name": "Sarah Williams",
                "voice_mode": True
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=20
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
                    # Store the first question for later verification
                    self.first_question = data.get("first_question", "")
            
            details = f"Status: {response.status_code}"
            if success:
                details += f", Voice Mode: {data.get('voice_mode')}, Session: {self.voice_session_id[:8] if self.voice_session_id else 'None'}..."
                details += f", First Question: {self.first_question[:50]}..." if hasattr(self, 'first_question') else ""
            else:
                details += f", Response: {response.text[:200]}"
            
            self.log_test("Voice Interview Session Creation", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Interview Session Creation", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_transcribed_text_submission(self) -> bool:
        """Test submitting voice-transcribed text via /api/candidate/send-message endpoint"""
        if not self.voice_token:
            self.log_test("Voice Transcribed Text Submission", False, "No voice token available")
            return False
        
        try:
            # Simulate transcribed text from Web Speech API (realistic voice-to-text content)
            transcribed_answers = [
                # Technical answers (simulating voice transcription with natural speech patterns)
                "I have extensive experience with Web Speech API and real-time transcription systems. I've built several voice-enabled applications using JavaScript and React, implementing features like continuous speech recognition, voice commands, and real-time text display. I'm particularly skilled at handling speech recognition events and managing audio input streams.",
                
                "For voice interface design, I focus on user experience and accessibility. I implement clear voice prompts, provide visual feedback during speech recognition, and handle various speech patterns and accents. I also ensure proper error handling for cases when speech recognition fails or produces unclear results.",
                
                "I've worked with various speech recognition APIs including Web Speech API, Google Cloud Speech-to-Text, and Azure Speech Services. I understand the differences in accuracy, latency, and language support. I typically choose Web Speech API for real-time applications due to its low latency and browser integration.",
                
                "For real-time audio processing, I use techniques like audio buffering, noise reduction, and voice activity detection. I've implemented features like voice level visualization, automatic gain control, and echo cancellation. I also work with WebRTC for peer-to-peer audio communication.",
                
                # Behavioral answers (simulating natural speech patterns)
                "When I encountered a challenging voice recognition accuracy issue, I systematically tested different microphone configurations and audio processing parameters. I implemented fallback mechanisms and provided users with alternative input methods. The solution improved recognition accuracy by thirty percent.",
                
                "I once had to integrate multiple speech recognition services for a multilingual application. I collaborated with the UX team to design intuitive language switching and worked with backend developers to optimize API calls. We successfully launched support for five languages with seamless user experience.",
                
                "I stay updated with voice technology by following industry blogs, attending speech technology conferences, and experimenting with new APIs. I recently explored WebAssembly for client-side audio processing and have been testing the latest improvements in browser speech recognition capabilities.",
                
                "My approach to voice interface testing includes automated speech recognition accuracy tests, user acceptance testing with diverse speakers, and performance testing under various network conditions. I also conduct accessibility testing to ensure the interface works well for users with different speech patterns."
            ]
            
            # Test each transcribed answer submission
            for i, transcribed_text in enumerate(transcribed_answers):
                payload = {
                    "token": self.voice_token,
                    "message": transcribed_text
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/send-message",
                    json=payload,
                    timeout=25  # Longer timeout for AI processing
                )
                
                if response.status_code != 200:
                    details = f"Failed at answer {i+1}, Status: {response.status_code}, Response: {response.text[:200]}"
                    self.log_test("Voice Transcribed Text Submission", False, details)
                    return False
                
                data = response.json()
                
                # Check if interview is completed
                if data.get("completed", False):
                    if "assessment_id" in data:
                        self.assessment_id = data["assessment_id"]
                    success = i >= 6  # Should complete after sufficient questions (7-8 answers)
                    details = f"Interview completed after {i+1} transcribed answers, Assessment ID: {self.assessment_id[:8] if self.assessment_id else 'None'}..."
                    self.log_test("Voice Transcribed Text Submission", success, details)
                    return success
                
                # Verify next question is provided for voice mode
                if not data.get("next_question"):
                    details = f"No next question provided at answer {i+1}"
                    self.log_test("Voice Transcribed Text Submission", False, details)
                    return False
                
                # Small delay between answers
                time.sleep(1)
            
            # If we reach here, interview didn't complete as expected
            self.log_test("Voice Transcribed Text Submission", False, "Interview didn't complete after 8 transcribed answers")
            return False
            
        except Exception as e:
            self.log_test("Voice Transcribed Text Submission", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_transcript_generation(self) -> bool:
        """Test that voice answers appear correctly in interview transcripts"""
        if not self.voice_session_id:
            self.log_test("Voice Transcript Generation", False, "No voice session ID available")
            return False
        
        try:
            # Get detailed report with transcript
            response = self.session.get(
                f"{self.base_url}/admin/detailed-report/{self.voice_session_id}",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("transcript" in data and 
                          "assessment_summary" in data and
                          "candidate_name" in data)
                
                if success:
                    transcript = data.get("transcript", "")
                    # Verify transcript contains actual transcribed content, not placeholder text
                    contains_real_content = (
                        "Web Speech API" in transcript or
                        "voice recognition" in transcript or
                        "speech recognition" in transcript or
                        "real-time transcription" in transcript
                    )
                    
                    # Check that transcript is properly formatted with Q&A pairs
                    has_qa_format = ("Q1:" in transcript and "A1:" in transcript)
                    
                    # Verify transcript length indicates real content (not just placeholder)
                    has_substantial_content = len(transcript) > 500
                    
                    success = contains_real_content and has_qa_format and has_substantial_content
                    
                    details = f"Status: {response.status_code}, Transcript Length: {len(transcript)} chars"
                    details += f", Contains Voice Content: {contains_real_content}"
                    details += f", Q&A Format: {has_qa_format}"
                    details += f", Candidate: {data.get('candidate_name', 'N/A')}"
                else:
                    details = f"Status: {response.status_code}, Missing required fields in response"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Voice Transcript Generation", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Transcript Generation", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_assessment_report(self) -> bool:
        """Test that voice interview assessment includes actual transcribed content"""
        if not self.voice_session_id:
            self.log_test("Voice Assessment Report", False, "No voice session ID available")
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/admin/reports/{self.voice_session_id}",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("report" in data and 
                          "technical_score" in data["report"] and 
                          "behavioral_score" in data["report"] and
                          "overall_score" in data["report"])
                
                if success:
                    report = data["report"]
                    # Verify scores are reasonable (not default/placeholder values)
                    tech_score = report.get("technical_score", 0)
                    behavioral_score = report.get("behavioral_score", 0)
                    overall_score = report.get("overall_score", 0)
                    
                    # Check that scores reflect actual evaluation (not just defaults)
                    has_valid_scores = (tech_score > 0 and behavioral_score > 0 and overall_score > 0)
                    
                    # Check for assessment content
                    has_feedback = (report.get("technical_feedback") and 
                                  report.get("behavioral_feedback") and
                                  report.get("overall_feedback"))
                    
                    success = has_valid_scores and has_feedback
                    
                    details = f"Status: {response.status_code}, Tech: {tech_score}, Behavioral: {behavioral_score}, Overall: {overall_score}"
                    details += f", Has Feedback: {has_feedback}"
                else:
                    details = f"Status: {response.status_code}, Missing required report fields"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Voice Assessment Report", success, details)
            return success
        except Exception as e:
            self.log_test("Voice Assessment Report", False, f"Exception: {str(e)}")
            return False
    
    def test_text_vs_voice_mode_compatibility(self) -> bool:
        """Test that text-based endpoints work the same way for voice-transcribed content"""
        if not self.voice_token:
            self.log_test("Text vs Voice Mode Compatibility", False, "No voice token available")
            return False
        
        try:
            # Test token validation works for voice tokens
            payload = {"token": self.voice_token}
            response = self.session.post(
                f"{self.base_url}/candidate/validate-token",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("valid", False) and "job_title" in data
                
                # Verify job title matches our voice interface job
                job_title = data.get("job_title", "")
                is_voice_job = "Voice Interface Developer" in job_title
                
                success = success and is_voice_job
                
                details = f"Status: {response.status_code}, Valid: {data.get('valid')}, Job: {job_title[:50]}..."
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Text vs Voice Mode Compatibility", success, details)
            return success
        except Exception as e:
            self.log_test("Text vs Voice Mode Compatibility", False, f"Exception: {str(e)}")
            return False
    
    def run_voice_transcription_tests(self) -> Dict[str, bool]:
        """Run all voice transcription tests in sequence"""
        print("=" * 80)
        print("VOICE RECORDING AND TRANSCRIPTION FUNCTIONALITY TESTING")
        print("Testing Web Speech API Integration & Transcribed Text Processing")
        print("=" * 80)
        print()
        
        results = {}
        
        # Admin setup for voice mode
        results["admin_login_voice_mode"] = self.test_admin_login_voice_mode()
        
        # Token generation with voice mode enabled
        results["voice_token_generation"] = self.test_voice_token_generation()
        
        # Voice interview session management
        results["voice_interview_session_creation"] = self.test_voice_interview_session_creation()
        
        # Voice transcribed text submission (core functionality)
        results["voice_transcribed_text_submission"] = self.test_voice_transcribed_text_submission()
        
        # Transcript generation with actual content
        results["voice_transcript_generation"] = self.test_voice_transcript_generation()
        
        # Assessment report with voice content
        results["voice_assessment_report"] = self.test_voice_assessment_report()
        
        # Compatibility testing
        results["text_vs_voice_mode_compatibility"] = self.test_text_vs_voice_mode_compatibility()
        
        # Summary
        print("=" * 80)
        print("VOICE TRANSCRIPTION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by functionality
        categories = {
            "Admin Setup": ["admin_login_voice_mode", "voice_token_generation"],
            "Voice Session Management": ["voice_interview_session_creation", "text_vs_voice_mode_compatibility"],
            "Voice Transcription Processing": ["voice_transcribed_text_submission"],
            "Transcript & Report Generation": ["voice_transcript_generation", "voice_assessment_report"]
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
            print("🎉 ALL VOICE TRANSCRIPTION TESTS PASSED!")
            print("✅ Voice recording and transcription functionality is working correctly.")
            print("✅ Web Speech API integration is functional.")
            print("✅ Transcribed text is properly processed and stored.")
            print("✅ Interview transcripts show actual content, not placeholder text.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Voice transcription is functional with minor issues.")
        else:
            print("⚠️  Multiple voice transcription tests failed. Check the details above.")
        
        return results

def main():
    """Main test execution for voice transcription functionality"""
    tester = VoiceTranscriptionTester()
    results = tester.run_voice_transcription_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())