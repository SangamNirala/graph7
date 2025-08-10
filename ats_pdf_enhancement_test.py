#!/usr/bin/env python3
"""
ATS PDF Generation Enhancement Testing
Testing the updated ATS score calculation and PDF generation with new sections:
- Score Breakdown table
- How the Score was Calculated section  
- Improvement Roadmap by Category section
"""

import requests
import json
import time
import os
import io
from datetime import datetime
import PyPDF2

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://350119d5-292b-44b0-a739-5efd46504bc2.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class ATSPDFEnhancementTester:
    def __init__(self):
        self.session = requests.Session()
        self.ats_id = None
        self.pdf_content = None
        self.pdf_text = ""
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()

    def test_ats_score_calculation(self):
        """Test ATS score calculation with sample data"""
        try:
            # Create sample resume content
            resume_content = """
            Sarah Johnson
            Senior Backend Engineer
            Email: sarah.johnson@email.com
            Phone: (555) 123-4567
            
            PROFESSIONAL SUMMARY:
            Experienced Senior Backend Engineer with 7+ years of expertise in Python, FastAPI, and distributed systems.
            Proven track record of leading teams and delivering scalable solutions for high-traffic applications.
            
            TECHNICAL SKILLS:
            • Programming Languages: Python, JavaScript, Go, SQL
            • Frameworks: FastAPI, Django, Flask, React
            • Databases: PostgreSQL, MongoDB, Redis
            • Cloud Platforms: AWS (EC2, RDS, Lambda, S3), Docker, Kubernetes
            • Tools: Git, Jenkins, Prometheus, Grafana
            
            PROFESSIONAL EXPERIENCE:
            
            Senior Backend Engineer | TechCorp Inc. | 2020 - Present
            • Led a team of 5 engineers in developing microservices architecture serving 2M+ users
            • Implemented FastAPI-based REST APIs with 99.9% uptime and sub-100ms response times
            • Reduced database query time by 40% through optimization and caching strategies
            • Mentored junior developers and conducted code reviews for quality assurance
            
            Backend Engineer | StartupXYZ | 2018 - 2020
            • Developed Python-based web applications using Django and PostgreSQL
            • Implemented automated testing pipelines reducing deployment time by 60%
            • Collaborated with frontend team to deliver full-stack solutions
            • Participated in on-call rotation and incident response procedures
            
            Software Developer | DevSolutions | 2017 - 2018
            • Built RESTful APIs and integrated third-party services
            • Worked with MongoDB and implemented data migration scripts
            • Contributed to open-source projects and internal tooling
            
            EDUCATION:
            Bachelor of Science in Computer Science | University of Technology | 2017
            • Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Engineering
            
            CERTIFICATIONS:
            • AWS Certified Solutions Architect - Associate (2021)
            • MongoDB Certified Developer (2019)
            
            ACHIEVEMENTS:
            • Increased system performance by 45% through architectural improvements
            • Led successful migration of legacy system to microservices, reducing costs by $200K annually
            • Published technical blog posts with 10K+ views on backend best practices
            """
            
            # Sample job description
            job_description = """
            We are seeking a Senior Backend Engineer to join our growing engineering team. The ideal candidate will have:
            
            REQUIRED QUALIFICATIONS:
            • 5+ years of experience in backend development
            • Strong proficiency in Python and modern frameworks (FastAPI, Django)
            • Experience with relational and NoSQL databases (PostgreSQL, MongoDB)
            • Knowledge of cloud platforms, preferably AWS
            • Experience with containerization (Docker) and orchestration (Kubernetes)
            • Understanding of microservices architecture and distributed systems
            • Experience with API design and development
            • Strong problem-solving skills and attention to detail
            
            PREFERRED QUALIFICATIONS:
            • Team leadership experience
            • Experience with monitoring and observability tools
            • Knowledge of DevOps practices and CI/CD pipelines
            • Open source contributions
            • Experience with high-traffic, scalable applications
            
            RESPONSIBILITIES:
            • Design and implement scalable backend services and APIs
            • Lead technical discussions and architectural decisions
            • Mentor junior team members and conduct code reviews
            • Collaborate with cross-functional teams to deliver features
            • Participate in on-call rotation and system maintenance
            • Optimize application performance and reliability
            """
            
            # Prepare the request as form data with file upload
            files = {
                'resume': ('sample_resume.txt', resume_content.strip().encode('utf-8'), 'text/plain')
            }
            
            form_data = {
                'job_title': "Senior Backend Engineer",
                'job_description': job_description.strip()
            }
            
            # Make the API call
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=form_data)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["ats_id", "ats_score", "analysis_text", "pdf_filename"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("ATS Score Calculation", "FAIL", 
                                f"Missing required fields: {missing_fields}")
                    return False
                
                self.ats_id = data["ats_id"]
                ats_score = data["ats_score"]
                analysis_text = data["analysis_text"]
                pdf_filename = data["pdf_filename"]
                
                # Verify data quality
                if not isinstance(ats_score, (int, float)) or ats_score < 0 or ats_score > 100:
                    self.log_test("ATS Score Calculation", "FAIL", 
                                f"Invalid ATS score: {ats_score}")
                    return False
                
                if len(analysis_text) < 500:
                    self.log_test("ATS Score Calculation", "FAIL", 
                                f"Analysis text too short: {len(analysis_text)} characters")
                    return False
                
                self.log_test("ATS Score Calculation", "PASS", 
                            f"ATS ID: {self.ats_id}, Score: {ats_score}/100, Analysis: {len(analysis_text)} chars, PDF: {pdf_filename}")
                return True
                
            else:
                self.log_test("ATS Score Calculation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("ATS Score Calculation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_download(self):
        """Test PDF download functionality"""
        try:
            if not self.ats_id:
                self.log_test("PDF Download", "FAIL", "No ATS ID available")
                return False
            
            # Download the PDF
            response = self.session.get(f"{BASE_URL}/placement-preparation/ats-score/{self.ats_id}/download")
            
            if response.status_code == 200:
                # Verify content type
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' not in content_type:
                    self.log_test("PDF Download", "FAIL", 
                                f"Invalid content type: {content_type}")
                    return False
                
                # Store PDF content for analysis
                self.pdf_content = response.content
                pdf_size = len(self.pdf_content)
                
                # Verify PDF is not empty and has reasonable size
                if pdf_size < 1000:  # Less than 1KB is suspicious
                    self.log_test("PDF Download", "FAIL", 
                                f"PDF too small: {pdf_size} bytes")
                    return False
                
                self.log_test("PDF Download", "PASS", 
                            f"PDF downloaded successfully: {pdf_size} bytes, Content-Type: {content_type}")
                return True
                
            else:
                self.log_test("PDF Download", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("PDF Download", "FAIL", f"Exception: {str(e)}")
            return False

    def extract_pdf_text(self):
        """Extract text from PDF for content analysis"""
        try:
            if not self.pdf_content:
                self.log_test("PDF Text Extraction", "FAIL", "No PDF content available")
                return False
            
            # Extract text using PyPDF2
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(self.pdf_content))
            text_content = ""
            
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            
            self.pdf_text = text_content.strip()
            
            if len(self.pdf_text) < 100:
                self.log_test("PDF Text Extraction", "FAIL", 
                            f"Extracted text too short: {len(self.pdf_text)} characters")
                return False
            
            self.log_test("PDF Text Extraction", "PASS", 
                        f"Extracted {len(self.pdf_text)} characters from PDF")
            return True
            
        except Exception as e:
            self.log_test("PDF Text Extraction", "FAIL", f"Exception: {str(e)}")
            return False

    def test_score_breakdown_section(self):
        """Test for Score Breakdown table with 4 columns"""
        try:
            if not self.pdf_text:
                self.log_test("Score Breakdown Section", "FAIL", "No PDF text available")
                return False
            
            # Look for Score Breakdown section
            score_breakdown_indicators = [
                "📈 SCORE BREAKDOWN",
                "SCORE BREAKDOWN",
                "Category",
                "Score",
                "Percentage", 
                "Weight"
            ]
            
            found_indicators = []
            for indicator in score_breakdown_indicators:
                if indicator in self.pdf_text:
                    found_indicators.append(indicator)
            
            # Check if we have the main section header and column headers
            has_section = any("SCORE BREAKDOWN" in indicator for indicator in found_indicators)
            has_columns = all(col in found_indicators for col in ["Category", "Score", "Percentage", "Weight"])
            
            if has_section and has_columns:
                self.log_test("Score Breakdown Section", "PASS", 
                            f"Found Score Breakdown section with 4 columns: {found_indicators}")
                return True
            elif has_section:
                self.log_test("Score Breakdown Section", "FAIL", 
                            f"Found section but missing columns. Found: {found_indicators}")
                return False
            else:
                self.log_test("Score Breakdown Section", "FAIL", 
                            f"Score Breakdown section not found. Available indicators: {found_indicators}")
                return False
                
        except Exception as e:
            self.log_test("Score Breakdown Section", "FAIL", f"Exception: {str(e)}")
            return False

    def test_score_calculation_section(self):
        """Test for How the Score was Calculated section"""
        try:
            if not self.pdf_text:
                self.log_test("Score Calculation Section", "FAIL", "No PDF text available")
                return False
            
            # Look for Score Calculation section
            calculation_indicators = [
                "🧮 HOW THE SCORE WAS CALCULATED",
                "HOW THE SCORE WAS CALCULATED",
                "per-category",
                "explanation",
                "analysis"
            ]
            
            found_indicators = []
            for indicator in calculation_indicators:
                if indicator in self.pdf_text:
                    found_indicators.append(indicator)
            
            # Check if we have the main section
            has_section = any("HOW THE SCORE WAS CALCULATED" in indicator for indicator in found_indicators)
            
            if has_section:
                # Look for per-category explanations
                category_explanations = 0
                categories = ["Technical Skills", "Experience", "Education", "Keywords", "Format"]
                
                for category in categories:
                    if category.lower() in self.pdf_text.lower():
                        category_explanations += 1
                
                if category_explanations >= 2:  # At least 2 categories explained
                    self.log_test("Score Calculation Section", "PASS", 
                                f"Found calculation section with {category_explanations} category explanations")
                    return True
                else:
                    self.log_test("Score Calculation Section", "FAIL", 
                                f"Found section but insufficient category explanations: {category_explanations}")
                    return False
            else:
                self.log_test("Score Calculation Section", "FAIL", 
                            f"Score calculation section not found. Available: {found_indicators}")
                return False
                
        except Exception as e:
            self.log_test("Score Calculation Section", "FAIL", f"Exception: {str(e)}")
            return False

    def test_improvement_roadmap_section(self):
        """Test for Improvement Roadmap by Category section"""
        try:
            if not self.pdf_text:
                self.log_test("Improvement Roadmap Section", "FAIL", "No PDF text available")
                return False
            
            # Look for Improvement Roadmap section
            roadmap_indicators = [
                "🚀 IMPROVEMENT ROADMAP BY CATEGORY",
                "IMPROVEMENT ROADMAP BY CATEGORY",
                "IMPROVEMENT ROADMAP",
                "deficiencies",
                "improvements",
                "Priority"
            ]
            
            found_indicators = []
            for indicator in roadmap_indicators:
                if indicator in self.pdf_text:
                    found_indicators.append(indicator)
            
            # Check if we have the main section
            has_section = any("IMPROVEMENT ROADMAP" in indicator for indicator in found_indicators)
            
            if has_section:
                # Look for improvement elements
                improvement_elements = 0
                
                # Check for potential gains (+X format)
                if "+" in self.pdf_text and any(char.isdigit() for char in self.pdf_text):
                    improvement_elements += 1
                
                # Check for priority mentions
                if "Priority" in found_indicators or "priority" in self.pdf_text.lower():
                    improvement_elements += 1
                
                # Check for deficiencies/improvements
                if "deficiencies" in found_indicators or "improvements" in found_indicators:
                    improvement_elements += 1
                
                if improvement_elements >= 2:
                    self.log_test("Improvement Roadmap Section", "PASS", 
                                f"Found roadmap section with {improvement_elements} improvement elements")
                    return True
                else:
                    self.log_test("Improvement Roadmap Section", "FAIL", 
                                f"Found section but insufficient improvement elements: {improvement_elements}")
                    return False
            else:
                self.log_test("Improvement Roadmap Section", "FAIL", 
                            f"Improvement roadmap section not found. Available: {found_indicators}")
                return False
                
        except Exception as e:
            self.log_test("Improvement Roadmap Section", "FAIL", f"Exception: {str(e)}")
            return False

    def test_backward_compatibility(self):
        """Test backward compatibility with legacy headers"""
        try:
            if not self.pdf_text:
                self.log_test("Backward Compatibility", "FAIL", "No PDF text available")
                return False
            
            # Check that PDF displays content without errors regardless of header format
            # The PDF should contain meaningful content even if using legacy headers
            
            # Look for essential content that should always be present
            essential_content = [
                "ATS",  # Should mention ATS somewhere
                "Score", # Should have score information
                "Resume", # Should reference resume
                "Analysis" # Should have analysis content
            ]
            
            found_content = []
            for content in essential_content:
                if content.lower() in self.pdf_text.lower():
                    found_content.append(content)
            
            # Check for reasonable content length (indicates proper parsing)
            content_length = len(self.pdf_text)
            has_sufficient_content = content_length > 500
            
            if len(found_content) >= 3 and has_sufficient_content:
                self.log_test("Backward Compatibility", "PASS", 
                            f"PDF displays content properly: {found_content}, Length: {content_length} chars")
                return True
            else:
                self.log_test("Backward Compatibility", "FAIL", 
                            f"Insufficient content or parsing issues. Found: {found_content}, Length: {content_length}")
                return False
                
        except Exception as e:
            self.log_test("Backward Compatibility", "FAIL", f"Exception: {str(e)}")
            return False

    def extract_pdf_snippets(self):
        """Extract and display snippets from the PDF showing new sections"""
        try:
            if not self.pdf_text:
                self.log_test("PDF Snippets Extraction", "FAIL", "No PDF text available")
                return False
            
            print("\n" + "="*60)
            print("PDF CONTENT SNIPPETS - NEW SECTIONS")
            print("="*60)
            
            # Extract Score Breakdown section
            if "SCORE BREAKDOWN" in self.pdf_text:
                start_idx = self.pdf_text.find("SCORE BREAKDOWN")
                end_idx = self.pdf_text.find("\n\n", start_idx + 100)  # Find next double newline
                if end_idx == -1:
                    end_idx = start_idx + 300  # Fallback to 300 chars
                
                score_breakdown_snippet = self.pdf_text[start_idx:end_idx]
                print("\n📈 SCORE BREAKDOWN SECTION:")
                print("-" * 40)
                print(score_breakdown_snippet[:400] + "..." if len(score_breakdown_snippet) > 400 else score_breakdown_snippet)
            
            # Extract Score Calculation section
            if "HOW THE SCORE WAS CALCULATED" in self.pdf_text:
                start_idx = self.pdf_text.find("HOW THE SCORE WAS CALCULATED")
                end_idx = self.pdf_text.find("\n\n", start_idx + 100)
                if end_idx == -1:
                    end_idx = start_idx + 400
                
                calculation_snippet = self.pdf_text[start_idx:end_idx]
                print("\n🧮 HOW THE SCORE WAS CALCULATED SECTION:")
                print("-" * 40)
                print(calculation_snippet[:400] + "..." if len(calculation_snippet) > 400 else calculation_snippet)
            
            # Extract Improvement Roadmap section
            if "IMPROVEMENT ROADMAP" in self.pdf_text:
                start_idx = self.pdf_text.find("IMPROVEMENT ROADMAP")
                end_idx = self.pdf_text.find("\n\n", start_idx + 100)
                if end_idx == -1:
                    end_idx = start_idx + 400
                
                roadmap_snippet = self.pdf_text[start_idx:end_idx]
                print("\n🚀 IMPROVEMENT ROADMAP SECTION:")
                print("-" * 40)
                print(roadmap_snippet[:400] + "..." if len(roadmap_snippet) > 400 else roadmap_snippet)
            
            print("\n" + "="*60)
            
            self.log_test("PDF Snippets Extraction", "PASS", "Successfully extracted PDF content snippets")
            return True
            
        except Exception as e:
            self.log_test("PDF Snippets Extraction", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all ATS PDF enhancement tests"""
        print("=" * 80)
        print("ATS PDF GENERATION ENHANCEMENT TESTING")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: ATS Score Calculation
        test_results.append(self.test_ats_score_calculation())
        
        # Test 2: PDF Download
        test_results.append(self.test_pdf_download())
        
        # Test 3: PDF Text Extraction
        test_results.append(self.extract_pdf_text())
        
        # Test 4: New PDF Sections
        test_results.append(self.test_score_breakdown_section())
        test_results.append(self.test_score_calculation_section())
        test_results.append(self.test_improvement_roadmap_section())
        
        # Test 5: Backward Compatibility
        test_results.append(self.test_backward_compatibility())
        
        # Test 6: Extract PDF Snippets (always runs for documentation)
        self.extract_pdf_snippets()
        
        # Summary
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! ATS PDF generation enhancements are working correctly.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = ATSPDFEnhancementTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ ATS PDF ENHANCEMENT TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ ATS PDF ENHANCEMENT TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()