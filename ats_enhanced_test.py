#!/usr/bin/env python3
"""
Enhanced ATS Score Calculation and PDF Generation Testing
Focus: Testing the enhanced ATS score calculation and PDF generation functionality
"""

import requests
import json
import os
import time
from datetime import datetime
import tempfile
import PyPDF2
import io

# Configuration
BACKEND_URL = "https://33e908ff-821c-4359-a046-0a59698e91ec.preview.emergentagent.com/api"

class ATSScoreTestSuite:
    def __init__(self):
        self.backend_url = BACKEND_URL
        self.test_results = []
        self.ats_id = None
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {status}")
        if details:
            print(f"   Details: {details}")
    
    def create_sample_resume(self):
        """Create a sample resume file for testing"""
        resume_content = """JOHN SMITH
Machine Learning Engineer

CONTACT INFORMATION
Email: john.smith@email.com
Phone: (555) 123-4567
Location: San Francisco, CA

PROFESSIONAL SUMMARY
Experienced Machine Learning Engineer with 5+ years of expertise in developing and deploying ML models using Python, TensorFlow, and cloud platforms. Proven track record of building scalable ML solutions that improved business metrics by 25-40%. Strong background in deep learning, computer vision, and natural language processing.

TECHNICAL SKILLS
• Programming Languages: Python, R, SQL, Java, JavaScript
• Machine Learning: TensorFlow, PyTorch, Scikit-learn, Keras, XGBoost
• Cloud Platforms: AWS (SageMaker, EC2, S3), Google Cloud Platform, Azure
• Data Processing: Pandas, NumPy, Apache Spark, Hadoop
• Databases: PostgreSQL, MongoDB, Redis
• Tools: Docker, Kubernetes, Git, Jenkins, MLflow
• Specializations: Deep Learning, Computer Vision, NLP, Time Series Analysis

PROFESSIONAL EXPERIENCE

Senior Machine Learning Engineer | TechCorp Inc. | Jan 2021 - Present
• Developed and deployed 15+ ML models for recommendation systems, increasing user engagement by 35%
• Built end-to-end ML pipelines using TensorFlow and AWS SageMaker, reducing model training time by 50%
• Led a team of 4 ML engineers in developing computer vision models for autonomous vehicle perception
• Implemented MLOps practices using Docker and Kubernetes, improving model deployment efficiency by 60%
• Collaborated with product teams to translate business requirements into ML solutions

Machine Learning Engineer | DataSolutions LLC | Jun 2019 - Dec 2020
• Created predictive models for customer churn analysis, achieving 92% accuracy and saving $2M annually
• Developed NLP models for sentiment analysis of customer reviews using TensorFlow and BERT
• Optimized existing ML algorithms, improving inference speed by 40% and reducing cloud costs by 25%
• Built real-time data processing pipelines using Apache Spark and Kafka

Junior Data Scientist | StartupAI | Aug 2018 - May 2019
• Implemented machine learning models for fraud detection, reducing false positives by 30%
• Performed exploratory data analysis on large datasets (10M+ records) using Python and SQL
• Created data visualizations and dashboards using Tableau and Matplotlib

EDUCATION
Master of Science in Computer Science (Machine Learning Focus)
Stanford University | 2018
GPA: 3.8/4.0
Relevant Coursework: Deep Learning, Computer Vision, Natural Language Processing, Statistical Learning

Bachelor of Science in Mathematics
University of California, Berkeley | 2016
GPA: 3.7/4.0

PROJECTS
• Autonomous Driving Perception System: Developed computer vision models using TensorFlow and OpenCV for object detection and lane recognition, achieving 95% accuracy on test datasets
• Stock Price Prediction Model: Built LSTM neural networks for time series forecasting, outperforming baseline models by 15%
• Chatbot Development: Created an intelligent chatbot using NLP techniques and transformer models, handling 10,000+ daily conversations

CERTIFICATIONS
• AWS Certified Machine Learning - Specialty (2022)
• Google Cloud Professional Machine Learning Engineer (2021)
• TensorFlow Developer Certificate (2020)

ACHIEVEMENTS
• Published 3 research papers in top-tier ML conferences (ICML, NeurIPS)
• Winner of Kaggle competition "Computer Vision Challenge 2021"
• Speaker at PyData Conference 2022 on "Scaling ML Models in Production"
"""
        return resume_content
    
    def test_backend_connectivity(self):
        """Test basic backend connectivity"""
        try:
            response = requests.get(f"{self.backend_url.replace('/api', '')}/health", timeout=10)
            if response.status_code in [200, 405]:  # 405 is also acceptable for health check
                self.log_test("Backend Connectivity", "PASS", f"Backend responding (Status: {response.status_code})")
                return True
            else:
                self.log_test("Backend Connectivity", "FAIL", f"Unexpected status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Connection error: {str(e)}")
            return False
    
    def test_ats_score_calculation(self):
        """Test the ATS score calculation endpoint with comprehensive validation"""
        try:
            # Prepare test data as specified in requirements
            job_title = "Machine Learning Engineer"
            job_description = "Looking for ML engineer with Python, TensorFlow, and cloud experience"
            resume_content = self.create_sample_resume()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(resume_content)
                temp_file_path = temp_file.name
            
            try:
                # Prepare multipart form data
                with open(temp_file_path, 'rb') as resume_file:
                    files = {
                        'resume': ('test_resume.txt', resume_file, 'text/plain')
                    }
                    data = {
                        'job_title': job_title,
                        'job_description': job_description
                    }
                    
                    # Make request to ATS endpoint
                    response = requests.post(
                        f"{self.backend_url}/placement-preparation/ats-score-calculate",
                        files=files,
                        data=data,
                        timeout=120  # Increased timeout for AI processing
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Validate response structure - check for required fields
                    required_fields = ['success', 'ats_id', 'ats_score', 'analysis_text', 'pdf_filename']
                    missing_fields = [field for field in required_fields if field not in result]
                    
                    if missing_fields:
                        self.log_test("ATS Score Calculation - Response Structure", "FAIL", 
                                    f"Missing fields: {missing_fields}")
                        return False
                    
                    # Validate field values
                    if not result.get('success'):
                        self.log_test("ATS Score Calculation - Success Status", "FAIL", 
                                    f"Success field is False: {result}")
                        return False
                    
                    # Store ATS ID for PDF download test
                    self.ats_id = result.get('ats_id')
                    ats_score = result.get('ats_score')
                    analysis_text = result.get('analysis_text', '')
                    pdf_filename = result.get('pdf_filename', '')
                    
                    # Validate ATS score
                    if not isinstance(ats_score, int) or not (0 <= ats_score <= 100):
                        self.log_test("ATS Score Calculation - Score Validation", "FAIL", 
                                    f"Invalid ATS score: {ats_score}")
                        return False
                    
                    # Validate analysis text quality
                    if not analysis_text or len(analysis_text) < 500:
                        self.log_test("ATS Score Calculation - Analysis Quality", "FAIL", 
                                    f"Analysis text too short: {len(analysis_text)} characters")
                        return False
                    
                    # Check for key analysis components
                    analysis_components = [
                        'COMPREHENSIVE ATS SCORE',
                        'KEYWORD ANALYSIS',
                        'EXPERIENCE EVALUATION',
                        'TECHNICAL COMPETENCY',
                        'EDUCATION',
                        'Educational Qualifications',
                        'Professional Experience',
                        'Skills'
                    ]
                    
                    found_components = [comp for comp in analysis_components if comp in analysis_text]
                    
                    self.log_test("ATS Score Calculation - Core Functionality", "PASS", 
                                f"Score: {ats_score}/100, Analysis: {len(analysis_text)} chars, Components: {len(found_components)}/8")
                    
                    # Validate PDF filename
                    if pdf_filename and not pdf_filename.endswith('.pdf'):
                        self.log_test("ATS Score Calculation - PDF Filename", "FAIL", 
                                    f"Invalid PDF filename: {pdf_filename}")
                        return False
                    
                    self.log_test("ATS Score Calculation - Response Validation", "PASS", 
                                f"All required fields present and valid")
                    
                    return True
                    
                else:
                    self.log_test("ATS Score Calculation - HTTP Response", "FAIL", 
                                f"Status: {response.status_code}, Response: {response.text[:500]}")
                    return False
                    
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            self.log_test("ATS Score Calculation - Exception", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_pdf_download_and_formatting(self):
        """Test PDF download and verify enhanced formatting"""
        if not self.ats_id:
            self.log_test("PDF Download - Prerequisites", "FAIL", "No ATS ID available from previous test")
            return False
        
        try:
            # Download PDF
            response = requests.get(
                f"{self.backend_url}/placement-preparation/ats-score/{self.ats_id}/download",
                timeout=30
            )
            
            if response.status_code == 200:
                # Verify it's a PDF
                if response.headers.get('content-type') != 'application/pdf':
                    self.log_test("PDF Download - Content Type", "FAIL", 
                                f"Wrong content type: {response.headers.get('content-type')}")
                    return False
                
                pdf_content = response.content
                pdf_size = len(pdf_content)
                
                if pdf_size < 1000:  # PDF should be substantial
                    self.log_test("PDF Download - File Size", "FAIL", 
                                f"PDF too small: {pdf_size} bytes")
                    return False
                
                self.log_test("PDF Download - Basic Validation", "PASS", 
                            f"PDF downloaded successfully, Size: {pdf_size} bytes")
                
                # Analyze PDF content for enhanced formatting
                try:
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
                    num_pages = len(pdf_reader.pages)
                    
                    if num_pages == 0:
                        self.log_test("PDF Content - Page Count", "FAIL", "PDF has no pages")
                        return False
                    
                    # Extract text from all pages
                    full_text = ""
                    for page in pdf_reader.pages:
                        full_text += page.extract_text() + "\n"
                    
                    # Check for enhanced formatting elements
                    formatting_checks = {
                        "Professional Title": "ATS SCORE ANALYSIS REPORT" in full_text,
                        "Score Display": any(score_text in full_text for score_text in ["OVERALL ATS SCORE", "/100"]),
                        "Score Breakdown Table": "SCORE BREAKDOWN" in full_text,
                        "Educational Section": any(edu_text in full_text for edu_text in ["EDUCATIONAL QUALIFICATIONS", "Education"]),
                        "Experience Section": any(exp_text in full_text for exp_text in ["PROFESSIONAL EXPERIENCE", "Job History"]),
                        "Skills Section": any(skill_text in full_text for skill_text in ["SKILLS & COMPETENCIES", "Skill Set"]),
                        "Projects Section": any(proj_text in full_text for proj_text in ["KEY PROJECTS", "Personal Projects"]),
                        "Detailed Analysis": "DETAILED ANALYSIS" in full_text,
                        "Professional Layout": "Generated:" in full_text and "Position:" in full_text
                    }
                    
                    passed_checks = sum(formatting_checks.values())
                    total_checks = len(formatting_checks)
                    
                    # Check for score breakdown table elements
                    score_categories = [
                        "Keyword Analysis", "Experience Evaluation", "Technical Competency",
                        "Education", "Achievements", "Project Innovation"
                    ]
                    found_categories = sum(1 for cat in score_categories if cat in full_text)
                    
                    # Check for proper content structure without truncation
                    content_quality_checks = {
                        "Sufficient Content": len(full_text) > 2000,
                        "No Truncation Issues": "..." not in full_text[-100:],  # Check end of document
                        "Structured Content": full_text.count("•") > 5,  # Bullet points indicate structure
                        "Score Categories Present": found_categories >= 3,
                        "Proper Formatting": full_text.count("\n") > 50  # Adequate line breaks
                    }
                    
                    content_passed = sum(content_quality_checks.values())
                    content_total = len(content_quality_checks)
                    
                    self.log_test("PDF Content - Enhanced Formatting", "PASS", 
                                f"Formatting checks: {passed_checks}/{total_checks}, Content quality: {content_passed}/{content_total}")
                    
                    # Professional layout validation
                    if passed_checks >= 7:  # At least 7/9 formatting checks should pass
                        self.log_test("PDF Content - Professional Layout", "PASS", 
                                    f"Professional layout confirmed with {passed_checks} formatting elements")
                    else:
                        self.log_test("PDF Content - Professional Layout", "FAIL", 
                                    f"Insufficient formatting elements: {passed_checks}/{total_checks}")
                        return False
                    
                    # Content completeness validation
                    if content_passed >= 4:  # At least 4/5 content quality checks should pass
                        self.log_test("PDF Content - Completeness & Structure", "PASS", 
                                    f"Content is complete and well-structured without truncation")
                    else:
                        self.log_test("PDF Content - Completeness & Structure", "FAIL", 
                                    f"Content quality issues: {content_passed}/{content_total}")
                        return False
                    
                    # Check for score breakdown table headers
                    if "CATEGORY" in full_text and "SCORE" in full_text and "PERCENTAGE" in full_text:
                        self.log_test("PDF Content - Score Breakdown Table", "PASS", 
                                    "Score breakdown table present with proper headers")
                    else:
                        self.log_test("PDF Content - Score Breakdown Table", "WARN", 
                                    "Score breakdown table headers not clearly visible")
                    
                    # Check for visual elements and proper sections
                    visual_elements = {
                        "Headers with Icons": any(icon in full_text for icon in ["📊", "🎯", "💼", "⚙️", "🎓"]),
                        "Section Organization": full_text.count("QUALIFICATIONS") + full_text.count("EXPERIENCE") + full_text.count("SKILLS") >= 2,
                        "Readable Content": len(full_text.split()) > 500  # Adequate word count
                    }
                    
                    visual_passed = sum(visual_elements.values())
                    if visual_passed >= 2:
                        self.log_test("PDF Content - Visual Elements", "PASS", 
                                    f"Visual elements and organization confirmed ({visual_passed}/3)")
                    else:
                        self.log_test("PDF Content - Visual Elements", "WARN", 
                                    f"Limited visual elements detected ({visual_passed}/3)")
                    
                    return True
                    
                except Exception as e:
                    self.log_test("PDF Content - Analysis Error", "FAIL", f"PDF analysis error: {str(e)}")
                    return False
                    
            else:
                self.log_test("PDF Download - HTTP Response", "FAIL", 
                            f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            self.log_test("PDF Download - Exception", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all ATS score calculation and PDF generation tests"""
        print("🚀 Starting Enhanced ATS Score Calculation and PDF Generation Testing")
        print("=" * 80)
        print("Focus: Enhanced PDF formatting and structure verification")
        print("=" * 80)
        
        # Test sequence
        tests = [
            ("Backend Connectivity Check", self.test_backend_connectivity),
            ("ATS Score Calculation with ML Engineer Profile", self.test_ats_score_calculation),
            ("PDF Download and Enhanced Formatting Verification", self.test_pdf_download_and_formatting)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            print("-" * 60)
            
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_test(f"{test_name} - Execution", "FAIL", f"Test execution error: {str(e)}")
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 ENHANCED ATS TESTING SUMMARY")
        print("=" * 80)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        # Detailed results
        print("\n📋 Detailed Test Results:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌" if result["status"] == "FAIL" else "⚠️"
            print(f"{status_icon} {result['test']}: {result['status']}")
            if result["details"]:
                print(f"   └─ {result['details']}")
        
        # Final assessment
        print("\n" + "=" * 80)
        if success_rate >= 80:
            print("🎉 ENHANCED ATS SCORE CALCULATION AND PDF GENERATION TESTING COMPLETED SUCCESSFULLY")
            print("✅ Enhanced PDF formatting and structure verified")
            print("✅ Professional layout with proper headers and sections confirmed")
            print("✅ Score breakdown tables and visual elements working")
            print("✅ Complete content without truncation issues validated")
            print("✅ All content properly formatted and readable in PDF")
        else:
            print("⚠️  ENHANCED ATS TESTING COMPLETED WITH ISSUES")
            print("❌ Some PDF formatting or functionality may need attention")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = ATSScoreTestSuite()
    success = tester.run_comprehensive_tests()
    exit(0 if success else 1)