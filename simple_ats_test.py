#!/usr/bin/env python3
"""
Simple ATS Test to see what's actually being generated
"""

import requests
import json

BACKEND_URL = "https://d7abf0b1-06b8-42dc-8da6-e28d2be0b44a.preview.emergentagent.com"
ATS_ENDPOINT = f"{BACKEND_URL}/api/placement-preparation/ats-score-calculate"

def test_simple_ats():
    resume_content = """John Smith
Software Engineer
john@email.com

EXPERIENCE
Software Engineer at TechCorp (2020-2023)
- Developed Python applications
- Worked with React and MongoDB
- Led team of 3 developers

SKILLS
Python, JavaScript, React, MongoDB, SQL

EDUCATION
BS Computer Science, 2020
"""
    
    files = {
        'resume': ('simple_resume.txt', resume_content.encode(), 'text/plain')
    }
    
    data = {
        'job_title': 'Software Engineer',
        'job_description': 'Looking for Software Engineer with Python, React, MongoDB experience'
    }
    
    print("🚀 Testing simple ATS calculation...")
    response = requests.post(ATS_ENDPOINT, files=files, data=data, timeout=60)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"ATS Score: {result.get('ats_score')}")
        print(f"PDF Filename: {result.get('pdf_filename')}")
        
        analysis_text = result.get('analysis_text', '')
        print(f"\nAnalysis Text Length: {len(analysis_text)} characters")
        print("\n" + "="*80)
        print("ANALYSIS TEXT CONTENT:")
        print("="*80)
        print(analysis_text)
        print("="*80)
        
        return result
    else:
        print(f"Error: {response.text}")
        return None

if __name__ == "__main__":
    test_simple_ats()