#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Rejection Reasons Analysis Functionality
Testing Agent - Focus on New Rejection Reasons Feature
"""

import requests
import json
import os
import time
from datetime import datetime
import tempfile

# Configuration
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://ac4a8740-efd2-428f-8ad3-3fb890045006.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

def log_test_result(test_name, status, details=""):
    """Log test results with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
    print(f"[{timestamp}] {status_symbol} {test_name}: {status}")
    if details:
        print(f"    Details: {details}")
    print()

def test_backend_connectivity():
    """Test basic backend connectivity"""
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=10)
        if response.status_code == 200:
            log_test_result("Backend Connectivity", "PASS", f"Status: {response.status_code}")
            return True
        else:
            log_test_result("Backend Connectivity", "FAIL", f"Status: {response.status_code}")
            return False
    except Exception as e:
        log_test_result("Backend Connectivity", "FAIL", f"Error: {str(e)}")
        return False

def create_test_resume_file():
    """Create a realistic test resume file for testing"""
    resume_content = """SARAH JOHNSON
Senior Software Engineer
Email: sarah.johnson@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/sarahjohnson | GitHub: github.com/sarahjohnson

PROFESSIONAL SUMMARY
Experienced software engineer with 6+ years developing scalable web applications using modern technologies. 
Strong background in full-stack development, cloud architecture, and agile methodologies.

TECHNICAL SKILLS
• Programming Languages: JavaScript, Python, Java
• Frontend: React, Vue.js, HTML5, CSS3, TypeScript
• Backend: Node.js, Express.js, Django, Spring Boot
• Databases: PostgreSQL, MongoDB, Redis
• Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
• Tools: Git, Jenkins, JIRA, Postman

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021 - Present
• Led development of microservices architecture serving 100K+ daily users
• Implemented CI/CD pipelines reducing deployment time by 60%
• Mentored 3 junior developers and conducted code reviews
• Built RESTful APIs and integrated third-party services

Software Engineer | StartupXYZ | 2019 - 2021
• Developed responsive web applications using React and Node.js
• Collaborated with cross-functional teams in agile environment
• Optimized database queries improving performance by 40%
• Participated in on-call rotation for production support

Junior Developer | WebSolutions | 2018 - 2019
• Built frontend components using HTML, CSS, and JavaScript
• Assisted in bug fixes and feature enhancements
• Learned version control with Git and participated in code reviews

EDUCATION
Bachelor of Science in Computer Science
State University | 2018
GPA: 3.7/4.0

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate (2022)
• Certified Scrum Master (2021)

PROJECTS
• E-commerce Platform: Built full-stack application with React, Node.js, and PostgreSQL
• Task Management API: Developed RESTful API with authentication and real-time updates
• Data Visualization Dashboard: Created interactive charts using D3.js and Python"""
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_file.write(resume_content)
    temp_file.close()
    return temp_file.name, resume_content

