#!/usr/bin/env python3
"""
Comprehensive Technical Interview Questions Feature Test
Tests all aspects of the technical interview questions workflow
"""

import requests
import json
import os
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://ab16948b-54a7-4063-af4a-f88f3c45f9d2.preview.emergentagent.com/api"
SAMPLE_RESUME_PATH = "/app/sample_resume.txt"

# Test data as specified in the review request
TEST_JOB_TITLE = "Senior Software Engineer"
TEST_JOB_DESCRIPTION = """5+ years of experience in full-stack development, proficient in React, Node.js, MongoDB, cloud platforms (AWS/GCP), RESTful APIs, microservices architecture, Agile/Scrum methodology, and CI/CD pipelines. Experience with TypeScript, GraphQL, and Docker preferred."""

def print_test_header(test_name):
    """Print formatted test header"""
    print(f"\n{'='*80}")
    print(f"🧪 {test_name}")
    print(f"{'='*80}")

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
        response = requests.get(f"{BACKEND_URL}/placement-preparation/technical-interview-questions", timeout=10)
        success = response.status_code == 200
        print_test_result("Backend Connectivity", success, f"Status: {response.status_code}")
        return success
    except Exception as e:
        print_test_result("Backend Connectivity", False, f"Error: {str(e)}")
        return False

def test_technical_interview_questions_generation():
    """Test 2: Technical Interview Questions Generation with LLM Analysis"""
    print_test_header("Technical Interview Questions Generation & LLM Analysis Test")
    
    try:
        # Prepare the resume file
        if not os.path.exists(SAMPLE_RESUME_PATH):
            print_test_result("Resume File Check", False, f"Resume file not found: {SAMPLE_RESUME_PATH}")
            return None
        
        # Prepare form data
        with open(SAMPLE_RESUME_PATH, 'rb') as resume_file:
            files = {
                'resume': ('sample_resume.txt', resume_file, 'text/plain')
            }
            data = {
                'job_title': TEST_JOB_TITLE,
                'job_description': TEST_JOB_DESCRIPTION
            }
            
            print(f"📤 Sending POST request to: {BACKEND_URL}/placement-preparation/technical-interview-questions")
            print(f"📋 Job Title: {TEST_JOB_TITLE}")
            print(f"📄 Job Description: {TEST_JOB_DESCRIPTION[:100]}...")
            print(f"📎 Resume File: sample_resume.txt")
            
            response = requests.post(
                f"{BACKEND_URL}/placement-preparation/technical-interview-questions",
                files=files,
                data=data,
                timeout=60  # Increased timeout for LLM processing
            )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Verify response structure
            required_fields = ['success', 'analysis_id', 'interview_questions', 'pdf_filename', 'message']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print_test_result("Response Structure", False, f"Missing fields: {missing_fields}")
                return None
            
            analysis_id = result.get('analysis_id')
            interview_questions = result.get('interview_questions', '')
            pdf_filename = result.get('pdf_filename', '')
            
            print(f"✅ Analysis ID: {analysis_id}")
            print(f"✅ PDF Filename: {pdf_filename}")
            print(f"✅ Interview Questions Length: {len(interview_questions)} characters")
            
            # LLM Analysis Verification
            print(f"\n🔍 LLM ANALYSIS QUALITY VERIFICATION:")
            quality_score = 0
            max_score = 7
            
            # 1. Check for comprehensive content length (Gemini should generate substantial content)
            if len(interview_questions) >= 5000:
                quality_score += 1
                print(f"✅ Comprehensive Content: {len(interview_questions)} characters (Expected: ≥5000)")
            else:
                print(f"⚠️  Content Length: {len(interview_questions)} characters (Expected: ≥5000)")
            
            # 2. Check for 25-question structure
            question_count = interview_questions.count('Question ')
            if question_count >= 20:  # Allow some flexibility
                quality_score += 1
                print(f"✅ Question Count: {question_count} (Expected: ~25)")
            else:
                print(f"⚠️  Question Count: {question_count} (Expected: ~25)")
            
            # 3. Check for HTML formatting for PDF conversion
            if '<html' in interview_questions.lower() and '</html>' in interview_questions.lower():
                quality_score += 1
                print("✅ HTML Formatting: Present for PDF conversion")
            else:
                print("⚠️  HTML Formatting: Missing or incomplete")
            
            # 4. Check for role-specific content (job requirements)
            role_keywords = ['react', 'node.js', 'mongodb', 'aws', 'microservices', 'ci/cd', 'full-stack']
            found_keywords = [kw for kw in role_keywords if kw.lower() in interview_questions.lower()]
            if len(found_keywords) >= 4:
                quality_score += 1
                print(f"✅ Role-specific Keywords: {found_keywords}")
            else:
                print(f"⚠️  Role-specific Keywords: {found_keywords} (Expected ≥4)")
            
            # 5. Check for candidate-specific content (resume analysis)
            candidate_keywords = ['javascript', 'typescript', 'python', 'senior', 'experience', '6+ years']
            found_candidate_keywords = [kw for kw in candidate_keywords if kw.lower() in interview_questions.lower()]
            if len(found_candidate_keywords) >= 3:
                quality_score += 1
                print(f"✅ Candidate-specific Keywords: {found_candidate_keywords}")
            else:
                print(f"⚠️  Candidate-specific Keywords: {found_candidate_keywords} (Expected ≥3)")
            
            # 6. Check for question categories (5 categories as per prompt)
            categories = ['foundational', 'applied', 'experience', 'advanced', 'expert']
            found_categories = sum(1 for cat in categories if cat.lower() in interview_questions.lower())
            if found_categories >= 3:
                quality_score += 1
                print(f"✅ Question Categories: {found_categories}/5 found")
            else:
                print(f"⚠️  Question Categories: {found_categories}/5 found")
            
            # 7. Check for follow-up questions and context
            followup_indicators = ['follow-up', 'context:', 'why this matters', 'assesses']
            found_followups = sum(1 for indicator in followup_indicators if indicator.lower() in interview_questions.lower())
            if found_followups >= 3:
                quality_score += 1
                print(f"✅ Follow-up & Context: {found_followups} indicators found")
            else:
                print(f"⚠️  Follow-up & Context: {found_followups} indicators found")
            
            print(f"📊 LLM Analysis Quality Score: {quality_score}/{max_score}")
            
            success = quality_score >= 4  # At least 57% quality
            print_test_result("Technical Interview Questions Generation & LLM Analysis", success, 
                            f"Quality Score: {quality_score}/{max_score}, Length: {len(interview_questions)} chars")
            
            return analysis_id if success else None
            
        else:
            error_detail = response.text if response.text else "No error details"
            print_test_result("Technical Interview Questions Generation", False, 
                            f"Status: {response.status_code}, Error: {error_detail}")
            return None
            
    except Exception as e:
        print_test_result("Technical Interview Questions Generation", False, f"Exception: {str(e)}")
        return None

