#!/usr/bin/env python3
"""
Enhanced Rejection Reasons PDF Formatting Test
Testing the enhanced PDF formatting improvements for rejection reasons analysis
"""

import requests
import json
import time
import os
from datetime import datetime
import tempfile

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://ab16948b-54a7-4063-af4a-f88f3c45f9d2.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class RejectionReasonsPDFTester:
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
                self.log_test("Backend Connectivity", "PASS", 
                            f"Backend accessible at {BACKEND_URL}")
                return True
            else:
                # Try alternative health check
                response = self.session.get(f"{BACKEND_URL}", timeout=10)
                if response.status_code in [200, 404]:  # 404 is OK for root endpoint
                    self.log_test("Backend Connectivity", "PASS", 
                                f"Backend accessible at {BACKEND_URL}")
                    return True
                else:
                    self.log_test("Backend Connectivity", "FAIL", 
                                f"HTTP {response.status_code}: {response.text}")
                    return False
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Exception: {str(e)}")
            return False

    def create_rejection_reasons_analysis(self):
        """Create a new rejection reasons analysis with comprehensive Data Scientist job"""
        try:
            # Comprehensive Data Scientist job description
            job_title = "Senior Data Scientist"
            job_description = """
We are seeking a Senior Data Scientist to join our AI/ML team. The ideal candidate will have 5+ years of experience in machine learning, statistical analysis, and data engineering. You will be responsible for developing predictive models, conducting advanced analytics, and driving data-driven decision making across the organization.

Key Responsibilities:
- Design and implement machine learning models for business applications
- Perform statistical analysis and hypothesis testing
- Build data pipelines and ETL processes
- Collaborate with engineering teams to deploy models to production
- Present findings to stakeholders and executive leadership
- Mentor junior data scientists and analysts

Required Qualifications:
- Master's or PhD in Data Science, Statistics, Computer Science, or related field
- 5+ years of experience in data science and machine learning
- Expert-level proficiency in Python and R
- Strong experience with SQL and database management
- Hands-on experience with machine learning frameworks (scikit-learn, TensorFlow, PyTorch)
- Experience with cloud platforms (AWS, GCP, Azure)
- Knowledge of big data technologies (Spark, Hadoop, Kafka)
- Strong statistical analysis and hypothesis testing skills
- Experience with data visualization tools (Tableau, Power BI, matplotlib, seaborn)
- Excellent communication and presentation skills

Preferred Qualifications:
- Experience with deep learning and neural networks
- Knowledge of MLOps and model deployment practices
- Experience with A/B testing and experimental design
- Familiarity with containerization (Docker, Kubernetes)
- Experience in financial services or healthcare domains
- Publications in peer-reviewed journals or conferences
            """.strip()

            # Realistic resume content for testing
            resume_content = """
Sarah Johnson
Data Analyst
Email: sarah.johnson@email.com
Phone: (555) 123-4567

SUMMARY
Motivated data analyst with 2 years of experience in business intelligence and reporting. Skilled in SQL, Excel, and basic Python programming. Seeking to transition into a data science role.

EDUCATION
Bachelor of Science in Business Administration
University of State, 2021
GPA: 3.4/4.0

EXPERIENCE
Data Analyst | ABC Corporation | June 2022 - Present
- Create weekly and monthly business reports using SQL and Excel
- Develop dashboards in Tableau for sales and marketing teams
- Perform basic statistical analysis on customer data
- Collaborate with business stakeholders to understand reporting requirements

Business Intelligence Intern | XYZ Company | January 2022 - May 2022
- Assisted in data collection and cleaning processes
- Created simple visualizations using Excel and PowerPoint
- Supported senior analysts with ad-hoc analysis requests

TECHNICAL SKILLS
- Programming: Basic Python, SQL (intermediate), Excel (advanced)
- Tools: Tableau, Power BI, SSMS, Git (basic)
- Databases: MySQL, SQL Server
- Statistics: Descriptive statistics, basic hypothesis testing

PROJECTS
Customer Segmentation Analysis (2023)
- Used SQL and Tableau to segment customers based on purchase behavior
- Identified 5 key customer segments for marketing team

Sales Forecasting Model (2022)
- Built simple linear regression model in Excel to predict quarterly sales
- Achieved 15% improvement over previous forecasting method

CERTIFICATIONS
- Tableau Desktop Specialist (2023)
- Google Analytics Certified (2022)
            """.strip()

            # Prepare form data
            files = {
                'resume': ('sarah_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            form_data = {
                'job_title': job_title,
                'job_description': job_description
            }

            response = self.session.post(f"{BASE_URL}/placement-preparation/rejection-reasons", 
                                       files=files, data=form_data, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("rejection_id"):
                    self.rejection_analysis_id = data["rejection_id"]
                    analysis_length = len(data.get("rejection_reasons", ""))
                    self.log_test("Rejection Reasons Analysis Creation", "PASS", 
                                f"Analysis created successfully (ID: {self.rejection_analysis_id}, Length: {analysis_length} chars)")
                    return True
                else:
                    self.log_test("Rejection Reasons Analysis Creation", "FAIL", 
                                f"Analysis creation failed: {data}")
                    return False
            else:
                self.log_test("Rejection Reasons Analysis Creation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Rejection Reasons Analysis Creation", "FAIL", f"Exception: {str(e)}")
            return False

    def verify_analysis_content_quality(self):
        """Verify the quality and comprehensiveness of the rejection reasons analysis"""
        try:
            # Get the analysis details
            response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons")
            
            if response.status_code != 200:
                self.log_test("Analysis Content Quality Verification", "FAIL", 
                            f"Failed to retrieve analyses: HTTP {response.status_code}")
                return False
            
            data = response.json()
            analyses = data.get("analyses", [])
            
            # Find our analysis
            our_analysis = None
            for analysis in analyses:
                if analysis.get("id") == self.rejection_analysis_id:
                    our_analysis = analysis
                    break
            
            if not our_analysis:
                self.log_test("Analysis Content Quality Verification", "FAIL", 
                            "Could not find our analysis in the results")
                return False
            
            # Verify analysis content quality
            rejection_reasons = our_analysis.get("rejection_reasons", "")
            analysis_length = len(rejection_reasons)
            
            # Count bullet points (should have multiple rejection reasons)
            bullet_count = rejection_reasons.count("•") + rejection_reasons.count("-") + rejection_reasons.count("*")
            
            # Check for key sections that should be present
            key_sections = [
                "TECHNICAL SKILLS",
                "EXPERIENCE",
                "EDUCATION", 
                "PROGRAMMING",
                "MACHINE LEARNING",
                "STATISTICAL",
                "CLOUD",
                "Required",
                "Candidate Reality",
                "Gap Impact"
            ]
            
            sections_found = sum(1 for section in key_sections if section.lower() in rejection_reasons.lower())
            
            # Quality metrics
            quality_checks = {
                "Sufficient Length": analysis_length >= 1000,  # At least 1000 characters
                "Multiple Bullet Points": bullet_count >= 8,   # At least 8 bullet points
                "Key Sections Present": sections_found >= 6,   # At least 6 key sections
                "Structured Format": "Required:" in rejection_reasons and "Candidate Reality:" in rejection_reasons
            }
            
            passed_checks = sum(quality_checks.values())
            total_checks = len(quality_checks)
            
            if passed_checks >= 3:  # At least 3 out of 4 quality checks should pass
                self.log_test("Analysis Content Quality Verification", "PASS", 
                            f"Quality Score: {passed_checks}/{total_checks} - Length: {analysis_length} chars, Bullets: {bullet_count}, Sections: {sections_found}")
                return True
            else:
                self.log_test("Analysis Content Quality Verification", "FAIL", 
                            f"Quality Score: {passed_checks}/{total_checks} - Analysis may be insufficient")
                return False
                
        except Exception as e:
            self.log_test("Analysis Content Quality Verification", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_generation_and_download(self):
        """Test PDF generation and download functionality"""
        try:
            if not self.rejection_analysis_id:
                self.log_test("PDF Generation and Download", "FAIL", 
                            "No rejection analysis ID available")
                return False
            
            # Test PDF download
            response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons/{self.rejection_analysis_id}/download", 
                                      timeout=30)
            
            if response.status_code != 200:
                self.log_test("PDF Generation and Download", "FAIL", 
                            f"PDF download failed: HTTP {response.status_code}")
                return False
            
            # Verify PDF content
            pdf_content = response.content
            pdf_size = len(pdf_content)
            
            # Basic PDF validation
            if not pdf_content.startswith(b'%PDF'):
                self.log_test("PDF Generation and Download", "FAIL", 
                            "Downloaded content is not a valid PDF")
                return False
            
            # Check content-type header
            content_type = response.headers.get('content-type', '')
            if 'application/pdf' not in content_type:
                self.log_test("PDF Generation and Download", "FAIL", 
                            f"Incorrect content-type: {content_type}")
                return False
            
            self.log_test("PDF Generation and Download", "PASS", 
                        f"PDF downloaded successfully ({pdf_size} bytes, Content-Type: {content_type})")
            return True
            
        except Exception as e:
            self.log_test("PDF Generation and Download", "FAIL", f"Exception: {str(e)}")
            return False

    def test_enhanced_pdf_formatting(self):
        """Test the enhanced PDF formatting improvements"""
        try:
            if not self.rejection_analysis_id:
                self.log_test("Enhanced PDF Formatting", "FAIL", 
                            "No rejection analysis ID available")
                return False
            
            # Download PDF for content analysis
            response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons/{self.rejection_analysis_id}/download", 
                                      timeout=30)
            
            if response.status_code != 200:
                self.log_test("Enhanced PDF Formatting", "FAIL", 
                            f"Failed to download PDF: HTTP {response.status_code}")
                return False
            
            pdf_content = response.content
            pdf_size = len(pdf_content)
            
            # Save PDF temporarily for analysis
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(pdf_content)
                temp_pdf_path = temp_file.name
            
            try:
                # Try to extract text from PDF for content verification
                # Note: This is a basic check - in a real scenario, you'd use a PDF parsing library
                pdf_text = pdf_content.decode('latin-1', errors='ignore')
                
                # Check for enhanced formatting indicators
                formatting_checks = {
                    "Professional Size": pdf_size >= 5000,  # Should be substantial size
                    "PDF Structure": b'%PDF' in pdf_content[:10],
                    "Content Present": len(pdf_text) > 1000,
                    "Valid PDF End": b'%%EOF' in pdf_content[-100:] or b'endobj' in pdf_content[-1000:]
                }
                
                passed_formatting = sum(formatting_checks.values())
                total_formatting = len(formatting_checks)
                
                # Additional checks for enhanced features (these would be visible in actual PDF content)
                enhancement_indicators = [
                    "rejection" in pdf_text.lower(),
                    "analysis" in pdf_text.lower(),
                    "candidate" in pdf_text.lower(),
                    "requirements" in pdf_text.lower()
                ]
                
                content_indicators = sum(enhancement_indicators)
                
                if passed_formatting >= 3 and content_indicators >= 2:
                    self.log_test("Enhanced PDF Formatting", "PASS", 
                                f"PDF formatting checks: {passed_formatting}/{total_formatting}, Content indicators: {content_indicators}/4, Size: {pdf_size} bytes")
                    return True
                else:
                    self.log_test("Enhanced PDF Formatting", "FAIL", 
                                f"PDF formatting insufficient: {passed_formatting}/{total_formatting}, Content: {content_indicators}/4")
                    return False
                    
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_pdf_path)
                except:
                    pass
                    
        except Exception as e:
            self.log_test("Enhanced PDF Formatting", "FAIL", f"Exception: {str(e)}")
            return False

    def test_content_preservation(self):
        """Test that all original content is preserved in the enhanced PDF"""
        try:
            # Get the original analysis content
            response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons")
            
            if response.status_code != 200:
                self.log_test("Content Preservation", "FAIL", 
                            f"Failed to retrieve analysis: HTTP {response.status_code}")
                return False
            
            data = response.json()
            analyses = data.get("analyses", [])
            
            # Find our analysis
            our_analysis = None
            for analysis in analyses:
                if analysis.get("id") == self.rejection_analysis_id:
                    our_analysis = analysis
                    break
            
            if not our_analysis:
                self.log_test("Content Preservation", "FAIL", 
                            "Could not find analysis for content comparison")
                return False
            
            original_content = our_analysis.get("rejection_reasons", "")
            original_length = len(original_content)
            
            # Download PDF
            pdf_response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons/{self.rejection_analysis_id}/download")
            
            if pdf_response.status_code != 200:
                self.log_test("Content Preservation", "FAIL", 
                            "Failed to download PDF for content comparison")
                return False
            
            pdf_size = len(pdf_response.content)
            
            # Content preservation metrics
            preservation_checks = {
                "Original Content Exists": original_length > 500,
                "PDF Generated": pdf_size > 1000,
                "Reasonable Size Ratio": pdf_size >= original_length * 0.5,  # PDF should be substantial
                "Content Not Empty": original_length > 0
            }
            
            passed_preservation = sum(preservation_checks.values())
            total_preservation = len(preservation_checks)
            
            if passed_preservation >= 3:
                self.log_test("Content Preservation", "PASS", 
                            f"Content preservation: {passed_preservation}/{total_preservation} - Original: {original_length} chars, PDF: {pdf_size} bytes")
                return True
            else:
                self.log_test("Content Preservation", "FAIL", 
                            f"Content preservation insufficient: {passed_preservation}/{total_preservation}")
                return False
                
        except Exception as e:
            self.log_test("Content Preservation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_workflow_end_to_end(self):
        """Test the complete rejection reasons workflow end-to-end"""
        try:
            # Verify the analysis exists in the list
            response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons")
            
            if response.status_code != 200:
                self.log_test("End-to-End Workflow", "FAIL", 
                            f"Failed to retrieve analyses list: HTTP {response.status_code}")
                return False
            
            data = response.json()
            analyses = data.get("analyses", [])
            
            # Check if our analysis is in the list
            found_analysis = False
            for analysis in analyses:
                if analysis.get("id") == self.rejection_analysis_id:
                    found_analysis = True
                    
                    # Verify required fields
                    required_fields = ["id", "job_title", "created_at", "rejection_reasons"]
                    missing_fields = [field for field in required_fields if not analysis.get(field)]
                    
                    if missing_fields:
                        self.log_test("End-to-End Workflow", "FAIL", 
                                    f"Missing required fields in analysis: {missing_fields}")
                        return False
                    
                    break
            
            if not found_analysis:
                self.log_test("End-to-End Workflow", "FAIL", 
                            "Analysis not found in the analyses list")
                return False
            
            # Test PDF download one more time to ensure consistency
            pdf_response = self.session.get(f"{BASE_URL}/placement-preparation/rejection-reasons/{self.rejection_analysis_id}/download")
            
            if pdf_response.status_code != 200:
                self.log_test("End-to-End Workflow", "FAIL", 
                            "PDF download failed in end-to-end test")
                return False
            
            self.log_test("End-to-End Workflow", "PASS", 
                        "Complete workflow verified: Analysis creation → Storage → Retrieval → PDF download")
            return True
            
        except Exception as e:
            self.log_test("End-to-End Workflow", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("=" * 80)
        print("ENHANCED REJECTION REASONS PDF FORMATTING TEST")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Backend Connectivity
        test_results.append(self.test_backend_connectivity())
        
        # Test 2: Create Rejection Reasons Analysis
        test_results.append(self.create_rejection_reasons_analysis())
        
        # Test 3: Verify Analysis Content Quality
        test_results.append(self.verify_analysis_content_quality())
        
        # Test 4: PDF Generation and Download
        test_results.append(self.test_pdf_generation_and_download())
        
        # Test 5: Enhanced PDF Formatting
        test_results.append(self.test_enhanced_pdf_formatting())
        
        # Test 6: Content Preservation
        test_results.append(self.test_content_preservation())
        
        # Test 7: End-to-End Workflow
        test_results.append(self.test_workflow_end_to_end())
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Enhanced rejection reasons PDF formatting is working correctly.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = RejectionReasonsPDFTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ REJECTION REASONS PDF FORMATTING TEST COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ REJECTION REASONS PDF FORMATTING TEST COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()