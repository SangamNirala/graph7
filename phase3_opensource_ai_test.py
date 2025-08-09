#!/usr/bin/env python3
"""
Phase 3: Open-Source AI Integration Testing
Tests the new Phase 3 implementation that replaces proprietary AI services with open-source alternatives.

KEY FEATURES TO TEST:
1. Step 7.1: Replace Proprietary AI Services
   - /api/ai/status endpoint for open-source AI engine initialization
   - /api/ai/analyze-question for BERT-based question analysis
   - /api/ai/generate-questions-opensource for GPT-style question generation
   - /api/ai/analyze-response-opensource for candidate response analysis

2. Step 7.2: Advanced Speech Analysis
   - /api/ai/analyze-speech for professional-grade voice assessment
   - /api/voice/analyze-enhanced for comprehensive speech feature extraction

3. Step 7.3: Computer Vision Emotion Detection
   - /api/ai/analyze-video-emotion for facial expression analysis
   - /api/ai/analyze-session-video for real-time emotion tracking

4. Backward Compatibility
   - Ensure existing interview flow still works with new open-source InterviewAI class
"""

import requests
import json
import time
import base64
import io
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://b3855e00-962c-4d9a-8527-850a152dcbe3.preview.emergentagent.com/api"

class Phase3OpenSourceAITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_results = {}
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
        self.test_results[test_name] = success
    
    def test_ai_status_endpoint(self) -> bool:
        """Test /api/ai/status endpoint to verify open-source AI engine initialization"""
        try:
            response = self.session.get(f"{self.base_url}/ai/status", timeout=15)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "ai_status" in data and
                          "timestamp" in data)
                
                if success:
                    ai_status = data["ai_status"]
                    # Check for open-source AI components
                    details = f"Status: {response.status_code}, AI Status: {json.dumps(ai_status, indent=2)[:200]}..."
                else:
                    details = f"Status: {response.status_code}, Missing required fields in response"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("AI Status Endpoint - Open-Source Engine Initialization", success, details)
            return success
        except Exception as e:
            self.log_test("AI Status Endpoint - Open-Source Engine Initialization", False, f"Exception: {str(e)}")
            return False
    
    def test_analyze_question_bert(self) -> bool:
        """Test /api/ai/analyze-question for BERT-based question analysis"""
        try:
            test_question = "Can you explain the difference between supervised and unsupervised machine learning algorithms, and provide examples of when you would use each approach?"
            
            payload = {
                "question": test_question
            }
            
            response = self.session.post(
                f"{self.base_url}/ai/analyze-question",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "question_analysis" in data and
                          "timestamp" in data)
                
                if success:
                    analysis = data["question_analysis"]
                    # Check if analysis contains expected fields
                    if isinstance(analysis, dict) and not analysis.get("error"):
                        details = f"Status: {response.status_code}, Analysis keys: {list(analysis.keys())}"
                    else:
                        details = f"Status: {response.status_code}, Analysis error: {analysis.get('error', 'Unknown error')}"
                        success = False
                else:
                    details = f"Status: {response.status_code}, Missing required fields"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("BERT-based Question Analysis", success, details)
            return success
        except Exception as e:
            self.log_test("BERT-based Question Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_generate_questions_opensource(self) -> bool:
        """Test /api/ai/generate-questions-opensource for GPT-style question generation using Hugging Face models"""
        try:
            payload = {
                "job_description": "Senior Python Developer position requiring expertise in FastAPI, microservices architecture, and cloud deployment. The role involves leading a team of developers and architecting scalable backend systems.",
                "resume_content": "John Smith - Senior Software Engineer with 5+ years experience in Python, FastAPI, Docker, Kubernetes, and AWS. Led multiple microservices projects and mentored junior developers.",
                "question_type": "technical",
                "count": 3
            }
            
            response = self.session.post(
                f"{self.base_url}/ai/generate-questions-opensource",
                json=payload,
                timeout=30  # Longer timeout for AI generation
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "questions" in data and
                          "question_type" in data and
                          "count" in data)
                
                if success:
                    questions = data["questions"]
                    if isinstance(questions, list) and len(questions) > 0:
                        # Check if questions are actual strings and not error messages
                        if not any("not available" in str(q).lower() for q in questions):
                            details = f"Status: {response.status_code}, Generated {len(questions)} questions, Type: {data['question_type']}"
                        else:
                            details = f"Status: {response.status_code}, Open-source AI engine not available"
                            success = False
                    else:
                        details = f"Status: {response.status_code}, No questions generated"
                        success = False
                else:
                    details = f"Status: {response.status_code}, Missing required fields"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Open-Source Question Generation (Hugging Face)", success, details)
            return success
        except Exception as e:
            self.log_test("Open-Source Question Generation (Hugging Face)", False, f"Exception: {str(e)}")
            return False
    
    def test_analyze_response_opensource(self) -> bool:
        """Test /api/ai/analyze-response-opensource for candidate response analysis using open-source models"""
        try:
            payload = {
                "question": "Explain the difference between supervised and unsupervised machine learning.",
                "response": "Supervised learning uses labeled training data to learn patterns and make predictions on new data. Examples include classification and regression tasks. Unsupervised learning finds hidden patterns in data without labels, like clustering and dimensionality reduction. I've used supervised learning for customer churn prediction and unsupervised learning for customer segmentation in my previous projects.",
                "question_type": "technical"
            }
            
            response = self.session.post(
                f"{self.base_url}/ai/analyze-response-opensource",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "response_analysis" in data and
                          "timestamp" in data)
                
                if success:
                    analysis = data["response_analysis"]
                    if isinstance(analysis, dict) and not analysis.get("error"):
                        details = f"Status: {response.status_code}, Analysis completed with keys: {list(analysis.keys())}"
                    else:
                        details = f"Status: {response.status_code}, Analysis error: {analysis.get('error', 'Unknown error')}"
                        success = False
                else:
                    details = f"Status: {response.status_code}, Missing required fields"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Open-Source Response Analysis", success, details)
            return success
        except Exception as e:
            self.log_test("Open-Source Response Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_analyze_speech_advanced(self) -> bool:
        """Test /api/ai/analyze-speech for professional-grade voice assessment"""
        try:
            # Create dummy base64 audio data (simulating actual audio)
            dummy_audio = b"RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x08\x00\x00"
            audio_base64 = base64.b64encode(dummy_audio).decode('utf-8')
            
            payload = {
                "audio_data": audio_base64,
                "transcript": "I have extensive experience with Python development, particularly in building scalable web applications using FastAPI and Django frameworks."
            }
            
            response = self.session.post(
                f"{self.base_url}/ai/analyze-speech",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "speech_analysis" in data and
                          "timestamp" in data)
                
                if success:
                    analysis = data["speech_analysis"]
                    if isinstance(analysis, dict) and not analysis.get("error"):
                        details = f"Status: {response.status_code}, Speech analysis completed"
                    else:
                        details = f"Status: {response.status_code}, Speech analyzer not available: {analysis.get('error', 'Unknown error')}"
                        success = False
                else:
                    details = f"Status: {response.status_code}, Missing required fields"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Advanced Speech Analysis", success, details)
            return success
        except Exception as e:
            self.log_test("Advanced Speech Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_voice_analyze_enhanced(self) -> bool:
        """Test /api/voice/analyze-enhanced for comprehensive speech feature extraction"""
        try:
            # Create dummy base64 audio data
            dummy_audio = b"RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x08\x00\x00"
            audio_base64 = base64.b64encode(dummy_audio).decode('utf-8')
            
            payload = {
                "audio_data": audio_base64,
                "transcript": "My approach to software architecture involves careful consideration of scalability, maintainability, and performance requirements.",
                "session_id": "test-session-phase3-001"
            }
            
            response = self.session.post(
                f"{self.base_url}/voice/analyze-enhanced",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "enhanced_analysis" in data and
                          "timestamp" in data)
                
                if success:
                    analysis = data["enhanced_analysis"]
                    details = f"Status: {response.status_code}, Enhanced voice analysis completed"
                else:
                    details = f"Status: {response.status_code}, Missing required fields"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Enhanced Voice Analysis", success, details)
            return success
        except Exception as e:
            self.log_test("Enhanced Voice Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_analyze_video_emotion(self) -> bool:
        """Test /api/ai/analyze-video-emotion for facial expression analysis"""
        try:
            # Create a dummy base64 image (1x1 pixel PNG)
            dummy_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
            frame_base64 = base64.b64encode(dummy_image).decode('utf-8')
            
            payload = {
                "frame_data": frame_base64
            }
            
            response = self.session.post(
                f"{self.base_url}/ai/analyze-video-emotion",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "emotion_analysis" in data and
                          "timestamp" in data)
                
                if success:
                    analysis = data["emotion_analysis"]
                    if isinstance(analysis, dict) and not analysis.get("error"):
                        details = f"Status: {response.status_code}, Video emotion analysis completed"
                    else:
                        details = f"Status: {response.status_code}, Emotion detector not available: {analysis.get('error', 'Unknown error')}"
                        success = False
                else:
                    details = f"Status: {response.status_code}, Missing required fields"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Computer Vision Emotion Detection", success, details)
            return success
        except Exception as e:
            self.log_test("Computer Vision Emotion Detection", False, f"Exception: {str(e)}")
            return False
    
    def test_analyze_session_video(self) -> bool:
        """Test /api/ai/analyze-session-video for real-time emotion tracking"""
        try:
            # Simulate frame analyses from a video session
            frame_analyses = [
                {
                    "timestamp": 0.0,
                    "emotions": {"happy": 0.7, "neutral": 0.2, "focused": 0.1},
                    "attention_score": 0.8
                },
                {
                    "timestamp": 5.0,
                    "emotions": {"focused": 0.6, "neutral": 0.3, "happy": 0.1},
                    "attention_score": 0.9
                },
                {
                    "timestamp": 10.0,
                    "emotions": {"neutral": 0.5, "focused": 0.4, "happy": 0.1},
                    "attention_score": 0.7
                }
            ]
            
            payload = {
                "frame_analyses": frame_analyses,
                "session_duration": 15.0
            }
            
            response = self.session.post(
                f"{self.base_url}/ai/analyze-session-video",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("success", False) and 
                          "session_analysis" in data and
                          "timestamp" in data)
                
                if success:
                    analysis = data["session_analysis"]
                    if isinstance(analysis, dict) and not analysis.get("error"):
                        details = f"Status: {response.status_code}, Session video analysis completed"
                    else:
                        details = f"Status: {response.status_code}, Emotion detector not available: {analysis.get('error', 'Unknown error')}"
                        success = False
                else:
                    details = f"Status: {response.status_code}, Missing required fields"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Real-time Emotion Tracking", success, details)
            return success
        except Exception as e:
            self.log_test("Real-time Emotion Tracking", False, f"Exception: {str(e)}")
            return False
    
    def test_backward_compatibility_interview_flow(self) -> bool:
        """Test that existing interview flow still works with new open-source InterviewAI class"""
        try:
            # First, create a job and resume upload to get a token
            resume_content = """Sarah Johnson
Senior AI Engineer
Email: sarah.johnson@email.com
Phone: (555) 987-6543

EXPERIENCE:
- 6+ years in AI/ML development
- Expert in Python, TensorFlow, PyTorch
- Experience with open-source AI models
- Built production ML systems at scale

SKILLS:
- Python, TensorFlow, PyTorch, Hugging Face
- BERT, GPT, Computer Vision, NLP
- Docker, Kubernetes, MLOps
- Team leadership and mentoring"""
            
            files = {
                'resume_file': ('resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior AI Engineer - Open Source Specialist',
                'job_description': 'We are seeking a senior AI engineer with expertise in open-source AI models and frameworks. The role involves implementing cutting-edge AI solutions using Hugging Face, BERT, and other open-source technologies.',
                'job_requirements': 'Requirements: 5+ years AI/ML experience, expertise in open-source AI frameworks, Python proficiency, production ML system experience.'
            }
            
            # Upload job and resume
            response = self.session.post(
                f"{self.base_url}/admin/upload-job",
                files=files,
                data=data,
                timeout=15
            )
            
            if response.status_code != 200:
                self.log_test("Backward Compatibility - Interview Flow", False, "Failed to create token for compatibility test")
                return False
            
            result = response.json()
            token = result.get("token")
            
            if not token:
                self.log_test("Backward Compatibility - Interview Flow", False, "No token received")
                return False
            
            # Start interview
            payload = {
                "token": token,
                "candidate_name": "Sarah Johnson",
                "voice_mode": False
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
                          "question_number" in data)
                
                if success:
                    session_id = data["session_id"]
                    
                    # Send one answer to test the flow
                    answer_payload = {
                        "token": token,
                        "message": "I have extensive experience with open-source AI frameworks including Hugging Face Transformers, PyTorch, and TensorFlow. I've implemented BERT models for NLP tasks and fine-tuned GPT models for specific use cases."
                    }
                    
                    response = self.session.post(
                        f"{self.base_url}/candidate/send-message",
                        json=answer_payload,
                        timeout=25
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if "next_question" in data or data.get("completed", False):
                            details = f"Interview flow working correctly with open-source AI integration"
                        else:
                            details = f"Interview flow issue: {response.text[:200]}"
                            success = False
                    else:
                        details = f"Answer processing failed: Status {response.status_code}"
                        success = False
                else:
                    details = f"Interview start failed: Missing required fields"
            else:
                details = f"Interview start failed: Status {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Backward Compatibility - Interview Flow", success, details)
            return success
        except Exception as e:
            self.log_test("Backward Compatibility - Interview Flow", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all Phase 3 open-source AI integration tests"""
        print("=" * 80)
        print("PHASE 3: OPEN-SOURCE AI INTEGRATION TESTING")
        print("Testing replacement of proprietary AI services with open-source alternatives")
        print("=" * 80)
        print()
        
        # Step 7.1: Replace Proprietary AI Services
        print("🔧 STEP 7.1: REPLACE PROPRIETARY AI SERVICES")
        print("-" * 50)
        self.test_ai_status_endpoint()
        self.test_analyze_question_bert()
        self.test_generate_questions_opensource()
        self.test_analyze_response_opensource()
        print()
        
        # Step 7.2: Advanced Speech Analysis
        print("🎤 STEP 7.2: ADVANCED SPEECH ANALYSIS")
        print("-" * 50)
        self.test_analyze_speech_advanced()
        self.test_voice_analyze_enhanced()
        print()
        
        # Step 7.3: Computer Vision Emotion Detection
        print("👁️ STEP 7.3: COMPUTER VISION EMOTION DETECTION")
        print("-" * 50)
        self.test_analyze_video_emotion()
        self.test_analyze_session_video()
        print()
        
        # Backward Compatibility
        print("🔄 BACKWARD COMPATIBILITY")
        print("-" * 50)
        self.test_backward_compatibility_interview_flow()
        print()
        
        # Summary
        print("=" * 80)
        print("PHASE 3 TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results.values() if result)
        total = len(self.test_results)
        
        # Group results by category
        categories = {
            "Step 7.1 - Replace Proprietary AI Services": [
                "AI Status Endpoint - Open-Source Engine Initialization",
                "BERT-based Question Analysis", 
                "Open-Source Question Generation (Hugging Face)",
                "Open-Source Response Analysis"
            ],
            "Step 7.2 - Advanced Speech Analysis": [
                "Advanced Speech Analysis",
                "Enhanced Voice Analysis"
            ],
            "Step 7.3 - Computer Vision Emotion Detection": [
                "Computer Vision Emotion Detection",
                "Real-time Emotion Tracking"
            ],
            "Backward Compatibility": [
                "Backward Compatibility - Interview Flow"
            ]
        }
        
        for category, test_names in categories.items():
            print(f"\n{category}:")
            for test_name in test_names:
                if test_name in self.test_results:
                    status = "✅ PASS" if self.test_results[test_name] else "❌ FAIL"
                    print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL PHASE 3 TESTS PASSED! Open-source AI integration is working correctly.")
        elif passed >= total * 0.7:
            print("✅ MOSTLY WORKING! Most open-source AI features are functional.")
        else:
            print("⚠️  Multiple tests failed. Open-source AI components may not be fully initialized.")
        
        return self.test_results

def main():
    """Main test execution"""
    tester = Phase3OpenSourceAITester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())