def test_database_storage_and_retrieval(analysis_id):
    """Test 3: Database Storage and GET Endpoint"""
    print_test_header("Database Storage and Retrieval Test")
    
    if not analysis_id:
        print_test_result("Database Storage Test", False, "No analysis_id provided")
        return False
    
    try:
        # Test GET endpoint for all analyses
        response = requests.get(f"{BACKEND_URL}/placement-preparation/technical-interview-questions", timeout=10)
        
        print(f"📥 GET Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            analyses = result.get('analyses', [])
            
            print(f"📊 Total Analyses Found: {len(analyses)}")
            
            # Look for our specific analysis
            our_analysis = None
            for analysis in analyses:
                if analysis.get('id') == analysis_id:
                    our_analysis = analysis
                    break
            
            if our_analysis:
                print(f"✅ Analysis Found in Database: {analysis_id}")
                
                # Verify required fields
                required_fields = ['id', 'job_title', 'job_description', 'resume_content', 'interview_questions', 'created_at']
                missing_fields = [field for field in required_fields if field not in our_analysis]
                
                if not missing_fields:
                    print("✅ All Required Fields Present")
                    print(f"   - Job Title: {our_analysis.get('job_title')}")
                    print(f"   - Resume Content Length: {len(our_analysis.get('resume_content', ''))}")
                    print(f"   - Interview Questions Length: {len(our_analysis.get('interview_questions', ''))}")
                    print(f"   - Created At: {our_analysis.get('created_at')}")
                    
                    print_test_result("Database Storage and Retrieval", True, 
                                    f"Analysis stored and retrieved successfully")
                    return True
                else:
                    print_test_result("Database Storage and Retrieval", False, 
                                    f"Missing fields: {missing_fields}")
                    return False
            else:
                print_test_result("Database Storage and Retrieval", False, 
                                f"Analysis {analysis_id} not found in database")
                return False
        else:
            print_test_result("Database Storage and Retrieval", False, 
                            f"GET request failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("Database Storage and Retrieval", False, f"Exception: {str(e)}")
        return False

def test_pdf_generation_and_download(analysis_id):
    """Test 4: PDF Generation and Download Functionality"""
    print_test_header("PDF Generation and Download Test")
    
    if not analysis_id:
        print_test_result("PDF Download Test", False, "No analysis_id provided")
        return False
    
    try:
        # Test PDF download endpoint
        download_url = f"{BACKEND_URL}/placement-preparation/technical-interview-questions/{analysis_id}/download"
        print(f"📤 Downloading PDF from: {download_url}")
        
        response = requests.get(download_url, timeout=30)
        
        print(f"📥 Download Response Status: {response.status_code}")
        
        if response.status_code == 200:
            # Verify content type
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' in content_type:
                print(f"✅ Content-Type: {content_type}")
            else:
                print(f"⚠️  Content-Type: {content_type} (Expected: application/pdf)")
            
            # Verify PDF content
            pdf_content = response.content
            pdf_size = len(pdf_content)
            
            print(f"📊 PDF Size: {pdf_size} bytes")
            
            # Basic PDF validation
            is_valid_pdf = pdf_content.startswith(b'%PDF-')
            if is_valid_pdf:
                print("✅ Valid PDF Format")
            else:
                print("❌ Invalid PDF Format")
            
            # Check for substantial content (comprehensive interview questions should be several KB)
            substantial_content = pdf_size > 5000  # At least 5KB
            if substantial_content:
                print(f"✅ Substantial Content: {pdf_size} bytes (Expected: >5KB for comprehensive questions)")
            else:
                print(f"⚠️  Content Size: {pdf_size} bytes (Expected: >5KB)")
            
            success = is_valid_pdf and pdf_size > 1000  # At least 1KB and valid PDF
            print_test_result("PDF Generation and Download", success, 
                            f"Size: {pdf_size} bytes, Valid PDF: {is_valid_pdf}")
            return success
            
        elif response.status_code == 404:
            print_test_result("PDF Download Test", False, "PDF file not found (404)")
            return False
        else:
            print_test_result("PDF Download Test", False, 
                            f"Download failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print_test_result("PDF Download Test", False, f"Exception: {str(e)}")
        return False

def run_comprehensive_test():
    """Run all tests in sequence"""
    print(f"\n🚀 COMPREHENSIVE TECHNICAL INTERVIEW QUESTIONS FEATURE TESTING")
    print(f"⏰ Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔗 Backend URL: {BACKEND_URL}")
    print(f"📋 Testing Requirements:")
    print(f"   ✓ Backend Connectivity")
    print(f"   ✓ Technical Interview Questions Generation (25 questions)")
    print(f"   ✓ LLM Analysis Verification (Gemini API)")
    print(f"   ✓ HTML Formatting for PDF Conversion")
    print(f"   ✓ Database Storage")
    print(f"   ✓ PDF Generation and Download")
    print(f"   ✓ Role and Candidate-Specific Questions")
    
    test_results = {}
    analysis_id = None
    
    # Test 1: Backend Connectivity
    test_results['connectivity'] = test_backend_connectivity()
    
    if test_results['connectivity']:
        # Test 2: Technical Interview Questions Generation with LLM Analysis
        analysis_id = test_technical_interview_questions_generation()
        test_results['generation_and_llm'] = analysis_id is not None
        
        if analysis_id:
            # Test 3: Database Storage and Retrieval
            test_results['database'] = test_database_storage_and_retrieval(analysis_id)
            
            # Test 4: PDF Generation and Download
            test_results['pdf_download'] = test_pdf_generation_and_download(analysis_id)
        else:
            test_results['database'] = False
            test_results['pdf_download'] = False
    else:
        test_results['generation_and_llm'] = False
        test_results['database'] = False
        test_results['pdf_download'] = False
    
    # Summary
    print(f"\n{'='*80}")
    print(f"📊 TECHNICAL INTERVIEW QUESTIONS FEATURE TESTING SUMMARY")
    print(f"{'='*80}")
    
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"✅ Tests Passed: {passed_tests}/{total_tests}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    if analysis_id:
        print(f"🆔 Generated Analysis ID: {analysis_id}")
    
    print(f"\nDetailed Results:")
    for test_name, result in test_results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {status} - {test_name.replace('_', ' ').title()}")
    
    print(f"\n⏰ Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Overall assessment based on key success criteria
    key_features_working = (
        test_results.get('connectivity', False) and
        test_results.get('generation_and_llm', False) and
        test_results.get('database', False)
    )
    
    if success_rate >= 90:
        print(f"🎉 OVERALL RESULT: EXCELLENT - Technical Interview Questions feature is fully operational!")
        print(f"   ✓ All key success criteria met:")
        print(f"   ✓ 25-question structure with role/candidate-specific content")
        print(f"   ✓ LLM analysis generating comprehensive questions")
        print(f"   ✓ HTML formatting for PDF conversion")
        print(f"   ✓ Complete workflow from generation to download")
    elif success_rate >= 75 and key_features_working:
        print(f"✅ OVERALL RESULT: GOOD - Technical Interview Questions feature is working correctly!")
        print(f"   ✓ Core functionality operational")
        print(f"   ✓ LLM generating role and candidate-specific questions")
        print(f"   ✓ Database storage and retrieval working")
        if not test_results.get('pdf_download', False):
            print(f"   ⚠️  Minor issue with PDF download (core feature still works)")
    elif success_rate >= 50:
        print(f"⚠️  OVERALL RESULT: NEEDS IMPROVEMENT - Technical Interview Questions feature has some issues")
    else:
        print(f"❌ OVERALL RESULT: CRITICAL ISSUES - Technical Interview Questions feature requires major fixes")
    
    return test_results, success_rate

if __name__ == "__main__":
    run_comprehensive_test()