#!/usr/bin/env python3
"""
Detailed Rejection Reasons Analysis Test
Focus: Examining the actual LLM output to identify why only 3 bullet points are generated
"""

import requests
import json
import os
import time
from datetime import datetime
import tempfile

# Configuration
BACKEND_URL = "https://65275256-099e-4a3f-b83d-fcbfb7a6d86b.preview.emergentagent.com/api"

def test_detailed_rejection_analysis():
    """
    Test the rejection reasons analysis with detailed output examination
    """
    print("🔍 DETAILED REJECTION REASONS ANALYSIS TEST")
    print("=" * 80)
    
    # Test data with clear technical requirements to generate multiple rejection reasons
    job_title = "Senior Full Stack Developer"
    job_description = """
We are seeking a Senior Full Stack Developer with 5+ years of experience to join our growing team.

REQUIRED TECHNICAL SKILLS:
- React.js and Next.js framework expertise
- Node.js and Express.js backend development
- TypeScript proficiency (mandatory)
- PostgreSQL database design and optimization
- AWS cloud services (EC2, S3, RDS, Lambda)
- Docker containerization and Kubernetes orchestration
- GraphQL API development and Apollo Client
- Redis caching implementation
- Elasticsearch for search functionality
- Git version control and CI/CD pipelines
- Jest and Cypress testing frameworks
- Microservices architecture experience

REQUIRED EXPERIENCE:
- 5+ years full-stack development experience
- 2+ years team leadership experience
- Experience with high-traffic applications (1M+ users)
- Agile/Scrum methodology experience
- Code review and mentoring experience
- Performance optimization experience
- Security best practices implementation

REQUIRED QUALIFICATIONS:
- Bachelor's degree in Computer Science or related field
- AWS Certified Solutions Architect certification
- Experience with startup environments
- Strong communication and collaboration skills
- Experience with remote team management

PREFERRED SKILLS:
- Python and Django knowledge
- Machine Learning integration experience
- Mobile app development (React Native)
- DevOps and infrastructure management
- Technical writing and documentation skills
"""

    # Create a realistic but limited resume that will generate multiple rejection reasons
    resume_content = """
John Smith
Software Developer
Email: john.smith@email.com
Phone: (555) 123-4567

SUMMARY:
Junior software developer with 2 years of experience in web development. 
Passionate about learning new technologies and building user-friendly applications.

TECHNICAL SKILLS:
- JavaScript (ES6+)
- HTML5 and CSS3
- Basic React.js knowledge
- MySQL database basics
- Git version control
- Basic Linux commands

EXPERIENCE:
Software Developer Intern | Tech Startup | 2022-2024
- Developed simple web applications using JavaScript and HTML
- Fixed bugs in existing codebase
- Participated in daily standup meetings
- Learned React.js basics during internship
- Worked with small team of 3 developers

Junior Web Developer | Small Agency | 2021-2022
- Created static websites using HTML, CSS, and JavaScript
- Basic WordPress customization
- Client communication and requirement gathering

EDUCATION:
Associate Degree in Information Technology | Community College | 2021
- Coursework in basic programming and web development
- GPA: 3.2/4.0

PROJECTS:
- Personal Portfolio Website (HTML, CSS, JavaScript)
- Simple Todo App (React.js, local storage)
- Basic Calculator (JavaScript)
"""

    # Create temporary resume file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
        temp_file.write(resume_content)
        temp_file_path = temp_file.name

    try:
        print("📝 Test Data:")
        print(f"Job Title: {job_title}")
        print(f"Job Description Length: {len(job_description)} characters")
        print(f"Resume Content Length: {len(resume_content)} characters")
        print()

        # Main Rejection Reasons Analysis
        print("🔗 REJECTION REASONS ANALYSIS")
        with open(temp_file_path, 'rb') as f:
            files = {'resume': ('resume.txt', f, 'text/plain')}
            data = {
                'job_title': job_title,
                'job_description': job_description
            }
            
            print("📤 Sending rejection reasons analysis request...")
            start_time = time.time()
            response = requests.post(f"{BACKEND_URL}/placement-preparation/rejection-reasons", 
                                   data=data, files=files, timeout=60)
            end_time = time.time()
            
            print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Rejection reasons analysis completed successfully")
                
                # Extract and analyze the rejection reasons
                rejection_reasons = result.get('rejection_reasons', '')
                rejection_id = result.get('rejection_id', '')
                pdf_filename = result.get('pdf_filename', '')
                
                print(f"📄 Rejection ID: {rejection_id}")
                print(f"📄 PDF Filename: {pdf_filename}")
                print(f"📄 Analysis Length: {len(rejection_reasons)} characters")
                print()
                
                # Detailed Analysis of LLM Output
                print("🔍 DETAILED LLM OUTPUT ANALYSIS:")
                print("-" * 50)
                
                # Count bullet points
                bullet_points = [line for line in rejection_reasons.split('\n') if line.strip().startswith('•')]
                print(f"📊 Total bullet points found: {len(bullet_points)}")
                
                # Count sub-points
                sub_points = [line for line in rejection_reasons.split('\n') if line.strip().startswith('-')]
                print(f"📊 Total sub-points found: {len(sub_points)}")
                
                # Analyze structure
                lines = rejection_reasons.split('\n')
                non_empty_lines = [line for line in lines if line.strip()]
                print(f"📊 Total non-empty lines: {len(non_empty_lines)}")
                
                # Check for required sections
                required_sections = [
                    "REJECTION REASONS",
                    "TECHNICAL SKILL",
                    "EXPERIENCE",
                    "EDUCATIONAL",
                    "PROGRAMMING LANGUAGES",
                    "FRAMEWORKS",
                    "DATABASE",
                    "CLOUD PLATFORMS"
                ]
                
                found_sections = []
                for section in required_sections:
                    if section.upper() in rejection_reasons.upper():
                        found_sections.append(section)
                
                print(f"📊 Required sections found: {len(found_sections)}/{len(required_sections)}")
                print(f"📊 Found sections: {found_sections}")
                print()
                
                # Display all bullet points for analysis
                print("📋 ALL BULLET POINTS ANALYSIS:")
                print("-" * 40)
                for i, bullet in enumerate(bullet_points, 1):
                    print(f"{i}. {bullet.strip()}")
                print()
                
                # Check if analysis meets requirements
                meets_length_req = len(rejection_reasons) >= 1000
                meets_bullet_req = len(bullet_points) >= 8
                
                print("📊 REQUIREMENT ANALYSIS:")
                print(f"✅ Length requirement (1000+ chars): {'PASS' if meets_length_req else 'FAIL'} ({len(rejection_reasons)} chars)")
                print(f"✅ Bullet points requirement (8+): {'PASS' if meets_bullet_req else 'FAIL'} ({len(bullet_points)} bullets)")
                print()
                
                # Show full analysis for debugging
                print("📄 FULL LLM ANALYSIS OUTPUT:")
                print("=" * 60)
                print(rejection_reasons)
                print("=" * 60)
                print()
                
                # Analysis of the issue
                if len(bullet_points) < 8:
                    print("🚨 ISSUE ANALYSIS:")
                    print(f"❌ LLM generated only {len(bullet_points)} bullet points instead of expected 8+")
                    print("❌ This confirms the user's concern about insufficient rejection reasons")
                    print()
                    
                    # Check if the prompt is being followed
                    prompt_indicators = [
                        "COMPREHENSIVE EVALUATION PROTOCOL",
                        "EXHAUSTIVE GAP IDENTIFICATION", 
                        "MANDATORY OUTPUT FORMAT",
                        "PROCESSING RULES FOR COMPREHENSIVE COVERAGE"
                    ]
                    
                    found_indicators = [ind for ind in prompt_indicators if ind in rejection_reasons.upper()]
                    print(f"📊 Prompt structure indicators found: {len(found_indicators)}/{len(prompt_indicators)}")
                    
                    # Check for evidence structure
                    evidence_structure = [
                        "Required:",
                        "Candidate Reality:",
                        "Gap Impact:"
                    ]
                    
                    found_evidence = [ev for ev in evidence_structure if ev in rejection_reasons]
                    print(f"📊 Evidence structure found: {len(found_evidence)}/{len(evidence_structure)}")
                    
                    print()
                    print("🔧 POTENTIAL ROOT CAUSES:")
                    print("1. LLM prompt may be too complex - model might be ignoring detailed instructions")
                    print("2. Gemini model might have response length limitations")
                    print("3. Model might be prioritizing quality over quantity")
                    print("4. Temperature/parameters might need adjustment for more comprehensive output")
                    print("5. The prompt structure might need simplification for better instruction following")
                
                return True
                
            else:
                print(f"❌ Rejection reasons analysis failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False

    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def main():
    """Main testing function"""
    print("🚀 STARTING DETAILED REJECTION REASONS ANALYSIS")
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = test_detailed_rejection_analysis()
    
    print()
    print(f"🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Overall result: {'✅ SUCCESS' if success else '❌ FAILED'}")

if __name__ == "__main__":
    main()