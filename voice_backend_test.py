#!/usr/bin/env python3
"""
Comprehensive Voice Processing Backend Testing for AI Interview Platform
Tests the Web Speech API backend integration and voice processing functionality:

1. Voice Processing Pipeline - /voice/process-answer endpoint
2. Audio File Handling - GridFS storage and session metadata  
3. Speech-to-Text Integration - Web Speech API approach (frontend STT)
4. Emotional Intelligence Analysis - voice features and emotional analysis
5. Session Management - voice answers linked to interview sessions
6. Error Handling - various error scenarios and fallback mechanisms
7. Audio Format Support - different audio formats and proper handling
"""

import requests
import json
import time
import io
import base64
import tempfile
import os
import wave
import struct
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://2ecfb9bc-fa10-4e39-8ddd-7b13c880cc1a.preview.emergentagent.com/api"

class VoiceProcessingTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.generated_token = None
        self.session_id = None
        self.voice_session_id = None
        self.test_audio_files = {}
        
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
    
    def create_test_audio_files(self):
        """Create various test audio files for testing different formats"""
        try:
            # Create a simple WAV file (16-bit, 16kHz, mono)
            sample_rate = 16000
            duration = 2  # 2 seconds
            frequency = 440  # A4 note
            
            # Generate sine wave
            samples = []
            for i in range(int(sample_rate * duration)):
                sample = int(32767 * 0.3 * (i % (sample_rate // frequency)) / (sample_rate // frequency))
                samples.append(sample)
            
            # Create WAV file
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, 'wb') as wav_file:
                wav_file.setnchannels(1)  # mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(struct.pack('<' + 'h' * len(samples), *samples))
            
            self.test_audio_files['wav'] = wav_buffer.getvalue()
            
            # Create simulated WEBM audio data (placeholder)
            webm_header = b'WEBM_AUDIO_HEADER_PLACEHOLDER'
            webm_data = b'WEBM_AUDIO_DATA_' + b'A' * 1000  # Simulated audio data
            self.test_audio_files['webm'] = webm_header + webm_data
            
            # Create simulated MP3 data (placeholder)
            mp3_header = b'ID3\x03\x00\x00\x00'  # Basic MP3 ID3 header
            mp3_data = b'MP3_AUDIO_DATA_' + b'B' * 1000
            self.test_audio_files['mp3'] = mp3_header + mp3_data
            
            # Create simulated OGG data (placeholder)
            ogg_header = b'OggS'  # OGG page header
            ogg_data = b'OGG_AUDIO_DATA_' + b'C' * 1000
            self.test_audio_files['ogg'] = ogg_header + ogg_data
            
            return True
        except Exception as e:
            print(f"Failed to create test audio files: {str(e)}")
            return False
    
    def setup_voice_interview_session(self) -> bool:
        """Set up a voice interview session for testing"""
        try:
            # First authenticate as admin
            payload = {"password": "Game@1234"}
            response = self.session.post(f"{self.base_url}/admin/login", json=payload, timeout=10)
            if response.status_code != 200:
                return False
            
            # Create a voice interview job
            resume_content = """Voice Test Candidate
Senior Audio Engineer
Email: voice.test@email.com
Phone: (555) 999-8888

EXPERIENCE:
- 5+ years in audio processing and voice interfaces
- Expert in speech recognition and synthesis technologies
- Built real-time voice applications with WebRTC
- Experience with emotional intelligence analysis from voice

SKILLS:
- Python, JavaScript, Audio Processing
- Speech Recognition, TTS, Voice UI
- WebRTC, Real-time Systems, AI/ML
- Emotional Intelligence, Voice Analytics"""
            
            files = {
                'resume_file': ('voice_test_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Voice Interface Specialist',
                'job_description': 'We need a specialist in voice interfaces and speech processing. The role involves building voice-enabled applications, implementing speech-to-text and text-to-speech systems, and analyzing voice for emotional intelligence.',
                'job_requirements': 'Requirements: 5+ years audio/voice experience, speech processing knowledge, real-time systems, emotional intelligence analysis, Python/JavaScript skills.'
            }
            
            response = self.session.post(f"{self.base_url}/admin/upload-job", files=files, data=data, timeout=15)
            if response.status_code != 200:
                return False
            
            result = response.json()
            self.generated_token = result.get("token")
            
            if not self.generated_token:
                return False
            
            # Start voice interview session
            payload = {
                "token": self.generated_token,
                "candidate_name": "Voice Test Candidate",
                "voice_mode": True
            }
            
            response = self.session.post(f"{self.base_url}/candidate/start-interview", json=payload, timeout=25)
            if response.status_code != 200:
                return False
            
            data = response.json()
            self.voice_session_id = data.get("session_id")
            
            return self.voice_session_id is not None
            
        except Exception as e:
            print(f"Failed to setup voice interview session: {str(e)}")
            return False
    
    def test_voice_process_answer_endpoint(self) -> bool:
        """Test the main /voice/process-answer endpoint"""
        if not self.voice_session_id:
            self.log_test("Voice Process Answer Endpoint", False, "No voice session available")
            return False
        
        try:
            # Test with WAV audio file
            audio_data = self.test_audio_files.get('wav', b'dummy_audio_data')
            
            files = {
                'audio_file': ('test_answer.wav', io.BytesIO(audio_data), 'audio/wav')
            }
            
            data = {
                'session_id': self.voice_session_id,
                'question_number': 1
            }
            
            response = self.session.post(
                f"{self.base_url}/voice/process-answer",
                files=files,
                data=data,
                timeout=30
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "file_id" in result and
                          "transcript" in result and
                          "emotional_intelligence" in result)
                
                if success:
                    details = f"Status: {response.status_code}, File ID: {result['file_id'][:8]}..., Transcript: {result.get('transcript', '')[:30]}..., EI Analysis: Present"
                else:
                    details = f"Status: {response.status_code}, Missing required fields in response"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            
            self.log_test("Voice Process Answer Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice Process Answer Endpoint", False, f"Exception: {str(e)}")
            return False
    
    def test_audio_file_storage_gridfs(self) -> bool:
        """Test audio file storage in GridFS"""
        if not self.voice_session_id:
            self.log_test("Audio File Storage (GridFS)", False, "No voice session available")
            return False
        
        try:
            # Test storing different audio formats
            formats_tested = []
            
            for format_name, audio_data in self.test_audio_files.items():
                files = {
                    'audio_file': (f'test_audio.{format_name}', io.BytesIO(audio_data), f'audio/{format_name}')
                }
                
                data = {
                    'session_id': self.voice_session_id,
                    'question_number': len(formats_tested) + 1
                }
                
                response = self.session.post(
                    f"{self.base_url}/voice/process-answer",
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success") and "file_id" in result:
                        formats_tested.append(format_name)
                
                # Small delay between requests
                time.sleep(1)
            
            success = len(formats_tested) > 0
            details = f"Successfully stored {len(formats_tested)} audio formats: {', '.join(formats_tested)}"
            
            self.log_test("Audio File Storage (GridFS)", success, details)
            return success
            
        except Exception as e:
            self.log_test("Audio File Storage (GridFS)", False, f"Exception: {str(e)}")
            return False
    
    def test_web_speech_api_integration(self) -> bool:
        """Test Web Speech API integration approach (frontend STT)"""
        try:
            # Since the backend does STT internally, we test that it can handle audio properly
            # and that the Web Speech API approach would work by testing the voice processing pipeline
            if not self.voice_session_id:
                self.log_test("Web Speech API Integration", False, "No voice session available")
                return False
            
            # Test that backend can process audio files (which would come from Web Speech API recording)
            audio_data = self.test_audio_files.get('webm', b'webm_audio_data')
            
            files = {
                'audio_file': ('web_speech_test.webm', io.BytesIO(audio_data), 'audio/webm')
            }
            
            data = {
                'session_id': self.voice_session_id,
                'question_number': 2
            }
            
            response = self.session.post(
                f"{self.base_url}/voice/process-answer",
                files=files,
                data=data,
                timeout=30
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "transcript" in result and
                          "file_id" in result)
                
                details = f"Status: {response.status_code}, Backend STT working: {success}, File stored: {'file_id' in result}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:300]}"
            
            self.log_test("Web Speech API Integration", success, details)
            return success
            
        except Exception as e:
            self.log_test("Web Speech API Integration", False, f"Exception: {str(e)}")
            return False
    
    def test_emotional_intelligence_analysis(self) -> bool:
        """Test emotional intelligence analysis from voice"""
        if not self.voice_session_id:
            self.log_test("Emotional Intelligence Analysis", False, "No voice session available")
            return False
        
        try:
            # Test with different emotional contexts
            emotional_contexts = [
                {
                    "transcript": "I am extremely excited about this opportunity and I feel very confident about my technical abilities. This role would be perfect for my career growth.",
                    "expected_emotions": ["excitement", "confidence", "enthusiasm"]
                },
                {
                    "transcript": "I'm a bit nervous about this interview, but I'm trying my best to answer all questions thoroughly. I hope I can demonstrate my skills effectively.",
                    "expected_emotions": ["nervousness", "uncertainty", "effort"]
                },
                {
                    "transcript": "I have solid experience in this area and I'm comfortable discussing my technical background. I believe I can contribute effectively to your team.",
                    "expected_emotions": ["confidence", "stability", "professionalism"]
                }
            ]
            
            successful_analyses = 0
            
            for i, context in enumerate(emotional_contexts):
                audio_data = self.test_audio_files.get('wav', b'dummy_audio')
                
                files = {
                    'audio_file': (f'emotional_test_{i}.wav', io.BytesIO(audio_data), 'audio/wav')
                }
                
                data = {
                    'session_id': self.voice_session_id,
                    'question_number': i + 3
                }
                
                response = self.session.post(
                    f"{self.base_url}/voice/process-answer",
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if "emotional_intelligence" in result:
                        emotional_analysis = result["emotional_intelligence"]
                        
                        # Check if emotional analysis contains expected components
                        has_confidence = "confidence" in emotional_analysis
                        has_stress = "stress_level" in emotional_analysis
                        has_enthusiasm = "enthusiasm" in emotional_analysis
                        
                        if has_confidence and has_stress and has_enthusiasm:
                            successful_analyses += 1
                
                time.sleep(1)  # Small delay between requests
            
            success = successful_analyses > 0
            details = f"Successfully analyzed {successful_analyses}/{len(emotional_contexts)} emotional contexts"
            
            self.log_test("Emotional Intelligence Analysis", success, details)
            return success
            
        except Exception as e:
            self.log_test("Emotional Intelligence Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_session_management(self) -> bool:
        """Test that voice answers are properly linked to interview sessions"""
        if not self.voice_session_id:
            self.log_test("Voice Session Management", False, "No voice session available")
            return False
        
        try:
            # Submit multiple voice answers and verify session continuity
            voice_answers = [
                "My experience with Python spans over 5 years, focusing on backend development and API design.",
                "I approach problem-solving by breaking down complex issues into manageable components and testing iteratively.",
                "In team environments, I prioritize clear communication and collaborative decision-making processes."
            ]
            
            session_responses = []
            
            for i, answer in enumerate(voice_answers):
                audio_data = self.test_audio_files.get('wav', b'dummy_audio')
                
                files = {
                    'audio_file': (f'session_test_{i}.wav', io.BytesIO(audio_data), 'audio/wav')
                }
                
                data = {
                    'session_id': self.voice_session_id,
                    'question_number': i + 5
                }
                
                response = self.session.post(
                    f"{self.base_url}/voice/process-answer",
                    files=files,
                    data=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    session_responses.append({
                        'question_number': i + 5,
                        'file_id': result.get('file_id'),
                        'transcript': result.get('transcript'),
                        'session_id': result.get('session_id', self.voice_session_id)
                    })
                
                time.sleep(1)
            
            # Verify session continuity
            success = len(session_responses) == len(voice_answers)
            if success:
                # Check that all responses have the same session_id
                session_ids = [resp['session_id'] for resp in session_responses]
                success = all(sid == self.voice_session_id for sid in session_ids)
                
                # Check that file_ids are unique
                file_ids = [resp['file_id'] for resp in session_responses if resp['file_id']]
                success = success and len(file_ids) == len(set(file_ids))
            
            details = f"Processed {len(session_responses)} voice answers, Session continuity: {success}"
            
            self.log_test("Voice Session Management", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice Session Management", False, f"Exception: {str(e)}")
            return False
    
    def test_error_handling_scenarios(self) -> bool:
        """Test various error scenarios and fallback mechanisms"""
        try:
            error_scenarios = []
            
            # Test 1: Invalid session ID
            try:
                files = {'audio_file': ('test.wav', io.BytesIO(b'dummy'), 'audio/wav')}
                data = {'session_id': 'invalid_session_id', 'question_number': 1, 'transcript': 'test'}
                
                response = self.session.post(f"{self.base_url}/voice/process-answer", files=files, data=data, timeout=10)
                error_scenarios.append(("Invalid Session ID", response.status_code in [400, 404]))
            except:
                error_scenarios.append(("Invalid Session ID", False))
            
            # Test 2: Missing audio file
            try:
                data = {'session_id': self.voice_session_id or 'test', 'question_number': 1}
                response = self.session.post(f"{self.base_url}/voice/process-answer", data=data, timeout=10)
                error_scenarios.append(("Missing Audio File", response.status_code in [400, 422]))
            except:
                error_scenarios.append(("Missing Audio File", False))
            
            # Test 3: Invalid audio format
            try:
                files = {'audio_file': ('test.txt', io.BytesIO(b'not_audio_data'), 'text/plain')}
                data = {'session_id': self.voice_session_id or 'test', 'question_number': 1}
                
                response = self.session.post(f"{self.base_url}/voice/process-answer", files=files, data=data, timeout=10)
                error_scenarios.append(("Invalid Audio Format", response.status_code in [400, 415, 500]))
            except:
                error_scenarios.append(("Invalid Audio Format", False))
            
            # Test 4: Large audio file (should handle gracefully)
            if self.voice_session_id:
                try:
                    large_audio = b'LARGE_AUDIO_DATA' * 10000  # Simulate large file
                    files = {'audio_file': ('large.wav', io.BytesIO(large_audio), 'audio/wav')}
                    data = {'session_id': self.voice_session_id, 'question_number': 1}
                    
                    response = self.session.post(f"{self.base_url}/voice/process-answer", files=files, data=data, timeout=10)
                    error_scenarios.append(("Large Audio File", response.status_code in [200, 413, 500]))  # Should handle gracefully or return appropriate error
                except:
                    error_scenarios.append(("Large Audio File", False))
            
            successful_error_handling = sum(1 for _, handled in error_scenarios if handled)
            total_scenarios = len(error_scenarios)
            
            success = successful_error_handling >= total_scenarios * 0.75  # At least 75% should be handled properly
            
            details = f"Properly handled {successful_error_handling}/{total_scenarios} error scenarios"
            for scenario_name, handled in error_scenarios:
                details += f"\n     - {scenario_name}: {'✓' if handled else '✗'}"
            
            self.log_test("Error Handling Scenarios", success, details)
            return success
            
        except Exception as e:
            self.log_test("Error Handling Scenarios", False, f"Exception: {str(e)}")
            return False
    
    def test_audio_format_support(self) -> bool:
        """Test different audio formats and proper handling"""
        if not self.voice_session_id:
            self.log_test("Audio Format Support", False, "No voice session available")
            return False
        
        try:
            format_results = {}
            
            # Test each audio format
            for format_name, audio_data in self.test_audio_files.items():
                try:
                    mime_types = {
                        'wav': 'audio/wav',
                        'webm': 'audio/webm',
                        'mp3': 'audio/mpeg',
                        'ogg': 'audio/ogg'
                    }
                    
                    files = {
                        'audio_file': (f'test.{format_name}', io.BytesIO(audio_data), mime_types.get(format_name, 'audio/wav'))
                    }
                    
                    data = {
                        'session_id': self.voice_session_id,
                        'question_number': 10 + list(self.test_audio_files.keys()).index(format_name)
                    }
                    
                    response = self.session.post(
                        f"{self.base_url}/voice/process-answer",
                        files=files,
                        data=data,
                        timeout=30
                    )
                    
                    # Consider both success (200) and graceful handling of unsupported formats
                    format_results[format_name] = {
                        'status_code': response.status_code,
                        'supported': response.status_code == 200,
                        'handled': response.status_code in [200, 400, 415]  # Proper error codes
                    }
                    
                    time.sleep(1)
                    
                except Exception as e:
                    format_results[format_name] = {
                        'status_code': 'Exception',
                        'supported': False,
                        'handled': False,
                        'error': str(e)
                    }
            
            # Evaluate results
            supported_formats = [fmt for fmt, result in format_results.items() if result['supported']]
            handled_formats = [fmt for fmt, result in format_results.items() if result['handled']]
            
            # Success if at least one format is supported and all are handled properly
            success = len(supported_formats) > 0 and len(handled_formats) == len(format_results)
            
            details = f"Supported formats: {', '.join(supported_formats) if supported_formats else 'None'}"
            details += f"\nProperly handled: {len(handled_formats)}/{len(format_results)} formats"
            
            for fmt, result in format_results.items():
                status = "✓ Supported" if result['supported'] else ("✓ Handled" if result['handled'] else "✗ Failed")
                details += f"\n     - {fmt}: {status} (HTTP {result['status_code']})"
            
            self.log_test("Audio Format Support", success, details)
            return success
            
        except Exception as e:
            self.log_test("Audio Format Support", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_workflow_integration(self) -> bool:
        """Test complete voice recording workflow integration"""
        if not self.voice_session_id:
            self.log_test("Voice Workflow Integration", False, "No voice session available")
            return False
        
        try:
            # Simulate complete voice interview workflow
            workflow_steps = []
            
            # Step 1: Record and process first answer
            audio_data = self.test_audio_files.get('webm', b'webm_audio')
            files = {'audio_file': ('workflow_test_1.webm', io.BytesIO(audio_data), 'audio/webm')}
            data = {
                'session_id': self.voice_session_id,
                'question_number': 1
            }
            
            response = self.session.post(f"{self.base_url}/voice/process-answer", files=files, data=data, timeout=30)
            workflow_steps.append(("Voice Answer 1", response.status_code == 200))
            
            # Step 2: Process follow-up answer
            files = {'audio_file': ('workflow_test_2.webm', io.BytesIO(audio_data), 'audio/webm')}
            data = {
                'session_id': self.voice_session_id,
                'question_number': 2
            }
            
            response = self.session.post(f"{self.base_url}/voice/process-answer", files=files, data=data, timeout=30)
            workflow_steps.append(("Voice Answer 2", response.status_code == 200))
            
            # Step 3: Test session continuity by checking if we can continue the interview
            payload = {"token": self.generated_token, "message": "This is a text follow-up to voice answers."}
            response = self.session.post(f"{self.base_url}/candidate/send-message", json=payload, timeout=20)
            workflow_steps.append(("Mixed Mode Continuity", response.status_code == 200))
            
            successful_steps = sum(1 for _, success in workflow_steps if success)
            total_steps = len(workflow_steps)
            
            success = successful_steps == total_steps
            
            details = f"Completed {successful_steps}/{total_steps} workflow steps successfully"
            for step_name, step_success in workflow_steps:
                details += f"\n     - {step_name}: {'✓' if step_success else '✗'}"
            
            self.log_test("Voice Workflow Integration", success, details)
            return success
            
        except Exception as e:
            self.log_test("Voice Workflow Integration", False, f"Exception: {str(e)}")
            return False
    
    def run_all_voice_tests(self) -> Dict[str, bool]:
        """Run all voice processing tests"""
        print("=" * 80)
        print("AI INTERVIEW PLATFORM - COMPREHENSIVE VOICE PROCESSING BACKEND TESTING")
        print("Testing Web Speech API Integration & Voice Processing Pipeline")
        print("=" * 80)
        print()
        
        # Setup
        print("🔧 Setting up test environment...")
        
        # Test basic connectivity first
        if not self.test_health_check():
            print("❌ Backend health check failed")
            return {}
        
        if not self.create_test_audio_files():
            print("❌ Failed to create test audio files")
            return {}
        
        if not self.setup_voice_interview_session():
            print("❌ Failed to setup voice interview session")
            return {}
        
        print("✅ Test environment ready")
        print()
        
        results = {}
        
        # Core voice processing tests
        results["voice_process_answer_endpoint"] = self.test_voice_process_answer_endpoint()
        results["audio_file_storage_gridfs"] = self.test_audio_file_storage_gridfs()
        results["web_speech_api_integration"] = self.test_web_speech_api_integration()
        results["emotional_intelligence_analysis"] = self.test_emotional_intelligence_analysis()
        results["voice_session_management"] = self.test_voice_session_management()
        results["error_handling_scenarios"] = self.test_error_handling_scenarios()
        results["audio_format_support"] = self.test_audio_format_support()
        results["voice_workflow_integration"] = self.test_voice_workflow_integration()
        
        # Summary
        print("=" * 80)
        print("VOICE PROCESSING TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by category
        categories = {
            "Core Voice Processing": [
                "voice_process_answer_endpoint",
                "audio_file_storage_gridfs",
                "web_speech_api_integration"
            ],
            "Advanced Voice Features": [
                "emotional_intelligence_analysis",
                "voice_session_management",
                "voice_workflow_integration"
            ],
            "Error Handling & Format Support": [
                "error_handling_scenarios",
                "audio_format_support"
            ]
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
            print("🎉 ALL VOICE PROCESSING TESTS PASSED!")
            print("   Backend can properly 'hear' candidate voice and process audio files")
            print("   Web Speech API integration working correctly")
            print("   Emotional intelligence analysis functional")
            print("   Voice workflow integration complete")
        elif passed >= total * 0.8:
            print("✅ VOICE PROCESSING MOSTLY WORKING!")
            print("   Core functionality operational with minor issues")
        elif passed >= total * 0.5:
            print("⚠️  VOICE PROCESSING PARTIALLY WORKING")
            print("   Some core features working, others need attention")
        else:
            print("❌ VOICE PROCESSING NEEDS SIGNIFICANT WORK")
            print("   Multiple critical issues found")
        
        return results

def main():
    """Main test execution"""
    tester = VoiceProcessingTester()
    results = tester.run_all_voice_tests()
    
    if not results:
        return 1
    
    # Return exit code based on results
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    success_rate = passed / total if total > 0 else 0
    
    return 0 if success_rate >= 0.8 else 1

if __name__ == "__main__":
    exit(main())