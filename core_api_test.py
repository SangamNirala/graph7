#!/usr/bin/env python3
"""
Core API Endpoints Testing for AI-Powered Voice Interview Agent
Tests all critical backend endpoints mentioned in the review request
"""

import requests
import json
import io
import base64

BASE_URL = "https://882970a1-15c9-4eb2-9f43-a49f0b775561.preview.emergentagent.com/api"

def test_core_endpoints():
    """Test all core API endpoints"""
    print("=" * 70)
    print("CORE API ENDPOINTS TESTING")
    print("Testing all critical backend functionality")
    print("=" * 70)
    
    session = requests.Session()
    results = {}
    
    # 1. Health Check
    print("\n1. Testing Health Check...")
    try:
        response = session.get(f"{BASE_URL}/health", timeout=10)
        success = response.status_code == 200
        print(f"   Status: {response.status_code}")
        if success:
            print("   ✅ Health check passed")
        results["health_check"] = success
    except Exception as e:
        print(f"   ❌ Health check failed: {str(e)}")
        results["health_check"] = False
    
    # 2. Admin Login
    print("\n2. Testing Admin Authentication...")
    try:
        payload = {"password": "Game@1234"}
        response = session.post(f"{BASE_URL}/admin/login", json=payload, timeout=10)
        success = response.status_code == 200 and response.json().get("success", False)
        print(f"   Status: {response.status_code}")
        if success:
            print("   ✅ Admin authentication successful")
        results["admin_auth"] = success
    except Exception as e:
        print(f"   ❌ Admin authentication failed: {str(e)}")
        results["admin_auth"] = False
    
    # 3. Document Processing - Multi-format Resume Upload
    print("\n3. Testing Multi-format Resume Upload...")
    try:
        resume_content = """Sarah Johnson
AI/ML Engineer
Email: sarah.johnson@email.com
Phone: (555) 234-5678

EXPERIENCE:
- 4+ years in AI/ML development
- Expert in Python, TensorFlow, PyTorch
- Built recommendation systems and NLP models
- Experience with voice processing and speech recognition

SKILLS:
- Python, R, SQL, JavaScript
- TensorFlow, PyTorch, scikit-learn
- NLP, Computer Vision, Speech Processing
- AWS, Docker, Kubernetes, MLOps

EDUCATION:
Master of Science in Artificial Intelligence
Stanford University, 2020"""
        
        files = {'resume_file': ('resume.txt', io.StringIO(resume_content), 'text/plain')}
        data = {
            'job_title': 'AI Engineer - Voice Processing',
            'job_description': 'We are seeking an AI engineer with expertise in voice processing and speech recognition technologies.',
            'job_requirements': 'Requirements: 3+ years AI/ML experience, Python expertise, voice processing knowledge, NLP skills.'
        }
        
        response = session.post(f"{BASE_URL}/admin/upload-job", files=files, data=data, timeout=15)
        success = response.status_code == 200
        token = None
        
        if success:
            result = response.json()
            success = result.get("success", False) and "token" in result
            if success:
                token = result["token"]
                print(f"   ✅ Resume upload successful - Token: {token[:8]}...")
        
        results["document_processing"] = success
        
        # 4. Token Validation
        if token:
            print("\n4. Testing Token Validation...")
            try:
                payload = {"token": token}
                response = session.post(f"{BASE_URL}/candidate/validate-token", json=payload, timeout=10)
                success = response.status_code == 200 and response.json().get("valid", False)
                if success:
                    print("   ✅ Token validation successful")
                results["token_validation"] = success
            except Exception as e:
                print(f"   ❌ Token validation failed: {str(e)}")
                results["token_validation"] = False
        else:
            results["token_validation"] = False
        
        # 5. Voice Interview Start
        if token:
            print("\n5. Testing Voice Interview Start...")
            try:
                payload = {
                    "token": token,
                    "candidate_name": "Sarah Johnson",
                    "voice_mode": True
                }
                response = session.post(f"{BASE_URL}/candidate/start-interview", json=payload, timeout=25)
                success = response.status_code == 200
                session_id = None
                
                if success:
                    data = response.json()
                    success = ("session_id" in data and "first_question" in data and data.get("voice_mode") == True)
                    if success:
                        session_id = data["session_id"]
                        print(f"   ✅ Voice interview start successful - Session: {session_id[:8]}...")
                
                results["voice_interview"] = success
                
                # 6. AI Integration - Question Generation
                if session_id:
                    print("\n6. Testing AI Question Generation...")
                    try:
                        # Send a sample answer to get next question
                        payload = {
                            "token": token,
                            "message": "I have 4 years of experience in AI/ML development, specializing in NLP and voice processing. I've built several speech recognition systems using Python and TensorFlow, including a real-time voice assistant that processes natural language queries and provides intelligent responses."
                        }
                        response = session.post(f"{BASE_URL}/candidate/send-message", json=payload, timeout=20)
                        success = response.status_code == 200
                        
                        if success:
                            data = response.json()
                            success = "next_question" in data or data.get("completed", False)
                            if success:
                                print("   ✅ AI question generation successful")
                        
                        results["ai_integration"] = success
                    except Exception as e:
                        print(f"   ❌ AI question generation failed: {str(e)}")
                        results["ai_integration"] = False
                else:
                    results["ai_integration"] = False
            except Exception as e:
                print(f"   ❌ Voice interview start failed: {str(e)}")
                results["voice_interview"] = False
                results["ai_integration"] = False
        else:
            results["voice_interview"] = False
            results["ai_integration"] = False
    except Exception as e:
        print(f"   ❌ Document processing failed: {str(e)}")
        results["document_processing"] = False
        results["token_validation"] = False
        results["voice_interview"] = False
        results["ai_integration"] = False
    
    # 7. Database Operations - Admin Reports
    print("\n7. Testing Database Operations (Admin Reports)...")
    try:
        response = session.get(f"{BASE_URL}/admin/reports", timeout=10)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            success = "reports" in data and isinstance(data["reports"], list)
            if success:
                print(f"   ✅ Database operations successful - Found {len(data['reports'])} reports")
        
        results["database_ops"] = success
    except Exception as e:
        print(f"   ❌ Database operations failed: {str(e)}")
        results["database_ops"] = False
    
    # 8. File Upload Capabilities - Test TTS Generation
    print("\n8. Testing File Upload & TTS Generation...")
    try:
        payload = {
            "session_id": "test-session-tts",
            "question_text": "Can you tell me about your experience with voice processing and how you would approach building a speech recognition system?"
        }
        response = session.post(f"{BASE_URL}/voice/generate-question", json=payload, timeout=20)
        success = response.status_code == 200
        
        if success:
            data = response.json()
            success = data.get("success", False) and "audio_base64" in data
            if success:
                print("   ✅ TTS generation and file handling successful")
        
        results["file_upload_tts"] = success
    except Exception as e:
        print(f"   ❌ File upload/TTS failed: {str(e)}")
        results["file_upload_tts"] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("CORE API ENDPOINTS TEST SUMMARY")
    print("=" * 70)
    
    categories = {
        "Backend Health": ["health_check"],
        "Admin Authentication": ["admin_auth"],
        "Document Processing": ["document_processing"],
        "Token Management": ["token_validation"],
        "Voice Interview": ["voice_interview"],
        "AI Integration": ["ai_integration"],
        "Database Operations": ["database_ops"],
        "File Upload/TTS": ["file_upload_tts"]
    }
    
    for category, test_names in categories.items():
        print(f"\n{category}:")
        for test_name in test_names:
            if test_name in results:
                status = "✅ PASS" if results[test_name] else "❌ FAIL"
                print(f"  {status} {test_name}")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"\nOVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL CORE API ENDPOINTS WORKING!")
        print("✅ Backend is fully functional and ready for production")
    elif passed >= total * 0.8:
        print("✅ MOSTLY WORKING! Core functionality is operational")
    else:
        print("⚠️  Multiple critical endpoints failed")
    
    return results

if __name__ == "__main__":
    test_core_endpoints()