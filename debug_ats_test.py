#!/usr/bin/env python3
"""
Debug ATS PDF Generation - Minimal Test
"""

import requests
import json
import os

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://33e908ff-821c-4359-a046-0a59698e91ec.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

def debug_ats_calculation():
    """Debug test with minimal data"""
    
    # Minimal resume content
    resume_content = "John Doe\nSoftware Engineer\nPython, JavaScript"
    
    # Minimal job description
    job_description = "Python developer needed."
    
    try:
        session = requests.Session()
        
        # Prepare the request as form data with file upload
        files = {
            'resume': ('debug_resume.txt', resume_content.encode('utf-8'), 'text/plain')
        }
        
        form_data = {
            'job_title': "Python Developer",
            'job_description': job_description
        }
        
        print("Making minimal ATS calculation request...")
        response = session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                               files=files, data=form_data)
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"ATS ID: {data.get('ats_id')}")
            print(f"ATS Score: {data.get('ats_score')}")
            print(f"PDF Filename: '{data.get('pdf_filename')}'")
            print(f"Analysis length: {len(data.get('analysis_text', ''))}")
            
            # Check if PDF was generated
            if data.get('pdf_filename'):
                print("✅ PDF generation successful!")
            else:
                print("❌ PDF generation failed!")
            
        else:
            print(f"Request failed: {response.text}")
            
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == "__main__":
    debug_ats_calculation()