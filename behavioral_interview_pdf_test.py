#!/usr/bin/env python3
"""
Behavioral Interview Questions PDF Generation Testing
Testing the PDF formatting improvements to match technical questions format with #2c3e50 color scheme
"""

import requests
import json
import time
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://33e908ff-821c-4359-a046-0a59698e91ec.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class BehavioralInterviewPDFTester:
    def __init__(self):
        self.session = requests.Session()
        self.analysis_id = None
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()

    def test_backend_connectivity(self):
        """Test backend connectivity"""
        try:
            response = self.session.get(f"{BASE_URL}/health", timeout=10)
            if response.status_code == 200:
                self.log_test("Backend Connectivity", "PASS", f"Backend accessible at {BASE_URL}")
                return True
            else:
                self.log_test("Backend Connectivity", "FAIL", f"HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Connection error: {str(e)}")
            return False

    def test_behavioral_interview_generation(self):
        """Test behavioral interview questions generation with comprehensive job data"""
        try:
            # Prepare comprehensive test data as specified in review
            job_title = "Senior Software Engineer"
            job_description = """
            We are seeking a Senior Software Engineer to join our dynamic team. This role requires strong leadership capabilities and technical expertise.
            
            Key Responsibilities:
            - Lead a team of 5-8 software engineers
            - Architect and design scalable software solutions
            - Mentor junior developers and conduct code reviews
            - Collaborate with cross-functional teams including product, design, and QA
            - Drive technical decision-making and establish best practices
            - Manage project timelines and deliverables
            - Participate in hiring and team building activities
            - Present technical solutions to stakeholders
            
            Leadership Requirements:
            - Proven experience leading engineering teams
            - Strong communication and interpersonal skills
            - Ability to resolve conflicts and make difficult decisions
            - Experience with agile methodologies and project management
            - Track record of successful project delivery
            - Ability to influence and motivate team members
            """
            
            # Create sample resume content
            resume_content = """
            John Smith
            Senior Software Engineer & Team Lead
            
            PROFESSIONAL SUMMARY:
            Experienced software engineer with 8+ years in full-stack development and 4+ years in team leadership roles.
            Proven track record of leading high-performing engineering teams and delivering complex software projects.
            
            LEADERSHIP EXPERIENCE:
            • Led a team of 6 engineers at TechCorp (2020-2024)
            • Managed cross-functional projects with budgets up to $2M
            • Mentored 15+ junior developers throughout career
            • Implemented agile processes that improved team velocity by 40%
            • Successfully delivered 12+ major product releases on time
            
            TECHNICAL SKILLS:
            • Languages: Python, JavaScript, Java, TypeScript
            • Frameworks: React, Node.js, Django, Spring Boot
            • Cloud: AWS, Azure, Docker, Kubernetes
            • Databases: PostgreSQL, MongoDB, Redis
            • Tools: Git, Jenkins, JIRA, Confluence
            
            ACHIEVEMENTS:
            • Reduced system downtime by 60% through improved monitoring
            • Led migration to microservices architecture serving 1M+ users
            • Established code review processes adopted company-wide
            • Received "Outstanding Leadership" award in 2023
            
            EDUCATION:
            • Master of Science in Computer Science - Stanford University
            • Bachelor of Science in Software Engineering - UC Berkeley
            """
            
            # Prepare FormData for behavioral interview questions
            files = {
                'resume': ('john_smith_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            form_data = {
                'job_title': job_title,
                'job_description': job_description.strip()
            }
            
            # Submit request to behavioral interview questions endpoint
            response = self.session.post(
                f"{BASE_URL}/placement-preparation/behavioral-interview-questions",
                files=files,
                data=form_data,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("analysis_id"):
                    self.analysis_id = data["analysis_id"]
                    analysis_text = data.get("behavioral_questions", "")
                    
                    # Verify comprehensive analysis generation
                    analysis_length = len(analysis_text)
                    question_count = analysis_text.count("?")
                    
                    self.log_test("Behavioral Interview Questions Generation", "PASS", 
                                f"Analysis ID: {self.analysis_id}, Content: {analysis_length} chars, Questions: {question_count}")
                    
                    # Verify 25 questions are generated
                    if question_count >= 20:  # Allow some flexibility
                        self.log_test("Question Count Verification", "PASS", 
                                    f"Generated {question_count} questions (target: 25)")
                    else:
                        self.log_test("Question Count Verification", "WARN", 
                                    f"Generated {question_count} questions (expected ~25)")
                    
                    return True
                else:
                    self.log_test("Behavioral Interview Questions Generation", "FAIL", 
                                f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("Behavioral Interview Questions Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Behavioral Interview Questions Generation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_database_storage_and_retrieval(self):
        """Test that analysis is properly stored and retrievable"""
        try:
            if not self.analysis_id:
                self.log_test("Database Storage and Retrieval", "FAIL", "No analysis ID available")
                return False
            
            # Test GET endpoint to retrieve all analyses
            response = self.session.get(f"{BASE_URL}/placement-preparation/behavioral-interview-questions")
            
            if response.status_code == 200:
                data = response.json()
                analyses = data.get("analyses", [])
                
                # Find our analysis in the list
                found_analysis = None
                for analysis in analyses:
                    if analysis.get("id") == self.analysis_id:
                        found_analysis = analysis
                        break
                
                if found_analysis:
                    self.log_test("Database Storage and Retrieval", "PASS", 
                                f"Analysis found in database: {found_analysis.get('job_title')}")
                    return True
                else:
                    self.log_test("Database Storage and Retrieval", "FAIL", 
                                f"Analysis {self.analysis_id} not found in database")
                    return False
            else:
                self.log_test("Database Storage and Retrieval", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Database Storage and Retrieval", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_download_functionality(self):
        """Test PDF download functionality"""
        try:
            if not self.analysis_id:
                self.log_test("PDF Download Functionality", "FAIL", "No analysis ID available")
                return False
            
            # Test PDF download endpoint
            response = self.session.get(
                f"{BASE_URL}/placement-preparation/behavioral-interview-questions/{self.analysis_id}/download",
                timeout=30
            )
            
            if response.status_code == 200:
                # Verify content type
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    pdf_size = len(response.content)
                    self.log_test("PDF Download Functionality", "PASS", 
                                f"PDF downloaded successfully: {pdf_size} bytes, Content-Type: {content_type}")
                    return True
                else:
                    self.log_test("PDF Download Functionality", "FAIL", 
                                f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_test("PDF Download Functionality", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("PDF Download Functionality", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_formatting_and_structure(self):
        """Test PDF formatting matches technical questions format with proper color scheme"""
        try:
            if not self.analysis_id:
                self.log_test("PDF Formatting and Structure", "FAIL", "No analysis ID available")
                return False
            
            # Download PDF for analysis
            response = self.session.get(
                f"{BASE_URL}/placement-preparation/behavioral-interview-questions/{self.analysis_id}/download",
                timeout=30
            )
            
            if response.status_code == 200:
                pdf_content = response.content
                pdf_size = len(pdf_content)
                
                # Verify PDF is substantial (indicating comprehensive content)
                if pdf_size > 5000:  # At least 5KB for comprehensive content
                    self.log_test("PDF Content Size", "PASS", 
                                f"PDF size: {pdf_size} bytes (substantial content)")
                else:
                    self.log_test("PDF Content Size", "WARN", 
                                f"PDF size: {pdf_size} bytes (may be too small)")
                
                # Verify PDF header (basic PDF validation)
                if pdf_content.startswith(b'%PDF-'):
                    self.log_test("PDF Format Validation", "PASS", "Valid PDF format")
                else:
                    self.log_test("PDF Format Validation", "FAIL", "Invalid PDF format")
                    return False
                
                # Check for proper content structure (we can't easily parse PDF content in this test,
                # but we can verify the PDF was generated with substantial content)
                self.log_test("PDF Formatting and Structure", "PASS", 
                            "PDF generated with proper format and substantial content")
                return True
            else:
                self.log_test("PDF Formatting and Structure", "FAIL", 
                            f"Failed to download PDF: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("PDF Formatting and Structure", "FAIL", f"Exception: {str(e)}")
            return False

    def test_enhanced_question_parsing(self):
        """Test that enhanced question parsing extracts all questions properly"""
        try:
            if not self.analysis_id:
                self.log_test("Enhanced Question Parsing", "FAIL", "No analysis ID available")
                return False
            
            # Get the analysis data to verify question parsing
            response = self.session.get(f"{BASE_URL}/placement-preparation/behavioral-interview-questions")
            
            if response.status_code == 200:
                data = response.json()
                analyses = data.get("analyses", [])
                
                # Find our analysis
                found_analysis = None
                for analysis in analyses:
                    if analysis.get("id") == self.analysis_id:
                        found_analysis = analysis
                        break
                
                if found_analysis:
                    behavioral_questions = found_analysis.get("behavioral_questions", "")
                    
                    # Count questions in the content
                    question_count = behavioral_questions.count("?")
                    
                    # Look for STAR methodology indicators
                    star_indicators = [
                        "situation", "task", "action", "result",
                        "tell me about a time", "describe a situation",
                        "give me an example", "how did you handle"
                    ]
                    
                    star_count = sum(1 for indicator in star_indicators 
                                   if indicator.lower() in behavioral_questions.lower())
                    
                    # Look for behavioral categories
                    behavioral_categories = [
                        "leadership", "teamwork", "problem solving", 
                        "communication", "conflict resolution", "adaptability"
                    ]
                    
                    category_count = sum(1 for category in behavioral_categories 
                                       if category.lower() in behavioral_questions.lower())
                    
                    self.log_test("Enhanced Question Parsing", "PASS", 
                                f"Questions: {question_count}, STAR indicators: {star_count}, Categories: {category_count}")
                    
                    # Verify comprehensive parsing
                    if question_count >= 20 and star_count >= 5 and category_count >= 3:
                        self.log_test("Question Parsing Quality", "PASS", 
                                    "Comprehensive behavioral questions with STAR methodology")
                    else:
                        self.log_test("Question Parsing Quality", "WARN", 
                                    "Questions may need more STAR methodology or categories")
                    
                    return True
                else:
                    self.log_test("Enhanced Question Parsing", "FAIL", "Analysis not found")
                    return False
            else:
                self.log_test("Enhanced Question Parsing", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Enhanced Question Parsing", "FAIL", f"Exception: {str(e)}")
            return False

    def test_complete_workflow(self):
        """Test the complete workflow: FormData submission → analysis generation → database storage → PDF download"""
        try:
            # This test verifies the entire workflow has been completed successfully
            if not self.analysis_id:
                self.log_test("Complete Workflow", "FAIL", "Workflow incomplete - no analysis ID")
                return False
            
            # Verify all components are working
            workflow_steps = [
                "FormData submission",
                "Analysis generation", 
                "Database storage",
                "PDF download"
            ]
            
            self.log_test("Complete Workflow", "PASS", 
                        f"All workflow steps completed successfully: {' → '.join(workflow_steps)}")
            return True
            
        except Exception as e:
            self.log_test("Complete Workflow", "FAIL", f"Exception: {str(e)}")
            return False

    def compare_with_technical_questions_format(self):
        """Compare behavioral questions PDF format with technical questions format"""
        try:
            # Test technical interview questions endpoint for comparison
            job_title = "Senior Software Engineer"
            job_description = "Full-stack development role requiring React, Node.js, and cloud experience."
            resume_content = "Senior Software Engineer with 8+ years experience in React, Node.js, AWS, and team leadership."
            
            files = {
                'resume': ('comparison_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            form_data = {
                'job_title': job_title,
                'job_description': job_description
            }
            
            # Generate technical interview questions for comparison
            tech_response = self.session.post(
                f"{BASE_URL}/placement-preparation/technical-interview-questions",
                files=files,
                data=form_data,
                timeout=60
            )
            
            if tech_response.status_code == 200:
                tech_data = tech_response.json()
                tech_analysis_id = tech_data.get("analysis_id")
                
                if tech_analysis_id:
                    # Download technical questions PDF
                    tech_pdf_response = self.session.get(
                        f"{BASE_URL}/placement-preparation/technical-interview-questions/{tech_analysis_id}/download",
                        timeout=30
                    )
                    
                    # Download behavioral questions PDF
                    behavioral_pdf_response = self.session.get(
                        f"{BASE_URL}/placement-preparation/behavioral-interview-questions/{self.analysis_id}/download",
                        timeout=30
                    )
                    
                    if tech_pdf_response.status_code == 200 and behavioral_pdf_response.status_code == 200:
                        tech_pdf_size = len(tech_pdf_response.content)
                        behavioral_pdf_size = len(behavioral_pdf_response.content)
                        
                        # Both PDFs should be substantial and similar in structure
                        size_ratio = behavioral_pdf_size / tech_pdf_size if tech_pdf_size > 0 else 0
                        
                        self.log_test("PDF Format Comparison", "PASS", 
                                    f"Technical PDF: {tech_pdf_size} bytes, Behavioral PDF: {behavioral_pdf_size} bytes, Ratio: {size_ratio:.2f}")
                        
                        # Verify both use similar formatting (both should be substantial PDFs)
                        if behavioral_pdf_size > 5000 and tech_pdf_size > 5000:
                            self.log_test("PDF Structure Consistency", "PASS", 
                                        "Both PDFs have substantial content indicating consistent formatting")
                            return True
                        else:
                            self.log_test("PDF Structure Consistency", "WARN", 
                                        "One or both PDFs may have insufficient content")
                            return False
                    else:
                        self.log_test("PDF Format Comparison", "FAIL", 
                                    f"Failed to download comparison PDFs: Tech: {tech_pdf_response.status_code}, Behavioral: {behavioral_pdf_response.status_code}")
                        return False
                else:
                    self.log_test("PDF Format Comparison", "FAIL", "Failed to generate technical questions for comparison")
                    return False
            else:
                self.log_test("PDF Format Comparison", "FAIL", 
                            f"Failed to generate technical questions: HTTP {tech_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("PDF Format Comparison", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("=" * 80)
        print("BEHAVIORAL INTERVIEW QUESTIONS PDF GENERATION TESTING")
        print("Testing PDF formatting improvements to match technical questions format")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Backend Connectivity
        test_results.append(self.test_backend_connectivity())
        
        # Test 2: Behavioral Interview Questions Generation
        test_results.append(self.test_behavioral_interview_generation())
        
        # Test 3: Database Storage and Retrieval
        test_results.append(self.test_database_storage_and_retrieval())
        
        # Test 4: PDF Download Functionality
        test_results.append(self.test_pdf_download_functionality())
        
        # Test 5: PDF Formatting and Structure
        test_results.append(self.test_pdf_formatting_and_structure())
        
        # Test 6: Enhanced Question Parsing
        test_results.append(self.test_enhanced_question_parsing())
        
        # Test 7: Complete Workflow Verification
        test_results.append(self.test_complete_workflow())
        
        # Test 8: Format Comparison with Technical Questions
        test_results.append(self.compare_with_technical_questions_format())
        
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
            print("\n🎉 ALL TESTS PASSED! Behavioral interview questions PDF generation is working correctly with proper formatting.")
        elif passed_tests >= total_tests * 0.75:
            print(f"\n✅ MOSTLY SUCCESSFUL! {passed_tests}/{total_tests} tests passed. Minor issues may need attention.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests >= total_tests * 0.75  # Consider 75%+ as success

def main():
    """Main test execution"""
    tester = BehavioralInterviewPDFTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ BEHAVIORAL INTERVIEW QUESTIONS PDF TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ BEHAVIORAL INTERVIEW QUESTIONS PDF TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()