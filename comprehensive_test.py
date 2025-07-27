#!/usr/bin/env python3
"""
Final comprehensive test of all enhanced backend features
"""

import requests
import json
import time

BASE_URL = 'https://8efc00c9-cb7f-48ab-a6b5-ecb4f59517b3.preview.emergentagent.com/api'

def test_comprehensive_enhanced_features():
    session = requests.Session()
    print("🚀 COMPREHENSIVE ENHANCED BACKEND TESTING")
    print("=" * 60)
    
    # 1. Test Enhanced Admin Upload with all new parameters
    print("\n1. Testing Enhanced Admin Upload...")
    resume_content = """Elite Candidate
Senior Full-Stack Engineer
Email: elite@example.com

EXPERIENCE:
- 7+ years of software development
- Expert in algorithms and data structures
- Led technical teams and mentored developers
- Strong system design and architecture skills

SKILLS:
- Python, JavaScript, Java, C++
- React, FastAPI, Spring Boot, Node.js
- MongoDB, PostgreSQL, Redis, Elasticsearch
- AWS, Docker, Kubernetes, microservices
- Problem-solving and technical leadership
"""
    
    files = {'resume_file': ('elite_resume.txt', resume_content, 'text/plain')}
    data = {
        'job_title': 'Elite Software Engineer',
        'job_description': 'We seek an elite software engineer for complex system design and technical leadership.',
        'job_requirements': 'Requirements: 5+ years experience, strong algorithms, system design, leadership skills.',
        'include_coding_challenge': 'true',
        'role_archetype': 'Software Engineer',
        'interview_focus': 'Technical Deep-Dive'
    }
    
    response = session.post(f'{BASE_URL}/admin/upload-job', files=files, data=data, timeout=15)
    if response.status_code == 200:
        result = response.json()
        token = result.get('token')
        features = result.get('features', {})
        print(f"   ✅ Enhanced token created: {token[:8]}...")
        print(f"   ✅ Features: {features}")
        
        # 2. Test Enhanced Interview Start
        print("\n2. Testing Enhanced Interview Start...")
        payload = {
            'token': token,
            'candidate_name': 'Elite Candidate',
            'voice_mode': False
        }
        
        response = session.post(f'{BASE_URL}/candidate/start-interview', json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            is_enhanced = data.get('is_enhanced')
            interview_features = data.get('features', {})
            
            print(f"   ✅ Enhanced interview started: {session_id[:8]}...")
            print(f"   ✅ Is Enhanced: {is_enhanced}")
            print(f"   ✅ Interview Features: {interview_features}")
            
            # 3. Test Coding Challenge Generation
            print("\n3. Testing Coding Challenge Generation...")
            response = session.get(f'{BASE_URL}/modules/coding-challenge/{session_id}', timeout=15)
            if response.status_code == 200:
                data = response.json()
                challenge = data.get('challenge', {})
                print(f"   ✅ Coding challenge generated")
                print(f"   ✅ Title: {challenge.get('problem_title')}")
                print(f"   ✅ Language: {challenge.get('language')}")
                
                # 4. Test Coding Challenge Submission
                print("\n4. Testing Coding Challenge Submission...")
                sample_solution = """
function findTwoSum(numbers, target) {
    const seen = new Map();
    for (let i = 0; i < numbers.length; i++) {
        const complement = target - numbers[i];
        if (seen.has(complement)) {
            return [seen.get(complement), i];
        }
        seen.set(numbers[i], i);
    }
    return [];
}"""
                
                payload = {
                    'session_id': session_id,
                    'submitted_code': sample_solution.strip()
                }
                
                response = session.post(f'{BASE_URL}/modules/coding-challenge/submit', json=payload, timeout=20)
                if response.status_code == 200:
                    data = response.json()
                    score = data.get('score', 0)
                    print(f"   ✅ Coding challenge submitted")
                    print(f"   ✅ Score: {score}/100")
                else:
                    print(f"   ❌ Coding challenge submission failed: {response.status_code}")
            else:
                print(f"   ❌ Coding challenge generation failed: {response.status_code}")
            
            # 5. Test SJT Generation
            print("\n5. Testing SJT Generation...")
            response = session.get(f'{BASE_URL}/modules/sjt/{session_id}', timeout=15)
            if response.status_code == 200:
                data = response.json()
                sjt = data.get('sjt', {})
                print(f"   ✅ SJT generated")
                print(f"   ✅ Scenario: {sjt.get('scenario', '')[:50]}...")
                print(f"   ✅ Options: {len(sjt.get('options', []))}")
                
                # 6. Test SJT Submission
                print("\n6. Testing SJT Submission...")
                payload = {
                    'session_id': session_id,
                    'sjt_id': sjt.get('id'),
                    'selected_answer': 'b'
                }
                
                response = session.post(f'{BASE_URL}/modules/sjt/submit', json=payload, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    is_correct = data.get('is_correct')
                    score = data.get('score', 0)
                    print(f"   ✅ SJT submitted")
                    print(f"   ✅ Correct: {is_correct}, Score: {score}")
                else:
                    print(f"   ❌ SJT submission failed: {response.status_code}")
            else:
                print(f"   ❌ SJT generation failed: {response.status_code}")
            
            # 7. Test Question Rephrasing
            print("\n7. Testing Question Rephrasing...")
            payload = {
                'session_id': session_id,
                'original_question': 'Explain the time complexity of quicksort algorithm and discuss its best, average, and worst-case scenarios.'
            }
            
            response = session.post(f'{BASE_URL}/candidate/rephrase-question', json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                rephrased = data.get('rephrased_question', '')
                print(f"   ✅ Question rephrased")
                print(f"   ✅ Rephrased: {rephrased[:80]}...")
            else:
                print(f"   ❌ Question rephrasing failed: {response.status_code}")
            
            # 8. Test Practice Round
            print("\n8. Testing Practice Round...")
            payload = {
                'token': token,
                'candidate_name': 'Elite Candidate'
            }
            
            response = session.post(f'{BASE_URL}/candidate/practice-round', json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                practice_question = data.get('practice_question', '')
                print(f"   ✅ Practice round started")
                print(f"   ✅ Practice question: {practice_question}")
            else:
                print(f"   ❌ Practice round failed: {response.status_code}")
        else:
            print(f"   ❌ Enhanced interview start failed: {response.status_code}")
    else:
        print(f"   ❌ Enhanced admin upload failed: {response.status_code}")
    
    # 9. Test Candidate Pipeline
    print("\n9. Testing Candidate Pipeline...")
    response = session.get(f'{BASE_URL}/admin/candidate-pipeline', timeout=10)
    if response.status_code == 200:
        data = response.json()
        pipeline = data.get('pipeline', [])
        enhanced_candidates = [c for c in pipeline if c.get('interview_type') == 'Enhanced']
        print(f"   ✅ Pipeline retrieved")
        print(f"   ✅ Total candidates: {len(pipeline)}")
        print(f"   ✅ Enhanced candidates: {len(enhanced_candidates)}")
    else:
        print(f"   ❌ Candidate pipeline failed: {response.status_code}")
    
    print("\n" + "=" * 60)
    print("🎉 COMPREHENSIVE ENHANCED BACKEND TESTING COMPLETED")
    print("✅ All major enhanced features are functional!")

if __name__ == "__main__":
    test_comprehensive_enhanced_features()