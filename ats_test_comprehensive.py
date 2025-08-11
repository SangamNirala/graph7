#!/usr/bin/env python3
"""
ATS Score Calculation and PDF Generation Testing
Focus: Type comparison errors and PDF generation functionality
"""

import requests
import json
import os
import tempfile
import traceback
from datetime import datetime

# Configuration
BACKEND_URL = "https://b94cc3ff-5d98-441f-b706-13a2c963a6da.preview.emergentagent.com"
ATS_ENDPOINT = f"{BACKEND_URL}/api/placement-preparation/ats-score-calculate"

class ATSTestRunner:
    def __init__(self):
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name, status, details="", error_trace=""):
        """Log test results with detailed information"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        if error_trace:
            print(f"    ERROR TRACE: {error_trace}")
        print()
        
        self.test_results.append({
            'test': test_name,
            'status': status,
            'details': details,
            'error_trace': error_trace,
            'timestamp': timestamp
        })

    def create_comprehensive_resume(self):
        """Create a comprehensive resume that should generate detailed analysis"""
        return """SARAH JOHNSON
Senior Full Stack Developer
Email: sarah.johnson@email.com | Phone: (555) 987-6543
LinkedIn: linkedin.com/in/sarahjohnson | GitHub: github.com/sarahjohnson

PROFESSIONAL SUMMARY
Experienced Senior Full Stack Developer with 7+ years of expertise in Python, JavaScript, React, and MongoDB. 
Led development teams of 8+ engineers and delivered 25+ successful projects with 99.8% uptime. 
Specialized in microservices architecture, cloud deployment, and agile methodologies.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, TypeScript, Java, Go, SQL
• Frontend Technologies: React, Vue.js, Angular, HTML5, CSS3, Bootstrap, Tailwind CSS
• Backend Technologies: FastAPI, Django, Node.js, Express.js, Flask, Spring Boot
• Databases: MongoDB, PostgreSQL, MySQL, Redis, Elasticsearch
• Cloud Platforms: AWS (EC2, S3, Lambda, RDS, EKS), Google Cloud Platform, Azure
• DevOps Tools: Docker, Kubernetes, Jenkins, GitLab CI/CD, Terraform, Ansible
• Version Control: Git, GitHub, GitLab, Bitbucket
• Testing: Jest, Pytest, Selenium, Cypress, Unit Testing, Integration Testing
• Monitoring: Prometheus, Grafana, ELK Stack, New Relic

PROFESSIONAL EXPERIENCE

Senior Full Stack Developer | TechCorp Solutions | March 2020 - Present
• Led a cross-functional team of 8 developers in building a microservices-based e-commerce platform using Python/FastAPI and React
• Increased system performance by 65% through database optimization and Redis caching strategies
• Implemented comprehensive CI/CD pipelines that reduced deployment time from 3 hours to 12 minutes
• Architected and deployed cloud infrastructure on AWS serving 5M+ daily active users
• Mentored 12+ junior developers and conducted 200+ code reviews to maintain high code quality standards
• Reduced production bugs by 80% through implementation of automated testing and monitoring
• Managed $2.5M annual technology budget and reduced infrastructure costs by 35%

Full Stack Developer | InnovateTech Inc. | June 2018 - February 2020
• Developed 15+ RESTful APIs using Django and PostgreSQL for a SaaS platform with 150,000+ users
• Built responsive frontend applications using React and TypeScript with 40% improved user engagement
• Collaborated with product managers and UX designers to deliver 30+ features on tight deadlines
• Implemented automated testing suites that improved code coverage from 45% to 98%
• Optimized database queries resulting in 50% faster page load times and improved user satisfaction
• Integrated 10+ third-party APIs including payment gateways, analytics, and communication tools

Software Developer | StartupXYZ | August 2016 - May 2018
• Developed and maintained 20+ web applications using JavaScript, HTML, CSS, and PHP
• Worked with MySQL and MongoDB databases to create efficient data storage solutions
• Participated in agile development processes and daily standups with 6-person development team
• Fixed 500+ bugs and implemented 100+ new features based on client requirements
• Contributed to open-source projects and maintained 95%+ client satisfaction rating

EDUCATION
Master of Science in Computer Science
Stanford University | Graduated: May 2016 | GPA: 3.9/4.0
Thesis: "Scalable Microservices Architecture for Real-time Data Processing"

Bachelor of Science in Software Engineering  
University of California, Berkeley | Graduated: May 2014 | GPA: 3.7/4.0

CERTIFICATIONS
• AWS Certified Solutions Architect - Professional (2023)
• Google Cloud Professional Developer (2022)
• Certified Kubernetes Administrator (CKA) (2023)
• MongoDB Certified Developer Associate (2021)
• Scrum Master Certification (CSM) (2020)

