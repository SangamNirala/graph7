#!/usr/bin/env python3
"""
Test the complete rejection reasons workflow to verify data flow
"""

import requests
import json
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://882970a1-15c9-4eb2-9f43-a49f0b775561.preview.emergentagent.com')

def test_rejection_reasons_workflow():
    """Test the complete rejection reasons workflow"""
    
    print("🔍 REJECTION REASONS WORKFLOW TEST")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now()}")
    print()
    
    # Step 1: Create a rejection reasons analysis
    print("📋 STEP 1: Create Rejection Reasons Analysis")
    print("-" * 50)
    
    # Sample resume content for testing
    sample_resume = """
    John Doe
    Software Developer
    Email: john.doe@email.com
    Phone: (555) 123-4567
    
    EXPERIENCE:
    Junior Developer at ABC Company (2022-2024)
    - Worked on basic web development projects
    - Used HTML, CSS, JavaScript
    - Participated in team meetings
    
    EDUCATION:
    Bachelor's in Computer Science (2022)
    State University
    
    SKILLS:
    - HTML, CSS, JavaScript
    - Basic Python
    - Git version control
    """
    
    # Sample job description requiring more advanced skills
    job_description = """
    Senior Full Stack Developer Position
    
    We are seeking an experienced Senior Full Stack Developer to join our team.
    
    REQUIRED SKILLS:
    - 5+ years of professional software development experience
    - Expert-level React.js and Node.js development
    - Experience with TypeScript, GraphQL, and modern frameworks
    - Cloud platforms (AWS, Azure, or GCP) experience
    - Database design and optimization (PostgreSQL, MongoDB)
    - Microservices architecture and containerization (Docker, Kubernetes)
    - CI/CD pipeline setup and DevOps practices
    - Leadership and mentoring experience
    - Strong system design and architecture skills
    
    PREFERRED:
    - Machine Learning and AI integration experience
    - Mobile development (React Native or Flutter)
    - Blockchain or cryptocurrency experience
    """
    
    job_title = "Senior Full Stack Developer"
    
    try:
        url = f"{BACKEND_URL}/api/placement-preparation/rejection-reasons"
        
        # Create form data
        files = {
            'resume': ('test_resume.txt', sample_resume, 'text/plain')
        }
        data = {
            'job_title': job_title,
            'job_description': job_description
        }
        
        print(f"URL: {url}")
        print(f"Job Title: {job_title}")
        print(f"Resume Length: {len(sample_resume)} characters")
        print(f"Job Description Length: {len(job_description)} characters")
        
        response = requests.post(url, files=files, data=data, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: Rejection reasons analysis created")
            print(f"Response keys: {list(result.keys())}")
            
            if 'rejection_id' in result:
                rejection_id = result['rejection_id']
                print(f"Rejection ID: {rejection_id}")
                
                if 'analysis_text' in result:
                    analysis_text = result['analysis_text']
                    print(f"Analysis Length: {len(analysis_text)} characters")
                    print(f"Analysis Preview: {analysis_text[:300]}...")
                
                # Step 2: Verify the analysis was stored
                print()
                print("📋 STEP 2: Verify Analysis Storage")
                print("-" * 50)
                
                get_url = f"{BACKEND_URL}/api/placement-preparation/rejection-reasons"
                get_response = requests.get(get_url, timeout=30)
                
                if get_response.status_code == 200:
                    analyses_data = get_response.json()
                    analyses = analyses_data.get('analyses', [])
                    print(f"✅ Found {len(analyses)} rejection analyses in database")
                    
                    if analyses:
                        latest_analysis = analyses[-1]  # Get the most recent one
                        print(f"Latest analysis ID: {latest_analysis.get('id', 'N/A')}")
                        print(f"Latest analysis has PDF path: {'pdf_path' in latest_analysis}")
                        print(f"Latest analysis has PDF filename: {'pdf_filename' in latest_analysis}")
                        
                        # Step 3: Test PDF download
                        if 'id' in latest_analysis:
                            print()
                            print("📋 STEP 3: Test PDF Download")
                            print("-" * 50)
                            
                            pdf_url = f"{BACKEND_URL}/api/placement-preparation/rejection-reasons/{latest_analysis['id']}/download"
                            pdf_response = requests.get(pdf_url, timeout=30)
                            
                            print(f"PDF Download URL: {pdf_url}")
                            print(f"PDF Download Status: {pdf_response.status_code}")
                            
                            if pdf_response.status_code == 200:
                                print(f"✅ PDF download successful")
                                print(f"PDF Content-Type: {pdf_response.headers.get('content-type', 'N/A')}")
                                print(f"PDF Size: {len(pdf_response.content)} bytes")
                            else:
                                print(f"❌ PDF download failed: {pdf_response.text}")
                    else:
                        print("❌ No analyses found in database after creation")
                else:
                    print(f"❌ Failed to retrieve analyses: {get_response.status_code}")
                    print(f"Response: {get_response.text}")
            else:
                print("❌ No rejection_id in response")
                print(f"Response: {result}")
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response text: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    print()
    print("🔍 WORKFLOW TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_rejection_reasons_workflow()