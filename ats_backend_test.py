#!/usr/bin/env python3
"""
Comprehensive Backend Testing for ATS Score Calculator Endpoint
Testing Agent - ATS Score Calculator Implementation Verification
"""

import requests
import json
import os
import time
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = "https://33e908ff-821c-4359-a046-0a59698e91ec.preview.emergentagent.com/api"

def print_test_header(test_name):
    """Print formatted test header"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_test_result(test_name, success, details=""):
    """Print formatted test result"""
    status = "✅ PASSED" if success else "❌ FAILED"
    print(f"{status} - {test_name}")
    if details:
        print(f"   Details: {details}")

def test_backend_connectivity():
    """Test 1: Backend Connectivity"""
    print_test_header("Backend Connectivity Test")
    
    try:
        # Test basic connectivity
        response = requests.get(f"{BACKEND_URL.replace('/api', '')}/health", timeout=10)
        success = response.status_code in [200, 404, 405]  # Any response means server is up
        print_test_result("Backend Service Connectivity", success, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test_result("Backend Service Connectivity", False, f"Error: {str(e)}")
        return False

def test_ats_endpoint_accessibility():
    """Test 2: ATS Endpoint Accessibility"""
    print_test_header("ATS Endpoint Accessibility Test")
    
    try:
        # Test endpoint accessibility with GET (should return 405 Method Not Allowed)
        response = requests.get(f"{BACKEND_URL}/placement-preparation/ats-score-calculate", timeout=10)
        success = response.status_code == 405  # POST endpoint, GET should return 405
        print_test_result("ATS Endpoint Accessibility", success, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test_result("ATS Endpoint Accessibility", False, f"Error: {str(e)}")
        return False

def create_sample_resume_content():
    """Create sample resume content for testing"""
    return """JANE SMITH
Senior Software Engineer

CONTACT INFORMATION
Email: jane.smith@email.com
Phone: (555) 123-4567
Location: San Francisco, CA

PROFESSIONAL SUMMARY
Experienced Senior Software Engineer with 5+ years of expertise in Python, JavaScript, React, and cloud technologies. Proven track record of building scalable web applications and leading development teams. Strong background in AWS, MongoDB, and modern development practices.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, TypeScript, Java
• Frontend Technologies: React, Vue.js, HTML5, CSS3, Bootstrap
• Backend Technologies: FastAPI, Django, Node.js, Express.js
• Databases: MongoDB, PostgreSQL, MySQL, Redis
• Cloud Platforms: AWS (EC2, S3, Lambda, RDS), Docker, Kubernetes
• Development Tools: Git, Jenkins, JIRA, VS Code
• Testing: Jest, Pytest, Selenium, Unit Testing

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | Jan 2021 - Present
• Led development of microservices architecture serving 100K+ daily users
• Implemented React-based dashboard reducing load times by 40%
• Mentored team of 4 junior developers and conducted code reviews
• Integrated AWS services including Lambda, S3, and RDS for scalable solutions
• Achieved 99.9% uptime for critical production systems

Software Engineer | StartupXYZ | Jun 2019 - Dec 2020
• Developed full-stack web applications using Python/Django and React
• Built RESTful APIs handling 10K+ requests per day
• Implemented automated testing reducing bugs by 60%
• Collaborated with product team to deliver features on tight deadlines
• Optimized database queries improving application performance by 35%

Junior Developer | WebSolutions LLC | Aug 2018 - May 2019
• Created responsive web interfaces using HTML, CSS, and JavaScript
• Assisted in backend development using Python and Flask
• Participated in agile development process and daily standups
• Fixed bugs and implemented minor feature enhancements

EDUCATION
Bachelor of Science in Computer Science
University of California, Berkeley | 2018
GPA: 3.7/4.0