def test_rejection_reasons_analysis():
    """Test the new rejection reasons analysis endpoint"""
    try:
        # Create test resume file
        resume_file_path, resume_content = create_test_resume_file()
        
        # Test data - realistic job requirements that will generate rejection reasons
        job_title = "Principal Machine Learning Engineer"
        job_description = """We are seeking a Principal Machine Learning Engineer to lead our AI initiatives.

REQUIRED QUALIFICATIONS:
• PhD in Computer Science, Machine Learning, or related field
• 10+ years of experience in machine learning and AI
• Expert-level proficiency in Python, TensorFlow, PyTorch
• Deep experience with NLP, computer vision, and deep learning
• Experience with MLOps, model deployment, and production systems
• Strong background in statistics, mathematics, and algorithms
• Experience leading ML teams of 5+ engineers
• Publications in top-tier ML conferences (NIPS, ICML, ICLR)
• Experience with distributed computing (Spark, Hadoop)
• Cloud ML platforms (AWS SageMaker, Google AI Platform)
• Real-time ML inference systems and model optimization
• A/B testing and experimentation frameworks
• Kubernetes and Docker for ML workloads
• Advanced degree in quantitative field required

PREFERRED QUALIFICATIONS:
• Experience in healthcare/medical AI applications
• Knowledge of federated learning and privacy-preserving ML
• Experience with edge computing and mobile ML deployment
• Background in reinforcement learning and robotics
• Industry experience at FAANG companies
• Track record of ML patents and intellectual property"""

        # Prepare multipart form data
        with open(resume_file_path, 'rb') as f:
            files = {
                'resume': ('test_resume.txt', f, 'text/plain')
            }
            data = {
                'job_title': job_title,
                'job_description': job_description
            }
            
            # Make request to rejection reasons endpoint
            response = requests.post(
                f"{API_BASE}/placement-preparation/rejection-reasons",
                files=files,
                data=data,
                timeout=60  # Longer timeout for LLM processing
            )
        
        # Clean up temp file
        os.unlink(resume_file_path)
        
        if response.status_code == 200:
            result = response.json()
            
            # Validate response structure
            required_fields = ['success', 'rejection_id', 'rejection_reasons', 'pdf_filename']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                log_test_result("Rejection Reasons Analysis - Response Structure", "FAIL", 
                              f"Missing fields: {missing_fields}")
                return False, None
            
            # Validate content
            if not result.get('success'):
                log_test_result("Rejection Reasons Analysis - Success Flag", "FAIL", 
                              "Success flag is False")
                return False, None
            
            rejection_reasons = result.get('rejection_reasons', '')
            if len(rejection_reasons) < 500:  # Should be comprehensive
                log_test_result("Rejection Reasons Analysis - Content Length", "FAIL", 
                              f"Analysis too short: {len(rejection_reasons)} characters")
                return False, None
            
            # Check for bullet points (comprehensive format)
            bullet_count = rejection_reasons.count('•')
            if bullet_count < 5:  # Should have multiple rejection reasons
                log_test_result("Rejection Reasons Analysis - Bullet Points", "FAIL", 
                              f"Too few bullet points: {bullet_count}")
                return False, None
            
            # Check for required sections/keywords
            required_keywords = ['REJECTION REASONS', 'Required:', 'Candidate Reality:', 'Gap Impact:']
            missing_keywords = [kw for kw in required_keywords if kw not in rejection_reasons]
            
            if missing_keywords:
                log_test_result("Rejection Reasons Analysis - Required Keywords", "FAIL", 
                              f"Missing keywords: {missing_keywords}")
                return False, None
            
            log_test_result("Rejection Reasons Analysis - Core Functionality", "PASS", 
                          f"Generated {len(rejection_reasons)} chars, {bullet_count} bullet points, ID: {result['rejection_id']}")
            
            return True, result
            
        else:
            log_test_result("Rejection Reasons Analysis - API Call", "FAIL", 
                          f"Status: {response.status_code}, Response: {response.text}")
            return False, None
            
    except Exception as e:
        log_test_result("Rejection Reasons Analysis - Exception", "FAIL", f"Error: {str(e)}")
        return False, None

