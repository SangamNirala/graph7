#!/usr/bin/env python3
"""
Test PDF content to see if reasons are included
"""

import requests
import json
import re

BACKEND_URL = "https://496a63fe-af0f-4647-916e-0b7ce5ebc17e.preview.emergentagent.com"
ATS_ENDPOINT = f"{BACKEND_URL}/api/placement-preparation/ats-score-calculate"

def test_pdf_content():
    resume_content = """John Smith
Senior Software Engineer
john.smith@email.com | (555) 123-4567

PROFESSIONAL SUMMARY
Experienced Software Engineer with 5+ years of expertise in Python, React, and MongoDB development. 
Led teams of 4+ developers and delivered 15+ successful projects with 99.9% uptime.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, TypeScript, Java
• Frontend: React, HTML5, CSS3, Redux
• Backend: FastAPI, Node.js, Express.js
• Databases: MongoDB, PostgreSQL, Redis
• Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD
• Tools: Git, Agile, Scrum, REST API development

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021 - Present
• Developed 10+ REST APIs using Python and FastAPI, serving 50,000+ daily users
• Implemented React-based frontend applications with 40% improved performance
• Led Agile development team of 4 engineers, delivering projects 20% ahead of schedule
• Optimized MongoDB queries, reducing response time by 60%
• Deployed applications on AWS using Docker and Kubernetes

Software Engineer | StartupXYZ | 2019 - 2021
• Built microservices architecture handling 1M+ requests per day
• Developed React components used across 5+ different applications
• Implemented automated testing, increasing code coverage to 95%
• Collaborated with cross-functional teams using Agile methodologies

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2019

CERTIFICATIONS
• AWS Certified Solutions Architect
• MongoDB Certified Developer

PROJECTS
• E-commerce Platform: Built full-stack application with React and Python, handling 10,000+ transactions
• Data Analytics Dashboard: Created real-time dashboard processing 1TB+ data daily
• API Gateway: Designed microservices gateway serving 20+ internal services
"""
    
    files = {
        'resume': ('comprehensive_resume.txt', resume_content.encode(), 'text/plain')
    }
    
    data = {
        'job_title': 'Senior Software Engineer',
        'job_description': '''We are seeking a Senior Software Engineer to join our growing engineering team.

Key Responsibilities:
• Design and develop scalable web applications using modern technologies
• Lead technical architecture decisions and mentor junior developers
• Collaborate with cross-functional teams to deliver high-quality software solutions
• Implement best practices for code quality, testing, and deployment

Required Skills:
• 5+ years of experience in full-stack development
• Strong proficiency in Python and JavaScript
• Experience with React, FastAPI, or Django
• Knowledge of cloud platforms (AWS, GCP, or Azure)
• Experience with databases (PostgreSQL, MongoDB)
• Familiarity with DevOps tools (Docker, Kubernetes, CI/CD)
• Strong problem-solving and communication skills

Preferred Skills:
• Experience with microservices architecture
• Knowledge of TypeScript
• Experience with automated testing
• Leadership experience
• AWS certifications
• Agile/Scrum methodology experience'''
    }
    
    print("🚀 Testing ATS calculation with comprehensive resume...")
    response = requests.post(ATS_ENDPOINT, files=files, data=data, timeout=60)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result.get('success')}")
        print(f"ATS Score: {result.get('ats_score')}")
        
        ats_id = result.get('ats_id')
        pdf_filename = result.get('pdf_filename')
        analysis_text = result.get('analysis_text', '')
        
        print(f"ATS ID: {ats_id}")
        print(f"PDF Filename: {pdf_filename}")
        print(f"Analysis Text Length: {len(analysis_text)} characters")
        
        # Extract key reasons from analysis text
        print("\n" + "="*80)
        print("KEY REASONS IN ANALYSIS TEXT:")
        print("="*80)
        
        # Look for improvement recommendations
        improvement_patterns = [
            r'CRITICAL IMPROVEMENT AREAS:.*?(?=\*\*|$)',
            r'SCORE ENHANCEMENT RECOMMENDATIONS:.*?(?=\*\*|$)',
            r'IMPLEMENTATION ROADMAP:.*?(?=\*\*|$)',
            r'IMMEDIATE FIXES.*?(?=\*\*|$)',
            r'HIGH PRIORITY:.*?(?=\n|$)',
            r'CRITICAL:.*?(?=\n|$)',
            r'FORMATTING:.*?(?=\n|$)'
        ]
        
        found_reasons = []
        for pattern in improvement_patterns:
            matches = re.findall(pattern, analysis_text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                clean_match = match.strip()[:200] + "..." if len(match) > 200 else match.strip()
                found_reasons.append(clean_match)
        
        for i, reason in enumerate(found_reasons, 1):
            print(f"{i}. {reason}")
            print()
        
        # Now test PDF download
        if ats_id and pdf_filename:
            print("="*80)
            print("TESTING PDF DOWNLOAD AND CONTENT:")
            print("="*80)
            
            pdf_download_url = f"{BACKEND_URL}/api/placement-preparation/ats-score/{ats_id}/download"
            print(f"PDF Download URL: {pdf_download_url}")
            
            pdf_response = requests.get(pdf_download_url, timeout=30)
            print(f"PDF Download Status: {pdf_response.status_code}")
            
            if pdf_response.status_code == 200:
                content_type = pdf_response.headers.get('content-type', '')
                content_length = len(pdf_response.content)
                print(f"PDF Content Type: {content_type}")
                print(f"PDF Size: {content_length} bytes")
                
                # Try to extract text from PDF
                try:
                    import PyPDF2
                    import io
                    
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_response.content))
                    pdf_text = ""
                    for page in pdf_reader.pages:
                        pdf_text += page.extract_text() + "\n"
                    
                    print(f"PDF Text Length: {len(pdf_text)} characters")
                    
                    # Check if key reasons appear in PDF
                    print("\n" + "="*60)
                    print("CHECKING IF REASONS APPEAR IN PDF:")
                    print("="*60)
                    
                    # Look for key improvement areas in PDF
                    pdf_improvement_indicators = [
                        'CRITICAL IMPROVEMENT',
                        'HIGH PRIORITY',
                        'IMMEDIATE FIXES',
                        'SCORE ENHANCEMENT',
                        'keyword',
                        'achievement',
                        'quantified',
                        'formatting',
                        'ATS compatibility'
                    ]
                    
                    found_in_pdf = []
                    missing_from_pdf = []
                    
                    for indicator in pdf_improvement_indicators:
                        if indicator.lower() in pdf_text.lower():
                            found_in_pdf.append(indicator)
                        else:
                            missing_from_pdf.append(indicator)
                    
                    print(f"✅ Found in PDF ({len(found_in_pdf)}): {found_in_pdf}")
                    print(f"❌ Missing from PDF ({len(missing_from_pdf)}): {missing_from_pdf}")
                    
                    # Show a sample of PDF content
                    print("\n" + "="*60)
                    print("PDF CONTENT SAMPLE (first 1000 characters):")
                    print("="*60)
                    print(pdf_text[:1000])
                    print("...")
                    
                    # Check if detailed analysis sections are in PDF
                    detailed_sections = [
                        'DETAILED ANALYSIS',
                        'SCORE BREAKDOWN',
                        'EDUCATIONAL QUALIFICATIONS',
                        'PROFESSIONAL EXPERIENCE',
                        'SKILLS & COMPETENCIES'
                    ]
                    
                    print("\n" + "="*60)
                    print("DETAILED SECTIONS IN PDF:")
                    print("="*60)
                    
                    for section in detailed_sections:
                        if section in pdf_text:
                            print(f"✅ {section}")
                        else:
                            print(f"❌ {section}")
                    
                    # Calculate content coverage
                    analysis_words = set(analysis_text.lower().split())
                    pdf_words = set(pdf_text.lower().split())
                    common_words = analysis_words.intersection(pdf_words)
                    coverage = len(common_words) / len(analysis_words) if analysis_words else 0
                    
                    print(f"\nContent Coverage: {coverage:.2%} ({len(common_words)}/{len(analysis_words)} words)")
                    
                    return {
                        'analysis_has_reasons': len(found_reasons) > 0,
                        'pdf_has_reasons': len(found_in_pdf) > 0,
                        'content_coverage': coverage,
                        'pdf_size': content_length,
                        'reasons_found': len(found_reasons),
                        'reasons_in_pdf': len(found_in_pdf)
                    }
                    
                except ImportError:
                    print("PyPDF2 not available for PDF text extraction")
                    return {
                        'analysis_has_reasons': len(found_reasons) > 0,
                        'pdf_downloaded': True,
                        'pdf_size': content_length,
                        'reasons_found': len(found_reasons)
                    }
            else:
                print(f"PDF Download Failed: {pdf_response.text}")
                return None
        else:
            print("No PDF generated")
            return None
    else:
        print(f"ATS Calculation Failed: {response.text}")
        return None

if __name__ == "__main__":
    result = test_pdf_content()
    if result:
        print("\n" + "="*80)
        print("SUMMARY:")
        print("="*80)
        print(f"Analysis has detailed reasons: {result.get('analysis_has_reasons', False)}")
        print(f"PDF has reasons: {result.get('pdf_has_reasons', False)}")
        print(f"Content coverage: {result.get('content_coverage', 0):.2%}")
        print(f"Reasons found in analysis: {result.get('reasons_found', 0)}")
        print(f"Reasons found in PDF: {result.get('reasons_in_pdf', 0)}")