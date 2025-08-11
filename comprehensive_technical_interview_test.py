#!/usr/bin/env python3
"""
Comprehensive Technical Interview Questions Feature Test
Tests the complete workflow as specified in the continuation request
"""

import requests
import json
import sys
import os
from io import BytesIO
import time

# Test configuration
API_BASE = "http://localhost:8001/api"
TEST_JOB_TITLE = "Senior Software Engineer"
TEST_JOB_DESCRIPTION = """
We are seeking a Senior Software Engineer with 5+ years of experience to join our growing technology team. 

Key Requirements:
- 5+ years of professional software development experience
- Strong proficiency in React.js and modern JavaScript (ES6+)
- Backend development experience with Node.js and Express
- Database experience with MongoDB and SQL databases
- Cloud platform experience (AWS, Azure, or GCP)
- Experience with microservices architecture
- Knowledge of CI/CD pipelines and DevOps practices
- Strong problem-solving and debugging skills
- Experience with version control (Git) and agile methodologies

Preferred Qualifications:
- Experience with TypeScript
- Knowledge of Docker and Kubernetes
- Experience with API design and RESTful services
- Understanding of software architecture patterns
- Experience mentoring junior developers
- Bachelor's degree in Computer Science or related field

Responsibilities:
- Design and develop scalable web applications
- Collaborate with cross-functional teams
- Lead technical discussions and code reviews
- Mentor junior team members
- Contribute to architecture decisions
"""

TEST_RESUME_CONTENT = """
John Smith
Senior Software Engineer
Email: john.smith@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johnsmith | GitHub: github.com/johnsmith

SUMMARY
Experienced Senior Software Engineer with 8+ years of expertise in full-stack web development, specializing in React.js, Node.js, and cloud-based solutions. Proven track record of leading technical teams, architecting scalable systems, and delivering high-quality software products in fast-paced environments.

TECHNICAL SKILLS
• Frontend: React.js, TypeScript, JavaScript (ES6+), HTML5, CSS3, Redux, Next.js
• Backend: Node.js, Express.js, Python, Java, RESTful APIs, GraphQL
• Databases: MongoDB, PostgreSQL, MySQL, Redis
• Cloud Platforms: AWS (EC2, S3, Lambda, RDS), Azure, Docker, Kubernetes
• DevOps: CI/CD pipelines, Jenkins, GitHub Actions, Docker, Terraform
• Tools: Git, Jira, Agile methodologies, Test-driven development

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2020 - Present
• Led development of microservices architecture serving 10M+ users daily
• Designed and implemented React-based dashboard reducing customer support tickets by 40%
• Architected Node.js backend services with 99.9% uptime and sub-200ms response times
• Mentored team of 5 junior developers and conducted technical interviews
• Implemented CI/CD pipelines reducing deployment time by 60%

Software Engineer | StartupXYZ | 2018 - 2020
• Built full-stack applications using React, Node.js, and MongoDB
• Developed RESTful APIs handling 1M+ requests per day
• Optimized database queries improving application performance by 50%
• Collaborated with product team to deliver features ahead of schedule

Software Developer | DevStudio | 2016 - 2018
• Developed responsive web applications using modern JavaScript frameworks
• Worked with cross-functional teams in agile environment
• Contributed to open-source projects and technical documentation

EDUCATION
Bachelor of Science in Computer Science
State University | 2016

ACHIEVEMENTS
• AWS Certified Solutions Architect
• Led migration of legacy system to cloud infrastructure
• Speaker at local tech meetups on React best practices
• Contributed to popular open-source libraries with 1000+ stars
"""

def test_backend_connectivity():
    """Test if backend is accessible"""
    print("🔧 Testing backend connectivity...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend connectivity successful")
            return True
        else:
            print(f"❌ Backend connectivity failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connectivity error: {e}")
        return False

