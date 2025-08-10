#!/usr/bin/env python3
"""
Focused Testing for Rejection Reasons POST Endpoint Functionality
Testing the specific rejection reasons workflow that was reported as failing with net::ERR_FAILED
"""

import requests
import json
import time
import os
from datetime import datetime
import io

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://882970a1-15c9-4eb2-9f43-a49f0b775561.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class RejectionReasonsWorkflowTester:
    def __init__(self):
        self.session = requests.Session()
        self.rejection_analysis_id = None
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()

    def test_backend_connectivity(self):
        """Test basic backend connectivity"""
        try:
            response = self.session.get(f"{BASE_URL}/health", timeout=10)
            if response.status_code == 200:
                self.log_test("Backend Connectivity", "PASS", f"Backend accessible at {BASE_URL}")
                return True
            else:
                # Try a different endpoint if health doesn't exist
                response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons", timeout=10)
                if response.status_code in [200, 404]:  # 404 is acceptable for empty list
                    self.log_test("Backend Connectivity", "PASS", f"Backend accessible at {BASE_URL}")
                    return True
                else:
                    self.log_test("Backend Connectivity", "FAIL", f"HTTP {response.status_code}: {response.text}")
                    return False
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Connection error: {str(e)}")
            return False

    def test_get_rejection_reasons_endpoint(self):
        """Test GET /api/placement-preparation/rejection-reasons endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                analyses = data.get("analyses", [])
                self.log_test("GET Rejection Reasons Endpoint", "PASS", 
                            f"Retrieved {len(analyses)} existing analyses")
                return True
            else:
                self.log_test("GET Rejection Reasons Endpoint", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("GET Rejection Reasons Endpoint", "FAIL", f"Exception: {str(e)}")
            return False

    def create_sample_resume_file(self):
        """Create a realistic sample resume for testing"""
        resume_content = """SARAH JOHNSON
Senior Data Scientist
Email: sarah.johnson@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/sarahjohnson

PROFESSIONAL SUMMARY
Experienced data scientist with 4+ years in machine learning, statistical analysis, and data visualization. 
Proven track record in developing predictive models and deriving actionable insights from complex datasets.

TECHNICAL SKILLS
• Programming Languages: Python, R, SQL
• Machine Learning: Scikit-learn, TensorFlow, Keras, XGBoost
• Data Visualization: Matplotlib, Seaborn, Plotly, Tableau
• Databases: PostgreSQL, MongoDB, MySQL
• Tools: Jupyter, Git, Docker, AWS

PROFESSIONAL EXPERIENCE

Data Scientist | TechCorp Inc. | 2020 - Present
• Developed machine learning models that improved customer retention by 15%
• Built automated data pipelines processing 1M+ records daily
• Created interactive dashboards for executive reporting
• Collaborated with cross-functional teams on product analytics

Junior Data Analyst | DataSolutions LLC | 2019 - 2020
• Performed statistical analysis on customer behavior data
• Created reports and visualizations for business stakeholders
• Assisted in A/B testing and experimental design

EDUCATION
Master of Science in Data Science | University of Technology | 2019
Bachelor of Science in Statistics | State University | 2017

PROJECTS
• Customer Churn Prediction Model: Achieved 92% accuracy using ensemble methods
• Sales Forecasting System: Reduced forecasting error by 25% using time series analysis
• Sentiment Analysis Tool: Built NLP pipeline for social media monitoring

