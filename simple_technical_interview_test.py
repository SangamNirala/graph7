#!/usr/bin/env python3
"""
Simple Technical Interview Questions Test
Tests the endpoint with basic functionality
"""

import requests
import json
import os
from datetime import datetime

# Configuration
BACKEND_URL = "https://9111a607-ad7c-4aad-8586-9dca4be775f2.preview.emergentagent.com/api"
SAMPLE_RESUME_PATH = "/app/sample_resume.txt"

# Test data
TEST_JOB_TITLE = "Senior Software Engineer"
TEST_JOB_DESCRIPTION = """5+ years of experience in full-stack development, proficient in React, Node.js, MongoDB, cloud platforms (AWS/GCP), RESTful APIs, microservices architecture, Agile/Scrum methodology, and CI/CD pipelines. Experience with TypeScript, GraphQL, and Docker preferred."""

def test_technical_interview_questions_basic():
    """Basic test for technical interview questions generation"""
    print("🧪 Testing Technical Interview Questions Generation...")
    
    try:
        # Prepare the resume file
        if not os.path.exists(SAMPLE_RESUME_PATH):
            print(f"❌ Resume file not found: {SAMPLE_RESUME_PATH}")
            return False
        
        # Prepare form data
        with open(SAMPLE_RESUME_PATH, 'rb') as resume_file:
            files = {
                'resume': ('sample_resume.txt', resume_file, 'text/plain')
            }
            data = {
                'job_title': TEST_JOB_TITLE,
                'job_description': TEST_JOB_DESCRIPTION
            }
            
            print(f"📤 Sending POST request...")
            print(f"📋 Job Title: {TEST_JOB_TITLE}")
            print(f"📄 Job Description: {TEST_JOB_DESCRIPTION[:100]}...")
            
            response = requests.post(
                f"{BACKEND_URL}/placement-preparation/technical-interview-questions",
                files=files,
                data=data,
                timeout=60
            )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS: Technical interview questions generated!")
            
            analysis_id = result.get('analysis_id')
            interview_questions = result.get('interview_questions', '')
            pdf_filename = result.get('pdf_filename', '')
            
            print(f"   Analysis ID: {analysis_id}")
            print(f"   PDF Filename: {pdf_filename}")
            print(f"   Questions Length: {len(interview_questions)} characters")
            
            # Check for basic content
            if 'Question' in interview_questions:
                print("✅ Questions found in response")
            else:
                print("⚠️  No questions found in response")
            
            return True
            
        elif response.status_code == 500:
            error_detail = response.json().get('detail', 'No error details')
            print(f"❌ Server Error (500): {error_detail}")
            
            # Check if it's a PDF generation issue
            if 'paraparser' in error_detail or 'br tag' in error_detail:
                print("🔍 Detected PDF generation issue with HTML parsing")
                print("💡 This suggests the LLM is generating content but PDF conversion is failing")
                return False
            else:
                print("🔍 Different server error")
                return False
        else:
            error_detail = response.text if response.text else "No error details"
            print(f"❌ Request failed with status {response.status_code}: {error_detail}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return False

def test_get_analyses():
    """Test GET endpoint for analyses"""
    print("\n🧪 Testing GET analyses endpoint...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/placement-preparation/technical-interview-questions", timeout=10)
        
        print(f"📥 GET Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            analyses = result.get('analyses', [])
            print(f"✅ SUCCESS: Found {len(analyses)} analyses")
            return True
        else:
            print(f"❌ GET request failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print(f"🚀 SIMPLE TECHNICAL INTERVIEW QUESTIONS TEST")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Backend URL: {BACKEND_URL}")
    
    # Test basic generation
    generation_success = test_technical_interview_questions_basic()
    
    # Test GET endpoint
    get_success = test_get_analyses()
    
    print(f"\n📊 SUMMARY:")
    print(f"   Generation Test: {'✅ PASSED' if generation_success else '❌ FAILED'}")
    print(f"   GET Test: {'✅ PASSED' if get_success else '❌ FAILED'}")
    
    if generation_success and get_success:
        print(f"🎉 OVERALL: Technical Interview Questions feature is working!")
    elif generation_success or get_success:
        print(f"⚠️  OVERALL: Partial functionality - some features working")
    else:
        print(f"❌ OVERALL: Technical Interview Questions feature needs fixes")