def test_technical_interview_questions_generation():
    """Test POST endpoint for generating technical interview questions"""
    print("\n🚀 Testing Technical Interview Questions Generation...")
    
    try:
        # Create resume file in memory
        resume_file = BytesIO(TEST_RESUME_CONTENT.encode('utf-8'))
        
        # Prepare FormData
        files = {
            'resume': ('test_resume.txt', resume_file, 'text/plain')
        }
        data = {
            'job_title': TEST_JOB_TITLE,
            'job_description': TEST_JOB_DESCRIPTION
        }
        
        # Make request
        response = requests.post(
            f"{API_BASE}/placement-preparation/technical-interview-questions",
            data=data,
            files=files,
            timeout=60  # Increased timeout for LLM processing
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis_id = result.get('id')
            interview_questions = result.get('interview_questions', '')
            
            print(f"✅ Technical Interview Questions generated successfully")
            print(f"📊 Analysis ID: {analysis_id}")
            print(f"📝 Content Length: {len(interview_questions)} characters")
            
            # Analyze content quality
            question_count = interview_questions.count('Question ')
            print(f"🔢 Detected Questions: {question_count}")
            
            # Check for required categories
            categories = [
                'FOUNDATIONAL KNOWLEDGE',
                'PRACTICAL APPLICATION', 
                'EXPERIENCE-DEPTH VALIDATION',
                'ADVANCED ARCHITECTURAL THINKING',
                'EXPERT-LEVEL ROLE ALIGNMENT'
            ]
            
            found_categories = []
            for category in categories:
                if category in interview_questions.upper():
                    found_categories.append(category)
            
            print(f"📋 Categories Found: {len(found_categories)}/5")
            for cat in found_categories:
                print(f"   ✅ {cat}")
            
            # Check for HTML formatting
            html_indicators = ['<html', '<body', '<div class=', '<style']
            html_found = sum(1 for indicator in html_indicators if indicator in interview_questions.lower())
            print(f"🎨 HTML Formatting Indicators: {html_found}/4")
            
            # Check for role-specific keywords
            role_keywords = ['React', 'Node.js', 'MongoDB', 'AWS', 'microservices', 'JavaScript']
            keywords_found = []
            for keyword in role_keywords:
                if keyword.lower() in interview_questions.lower():
                    keywords_found.append(keyword)
            
            print(f"🔍 Role-specific Keywords Found: {len(keywords_found)}/6")
            for keyword in keywords_found:
                print(f"   ✅ {keyword}")
            
            # Quality assessment
            if question_count >= 25 and len(found_categories) >= 5 and html_found >= 3:
                print("🎉 Quality Assessment: EXCELLENT - Meets all requirements")
                quality_score = 5
            elif question_count >= 20 and len(found_categories) >= 4 and html_found >= 2:
                print("✅ Quality Assessment: GOOD - Meets most requirements")
                quality_score = 4
            elif question_count >= 15 and len(found_categories) >= 3:
                print("⚠️ Quality Assessment: ACCEPTABLE - Basic requirements met")
                quality_score = 3
            else:
                print("❌ Quality Assessment: POOR - Requirements not met")
                quality_score = 2
            
            return {
                'success': True,
                'analysis_id': analysis_id,
                'content_length': len(interview_questions),
                'question_count': question_count,
                'categories_found': len(found_categories),
                'html_indicators': html_found,
                'keywords_found': len(keywords_found),
                'quality_score': quality_score
            }
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            print(f"❌ Technical Interview Questions generation failed: {response.status_code}")
            print(f"Error details: {error_data}")
            return {'success': False, 'error': error_data}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error during technical interview questions generation: {e}")
        return {'success': False, 'error': str(e)}
    except Exception as e:
        print(f"❌ Unexpected error during technical interview questions generation: {e}")
        return {'success': False, 'error': str(e)}

def test_get_analyses():
    """Test GET endpoint for retrieving all technical interview questions analyses"""
    print("\n📋 Testing Technical Interview Questions Retrieval...")
    
    try:
        response = requests.get(f"{API_BASE}/placement-preparation/technical-interview-questions", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            analyses = result.get('analyses', [])
            
            print(f"✅ Retrieved {len(analyses)} technical interview questions analyses")
            
            if analyses:
                latest = analyses[0]
                print(f"📊 Latest Analysis:")
                print(f"   ID: {latest.get('id')}")
                print(f"   Job Title: {latest.get('job_title')}")
                print(f"   Created: {latest.get('created_at')}")
                print(f"   Content Length: {len(latest.get('interview_questions', ''))}")
            
            return {'success': True, 'count': len(analyses), 'analyses': analyses}
        else:
            print(f"❌ Failed to retrieve analyses: {response.status_code}")
            return {'success': False}
            
    except Exception as e:
        print(f"❌ Error retrieving analyses: {e}")
        return {'success': False, 'error': str(e)}

def test_pdf_download(analysis_id):
    """Test PDF download functionality"""
    print(f"\n📄 Testing PDF Download for Analysis {analysis_id}...")
    
    try:
        response = requests.get(
            f"{API_BASE}/placement-preparation/technical-interview-questions/{analysis_id}/download",
            timeout=30
        )
        
        if response.status_code == 200:
            pdf_content = response.content
            content_type = response.headers.get('content-type')
            
            print(f"✅ PDF downloaded successfully")
            print(f"📊 PDF Size: {len(pdf_content)} bytes")
            print(f"📋 Content Type: {content_type}")
            
            # Validate PDF format
            if pdf_content.startswith(b'%PDF'):
                print("✅ Valid PDF format confirmed")
                return {'success': True, 'size': len(pdf_content)}
            else:
                print("❌ Invalid PDF format")
                return {'success': False, 'error': 'Invalid PDF format'}
                
        else:
            print(f"❌ PDF download failed: {response.status_code}")
            return {'success': False, 'error': f'Status {response.status_code}'}
            
    except Exception as e:
        print(f"❌ Error downloading PDF: {e}")
        return {'success': False, 'error': str(e)}

def main():
    """Run comprehensive technical interview questions feature test"""
    print("🎯 COMPREHENSIVE TECHNICAL INTERVIEW QUESTIONS FEATURE TEST")
    print("=" * 70)
    
    test_results = {
        'backend_connectivity': False,
        'generation': False,
        'retrieval': False,
        'pdf_download': False,
        'overall_success': False
    }
    
    # Test 1: Backend Connectivity
    if not test_backend_connectivity():
        print("\n❌ Backend connectivity failed. Cannot proceed with other tests.")
        sys.exit(1)
    test_results['backend_connectivity'] = True
    
    # Test 2: Technical Interview Questions Generation
    generation_result = test_technical_interview_questions_generation()
    if generation_result['success']:
        test_results['generation'] = True
        analysis_id = generation_result['analysis_id']
    else:
        print("\n❌ Technical Interview Questions generation failed. Skipping dependent tests.")
        return test_results
    
    # Test 3: Retrieval of Analyses
    retrieval_result = test_get_analyses()
    test_results['retrieval'] = retrieval_result['success']
    
    # Test 4: PDF Download
    if analysis_id:
        pdf_result = test_pdf_download(analysis_id)
        test_results['pdf_download'] = pdf_result['success']
    
    # Overall Assessment
    passed_tests = sum(1 for test in test_results.values() if test)
    total_tests = len(test_results) - 1  # Exclude overall_success
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"\n🏆 TEST SUMMARY")
    print("=" * 50)
    print(f"📊 Tests Passed: {passed_tests}/{total_tests}")
    print(f"✅ Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 100:
        print("🎉 ALL TESTS PASSED - Technical Interview Questions feature is fully operational!")
        test_results['overall_success'] = True
    elif success_rate >= 75:
        print("✅ MOSTLY SUCCESSFUL - Minor issues detected but core functionality works")
        test_results['overall_success'] = True
    else:
        print("❌ SIGNIFICANT ISSUES - Technical Interview Questions feature needs attention")
    
    # Specific findings for continuation request
    print(f"\n📋 CONTINUATION REQUEST VERIFICATION:")
    if generation_result['success']:
        if generation_result['question_count'] >= 25:
            print("✅ 25+ Questions: CONFIRMED")
        else:
            print(f"⚠️ 25+ Questions: PARTIAL ({generation_result['question_count']} found)")
            
        if generation_result['categories_found'] >= 5:
            print("✅ 5 Categories: CONFIRMED")
        else:
            print(f"⚠️ 5 Categories: PARTIAL ({generation_result['categories_found']}/5)")
            
        if generation_result['html_indicators'] >= 3:
            print("✅ HTML Formatting: CONFIRMED")
        else:
            print("⚠️ HTML Formatting: NEEDS IMPROVEMENT")
            
        if generation_result['quality_score'] >= 4:
            print("✅ Overall Quality: EXCELLENT")
        else:
            print("⚠️ Overall Quality: NEEDS IMPROVEMENT")
    
    return test_results

if __name__ == "__main__":
    try:
        results = main()
        print(f"\n🎯 Final Status: {'SUCCESS' if results['overall_success'] else 'NEEDS ATTENTION'}")
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test execution error: {e}")