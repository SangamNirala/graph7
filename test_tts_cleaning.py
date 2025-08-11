#!/usr/bin/env python3
import requests
import json

BASE_URL = 'https://33e908ff-821c-4359-a046-0a59698e91ec.preview.emergentagent.com/api'

def test_tts_text_cleaning():
    session = requests.Session()
    
    # Create a new token for TTS testing
    resume_content = """TTS Test Candidate
Software Engineer
Email: tts.test@email.com

EXPERIENCE:
- Expert in Python, JavaScript, and React
- Experience with FastAPI and MongoDB
- Strong problem-solving skills

SKILLS:
- Python, JavaScript, HTML, CSS, SQL
- FastAPI, React, MongoDB, PostgreSQL
- Git, Docker, AWS
"""
    
    files = {'resume_file': ('tts_resume.txt', resume_content, 'text/plain')}
    data = {
        'job_title': 'TTS Test Position',
        'job_description': 'Testing TTS functionality with technical questions that might contain backticks.',
        'job_requirements': 'Requirements: Python experience, web development skills.'
    }
    
    response = session.post(f'{BASE_URL}/admin/upload-job', files=files, data=data, timeout=15)
    if response.status_code == 200:
        result = response.json()
        token = result.get('token')
        print(f'✅ Created TTS test token: {token[:8]}...')
        
        # Start interview in voice mode
        payload = {
            'token': token,
            'candidate_name': 'TTS Test Candidate',
            'voice_mode': True
        }
        
        response = session.post(f'{BASE_URL}/candidate/start-interview', json=payload, timeout=25)
        if response.status_code == 200:
            data = response.json()
            first_question = data.get('first_question', '')
            has_backticks = '`' in first_question
            has_audio = 'question_audio' in data
            
            print(f'✅ Interview started successfully')
            print(f'   Question contains backticks: {has_backticks}')
            print(f'   Audio generated: {has_audio}')
            print(f'   First question: {first_question[:100]}...')
            
            if not has_backticks and has_audio:
                print('✅ Text cleaning for TTS is working correctly!')
                return True
            else:
                print('⚠️  Text cleaning may need attention')
                return False
        else:
            print(f'❌ Interview start failed: {response.status_code} - {response.text[:200]}')
            return False
    else:
        print(f'❌ Token creation failed: {response.status_code} - {response.text[:200]}')
        return False

if __name__ == "__main__":
    test_tts_text_cleaning()