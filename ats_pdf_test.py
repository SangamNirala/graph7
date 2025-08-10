#!/usr/bin/env python3
"""
ATS Score PDF Generation Testing for Placement Preparation System
Testing the current ATS Score calculation and PDF generation functionality to establish baseline quality
"""

import requests
import json
import time
import os
from datetime import datetime
import tempfile

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://350119d5-292b-44b0-a739-5efd46504bc2.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class ATSPDFTester:
    def __init__(self):
        self.session = requests.Session()
        self.ats_id = None
        self.pdf_size = 0
        self.analysis_text_length = 0
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()

    def test_backend_connectivity(self):
        """Test 1: Confirm backend service is running and accessible"""
        try:
            response = self.session.get(f"{BACKEND_URL}/api")
            
            if response.status_code in [200, 404]:  # 404 is fine, means server is running
                self.log_test("Backend Connectivity", "PASS", 
                            f"Backend service is accessible (Status: {response.status_code})")
                return True
            else:
                self.log_test("Backend Connectivity", "FAIL", 
                            f"Backend returned unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Connection failed: {str(e)}")
            return False

    def test_ats_score_calculation(self):
        """Test 2: Test the /api/placement-preparation/ats-score-calculate endpoint"""
        try:
            # Create realistic sample resume content for a Data Scientist role
            sample_resume_content = """
SARAH JOHNSON
Data Scientist | Machine Learning Engineer
Email: sarah.johnson@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/sarahjohnson | GitHub: github.com/sarahjohnson

PROFESSIONAL SUMMARY
Experienced Data Scientist with 5+ years of expertise in machine learning, statistical analysis, and data visualization. 
Proven track record of developing predictive models that increased business revenue by 25% and reduced operational costs by 30%. 
Skilled in Python, R, SQL, and cloud platforms with experience leading cross-functional teams.

TECHNICAL SKILLS
• Programming Languages: Python, R, SQL, Java, Scala
• Machine Learning: Scikit-learn, TensorFlow, PyTorch, XGBoost, Random Forest
• Data Visualization: Tableau, Power BI, Matplotlib, Seaborn, Plotly
• Big Data Technologies: Spark, Hadoop, Kafka, Airflow
• Cloud Platforms: AWS (S3, EC2, SageMaker), Google Cloud Platform, Azure
• Databases: PostgreSQL, MongoDB, Cassandra, Redis
• Tools: Git, Docker, Kubernetes, Jupyter, MLflow

PROFESSIONAL EXPERIENCE

Senior Data Scientist | TechCorp Inc. | 2021 - Present
• Developed and deployed 15+ machine learning models resulting in $2.5M annual cost savings
• Led a team of 4 data scientists and analysts on customer churn prediction project
• Implemented real-time recommendation system serving 1M+ users with 95% uptime
• Reduced model training time by 60% through optimization and parallel processing
• Collaborated with product teams to define KPIs and success metrics for 10+ projects

Data Scientist | DataSolutions LLC | 2019 - 2021
• Built predictive models for demand forecasting with 92% accuracy improvement
• Automated data pipeline processing 500GB+ daily data using Apache Airflow
• Created interactive dashboards in Tableau used by 50+ stakeholders
• Performed A/B testing analysis for product features affecting 100K+ users
• Mentored 3 junior data scientists and conducted technical interviews

Junior Data Analyst | Analytics Pro | 2018 - 2019
• Analyzed customer behavior data to identify trends and patterns
• Developed SQL queries and reports for business intelligence team
• Created data visualizations and presentations for executive leadership
• Participated in agile development process and sprint planning

EDUCATION
Master of Science in Data Science | Stanford University | 2018
• Relevant Coursework: Machine Learning, Statistical Modeling, Deep Learning, Big Data Analytics
• Thesis: "Predictive Analytics for Customer Lifetime Value in E-commerce"
• GPA: 3.8/4.0

Bachelor of Science in Computer Science | UC Berkeley | 2016
• Minor in Statistics
• Dean's List: 6 semesters
• GPA: 3.7/4.0

PROJECTS
Customer Segmentation Analysis (2023)
• Implemented K-means clustering on 1M+ customer records
• Identified 5 distinct customer segments leading to 20% increase in marketing ROI
• Technologies: Python, Scikit-learn, Pandas, Matplotlib

Fraud Detection System (2022)
• Developed ensemble model combining Random Forest and Neural Networks
• Achieved 98.5% accuracy in detecting fraudulent transactions
• Reduced false positive rate by 40% compared to existing system
• Technologies: Python, TensorFlow, XGBoost, AWS SageMaker

CERTIFICATIONS
• AWS Certified Machine Learning - Specialty (2023)
• Google Cloud Professional Data Engineer (2022)
• Certified Analytics Professional (CAP) (2021)
• Tableau Desktop Specialist (2020)

PUBLICATIONS & ACHIEVEMENTS
• "Advanced Techniques in Customer Churn Prediction" - Journal of Data Science (2023)
• Speaker at PyData Conference 2022: "Scaling ML Models in Production"
• Winner of DataHack 2021 Competition - Predictive Modeling Track
• Patent Pending: "Method for Real-time Anomaly Detection in Streaming Data"
            """.strip()
            
            # Create job description for Data Scientist role
            job_title = "Senior Data Scientist"
            job_description = """
We are seeking a Senior Data Scientist to join our growing analytics team. The ideal candidate will have strong experience in machine learning, statistical analysis, and data visualization. You will work on challenging problems involving large datasets and will be responsible for developing predictive models that drive business decisions.

Key Responsibilities:
- Develop and deploy machine learning models for various business use cases
- Analyze large datasets to identify trends, patterns, and insights
- Create data visualizations and dashboards for stakeholders
- Collaborate with cross-functional teams including product, engineering, and business
- Mentor junior team members and contribute to best practices
- Stay current with latest developments in data science and machine learning

Required Qualifications:
- Master's degree in Data Science, Computer Science, Statistics, or related field
- 5+ years of experience in data science or machine learning roles
- Strong programming skills in Python and R
- Experience with machine learning frameworks (scikit-learn, TensorFlow, PyTorch)
- Proficiency in SQL and database technologies
- Experience with cloud platforms (AWS, GCP, or Azure)
- Strong communication skills and ability to present findings to non-technical stakeholders
- Experience with data visualization tools (Tableau, Power BI, or similar)

Preferred Qualifications:
- PhD in quantitative field
- Experience with big data technologies (Spark, Hadoop)
- Knowledge of MLOps and model deployment practices
- Experience leading data science teams
- Publications or contributions to open source projects
            """.strip()
            
            # Create temporary file with resume content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(sample_resume_content)
                temp_file_path = temp_file.name
            
            try:
                # Prepare multipart form data
                with open(temp_file_path, 'rb') as resume_file:
                    files = {
                        'resume': ('sarah_johnson_resume.txt', resume_file, 'text/plain')
                    }
                    data = {
                        'job_title': job_title,
                        'job_description': job_description
                    }
                    
                    response = self.session.post(
                        f"{BASE_URL}/placement-preparation/ats-score-calculate",
                        files=files,
                        data=data,
                        timeout=60  # Increase timeout for AI processing
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extract key information
                    ats_score = result.get('ats_score', 0)
                    self.ats_id = result.get('ats_id', '')
                    analysis_text = result.get('analysis_text', '')
                    self.analysis_text_length = len(analysis_text)
                    
                    # Validate response structure
                    required_fields = ['ats_score', 'ats_id', 'analysis_text', 'pdf_generated']
                    missing_fields = [field for field in required_fields if field not in result]
                    
                    if missing_fields:
                        self.log_test("ATS Score Calculation", "FAIL", 
                                    f"Missing required fields: {missing_fields}")
                        return False
                    
                    if not result.get('pdf_generated', False):
                        self.log_test("ATS Score Calculation", "FAIL", 
                                    "PDF generation flag is False")
                        return False
                    
                    self.log_test("ATS Score Calculation", "PASS", 
                                f"ATS Score: {ats_score}/100, Analysis Length: {self.analysis_text_length} chars, ATS ID: {self.ats_id[:8]}...")
                    return True
                else:
                    self.log_test("ATS Score Calculation", "FAIL", 
                                f"HTTP {response.status_code}: {response.text}")
                    return False
                    
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            self.log_test("ATS Score Calculation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_generation_and_download(self):
        """Test 3 & 4: Verify PDF generation and test download endpoint"""
        try:
            if not self.ats_id:
                self.log_test("PDF Generation and Download", "FAIL", 
                            "No ATS ID available from previous test")
                return False
            
            # Test PDF download endpoint
            response = self.session.get(
                f"{BASE_URL}/placement-preparation/ats-score/{self.ats_id}/download",
                timeout=30
            )
            
            if response.status_code == 200:
                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' not in content_type:
                    self.log_test("PDF Generation and Download", "FAIL", 
                                f"Wrong content type: {content_type}")
                    return False
                
                # Check PDF size
                self.pdf_size = len(response.content)
                if self.pdf_size < 1000:  # PDF should be at least 1KB
                    self.log_test("PDF Generation and Download", "FAIL", 
                                f"PDF too small: {self.pdf_size} bytes")
                    return False
                
                # Verify PDF header
                pdf_header = response.content[:4]
                if pdf_header != b'%PDF':
                    self.log_test("PDF Generation and Download", "FAIL", 
                                "Invalid PDF format - missing PDF header")
                    return False
                
                self.log_test("PDF Generation and Download", "PASS", 
                            f"PDF downloaded successfully: {self.pdf_size} bytes, Content-Type: {content_type}")
                return True
            else:
                self.log_test("PDF Generation and Download", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("PDF Generation and Download", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_content_verification(self):
        """Test 5: Check that PDF contains expected sections"""
        try:
            if not self.ats_id:
                self.log_test("PDF Content Verification", "FAIL", 
                            "No ATS ID available for content verification")
                return False
            
            # Download PDF again for content analysis
            response = self.session.get(
                f"{BASE_URL}/placement-preparation/ats-score/{self.ats_id}/download",
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test("PDF Content Verification", "FAIL", 
                            f"Could not download PDF for content verification: {response.status_code}")
                return False
            
            # Save PDF temporarily for analysis
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_pdf:
                temp_pdf.write(response.content)
                temp_pdf_path = temp_pdf.name
            
            try:
                # Try to extract text from PDF using PyPDF2
                try:
                    import PyPDF2
                    import io
                    
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))
                    pdf_text = ""
                    for page in pdf_reader.pages:
                        pdf_text += page.extract_text() + "\n"
                    
                    # Check for expected sections in PDF
                    expected_sections = [
                        'ATS SCORE',
                        'SCORE',
                        'ANALYSIS',
                        'IMPROVEMENT',
                        'RECOMMENDATION'
                    ]
                    
                    found_sections = []
                    for section in expected_sections:
                        if section.upper() in pdf_text.upper():
                            found_sections.append(section)
                    
                    # Calculate content coverage
                    content_coverage = len(pdf_text) / max(self.analysis_text_length, 1) if self.analysis_text_length > 0 else 0
                    
                    if len(found_sections) >= 3:  # At least 3 expected sections
                        self.log_test("PDF Content Verification", "PASS", 
                                    f"Found {len(found_sections)}/{len(expected_sections)} expected sections: {', '.join(found_sections)}")
                        self.log_test("PDF Content Analysis", "INFO", 
                                    f"PDF text length: {len(pdf_text)} chars, Content coverage: {content_coverage:.2%}")
                        return True
                    else:
                        self.log_test("PDF Content Verification", "FAIL", 
                                    f"Only found {len(found_sections)}/{len(expected_sections)} expected sections: {', '.join(found_sections)}")
                        self.log_test("PDF Content Analysis", "INFO", 
                                    f"PDF text length: {len(pdf_text)} chars, Content coverage: {content_coverage:.2%}")
                        return False
                        
                except ImportError:
                    self.log_test("PDF Content Verification", "WARN", 
                                "PyPDF2 not available - cannot verify PDF content, but PDF download successful")
                    return True
                    
            finally:
                # Clean up temporary PDF file
                os.unlink(temp_pdf_path)
                
        except Exception as e:
            self.log_test("PDF Content Verification", "FAIL", f"Exception: {str(e)}")
            return False

    def test_ats_calculation_with_different_resume(self):
        """Additional Test: Test with a Software Developer resume to verify system flexibility"""
        try:
            # Create sample resume for Software Developer
            software_dev_resume = """
ALEX CHEN
Full Stack Software Developer
Email: alex.chen@email.com | Phone: (555) 987-6543
GitHub: github.com/alexchen | Portfolio: alexchen.dev

SUMMARY
Full Stack Software Developer with 4+ years of experience building scalable web applications. 
Expertise in React, Node.js, Python, and cloud technologies. Proven track record of delivering 
high-quality software solutions that improved user engagement by 40% and reduced load times by 50%.

TECHNICAL SKILLS
• Frontend: React, Vue.js, JavaScript, TypeScript, HTML5, CSS3, Sass
• Backend: Node.js, Python, Django, FastAPI, Express.js
• Databases: PostgreSQL, MongoDB, Redis, MySQL
• Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD, Jenkins
• Tools: Git, Webpack, Jest, Cypress, Postman

EXPERIENCE
Senior Software Developer | WebTech Solutions | 2022 - Present
• Developed and maintained 5+ React applications serving 100K+ users
• Built RESTful APIs using Node.js and Python handling 10K+ requests/day
• Implemented automated testing reducing bugs by 60%
• Led code reviews and mentored 2 junior developers

Software Developer | StartupCorp | 2020 - 2022
• Created responsive web applications using React and Vue.js
• Designed and implemented database schemas for 3 major projects
• Optimized application performance resulting in 50% faster load times
• Collaborated with UX/UI designers to implement pixel-perfect designs

EDUCATION
Bachelor of Science in Computer Science | UC San Diego | 2020
• Relevant Coursework: Data Structures, Algorithms, Software Engineering
• Senior Project: E-commerce platform built with MERN stack

PROJECTS
Task Management App (2023)
• Full-stack application built with React, Node.js, and MongoDB
• Implemented real-time updates using WebSocket
• Deployed on AWS with Docker containers

Weather Dashboard (2022)
• React application consuming multiple weather APIs
• Responsive design with interactive charts using D3.js
• Implemented caching to reduce API calls by 70%
            """.strip()
            
            job_title = "Full Stack Software Developer"
            job_description = """
We are looking for a Full Stack Software Developer to join our engineering team. 
You will be responsible for developing both frontend and backend components of our web applications.

Requirements:
- 3+ years of experience in full stack development
- Proficiency in React and Node.js
- Experience with databases (PostgreSQL, MongoDB)
- Knowledge of cloud platforms (AWS preferred)
- Strong problem-solving skills
- Experience with version control (Git)
            """.strip()
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(software_dev_resume)
                temp_file_path = temp_file.name
            
            try:
                with open(temp_file_path, 'rb') as resume_file:
                    files = {
                        'resume': ('alex_chen_resume.txt', resume_file, 'text/plain')
                    }
                    data = {
                        'job_title': job_title,
                        'job_description': job_description
                    }
                    
                    response = self.session.post(
                        f"{BASE_URL}/placement-preparation/ats-score-calculate",
                        files=files,
                        data=data,
                        timeout=60
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    ats_score = result.get('ats_score', 0)
                    analysis_length = len(result.get('analysis_text', ''))
                    
                    self.log_test("Software Developer ATS Test", "PASS", 
                                f"ATS Score: {ats_score}/100, Analysis Length: {analysis_length} chars")
                    return True
                else:
                    self.log_test("Software Developer ATS Test", "FAIL", 
                                f"HTTP {response.status_code}: {response.text}")
                    return False
                    
            finally:
                os.unlink(temp_file_path)
                
        except Exception as e:
            self.log_test("Software Developer ATS Test", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all ATS PDF tests in sequence"""
        print("=" * 80)
        print("ATS SCORE PDF GENERATION TESTING - BASELINE QUALITY ASSESSMENT")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Backend Connectivity
        test_results.append(self.test_backend_connectivity())
        
        # Test 2: ATS Score Calculation
        test_results.append(self.test_ats_score_calculation())
        
        # Test 3 & 4: PDF Generation and Download
        test_results.append(self.test_pdf_generation_and_download())
        
        # Test 5: PDF Content Verification
        test_results.append(self.test_pdf_content_verification())
        
        # Additional Test: Different Resume Type
        test_results.append(self.test_ats_calculation_with_different_resume())
        
        # Summary
        print("=" * 80)
        print("ATS PDF TESTING SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Baseline Quality Assessment
        print("\n" + "=" * 80)
        print("BASELINE QUALITY ASSESSMENT")
        print("=" * 80)
        
        if self.analysis_text_length > 0:
            print(f"📝 Analysis Text Length: {self.analysis_text_length} characters")
        
        if self.pdf_size > 0:
            print(f"📄 PDF File Size: {self.pdf_size} bytes ({self.pdf_size/1024:.1f} KB)")
        
        if self.ats_id:
            print(f"🆔 Sample ATS ID: {self.ats_id}")
        
        print(f"\n📋 Current PDF Generation Quality:")
        if passed_tests >= 4:
            print("✅ PDF generation is functional and ready for enhancement")
        elif passed_tests >= 2:
            print("⚠️  PDF generation has some issues that need to be addressed")
        else:
            print("❌ PDF generation has significant issues requiring immediate attention")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! ATS Score PDF generation is working correctly.")
            print("📈 System is ready for enhancement and improvement.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Issues identified for enhancement process.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    print("🚀 Starting ATS Score PDF Generation Testing...")
    print("🎯 Goal: Establish baseline quality before enhancement\n")
    
    tester = ATSPDFTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ ATS PDF TESTING COMPLETED SUCCESSFULLY")
        print("📊 Baseline established - system ready for enhancement")
        exit(0)
    else:
        print("\n⚠️  ATS PDF TESTING COMPLETED WITH SOME ISSUES")
        print("🔧 Issues identified for improvement during enhancement")
        exit(1)

if __name__ == "__main__":
    main()