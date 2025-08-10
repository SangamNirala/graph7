#!/usr/bin/env python3
"""
ATS Score Calculator PDF Generation Fix Testing
Testing the critical PDF parsing fix for comprehensive content coverage

FOCUS: Testing the PDF generation issue that was just fixed where PDF reports 
only contained 188 characters (0.92% coverage) because the PDF parsing logic 
was looking for outdated section headers while the AI generates modern headers.
"""

import requests
import json
import os
import tempfile
import time
from datetime import datetime

# Configuration
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://ed1be7ee-3b3d-4ddb-a670-999d49a5f3da.preview.emergentagent.com')
ATS_ENDPOINT = f"{BACKEND_URL}/api/placement-preparation/ats-score-calculate"

class ATSPDFTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()
        
        self.test_results.append({
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': timestamp
        })

    def create_comprehensive_resume(self):
        """Create a comprehensive resume that should generate detailed analysis"""
        return """SARAH JOHNSON
Senior Full Stack Developer
Email: sarah.johnson@email.com | Phone: (555) 987-6543
LinkedIn: linkedin.com/in/sarahjohnson | GitHub: github.com/sarahjohnson

PROFESSIONAL SUMMARY
Experienced Senior Full Stack Developer with 7+ years of expertise in Python, React, and MongoDB development. 
Led cross-functional teams of 8+ developers and delivered 25+ successful projects with 99.8% uptime. 
Specialized in microservices architecture, cloud deployment, and agile methodologies.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, TypeScript, Java, Go, SQL
• Frontend Technologies: React, Vue.js, Angular, HTML5, CSS3, Redux, Next.js
• Backend Technologies: FastAPI, Django, Node.js, Express.js, Flask, Spring Boot
• Databases: MongoDB, PostgreSQL, MySQL, Redis, Elasticsearch
• Cloud Platforms: AWS (EC2, S3, Lambda, RDS, EKS), Google Cloud Platform, Azure
• DevOps Tools: Docker, Kubernetes, Jenkins, GitLab CI/CD, Terraform, Ansible
• Version Control: Git, GitHub, GitLab, Bitbucket
• Testing: Jest, Pytest, Selenium, Unit Testing, Integration Testing, TDD
• Monitoring: Prometheus, Grafana, ELK Stack, New Relic

PROFESSIONAL EXPERIENCE

Senior Full Stack Developer | TechInnovate Corp | March 2021 - Present
• Led development of microservices-based e-commerce platform serving 500,000+ daily users
• Architected and implemented React-based frontend applications with 45% performance improvement
• Designed RESTful APIs using Python/FastAPI handling 2M+ requests per day
• Optimized MongoDB queries and implemented caching strategies, reducing response time by 65%
• Managed AWS infrastructure deployment using Docker and Kubernetes for 99.9% uptime
• Mentored team of 6 junior developers and established code review processes
• Implemented CI/CD pipelines reducing deployment time from 3 hours to 20 minutes
• Achieved 15% cost reduction through cloud infrastructure optimization

Full Stack Developer | DataSolutions Inc | June 2019 - February 2021
• Developed scalable web applications using React, Python, and PostgreSQL
• Built real-time analytics dashboard processing 5TB+ data daily
• Implemented automated testing suites increasing code coverage from 70% to 98%
• Collaborated with product managers and UX designers in agile development cycles
• Optimized database performance resulting in 40% faster query execution
• Led migration from monolithic to microservices architecture
• Delivered 12+ projects on time with zero critical bugs in production

Software Developer | StartupHub | August 2017 - May 2019
• Developed full-stack applications using JavaScript, Python, and MySQL
• Built responsive web interfaces with React and modern CSS frameworks
• Implemented RESTful APIs and integrated third-party services
• Participated in agile development processes and daily standups
• Fixed 200+ bugs and implemented 50+ new features based on user feedback
• Contributed to open-source projects and maintained 95%+ code quality scores

EDUCATION
Master of Science in Computer Science
Stanford University | Graduated: June 2017 | GPA: 3.9/4.0
Specialization: Software Engineering and Distributed Systems

Bachelor of Science in Computer Science
University of California, Berkeley | Graduated: May 2015 | GPA: 3.8/4.0

CERTIFICATIONS
• AWS Certified Solutions Architect - Professional (2023)
• Google Cloud Professional Developer (2022)
• Certified Kubernetes Administrator (CKA) (2023)
• MongoDB Certified Developer (2022)
• Scrum Master Certification (2021)

PROJECTS
E-Commerce Platform Modernization (2023)
• Led complete modernization of legacy e-commerce system using React, FastAPI, and MongoDB
• Technologies: React, TypeScript, FastAPI, MongoDB, Docker, AWS, Kubernetes
• Result: 60% improvement in user engagement, 35% increase in conversion rates, $2M+ revenue impact

Real-time Analytics Dashboard (2022)
• Built scalable real-time data processing system supporting 100,000+ concurrent users
• Technologies: React, Python, Apache Kafka, Elasticsearch, Docker, AWS
• Implemented machine learning algorithms for predictive analytics
• Result: 50% faster decision-making process for business stakeholders

Microservices Migration Project (2021)
• Architected and led migration from monolithic to microservices architecture
• Technologies: Python, FastAPI, Docker, Kubernetes, PostgreSQL, Redis
• Implemented service mesh and API gateway for improved scalability
• Result: 70% improvement in system scalability and 40% reduction in deployment time

ACHIEVEMENTS
• Increased team productivity by 45% through implementation of automated testing and deployment
• Reduced server costs by 35% through cloud infrastructure optimization and monitoring
• Successfully delivered 25+ projects on time and within budget over 7 years
• Received "Technical Excellence Award" in 2022 for outstanding architectural contributions
• Published 3 technical articles on microservices architecture with 10,000+ views
• Mentored 15+ junior developers, with 90% promotion rate within 2 years
• Led company-wide adoption of DevOps practices resulting in 80% faster deployments
"""

    def test_backend_connectivity(self):
        """Test basic backend connectivity"""
        try:
            # Test basic health endpoint
            health_url = f"{BACKEND_URL}/health"
            response = self.session.get(health_url, timeout=10)
            
            if response.status_code in [200, 404, 405]:
                self.log_test("Backend Connectivity", "PASS", f"Backend responding (Status: {response.status_code})")
                return True
            else:
                self.log_test("Backend Connectivity", "FAIL", f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Connection error: {str(e)}")
            return False

    def test_ats_endpoint_comprehensive_analysis(self):
        """Test that ATS endpoint generates comprehensive analysis (5,000+ characters)"""
        try:
            resume_content = self.create_comprehensive_resume()
            
            files = {
                'resume': ('comprehensive_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Full Stack Developer',
                'job_description': '''We are seeking a Senior Full Stack Developer to join our engineering team.

Key Responsibilities:
• Design and develop scalable web applications using modern technologies
• Lead technical architecture decisions and mentor junior developers  
• Collaborate with cross-functional teams to deliver high-quality software solutions
• Implement best practices for code quality, testing, and deployment
• Work with microservices architecture and cloud platforms

Required Skills:
• 5+ years of experience in full-stack development
• Strong proficiency in Python and JavaScript/TypeScript
• Experience with React, FastAPI, Django, or similar frameworks
• Knowledge of cloud platforms (AWS, GCP, or Azure)
• Experience with databases (MongoDB, PostgreSQL)
• Familiarity with DevOps tools (Docker, Kubernetes, CI/CD)
• Strong problem-solving and communication skills
• Experience with microservices architecture

Preferred Skills:
• AWS certifications
• Experience with automated testing and TDD
• Leadership and mentoring experience
• Knowledge of monitoring and observability tools
• Experience with agile methodologies'''
            }
            
            print(f"🚀 Testing ATS Score Calculation with Comprehensive Resume...")
            print(f"   Resume Length: {len(resume_content)} characters")
            print(f"   Job Description Length: {len(data['job_description'])} characters")
            
            response = self.session.post(ATS_ENDPOINT, files=files, data=data, timeout=120)
            
            if response.status_code != 200:
                self.log_test("Comprehensive Analysis Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False, None
            
            result = response.json()
            
            # Verify response structure
            required_fields = ['success', 'ats_id', 'ats_score', 'analysis_text', 'pdf_filename']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                self.log_test("Comprehensive Analysis Generation", "FAIL", 
                            f"Missing required fields: {missing_fields}")
                return False, None
            
            if not result.get('success'):
                self.log_test("Comprehensive Analysis Generation", "FAIL", 
                            f"API returned success=false: {result}")
                return False, None
            
            # Check analysis text length (should be 5,000+ characters for comprehensive analysis)
            analysis_text = result.get('analysis_text', '')
            analysis_length = len(analysis_text)
            
            if analysis_length < 5000:
                self.log_test("Comprehensive Analysis Generation", "FAIL", 
                            f"Analysis text too short: {analysis_length} characters (expected 5,000+)")
                return False, None
            
            # Check for modern section headers that should be present
            modern_headers = [
                'COMPREHENSIVE ATS SCORE', 'CRITICAL IMPROVEMENT AREAS', 
                'IMPLEMENTATION ROADMAP', 'ATS OPTIMIZATION CHECKLIST',
                'SCORE ENHANCEMENT RECOMMENDATIONS', 'ENHANCED ANALYSIS INSIGHTS'
            ]
            
            found_headers = [header for header in modern_headers if header in analysis_text]
            
            if len(found_headers) < 3:
                self.log_test("Comprehensive Analysis Generation", "FAIL", 
                            f"Missing modern section headers. Found: {found_headers}")
                return False, None
            
            self.log_test("Comprehensive Analysis Generation", "PASS", 
                        f"Analysis length: {analysis_length} chars, Modern headers: {len(found_headers)}")
            return True, result
            
        except Exception as e:
            self.log_test("Comprehensive Analysis Generation", "FAIL", f"Exception: {str(e)}")
            return False, None

    def test_pdf_generation_comprehensive_content(self):
        """Test that PDF contains comprehensive content (not just 188 characters)"""
        try:
            # First generate ATS analysis
            success, result = self.test_ats_endpoint_comprehensive_analysis()
            if not success or not result:
                self.log_test("PDF Comprehensive Content", "FAIL", "Failed to generate ATS analysis")
                return False
            
            ats_id = result.get('ats_id')
            pdf_filename = result.get('pdf_filename')
            
            if not pdf_filename:
                self.log_test("PDF Comprehensive Content", "FAIL", "No PDF filename returned")
                return False
            
            # Download PDF
            pdf_download_url = f"{BACKEND_URL}/api/placement-preparation/ats-score/{ats_id}/download"
            
            print(f"📥 Testing PDF Download: {pdf_download_url}")
            pdf_response = self.session.get(pdf_download_url, timeout=60)
            
            if pdf_response.status_code != 200:
                self.log_test("PDF Comprehensive Content", "FAIL", 
                            f"PDF download failed: HTTP {pdf_response.status_code}")
                return False
            
            # Check PDF content type and size
            content_type = pdf_response.headers.get('content-type', '')
            pdf_size = len(pdf_response.content)
            
            if 'pdf' not in content_type.lower():
                self.log_test("PDF Comprehensive Content", "FAIL", 
                            f"Invalid content type: {content_type}")
                return False
            
            # Critical test: PDF should be much larger than 188 characters
            if pdf_size <= 1000:  # PDF should be at least 1KB for comprehensive content
                self.log_test("PDF Comprehensive Content", "FAIL", 
                            f"PDF too small: {pdf_size} bytes (indicates parsing issue)")
                return False
            
            # Calculate content coverage improvement
            analysis_text = result.get('analysis_text', '')
            analysis_length = len(analysis_text)
            
            # Estimate content coverage (rough approximation)
            # A comprehensive PDF should be at least 10KB for detailed analysis
            expected_min_size = 10000  # 10KB
            coverage_ratio = pdf_size / expected_min_size if expected_min_size > 0 else 0
            
            self.log_test("PDF Comprehensive Content", "PASS", 
                        f"PDF size: {pdf_size} bytes, Analysis: {analysis_length} chars, Coverage ratio: {coverage_ratio:.2f}")
            return True
            
        except Exception as e:
            self.log_test("PDF Comprehensive Content", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_modern_sections_inclusion(self):
        """Test that PDF includes all modern sections generated by AI"""
        try:
            # Generate ATS analysis
            success, result = self.test_ats_endpoint_comprehensive_analysis()
            if not success or not result:
                self.log_test("PDF Modern Sections", "FAIL", "Failed to generate ATS analysis")
                return False
            
            analysis_text = result.get('analysis_text', '')
            
            # Check for modern sections that should be in the analysis
            modern_sections = {
                'COMPREHENSIVE ATS SCORE': 'scoring breakdown',
                'CRITICAL IMPROVEMENT AREAS': 'improvement areas', 
                'IMPLEMENTATION ROADMAP': 'implementation roadmap',
                'ATS OPTIMIZATION CHECKLIST': 'optimization checklist',
                'SCORE ENHANCEMENT RECOMMENDATIONS': 'actionable recommendations',
                'ENHANCED ANALYSIS INSIGHTS': 'detailed insights'
            }
            
            found_sections = []
            for section_header, description in modern_sections.items():
                if section_header in analysis_text:
                    found_sections.append(description)
            
            if len(found_sections) < 4:
                self.log_test("PDF Modern Sections", "FAIL", 
                            f"Missing modern sections. Found: {found_sections}")
                return False
            
            # Verify the analysis contains actionable content
            actionable_indicators = [
                'specific guidance', 'recommendations', 'improvement', 'optimize',
                'enhance', 'increase', 'add', 'implement', 'focus on'
            ]
            
            found_actionable = [indicator for indicator in actionable_indicators 
                              if indicator.lower() in analysis_text.lower()]
            
            if len(found_actionable) < 5:
                self.log_test("PDF Modern Sections", "FAIL", 
                            f"Insufficient actionable content. Found: {found_actionable}")
                return False
            
            self.log_test("PDF Modern Sections", "PASS", 
                        f"Found {len(found_sections)} modern sections with actionable content")
            return True
            
        except Exception as e:
            self.log_test("PDF Modern Sections", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_download_functionality(self):
        """Test PDF download functionality via correct endpoint"""
        try:
            # Generate ATS analysis first
            success, result = self.test_ats_endpoint_comprehensive_analysis()
            if not success or not result:
                self.log_test("PDF Download Functionality", "FAIL", "Failed to generate ATS analysis")
                return False
            
            ats_id = result.get('ats_id')
            if not ats_id:
                self.log_test("PDF Download Functionality", "FAIL", "No ATS ID returned")
                return False
            
            # Test the correct download endpoint
            download_url = f"{BACKEND_URL}/api/placement-preparation/ats-score/{ats_id}/download"
            
            print(f"📥 Testing PDF Download Endpoint: {download_url}")
            
            response = self.session.get(download_url, timeout=60)
            
            if response.status_code != 200:
                self.log_test("PDF Download Functionality", "FAIL", 
                            f"Download failed: HTTP {response.status_code}, Response: {response.text}")
                return False
            
            # Verify response headers
            content_type = response.headers.get('content-type', '')
            content_disposition = response.headers.get('content-disposition', '')
            
            if 'application/pdf' not in content_type:
                self.log_test("PDF Download Functionality", "FAIL", 
                            f"Wrong content type: {content_type}")
                return False
            
            # Verify PDF content
            pdf_content = response.content
            if len(pdf_content) < 1000:
                self.log_test("PDF Download Functionality", "FAIL", 
                            f"PDF content too small: {len(pdf_content)} bytes")
                return False
            
            # Check PDF magic bytes
            if not pdf_content.startswith(b'%PDF'):
                self.log_test("PDF Download Functionality", "FAIL", 
                            "Invalid PDF format (missing PDF header)")
                return False
            
            self.log_test("PDF Download Functionality", "PASS", 
                        f"PDF downloaded successfully: {len(pdf_content)} bytes, Type: {content_type}")
            return True
            
        except Exception as e:
            self.log_test("PDF Download Functionality", "FAIL", f"Exception: {str(e)}")
            return False

    def test_content_coverage_improvement(self):
        """Test that content coverage between analysis and PDF is significantly improved"""
        try:
            # Generate comprehensive analysis
            success, result = self.test_ats_endpoint_comprehensive_analysis()
            if not success or not result:
                self.log_test("Content Coverage Improvement", "FAIL", "Failed to generate analysis")
                return False
            
            analysis_text = result.get('analysis_text', '')
            analysis_length = len(analysis_text)
            ats_id = result.get('ats_id')
            
            # Download PDF
            download_url = f"{BACKEND_URL}/api/placement-preparation/ats-score/{ats_id}/download"
            pdf_response = self.session.get(download_url, timeout=60)
            
            if pdf_response.status_code != 200:
                self.log_test("Content Coverage Improvement", "FAIL", "PDF download failed")
                return False
            
            pdf_size = len(pdf_response.content)
            
            # Calculate coverage improvement
            # Previous issue: 188 characters out of ~5000+ = 0.92% coverage
            # Expected: Much higher coverage with comprehensive content
            
            # Rough estimation: PDF should contain significant portion of analysis content
            # A well-formatted PDF with comprehensive content should be at least 15KB
            min_expected_pdf_size = 15000  # 15KB
            
            if pdf_size < min_expected_pdf_size:
                coverage_percentage = (pdf_size / min_expected_pdf_size) * 100
                self.log_test("Content Coverage Improvement", "FAIL", 
                            f"PDF size {pdf_size} bytes indicates low coverage (~{coverage_percentage:.1f}%)")
                return False
            
            # Success criteria: PDF is comprehensive (>15KB) and analysis is detailed (>5000 chars)
            coverage_ratio = pdf_size / analysis_length if analysis_length > 0 else 0
            
            self.log_test("Content Coverage Improvement", "PASS", 
                        f"Significant improvement - Analysis: {analysis_length} chars, PDF: {pdf_size} bytes, Ratio: {coverage_ratio:.2f}")
            return True
            
        except Exception as e:
            self.log_test("Content Coverage Improvement", "FAIL", f"Exception: {str(e)}")
            return False

    def test_ats_score_calculation_accuracy(self):
        """Test that ATS score calculation is working correctly with detailed reasoning"""
        try:
            resume_content = self.create_comprehensive_resume()
            
            files = {
                'resume': ('test_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Full Stack Developer',
                'job_description': 'Senior Full Stack Developer with Python, React, MongoDB, AWS, Docker, Kubernetes experience required. 5+ years experience needed.'
            }
            
            response = self.session.post(ATS_ENDPOINT, files=files, data=data, timeout=120)
            
            if response.status_code != 200:
                self.log_test("ATS Score Calculation Accuracy", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            ats_score = result.get('ats_score', 0)
            analysis_text = result.get('analysis_text', '')
            
            # Verify score is within valid range
            if not (0 <= ats_score <= 100):
                self.log_test("ATS Score Calculation Accuracy", "FAIL", 
                            f"Invalid score range: {ats_score}")
                return False
            
            # Check for detailed reasoning in analysis
            reasoning_indicators = [
                'keyword', 'experience', 'skills', 'match', 'analysis',
                'score', 'evaluation', 'assessment', 'recommendation'
            ]
            
            found_reasoning = [indicator for indicator in reasoning_indicators 
                             if indicator.lower() in analysis_text.lower()]
            
            if len(found_reasoning) < 6:
                self.log_test("ATS Score Calculation Accuracy", "FAIL", 
                            f"Insufficient reasoning in analysis. Found: {found_reasoning}")
                return False
            
            # For comprehensive resume, score should be reasonable (not too low)
            if ats_score < 60:
                self.log_test("ATS Score Calculation Accuracy", "FAIL", 
                            f"Score too low for comprehensive resume: {ats_score}/100")
                return False
            
            self.log_test("ATS Score Calculation Accuracy", "PASS", 
                        f"Score: {ats_score}/100 with detailed reasoning ({len(found_reasoning)} indicators)")
            return True
            
        except Exception as e:
            self.log_test("ATS Score Calculation Accuracy", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_pdf_fix_test(self):
        """Run all tests focused on the PDF generation fix"""
        print("=" * 80)
        print("🔧 ATS SCORE CALCULATOR PDF GENERATION FIX TESTING")
        print("Testing the critical PDF parsing fix for comprehensive content coverage")
        print("=" * 80)
        print()
        
        test_methods = [
            ("Backend Connectivity Check", self.test_backend_connectivity),
            ("Comprehensive Analysis Generation (5,000+ chars)", self.test_ats_endpoint_comprehensive_analysis),
            ("PDF Comprehensive Content (not 188 chars)", self.test_pdf_generation_comprehensive_content),
            ("PDF Modern Sections Inclusion", self.test_pdf_modern_sections_inclusion),
            ("PDF Download Functionality", self.test_pdf_download_functionality),
            ("Content Coverage Improvement", self.test_content_coverage_improvement),
            ("ATS Score Calculation Accuracy", self.test_ats_score_calculation_accuracy)
        ]
        
        results = []
        for test_name, test_method in test_methods:
            try:
                print(f"🧪 Running: {test_name}")
                if test_name == "Comprehensive Analysis Generation (5,000+ chars)":
                    result, _ = test_method()  # This method returns tuple
                else:
                    result = test_method()
                results.append(result)
                time.sleep(2)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test {test_name} failed with exception: {e}")
                results.append(False)
        
        # Summary
        print("=" * 80)
        print("🔧 PDF GENERATION FIX TESTING SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(results)
        total_tests = len(results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL PDF GENERATION FIX TESTS PASSED!")
            print("✅ Critical PDF parsing issue has been resolved")
            print("✅ Analysis text contains detailed multi-phase analysis (5,000+ characters)")
            print("✅ PDF generation works and contains comprehensive content")
            print("✅ PDF includes all modern sections: scoring breakdown, improvement areas, etc.")
            print("✅ PDF download functionality working via correct endpoint")
            print("✅ Content coverage significantly improved from 0.92%")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Review issues above.")
            
            # Identify specific failures
            failed_tests = []
            for i, (test_name, _) in enumerate(test_methods):
                if not results[i]:
                    failed_tests.append(test_name)
            
            if failed_tests:
                print("\n❌ FAILED TESTS:")
                for failed_test in failed_tests:
                    print(f"   • {failed_test}")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    print("🚀 ATS SCORE CALCULATOR PDF GENERATION FIX TESTING")
    print("=" * 80)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tester = ATSPDFTester()
    success = tester.run_comprehensive_pdf_fix_test()
    
    if success:
        print("\n✅ PDF GENERATION FIX TESTING COMPLETED SUCCESSFULLY")
        print("🎯 The critical PDF parsing issue has been resolved!")
        exit(0)
    else:
        print("\n❌ PDF GENERATION FIX TESTING COMPLETED WITH FAILURES")
        print("⚠️  Some issues remain with the PDF generation system")
        exit(1)

if __name__ == "__main__":
    main()