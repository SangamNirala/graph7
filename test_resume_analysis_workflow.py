#!/usr/bin/env python3
"""
Test the resume analysis workflow to check if it's working
"""

import requests
import json
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://career-test.preview.emergentagent.com')

def test_resume_analysis_workflow():
    """Test the resume analysis workflow"""
    
    print("🔍 RESUME ANALYSIS WORKFLOW TEST")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now()}")
    print()
    
    # Check if resume-analysis endpoint exists (it should be a POST endpoint)
    print("📋 STEP 1: Test Resume Analysis Endpoint")
    print("-" * 50)
    
    # Sample data for testing
    sample_resume = """
    Jane Smith
    Senior Software Engineer
    Email: jane.smith@email.com
    Phone: (555) 987-6543
    
    EXPERIENCE:
    Senior Software Engineer at Tech Corp (2020-2024)
    - Led development of microservices architecture using Node.js and React
    - Implemented CI/CD pipelines with Docker and Kubernetes
    - Mentored junior developers and conducted code reviews
    - Optimized database queries resulting in 40% performance improvement
    
    Software Engineer at StartupXYZ (2018-2020)
    - Developed full-stack web applications using React, Node.js, and PostgreSQL
    - Integrated third-party APIs and payment systems
    - Collaborated with cross-functional teams in Agile environment
    
    EDUCATION:
    Master's in Computer Science (2018)
    Tech University
    
    SKILLS:
    - JavaScript, TypeScript, Python, Java
    - React, Node.js, Express.js, Next.js
    - PostgreSQL, MongoDB, Redis
    - AWS, Docker, Kubernetes
    - Git, CI/CD, Agile methodologies
    """
    
    job_description = """
    Senior Software Engineer Position
    
    We are looking for a Senior Software Engineer to join our growing team.
    
    REQUIREMENTS:
    - 4+ years of software development experience
    - Strong proficiency in JavaScript/TypeScript and React
    - Experience with Node.js and RESTful API development
    - Database experience (PostgreSQL or MongoDB)
    - Cloud platform experience (AWS preferred)
    - Experience with containerization (Docker)
    - Strong problem-solving and communication skills
    
    NICE TO HAVE:
    - Kubernetes experience
    - CI/CD pipeline experience
    - Mentoring experience
    - Agile/Scrum experience
    """
    
    job_title = "Senior Software Engineer"
    
    try:
        url = f"{BACKEND_URL}/api/placement-preparation/resume-analysis"
        
        # Create multipart form data with JSON request
        files = {
            'resume': ('test_resume.txt', sample_resume, 'text/plain')
        }
        
        # Create JSON request body
        request_data = {
            'job_title': job_title,
            'job_description': job_description
        }
        
        data = {
            'request': json.dumps(request_data)
        }
        
        print(f"URL: {url}")
        print(f"Job Title: {job_title}")
        print(f"Resume Length: {len(sample_resume)} characters")
        print(f"Job Description Length: {len(job_description)} characters")
        
        response = requests.post(url, files=files, data=data, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: Resume analysis created")
            print(f"Response keys: {list(result.keys())}")
            
            if 'analysis_id' in result:
                analysis_id = result['analysis_id']
                print(f"Analysis ID: {analysis_id}")
                
                # Step 2: Verify the analysis was stored
                print()
                print("📋 STEP 2: Verify Analysis Storage")
                print("-" * 50)
                
                get_url = f"{BACKEND_URL}/api/placement-preparation/resume-analyses"
                get_response = requests.get(get_url, timeout=30)
                
                if get_response.status_code == 200:
                    analyses_data = get_response.json()
                    analyses = analyses_data.get('analyses', [])
                    print(f"✅ Found {len(analyses)} resume analyses in database")
                    
                    if analyses:
                        latest_analysis = analyses[-1]  # Get the most recent one
                        print(f"Latest analysis ID: {latest_analysis.get('id', 'N/A')}")
                        print(f"Latest analysis keys: {list(latest_analysis.keys())}")
                        
                        # Step 3: Test PDF download if available
                        if 'id' in latest_analysis:
                            print()
                            print("📋 STEP 3: Test PDF Download")
                            print("-" * 50)
                            
                            pdf_url = f"{BACKEND_URL}/api/placement-preparation/resume-analysis/{latest_analysis['id']}/download"
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
                print("❌ No analysis_id in response")
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
    test_resume_analysis_workflow()