CERTIFICATIONS
• AWS Certified Machine Learning - Specialty
• Google Analytics Certified
"""
        return resume_content.strip()

    def test_post_rejection_reasons_with_formdata(self):
        """Test POST /api/placement-preparation/rejection-reasons endpoint with proper FormData"""
        try:
            # Create sample resume content
            resume_content = self.create_sample_resume_file()
            
            # Prepare FormData with file upload
            files = {
                'resume': ('sarah_resume.txt', resume_content.encode('utf-8'), 'text/plain')
            }
            
            form_data = {
                'job_title': 'Senior Data Scientist',
                'job_description': '''We are seeking a Senior Data Scientist with 5+ years of experience to join our AI team. 
                
Key Requirements:
- 5+ years of experience in machine learning and data science
- Expert-level proficiency in Python, R, and SQL
- Experience with deep learning frameworks (TensorFlow, PyTorch)
- Strong background in statistical modeling and hypothesis testing
- Experience with cloud platforms (AWS, GCP, Azure)
- PhD in Computer Science, Statistics, or related field preferred
- Experience with big data technologies (Spark, Hadoop)
- Knowledge of MLOps and model deployment
- Experience leading data science teams
- Published research in top-tier conferences/journals

Responsibilities:
- Lead complex machine learning projects from conception to deployment
- Mentor junior data scientists and analysts
- Collaborate with engineering teams on model productionization
- Present findings to C-level executives
- Drive innovation in AI/ML methodologies'''
            }
            
            self.log_test("POST Rejection Reasons - Sending Request", "INFO", 
                        f"Sending POST request to {BASE_URL}/placement-preparation/rejection-reasons")
            
            # Send POST request with FormData
            response = self.session.post(
                f"{BASE_URL}/placement-preparation/rejection-reasons", 
                files=files, 
                data=form_data,
                timeout=30  # Increased timeout for analysis processing
            )
            
            self.log_test("POST Rejection Reasons - Response Received", "INFO", 
                        f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["success", "rejection_id", "rejection_reasons"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("POST Rejection Reasons FormData", "FAIL", 
                                f"Missing required response fields: {missing_fields}")
                    return False
                
                if not data.get("success"):
                    self.log_test("POST Rejection Reasons FormData", "FAIL", 
                                f"Request not successful: {data.get('message', 'Unknown error')}")
                    return False
                
                self.rejection_analysis_id = data.get("rejection_id")
                analysis_text = data.get("rejection_reasons", "")
                
                # Verify analysis quality
                if len(analysis_text) < 500:
                    self.log_test("POST Rejection Reasons FormData", "FAIL", 
                                f"Analysis text too short: {len(analysis_text)} characters")
                    return False
                
                # Count bullet points in analysis
                bullet_count = analysis_text.count('•') + analysis_text.count('-') + analysis_text.count('*')
                
                self.log_test("POST Rejection Reasons FormData", "PASS", 
                            f"Analysis created successfully - ID: {self.rejection_analysis_id}, "
                            f"Analysis length: {len(analysis_text)} chars, Bullet points: {bullet_count}")
                return True
                
            elif response.status_code == 400:
                self.log_test("POST Rejection Reasons FormData", "FAIL", 
                            f"Bad Request (400): {response.text}")
                return False
            elif response.status_code == 500:
                self.log_test("POST Rejection Reasons FormData", "FAIL", 
                            f"Server Error (500): {response.text}")
                return False
            else:
                self.log_test("POST Rejection Reasons FormData", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            self.log_test("POST Rejection Reasons FormData", "FAIL", 
                        "Request timeout - server may be processing")
            return False
        except requests.exceptions.ConnectionError as e:
            self.log_test("POST Rejection Reasons FormData", "FAIL", 
                        f"Connection error (net::ERR_FAILED equivalent): {str(e)}")
            return False
        except Exception as e:
            self.log_test("POST Rejection Reasons FormData", "FAIL", f"Exception: {str(e)}")
            return False

    def test_analysis_storage_verification(self):
        """Test that the analysis was properly stored by retrieving it via GET"""
        try:
            if not self.rejection_analysis_id:
                self.log_test("Analysis Storage Verification", "FAIL", 
                            "No rejection analysis ID available from POST request")
                return False
            
            # Add a small delay to ensure the analysis is stored
            time.sleep(2)
            
            # Get all analyses to verify our analysis is stored
            response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons", timeout=15)
            
            if response.status_code != 200:
                self.log_test("Analysis Storage Verification", "FAIL", 
                            f"Failed to retrieve analyses: HTTP {response.status_code}")
                return False
            
            data = response.json()
            analyses = data.get("analyses", [])
            
            # Debug: Check what fields are available
            if analyses:
                sample_analysis = analyses[0]
                available_fields = list(sample_analysis.keys())
                self.log_test("Analysis Storage Verification", "INFO", 
                            f"Available fields in stored analysis: {available_fields}")
            
            # Find our analysis
            our_analysis = None
            for analysis in analyses:
                if analysis.get("id") == self.rejection_analysis_id:
                    our_analysis = analysis
                    break
            
            if not our_analysis:
                self.log_test("Analysis Storage Verification", "FAIL", 
                            f"Analysis with ID {self.rejection_analysis_id} not found in stored analyses")
                return False
            
            # Verify analysis structure - use more flexible field checking
            required_fields = ["id", "job_title"]
            missing_fields = [field for field in required_fields if field not in our_analysis]
            
            if missing_fields:
                self.log_test("Analysis Storage Verification", "FAIL", 
                            f"Stored analysis missing fields: {missing_fields}")
                return False
            
            self.log_test("Analysis Storage Verification", "PASS", 
                        f"Analysis properly stored and retrievable - Job: {our_analysis.get('job_title')}")
            return True
            
        except Exception as e:
            self.log_test("Analysis Storage Verification", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_download_functionality(self):
        """Test PDF download functionality for the created analysis"""
        try:
            if not self.rejection_analysis_id:
                self.log_test("PDF Download Functionality", "FAIL", 
                            "No rejection analysis ID available for PDF download")
                return False
            
            # Test PDF download endpoint
            pdf_url = f"{BASE_URL}/placement-preparation/rejection-reasons/{self.rejection_analysis_id}/download"
            response = self.session.get(pdf_url, timeout=20)
            
            if response.status_code == 200:
                # Verify it's a PDF
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' not in content_type:
                    self.log_test("PDF Download Functionality", "FAIL", 
                                f"Invalid content type: {content_type} (expected application/pdf)")
                    return False
                
                # Verify PDF content size
                pdf_size = len(response.content)
                if pdf_size < 1000:  # PDF should be at least 1KB
                    self.log_test("PDF Download Functionality", "FAIL", 
                                f"PDF too small: {pdf_size} bytes")
                    return False
                
                # Verify PDF header
                if not response.content.startswith(b'%PDF'):
                    self.log_test("PDF Download Functionality", "FAIL", 
                                "Invalid PDF format - missing PDF header")
                    return False
                
                self.log_test("PDF Download Functionality", "PASS", 
                            f"PDF downloaded successfully - Size: {pdf_size} bytes")
                return True
                
            elif response.status_code == 404:
                self.log_test("PDF Download Functionality", "FAIL", 
                            "PDF not found - analysis may not have been processed correctly")
                return False
            else:
                self.log_test("PDF Download Functionality", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("PDF Download Functionality", "FAIL", f"Exception: {str(e)}")
            return False

    def test_error_handling_invalid_file(self):
        """Test error handling with invalid file format"""
        try:
            # Test with invalid file format
            files = {
                'resume': ('invalid.xyz', b'invalid content', 'application/octet-stream')
            }
            
            form_data = {
                'job_title': 'Test Position',
                'job_description': 'Test description for error handling'
            }
            
            response = self.session.post(
                f"{BASE_URL}/placement-preparation/rejection-reasons", 
                files=files, 
                data=form_data,
                timeout=15
            )
            
            # Should return 400 for invalid file format
            if response.status_code == 400:
                self.log_test("Error Handling - Invalid File", "PASS", 
                            "Properly rejected invalid file format with 400 error")
                return True
            else:
                self.log_test("Error Handling - Invalid File", "FAIL", 
                            f"Expected 400 error, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Error Handling - Invalid File", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all rejection reasons workflow tests"""
        print("=" * 80)
        print("REJECTION REASONS POST ENDPOINT WORKFLOW TESTING")
        print("Testing the specific functionality reported as failing with net::ERR_FAILED")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Basic Connectivity
        test_results.append(self.test_backend_connectivity())
        
        # Test 2: GET Endpoint (baseline)
        test_results.append(self.test_get_rejection_reasons_endpoint())
        
        # Test 3: POST Endpoint with FormData (main focus)
        test_results.append(self.test_post_rejection_reasons_with_formdata())
        
        # Test 4: Verify Analysis Storage
        test_results.append(self.test_analysis_storage_verification())
        
        # Test 5: PDF Download Functionality
        test_results.append(self.test_pdf_download_functionality())
        
        # Test 6: Error Handling
        test_results.append(self.test_error_handling_invalid_file())
        
        # Summary
        print("=" * 80)
        print("REJECTION REASONS WORKFLOW TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Rejection reasons POST endpoint is working correctly.")
            print("The net::ERR_FAILED issue has been resolved.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed.")
            if test_results[2] == False:  # POST endpoint test failed
                print("❌ CRITICAL: POST endpoint is still failing - net::ERR_FAILED issue persists")
            else:
                print("✅ POST endpoint is working - other minor issues detected")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = RejectionReasonsWorkflowTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ REJECTION REASONS TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ REJECTION REASONS TESTING COMPLETED WITH ISSUES")
        exit(1)

if __name__ == "__main__":
    main()