def test_pdf_generation_and_download(rejection_id):
    """Test PDF generation and download functionality"""
    try:
        # Test PDF download endpoint
        response = requests.get(
            f"{API_BASE}/placement-preparation/rejection-reasons/{rejection_id}/download",
            timeout=30
        )
        
        if response.status_code == 200:
            # Validate PDF content
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' not in content_type:
                log_test_result("PDF Download - Content Type", "FAIL", 
                              f"Wrong content type: {content_type}")
                return False
            
            pdf_size = len(response.content)
            if pdf_size < 1000:  # PDF should be substantial
                log_test_result("PDF Download - File Size", "FAIL", 
                              f"PDF too small: {pdf_size} bytes")
                return False
            
            # Check PDF headers
            pdf_content = response.content
            if not pdf_content.startswith(b'%PDF'):
                log_test_result("PDF Download - PDF Format", "FAIL", 
                              "Invalid PDF format")
                return False
            
            log_test_result("PDF Generation and Download", "PASS", 
                          f"PDF downloaded successfully: {pdf_size} bytes, Content-Type: {content_type}")
            return True
            
        else:
            log_test_result("PDF Download - API Call", "FAIL", 
                          f"Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        log_test_result("PDF Generation and Download - Exception", "FAIL", f"Error: {str(e)}")
        return False

def test_database_storage():
    """Test database storage and retrieval of rejection reasons analyses"""
    try:
        # Test GET endpoint for all analyses
        response = requests.get(
            f"{API_BASE}/placement-preparation/rejection-reasons",
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if 'analyses' not in result:
                log_test_result("Database Storage - Response Structure", "FAIL", 
                              "Missing 'analyses' field in response")
                return False
            
            analyses = result['analyses']
            if not isinstance(analyses, list):
                log_test_result("Database Storage - Data Type", "FAIL", 
                              "Analyses should be a list")
                return False
            
            if len(analyses) == 0:
                log_test_result("Database Storage - Data Presence", "FAIL", 
                              "No analyses found in database")
                return False
            
            # Validate structure of first analysis
            first_analysis = analyses[0]
            required_fields = ['id', 'job_title', 'job_description', 'rejection_reasons', 'created_at']
            missing_fields = [field for field in required_fields if field not in first_analysis]
            
            if missing_fields:
                log_test_result("Database Storage - Analysis Structure", "FAIL", 
                              f"Missing fields in analysis: {missing_fields}")
                return False
            
            log_test_result("Database Storage and Retrieval", "PASS", 
                          f"Found {len(analyses)} analyses in database")
            return True
            
        else:
            log_test_result("Database Storage - API Call", "FAIL", 
                          f"Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        log_test_result("Database Storage - Exception", "FAIL", f"Error: {str(e)}")
        return False

def test_error_handling():
    """Test error handling for invalid inputs"""
    try:
        # Test 1: Invalid file format
        invalid_file_content = b"This is not a valid resume file"
        files = {
            'resume': ('test.xyz', invalid_file_content, 'application/octet-stream')
        }
        data = {
            'job_title': 'Test Job',
            'job_description': 'Test description'
        }
        
        response = requests.post(
            f"{API_BASE}/placement-preparation/rejection-reasons",
            files=files,
            data=data,
            timeout=30
        )
        
        if response.status_code != 400:
            log_test_result("Error Handling - Invalid File Format", "FAIL", 
                          f"Expected 400, got {response.status_code}")
            return False
        
        # Test 2: Missing required fields
        resume_file_path, _ = create_test_resume_file()
        with open(resume_file_path, 'rb') as f:
            files = {
                'resume': ('test_resume.txt', f, 'text/plain')
            }
            data = {
                'job_title': 'Test Job'
                # Missing job_description
            }
            
            response = requests.post(
                f"{API_BASE}/placement-preparation/rejection-reasons",
                files=files,
                data=data,
                timeout=30
            )
        
        os.unlink(resume_file_path)
        
        if response.status_code not in [400, 422]:  # FastAPI returns 422 for validation errors
            log_test_result("Error Handling - Missing Fields", "FAIL", 
                          f"Expected 400/422, got {response.status_code}")
            return False
        
        # Test 3: Invalid rejection ID for PDF download
        response = requests.get(
            f"{API_BASE}/placement-preparation/rejection-reasons/invalid-id/download",
            timeout=15
        )
        
        if response.status_code != 404:
            log_test_result("Error Handling - Invalid Rejection ID", "FAIL", 
                          f"Expected 404, got {response.status_code}")
            return False
        
        log_test_result("Error Handling", "PASS", 
                      "All error scenarios handled correctly")
        return True
        
    except Exception as e:
        log_test_result("Error Handling - Exception", "FAIL", f"Error: {str(e)}")
        return False

def test_comprehensive_analysis_quality():
    """Test the quality and comprehensiveness of rejection reasons analysis"""
    try:
        # Create test resume file
        resume_file_path, resume_content = create_test_resume_file()
        
        # Use a very specific job that should generate many rejection reasons
        job_title = "Senior Data Scientist - Healthcare AI"
        job_description = """We are seeking a Senior Data Scientist specializing in Healthcare AI applications.

REQUIRED QUALIFICATIONS:
• PhD in Statistics, Biostatistics, or Computational Biology
• 8+ years of experience in healthcare data science
• Expert proficiency in R, SAS, and STATA (Python secondary)
• Deep learning experience with medical imaging (radiology, pathology)
• Clinical trial design and biostatistical analysis
• FDA regulatory submission experience
• HIPAA compliance and healthcare data privacy expertise
• Experience with electronic health records (EHR) systems
• Medical device software development (FDA 510k process)
• Publications in medical journals (NEJM, Lancet, JAMA)
• Board certification in biostatistics or epidemiology
• Experience with genomics and precision medicine
• Real-world evidence (RWE) and health economics outcomes research
• Clinical decision support systems development
• Medical coding systems (ICD-10, CPT, SNOMED)
• Healthcare interoperability standards (HL7, FHIR)"""

        # Prepare multipart form data
        with open(resume_file_path, 'rb') as f:
            files = {
                'resume': ('test_resume.txt', f, 'text/plain')
            }
            data = {
                'job_title': job_title,
                'job_description': job_description
            }
            
            # Make request
            response = requests.post(
                f"{API_BASE}/placement-preparation/rejection-reasons",
                files=files,
                data=data,
                timeout=60
            )
        
        # Clean up temp file
        os.unlink(resume_file_path)
        
        if response.status_code == 200:
            result = response.json()
            rejection_reasons = result.get('rejection_reasons', '')
            
            # Quality checks
            quality_checks = {
                'Length': len(rejection_reasons) >= 1000,  # Should be comprehensive
                'Bullet Points': rejection_reasons.count('•') >= 8,  # Multiple rejection reasons
                'Evidence Structure': 'Required:' in rejection_reasons and 'Candidate Reality:' in rejection_reasons,
                'Gap Impact': 'Gap Impact:' in rejection_reasons,
                'Technical Skills': 'TECHNICAL' in rejection_reasons.upper(),
                'Experience': 'EXPERIENCE' in rejection_reasons.upper(),
                'Education': 'EDUCATION' in rejection_reasons.upper() or 'PhD' in rejection_reasons,
                'Healthcare Domain': 'healthcare' in rejection_reasons.lower() or 'medical' in rejection_reasons.lower()
            }
            
            passed_checks = sum(quality_checks.values())
            total_checks = len(quality_checks)
            
            if passed_checks >= total_checks * 0.8:  # 80% pass rate
                log_test_result("Comprehensive Analysis Quality", "PASS", 
                              f"Quality score: {passed_checks}/{total_checks}, Length: {len(rejection_reasons)} chars")
                return True
            else:
                failed_checks = [check for check, passed in quality_checks.items() if not passed]
                log_test_result("Comprehensive Analysis Quality", "FAIL", 
                              f"Failed checks: {failed_checks}, Score: {passed_checks}/{total_checks}")
                return False
            
        else:
            log_test_result("Comprehensive Analysis Quality - API Call", "FAIL", 
                          f"Status: {response.status_code}")
            return False
            
    except Exception as e:
        log_test_result("Comprehensive Analysis Quality - Exception", "FAIL", f"Error: {str(e)}")
        return False

def main():
    """Run comprehensive rejection reasons analysis testing"""
    print("=" * 80)
    print("🔍 REJECTION REASONS ANALYSIS FUNCTIONALITY TESTING")
    print("=" * 80)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"API Base: {API_BASE}")
    print()
    
    # Test results tracking
    test_results = []
    
    # Test 1: Backend Connectivity
    print("📡 Testing Backend Connectivity...")
    connectivity_result = test_backend_connectivity()
    test_results.append(("Backend Connectivity", connectivity_result))
    
    if not connectivity_result:
        print("❌ Backend connectivity failed. Stopping tests.")
        return
    
    # Test 2: Core Rejection Reasons Analysis
    print("🎯 Testing Core Rejection Reasons Analysis...")
    analysis_result, analysis_data = test_rejection_reasons_analysis()
    test_results.append(("Rejection Reasons Analysis", analysis_result))
    
    rejection_id = None
    if analysis_result and analysis_data:
        rejection_id = analysis_data.get('rejection_id')
    
    # Test 3: PDF Generation and Download
    if rejection_id:
        print("📄 Testing PDF Generation and Download...")
        pdf_result = test_pdf_generation_and_download(rejection_id)
        test_results.append(("PDF Generation and Download", pdf_result))
    else:
        print("⚠️ Skipping PDF test - no rejection ID available")
        test_results.append(("PDF Generation and Download", False))
    
    # Test 4: Database Storage and Retrieval
    print("💾 Testing Database Storage and Retrieval...")
    db_result = test_database_storage()
    test_results.append(("Database Storage", db_result))
    
    # Test 5: Error Handling
    print("⚠️ Testing Error Handling...")
    error_result = test_error_handling()
    test_results.append(("Error Handling", error_result))
    
    # Test 6: Comprehensive Analysis Quality
    print("🔬 Testing Comprehensive Analysis Quality...")
    quality_result = test_comprehensive_analysis_quality()
    test_results.append(("Analysis Quality", quality_result))
    
    # Final Results Summary
    print("=" * 80)
    print("📊 FINAL TEST RESULTS SUMMARY")
    print("=" * 80)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status_symbol = "✅" if result else "❌"
        print(f"{status_symbol} {test_name}: {'PASS' if result else 'FAIL'}")
        if result:
            passed_tests += 1
    
    print()
    success_rate = (passed_tests / total_tests) * 100
    print(f"🎯 Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎉 REJECTION REASONS ANALYSIS FUNCTIONALITY: OPERATIONAL")
    elif success_rate >= 60:
        print("⚠️ REJECTION REASONS ANALYSIS FUNCTIONALITY: PARTIALLY OPERATIONAL")
    else:
        print("❌ REJECTION REASONS ANALYSIS FUNCTIONALITY: NEEDS ATTENTION")
    
    print("=" * 80)
    
    return test_results

if __name__ == "__main__":
    main()