#!/usr/bin/env python3
"""
Focused ATS PDF Generation Test
"""

import requests
import tempfile
import os

BACKEND_URL = "https://00a8e650-3105-4677-9117-76e2639bccac.preview.emergentagent.com"
ATS_ENDPOINT = f"{BACKEND_URL}/api/placement-preparation/ats-score-calculate"

def test_pdf_generation():
    """Test PDF generation specifically"""
    
    # Simple resume content
    resume_content = """John Smith
Software Engineer
john@email.com

EXPERIENCE
Software Engineer at TechCorp (2020-2023)
• Developed web applications using Python and React
• Improved system performance by 30%
• Led team of 3 developers

SKILLS
• Python, JavaScript, React, MongoDB
• AWS, Docker, Git

EDUCATION
BS Computer Science, University of Tech (2020)
"""
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(resume_content)
        temp_file_path = temp_file.name
    
    try:
        with open(temp_file_path, 'rb') as resume_file:
            files = {
                'resume': ('test_resume.txt', resume_file, 'text/plain')
            }
            data = {
                'job_title': 'Software Engineer',
                'job_description': 'Software Engineer with Python, React, MongoDB experience needed.'
            }
            
            print("🚀 Testing ATS Score Calculation with Simple Resume...")
            
            response = requests.post(ATS_ENDPOINT, files=files, data=data, timeout=60)
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success: {result.get('success')}")
                print(f"🆔 ATS ID: {result.get('ats_id')}")
                print(f"📊 ATS Score: {result.get('ats_score')}")
                print(f"📄 PDF Filename: '{result.get('pdf_filename')}'")
                print(f"📝 Analysis Length: {len(result.get('analysis_text', ''))}")
                
                # Test PDF download if we have an ID
                ats_id = result.get('ats_id')
                if ats_id:
                    pdf_url = f"{BACKEND_URL}/api/placement-preparation/ats-score/{ats_id}/download"
                    print(f"📥 Testing PDF Download: {pdf_url}")
                    
                    pdf_response = requests.get(pdf_url, timeout=30)
                    print(f"📊 PDF Response Status: {pdf_response.status_code}")
                    
                    if pdf_response.status_code == 200:
                        print(f"✅ PDF Downloaded: {len(pdf_response.content)} bytes")
                        print(f"📄 Content Type: {pdf_response.headers.get('content-type')}")
                        
                        # Check PDF header
                        if pdf_response.content[:4] == b'%PDF':
                            print("✅ Valid PDF format")
                        else:
                            print("❌ Invalid PDF format")
                    else:
                        print(f"❌ PDF Download Failed: {pdf_response.text}")
                
                return result
            else:
                print(f"❌ Request Failed: {response.text}")
                return None
                
    finally:
        try:
            os.unlink(temp_file_path)
        except:
            pass

if __name__ == "__main__":
    test_pdf_generation()