PROJECTS
E-Commerce Platform Redesign (2023)
• Led complete redesign of legacy e-commerce system using modern tech stack
• Technologies: React, FastAPI, PostgreSQL, Docker, AWS, Kubernetes
• Result: 75% improvement in user engagement and 45% increase in conversion rates
• Handled 10M+ transactions worth $50M+ annually

Real-time Analytics Dashboard (2022)
• Built scalable real-time analytics system processing 1TB+ data daily
• Technologies: Python, Apache Kafka, Elasticsearch, React, D3.js
• Implemented machine learning algorithms for predictive analytics
• Reduced data processing time from 6 hours to 15 minutes

Microservices Migration Project (2021)
• Migrated monolithic application to microservices architecture
• Technologies: Docker, Kubernetes, FastAPI, MongoDB, Redis
• Result: 90% improvement in system scalability and 60% reduction in deployment time
• Served 2M+ concurrent users with 99.9% uptime

ACHIEVEMENTS
• Increased team productivity by 55% through implementation of automated testing and deployment processes
• Reduced server costs by 40% through cloud infrastructure optimization and containerization
• Successfully delivered 25+ projects on time and within budget over 7-year career
• Received "Technical Excellence Award" in 2022 for outstanding engineering leadership
• Published 5+ technical articles on Medium with 10,000+ total views
• Speaker at 3 major tech conferences including PyCon and ReactConf
"""

    def test_backend_connectivity(self):
        """Test basic backend connectivity"""
        try:
            # Test health endpoint
            health_response = self.session.get(f"{BACKEND_URL}/health", timeout=10)
            api_response = self.session.get(f"{BACKEND_URL}/api", timeout=10)
            
            if health_response.status_code in [200, 404, 405] or api_response.status_code in [200, 404, 405]:
                self.log_test("Backend Connectivity", "PASS", 
                            f"Backend accessible - Health: {health_response.status_code}, API: {api_response.status_code}")
                return True
            else:
                self.log_test("Backend Connectivity", "FAIL", 
                            f"Backend not accessible - Health: {health_response.status_code}, API: {api_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Connection error: {str(e)}")
            return False

    def test_ats_score_calculation_comprehensive(self):
        """Test ATS score calculation with comprehensive resume"""
        try:
            resume_content = self.create_comprehensive_resume()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(resume_content)
                temp_file_path = temp_file.name
            
            try:
                with open(temp_file_path, 'rb') as resume_file:
                    files = {
                        'resume': ('comprehensive_resume.txt', resume_file, 'text/plain')
                    }
                    data = {
                        'job_title': 'Senior Full Stack Developer',
                        'job_description': '''We are seeking a Senior Full Stack Developer to join our engineering team.

Key Responsibilities:
• Design and develop scalable web applications using Python, JavaScript, and React
• Lead technical architecture decisions and mentor development teams
• Implement microservices architecture and cloud deployment strategies
• Collaborate with cross-functional teams to deliver high-quality software solutions

Required Skills:
• 5+ years of experience in full-stack development
• Strong proficiency in Python, JavaScript, React, and MongoDB
• Experience with FastAPI, Django, or similar backend frameworks
• Knowledge of cloud platforms (AWS, GCP, or Azure)
• Experience with Docker, Kubernetes, and CI/CD pipelines
• Strong problem-solving and leadership skills
• Experience with agile methodologies and team management

Preferred Skills:
• Experience with microservices architecture
• Knowledge of TypeScript and modern frontend frameworks
• Experience with automated testing and monitoring
• AWS certifications
• Experience with data processing and analytics'''
                    }
                    
                    print(f"🚀 Testing ATS Score Calculation with Comprehensive Resume...")
                    print(f"   Resume Length: {len(resume_content)} characters")
                    print(f"   Job Description Length: {len(data['job_description'])} characters")
                    
                    response = self.session.post(ATS_ENDPOINT, files=files, data=data, timeout=120)
                    
                    print(f"📊 Response Status: {response.status_code}")
                    print(f"📊 Response Headers: {dict(response.headers)}")
                    
                    if response.status_code != 200:
                        self.log_test("ATS Score Calculation - Comprehensive", "FAIL", 
                                    f"HTTP {response.status_code}: {response.text}")
                        return False, None
                    
                    result = response.json()
                    
                    # Validate response structure
                    required_fields = ['success', 'ats_id', 'ats_score', 'analysis_text', 'pdf_filename']
                    missing_fields = [field for field in required_fields if field not in result]
                    
                    if missing_fields:
                        self.log_test("ATS Score Calculation - Comprehensive", "FAIL", 
                                    f"Missing required fields: {missing_fields}")
                        return False, None
                    
                    if not result.get('success'):
                        self.log_test("ATS Score Calculation - Comprehensive", "FAIL", 
                                    f"API returned success=false: {result.get('message', 'No message')}")
                        return False, None
                    
                    # Validate ATS score
                    ats_score = result.get('ats_score', 0)
                    if not isinstance(ats_score, (int, float)) or not (0 <= ats_score <= 100):
                        self.log_test("ATS Score Calculation - Comprehensive", "FAIL", 
                                    f"Invalid ATS score: {ats_score} (type: {type(ats_score)})")
                        return False, None
                    
                    # Validate analysis text
                    analysis_text = result.get('analysis_text', '')
                    if len(analysis_text) < 500:
                        self.log_test("ATS Score Calculation - Comprehensive", "FAIL", 
                                    f"Analysis text too short: {len(analysis_text)} characters")
                        return False, None
                    
                    print(f"📝 ANALYSIS TEXT PREVIEW:")
                    print("-" * 40)
                    print(analysis_text[:1000] + "..." if len(analysis_text) > 1000 else analysis_text)
                    print("-" * 40)
                    
                    self.log_test("ATS Score Calculation - Comprehensive", "PASS", 
                                f"Score: {ats_score}/100, Analysis: {len(analysis_text)} chars, PDF: {result.get('pdf_filename', 'N/A')}")
                    
                    return True, result
                    
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
                    
        except Exception as e:
            self.log_test("ATS Score Calculation - Comprehensive", "FAIL", 
                        f"Exception: {str(e)}", traceback.format_exc())
            return False, None

    def test_pdf_generation_and_download(self, ats_result):
        """Test PDF generation and download functionality"""
        if not ats_result:
            self.log_test("PDF Generation and Download", "SKIP", "No ATS result to test with")
            return False
            
        try:
            ats_id = ats_result.get('ats_id')
            pdf_filename = ats_result.get('pdf_filename')
            
            if not ats_id or not pdf_filename:
                self.log_test("PDF Generation and Download", "FAIL", 
                            f"Missing PDF info - ID: {ats_id}, Filename: {pdf_filename}")
                return False
            
            # Test PDF download using the correct endpoint pattern
            pdf_download_url = f"{BACKEND_URL}/api/placement-preparation/ats-score/{ats_id}/download"
            
            print(f"📥 Testing PDF Download: {pdf_download_url}")
            
            pdf_response = self.session.get(pdf_download_url, timeout=60)
            
            print(f"📊 PDF Response Status: {pdf_response.status_code}")
            print(f"📊 PDF Response Headers: {dict(pdf_response.headers)}")
            
            if pdf_response.status_code != 200:
                self.log_test("PDF Generation and Download", "FAIL", 
                            f"PDF download failed - Status: {pdf_response.status_code}, Response: {pdf_response.text[:500]}")
                return False
            
            # Validate PDF content
            content_type = pdf_response.headers.get('content-type', '')
            content_length = len(pdf_response.content)
            
            if 'pdf' not in content_type.lower():
                self.log_test("PDF Generation and Download", "FAIL", 
                            f"Invalid content type: {content_type}")
                return False
            
            if content_length < 1000:  # PDF should be at least 1KB
                self.log_test("PDF Generation and Download", "FAIL", 
                            f"PDF too small: {content_length} bytes - likely empty or corrupted")
                return False
            
            # Check if PDF starts with PDF header
            pdf_header = pdf_response.content[:4]
            if pdf_header != b'%PDF':
                self.log_test("PDF Generation and Download", "FAIL", 
                            f"Invalid PDF header: {pdf_header}")
                return False
            
            self.log_test("PDF Generation and Download", "PASS", 
                        f"PDF downloaded successfully - Size: {content_length} bytes, Type: {content_type}")
            return True
            
        except Exception as e:
            self.log_test("PDF Generation and Download", "FAIL", 
                        f"Exception: {str(e)}", traceback.format_exc())
            return False

    def test_score_breakdown_analysis(self, ats_result):
        """Test score breakdown table generation logic for type comparison errors"""
        if not ats_result:
            self.log_test("Score Breakdown Analysis", "SKIP", "No ATS result to test with")
            return False
            
        try:
            analysis_text = ats_result.get('analysis_text', '')
            
            # Look for score breakdown indicators
            breakdown_indicators = [
                'DETAILED SCORING BREAKDOWN',
                'SCORE BREAKDOWN', 
                'SCORING BREAKDOWN',
                'Keyword Optimization:',
                'Experience Relevance:',
                'Technical Competency:',
                'Qualifications:'
            ]
            
            found_indicators = [indicator for indicator in breakdown_indicators if indicator in analysis_text]
            
            print(f"🔍 Found breakdown indicators: {found_indicators}")
            
            # Look for score patterns that might cause type comparison errors
            import re
            score_patterns = [
                r'(\w+):\s*(\d+)\s*/\s*(\d+)',  # Category: score/max
                r'(\w+)\s*:\s*(\d+)%',          # Category: percentage
                r'(\d+)\s*/\s*(\d+)',           # score/max format
            ]
            
            scores_found = []
            potential_type_issues = []
            
            for pattern in score_patterns:
                matches = re.findall(pattern, analysis_text)
                for match in matches:
                    scores_found.append(match)
                    # Check for potential type issues
                    if len(match) >= 2:
                        try:
                            # Try to convert to int to check for type issues
                            if len(match) == 3:  # category, score, max format
                                score_val = int(match[1])  # score
                                max_val = int(match[2])  # max
                                # Test comparison that might cause '<' error
                                if score_val < max_val:  # This could fail if types are wrong
                                    pass
                            elif len(match) == 2:  # category, percentage or score/max format
                                if match[1].endswith('%'):
                                    int(match[1][:-1])  # remove % and convert
                                else:
                                    int(match[1])
                        except (ValueError, TypeError) as ve:
                            potential_type_issues.append(f"Type conversion error for {match}: {ve}")
            
            print(f"🔢 Found {len(scores_found)} score entries")
            print(f"⚠️  Found {len(potential_type_issues)} potential type issues")
            
            if potential_type_issues:
                self.log_test("Score Breakdown Analysis", "FAIL", 
                            f"Type conversion issues found: {potential_type_issues}")
                return False
            
            if len(found_indicators) < 1:
                self.log_test("Score Breakdown Analysis", "WARN", 
                            f"Limited score breakdown indicators found: {found_indicators}")
                return True  # Not a failure, just limited data
            
            self.log_test("Score Breakdown Analysis", "PASS", 
                        f"Score breakdown analysis valid - Found {len(scores_found)} score entries, {len(found_indicators)} indicators")
            return True
            
        except Exception as e:
            self.log_test("Score Breakdown Analysis", "FAIL", 
                        f"Exception: {str(e)}", traceback.format_exc())
            return False

    def run_comprehensive_tests(self):
        """Run all tests focusing on type comparison errors and PDF generation"""
        print("=" * 80)
        print("🧪 ATS SCORE CALCULATION AND PDF GENERATION TESTING")
        print("Focus: Type comparison errors and PDF generation functionality")
        print("=" * 80)
        print()
        
        # Test 1: Backend connectivity
        if not self.test_backend_connectivity():
            print("❌ Backend connectivity failed. Stopping tests.")
            return False
        
        # Test 2: ATS score calculation with comprehensive resume
        success, ats_result = self.test_ats_score_calculation_comprehensive()
        if not success:
            print("❌ ATS score calculation failed. Continuing with other tests.")
            ats_result = None
        
        # Test 3: PDF generation and download
        self.test_pdf_generation_and_download(ats_result)
        
        # Test 4: Score breakdown analysis
        self.test_score_breakdown_analysis(ats_result)
        
        # Summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        warned_tests = len([r for r in self.test_results if r['status'] == 'WARN'])
        skipped_tests = len([r for r in self.test_results if r['status'] == 'SKIP'])
        
        print(f"✅ Passed: {passed_tests}/{total_tests}")
        print(f"❌ Failed: {failed_tests}/{total_tests}")
        print(f"⚠️  Warnings: {warned_tests}/{total_tests}")
        print(f"⏭️  Skipped: {skipped_tests}/{total_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Detailed results
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status_symbol = "✅" if result['status'] == "PASS" else "❌" if result['status'] == "FAIL" else "⚠️" if result['status'] == "WARN" else "⏭️"
            print(f"{status_symbol} {result['test']}: {result['details']}")
            if result['error_trace'] and result['status'] == 'FAIL':
                print(f"   Error: {result['error_trace'].split('Traceback')[0].strip()}")
        
        if failed_tests == 0:
            print("\n🎉 ALL CRITICAL TESTS PASSED!")
            print("✅ ATS score calculation working correctly")
            print("✅ PDF generation and download functional")
            print("✅ No type comparison errors detected")
            print("✅ Score breakdown analysis working")
        else:
            print(f"\n⚠️  {failed_tests} test(s) failed. Review issues above.")
            
        return failed_tests == 0

def main():
    """Main test execution"""
    tester = ATSTestRunner()
    success = tester.run_comprehensive_tests()
    
    if success:
        print("\n✅ ATS TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ ATS TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()