#!/usr/bin/env python3
"""
Focused test to investigate the total_questions field issue
"""

import requests
import json
import io

BASE_URL = "https://eaf11cb1-62bc-4a4c-b83f-3b9ff2fe22cf.preview.emergentagent.com/api"

def test_total_questions_investigation():
    session = requests.Session()
    
    print("=== INVESTIGATING TOTAL_QUESTIONS FIELD ===\n")
    
    # Create enhanced token
    resume_content = """Test Candidate
Software Engineer
Email: test@email.com

EXPERIENCE:
- 5+ years of software development
- Expert in Python and system design
- Team leadership experience

SKILLS:
- Python, JavaScript, FastAPI
- System architecture and design
- Team leadership and mentoring"""
    
    files = {
        'resume_file': ('test_resume.txt', io.StringIO(resume_content), 'text/plain')
    }
    
    data = {
        'job_title': 'Senior Software Engineer',
        'job_description': 'We need a senior engineer with deep technical expertise.',
        'job_requirements': 'Requirements: 5+ years experience, system design skills.',
        'include_coding_challenge': True,
        'role_archetype': 'Software Engineer',
        'interview_focus': 'Technical Deep-Dive',
        'min_questions': 10,
        'max_questions': 12
    }
    
    print("1. Creating enhanced interview token...")
    response = session.post(f"{BASE_URL}/admin/upload-job-enhanced", files=files, data=data, timeout=15)
    
    if response.status_code != 200:
        print(f"❌ Failed to create token: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    result = response.json()
    token = result.get("token")
    print(f"✅ Token created: {token[:8]}...")
    
    # Start interview and examine response
    print("\n2. Starting interview and examining total_questions field...")
    payload = {
        "token": token,
        "candidate_name": "Investigation Test",
        "voice_mode": False
    }
    
    response = session.post(f"{BASE_URL}/candidate/start-interview", json=payload, timeout=20)
    
    if response.status_code != 200:
        print(f"❌ Failed to start interview: {response.status_code}")
        print(f"Response: {response.text}")
        return
    
    data = response.json()
    print("✅ Interview started successfully")
    print(f"Response keys: {list(data.keys())}")
    
    # Examine total_questions field
    if "total_questions" in data:
        total_questions = data["total_questions"]
        print(f"📊 total_questions field: {total_questions}")
        
        if total_questions == 8:
            print("⚠️  WARNING: total_questions is still hardcoded to 8!")
        else:
            print(f"✅ total_questions is dynamic: {total_questions}")
    else:
        print("❌ total_questions field is missing!")
    
    # Check for other relevant fields
    relevant_fields = ["technical_count", "behavioral_count", "question_type", "is_enhanced"]
    for field in relevant_fields:
        if field in data:
            print(f"📋 {field}: {data[field]}")
    
    # Check welcome message for question count info
    if "welcome_message" in data:
        welcome = data["welcome_message"]
        print(f"📝 Welcome message: {welcome[:200]}...")
        
        # Look for question count mentions in welcome message
        if "questions" in welcome.lower():
            print("✅ Welcome message mentions questions")
        else:
            print("⚠️  Welcome message doesn't mention question count")
    
    print(f"\n3. Full response structure:")
    print(json.dumps(data, indent=2)[:1000] + "..." if len(json.dumps(data, indent=2)) > 1000 else json.dumps(data, indent=2))

if __name__ == "__main__":
    test_total_questions_investigation()