PROJECTS
• E-commerce Platform: Built full-stack application with React frontend and FastAPI backend
• Data Analytics Dashboard: Created real-time dashboard using Python, MongoDB, and D3.js
• Mobile App API: Developed RESTful API serving iOS/Android applications

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate (2022)
• MongoDB Certified Developer (2021)
"""

def test_file_upload_processing():
    """Test 3: File Upload Processing"""
    print_test_header("File Upload Processing Test")
    
    try:
        # Create sample resume file content
        resume_content = create_sample_resume_content()
        
        # Prepare form data
        form_data = {
            'job_title': 'Senior Software Engineer',
            'job_description': 'We are looking for a Senior Software Engineer with 5+ years experience in Python, React, AWS, and MongoDB. Strong problem-solving skills required.'
        }
        
        # Create file-like object for upload
        files = {
            'resume': ('test_resume.txt', resume_content, 'text/plain')
        }
        
        # Test the ATS endpoint
        response = requests.post(
            f"{BACKEND_URL}/placement-preparation/ats-score-calculate",
            data=form_data,
            files=files,
            timeout=30
        )
        
        success = response.status_code == 200
        
        if success:
            response_data = response.json()
            print_test_result("File Upload Processing", True, f"Status: {response.status_code}")
            print(f"   Response keys: {list(response_data.keys())}")
            return response_data
        else:
            print_test_result("File Upload Processing", False, f"Status: {response.status_code}, Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print_test_result("File Upload Processing", False, f"Error: {str(e)}")
        return None

def test_gemini_api_integration(response_data):
    """Test 4: Gemini API Integration"""
    print_test_header("Gemini API Integration Test")
    
    if not response_data:
        print_test_result("Gemini API Integration", False, "No response data from previous test")
        return False
    
    try:
        # Check if analysis_text exists and has substantial content
        analysis_text = response_data.get('analysis_text', '')
        has_analysis = len(analysis_text) > 100  # Should have substantial analysis
        
        # Check for key analysis components
        has_score_section = 'ATS SCORE' in analysis_text or 'COMPREHENSIVE ATS SCORE' in analysis_text
        has_keyword_analysis = 'KEYWORD' in analysis_text.upper()
        has_experience_eval = 'EXPERIENCE' in analysis_text.upper()
        
        success = has_analysis and (has_score_section or has_keyword_analysis or has_experience_eval)
        
        print_test_result("Gemini API Integration", success, f"Analysis length: {len(analysis_text)} chars")
        print_test_result("Score Section Present", has_score_section)
        print_test_result("Keyword Analysis Present", has_keyword_analysis)
        print_test_result("Experience Evaluation Present", has_experience_eval)
        
        return success
        
    except Exception as e:
        print_test_result("Gemini API Integration", False, f"Error: {str(e)}")
        return False

def test_ats_score_extraction(response_data):
    """Test 5: ATS Score Extraction"""
    print_test_header("ATS Score Extraction Test")
    
    if not response_data:
        print_test_result("ATS Score Extraction", False, "No response data from previous test")
        return False
    
    try:
        ats_score = response_data.get('ats_score')
        
        # Validate ATS score
        score_exists = ats_score is not None
        score_valid_range = isinstance(ats_score, int) and 0 <= ats_score <= 100
        score_reasonable = isinstance(ats_score, int) and 30 <= ats_score <= 95  # Reasonable range
        
        success = score_exists and score_valid_range
        
        print_test_result("ATS Score Exists", score_exists, f"Score: {ats_score}")
        print_test_result("ATS Score Valid Range (0-100)", score_valid_range)
        print_test_result("ATS Score Reasonable Range (30-95)", score_reasonable)
        
        return success
        
    except Exception as e:
        print_test_result("ATS Score Extraction", False, f"Error: {str(e)}")
        return False

def test_pdf_generation(response_data):
    """Test 6: PDF Generation"""
    print_test_header("PDF Generation Test")
    
    if not response_data:
        print_test_result("PDF Generation", False, "No response data from previous test")
        return False
    
    try:
        pdf_filename = response_data.get('pdf_filename')
        
        # Validate PDF filename
        filename_exists = pdf_filename is not None and pdf_filename != ""
        filename_format = pdf_filename and pdf_filename.endswith('.pdf')
        filename_pattern = pdf_filename and 'ats_score_report_' in pdf_filename
        
        success = filename_exists and filename_format
        
        print_test_result("PDF Filename Exists", filename_exists, f"Filename: {pdf_filename}")
        print_test_result("PDF Filename Format", filename_format)
        print_test_result("PDF Filename Pattern", filename_pattern)
        
        return success
        
    except Exception as e:
        print_test_result("PDF Generation", False, f"Error: {str(e)}")
        return False

def test_database_storage(response_data):
    """Test 7: Database Storage"""
    print_test_header("Database Storage Test")
    
    if not response_data:
        print_test_result("Database Storage", False, "No response data from previous test")
        return False
    
    try:
        ats_id = response_data.get('ats_id')
        
        # Validate ATS ID (should be UUID format)
        id_exists = ats_id is not None and ats_id != ""
        id_format = ats_id and len(ats_id) >= 32  # UUID should be at least 32 chars
        
        success = id_exists and id_format
        
        print_test_result("ATS ID Generated", id_exists, f"ID: {ats_id}")
        print_test_result("ATS ID Format Valid", id_format)
        
        return success
        
    except Exception as e:
        print_test_result("Database Storage", False, f"Error: {str(e)}")
        return False

def test_response_format(response_data):
    """Test 8: Response Format Validation"""
    print_test_header("Response Format Validation Test")
    
    if not response_data:
        print_test_result("Response Format Validation", False, "No response data from previous test")
        return False
    
    try:
        # Check required fields
        required_fields = ['success', 'ats_id', 'ats_score', 'analysis_text', 'pdf_filename', 'message']
        
        field_results = {}
        for field in required_fields:
            field_exists = field in response_data
            field_results[field] = field_exists
            print_test_result(f"Field '{field}' Present", field_exists)
        
        # Check success field value
        success_value = response_data.get('success') == True
        print_test_result("Success Field Value", success_value, f"Value: {response_data.get('success')}")
        
        # Check message field
        message_exists = response_data.get('message') and len(response_data.get('message', '')) > 0
        print_test_result("Message Field Content", message_exists, f"Message: {response_data.get('message', '')[:50]}...")
        
        all_fields_present = all(field_results.values())
        success = all_fields_present and success_value and message_exists
        
        return success
        
    except Exception as e:
        print_test_result("Response Format Validation", False, f"Error: {str(e)}")
        return False

def run_comprehensive_ats_test():
    """Run comprehensive ATS Score Calculator endpoint test"""
    print(f"\n🚀 STARTING COMPREHENSIVE ATS SCORE CALCULATOR ENDPOINT TESTING")
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    test_results = {}
    
    # Test 1: Backend Connectivity
    test_results['connectivity'] = test_backend_connectivity()
    
    # Test 2: Endpoint Accessibility
    test_results['accessibility'] = test_ats_endpoint_accessibility()
    
    # Test 3: File Upload Processing (Main Test)
    response_data = test_file_upload_processing()
    test_results['file_upload'] = response_data is not None
    
    if response_data:
        # Test 4: Gemini API Integration
        test_results['gemini_integration'] = test_gemini_api_integration(response_data)
        
        # Test 5: ATS Score Extraction
        test_results['score_extraction'] = test_ats_score_extraction(response_data)
        
        # Test 6: PDF Generation
        test_results['pdf_generation'] = test_pdf_generation(response_data)
        
        # Test 7: Database Storage
        test_results['database_storage'] = test_database_storage(response_data)
        
        # Test 8: Response Format
        test_results['response_format'] = test_response_format(response_data)
    else:
        # Mark dependent tests as failed
        test_results['gemini_integration'] = False
        test_results['score_extraction'] = False
        test_results['pdf_generation'] = False
        test_results['database_storage'] = False
        test_results['response_format'] = False
    
    # Print Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUMMARY - ATS Score Calculator Endpoint")
    print(f"{'='*60}")
    
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print(f"\n📈 OVERALL RESULTS:")
    print(f"   Tests Passed: {passed_tests}/{total_tests}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    # Determine overall success
    critical_tests = ['connectivity', 'accessibility', 'file_upload', 'score_extraction', 'response_format']
    critical_passed = sum(1 for test in critical_tests if test_results.get(test, False))
    overall_success = critical_passed >= 4  # At least 4 out of 5 critical tests must pass
    
    print(f"   Overall Status: {'✅ SUCCESS' if overall_success else '❌ FAILURE'}")
    
    if response_data:
        print(f"\n📋 SAMPLE RESPONSE DATA:")
        print(f"   ATS Score: {response_data.get('ats_score', 'N/A')}")
        print(f"   PDF Filename: {response_data.get('pdf_filename', 'N/A')}")
        print(f"   Analysis Length: {len(response_data.get('analysis_text', ''))} characters")
        print(f"   Success: {response_data.get('success', 'N/A')}")
        print(f"   Message: {response_data.get('message', 'N/A')[:100]}...")
    
    return overall_success, test_results, response_data

if __name__ == "__main__":
    success, results, data = run_comprehensive_ats_test()
    exit(0 if success else 1)