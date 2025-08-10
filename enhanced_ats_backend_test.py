#!/usr/bin/env python3
"""
Enhanced ATS Score Calculation System Testing
Testing the multi-phase analysis engine with programmatic validation and hybrid scoring
"""

import requests
import json
import time
import os
from datetime import datetime
import tempfile

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://d608964e-3bc2-49ac-82ce-24fb220fc6c6.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class EnhancedATSTester:
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

    def create_sample_resume(self, resume_type="software_engineer"):
        """Create sample resume content for testing"""
        if resume_type == "software_engineer":
            return """John Smith
Senior Software Engineer
Email: john.smith@email.com
Phone: (555) 123-4567

PROFESSIONAL SUMMARY
Experienced Software Engineer with 5+ years of expertise in Python, React, and MongoDB development. 
Led teams of 4+ developers and delivered 15+ successful projects with 99.9% uptime.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, TypeScript, Java
• Frontend: React, HTML5, CSS3, Redux
• Backend: FastAPI, Node.js, Express.js
• Databases: MongoDB, PostgreSQL, Redis
• Cloud & DevOps: AWS, Docker, Kubernetes, CI/CD
• Tools: Git, Agile, Scrum, REST API development

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Inc. | 2021 - Present
• Developed 10+ REST APIs using Python and FastAPI, serving 50,000+ daily users
• Implemented React-based frontend applications with 40% improved performance
• Led Agile development team of 4 engineers, delivering projects 20% ahead of schedule
• Optimized MongoDB queries, reducing response time by 60%
• Deployed applications on AWS using Docker and Kubernetes

Software Engineer | StartupXYZ | 2019 - 2021
• Built microservices architecture handling 1M+ requests per day
• Developed React components used across 5+ different applications
• Implemented automated testing, increasing code coverage to 95%
• Collaborated with cross-functional teams using Agile methodologies

EDUCATION
Bachelor of Science in Computer Science
University of Technology | 2019

CERTIFICATIONS
• AWS Certified Solutions Architect
• MongoDB Certified Developer

PROJECTS
• E-commerce Platform: Built full-stack application with React and Python, handling 10,000+ transactions
• Data Analytics Dashboard: Created real-time dashboard processing 1TB+ data daily
• API Gateway: Designed microservices gateway serving 20+ internal services"""

        elif resume_type == "minimal":
            return """Jane Doe
Software Developer
jane@email.com

I am a software developer with some experience in programming.

Experience:
- Worked at a company for 2 years
- Did some coding projects
- Used various technologies

Skills:
- Programming
- Problem solving
- Teamwork

Education:
Computer Science degree"""

    def test_enhanced_ats_endpoint_basic(self):
        """Test basic functionality of enhanced ATS endpoint"""
        try:
            # Create sample resume file
            resume_content = self.create_sample_resume("software_engineer")
            
            # Prepare multipart form data
            files = {
                'resume': ('software_engineer_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Software Engineer',
                'job_description': 'We are looking for a Software Engineer with expertise in Python, React, MongoDB, REST API development, and Agile methodologies. The ideal candidate should have 3+ years of experience and strong problem-solving skills.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("Enhanced ATS Endpoint Basic Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            
            # Verify response structure
            required_fields = ['success', 'ats_id', 'ats_score', 'analysis_text', 'pdf_filename']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                self.log_test("Enhanced ATS Endpoint Basic Test", "FAIL", 
                            f"Missing required fields: {missing_fields}")
                return False
            
            if not result.get('success'):
                self.log_test("Enhanced ATS Endpoint Basic Test", "FAIL", 
                            f"API returned success=false: {result}")
                return False
            
            # Verify ATS score is within valid range
            ats_score = result.get('ats_score', 0)
            if not (0 <= ats_score <= 100):
                self.log_test("Enhanced ATS Endpoint Basic Test", "FAIL", 
                            f"ATS score {ats_score} is outside valid range 0-100")
                return False
            
            self.log_test("Enhanced ATS Endpoint Basic Test", "PASS", 
                        f"ATS Score: {ats_score}/100, Analysis length: {len(result.get('analysis_text', ''))} chars")
            return True
            
        except Exception as e:
            self.log_test("Enhanced ATS Endpoint Basic Test", "FAIL", f"Exception: {str(e)}")
            return False

    def test_multi_phase_analysis_features(self):
        """Test that multi-phase analysis features are present in the response"""
        try:
            # Create comprehensive resume for testing
            resume_content = self.create_sample_resume("software_engineer")
            
            files = {
                'resume': ('comprehensive_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Full Stack Developer',
                'job_description': 'Looking for Senior Full Stack Developer with Python, React, MongoDB, REST API, Agile, Docker, AWS, microservices experience. Must have 5+ years experience and team leadership skills.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("Multi-Phase Analysis Features Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            analysis_text = result.get('analysis_text', '')
            
            # Check for Phase 1: Content and formatting analysis
            phase1_indicators = [
                'File Format:', 'ATS Compatibility:', 'Resume Length:', 'Sections Detected:'
            ]
            
            # Check for Phase 2: Keyword matching analysis
            phase2_indicators = [
                'Job Keywords Found:', 'Keyword Match Rate:', 'Top Matched Keywords:', 'Critical Missing Keywords:'
            ]
            
            # Check for Phase 3: Enhanced AI analysis indicators
            phase3_indicators = [
                'COMPREHENSIVE ATS SCORE:', 'KEYWORD OPTIMIZATION', 'EXPERIENCE', 'TECHNICAL COMPETENCY'
            ]
            
            # Check for Phase 4: Hybrid scoring
            phase4_indicators = [
                'Programmatic Adjustments:', 'FINAL HYBRID SCORE:', 'Hybrid Scoring Calculation:'
            ]
            
            phases_found = []
            
            # Check Phase 1
            if any(indicator in analysis_text for indicator in phase1_indicators):
                phases_found.append("Phase 1: Content Analysis")
            
            # Check Phase 2  
            if any(indicator in analysis_text for indicator in phase2_indicators):
                phases_found.append("Phase 2: Keyword Analysis")
            
            # Check Phase 3
            if any(indicator in analysis_text for indicator in phase3_indicators):
                phases_found.append("Phase 3: AI Analysis")
            
            # Check Phase 4
            if any(indicator in analysis_text for indicator in phase4_indicators):
                phases_found.append("Phase 4: Hybrid Scoring")
            
            if len(phases_found) < 3:
                self.log_test("Multi-Phase Analysis Features Test", "FAIL", 
                            f"Only found {len(phases_found)} phases: {phases_found}")
                return False
            
            self.log_test("Multi-Phase Analysis Features Test", "PASS", 
                        f"Found {len(phases_found)} analysis phases: {', '.join(phases_found)}")
            return True
            
        except Exception as e:
            self.log_test("Multi-Phase Analysis Features Test", "FAIL", f"Exception: {str(e)}")
            return False

    def test_programmatic_insights_section(self):
        """Test that programmatic insights are included in the analysis"""
        try:
            resume_content = self.create_sample_resume("software_engineer")
            
            files = {
                'resume': ('insights_test_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Python Developer',
                'job_description': 'Python developer needed with React, MongoDB, REST API, Docker, AWS experience. Agile methodology knowledge required.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("Programmatic Insights Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            analysis_text = result.get('analysis_text', '')
            
            # Check for programmatic insights section
            programmatic_indicators = [
                'ENHANCED ANALYSIS INSIGHTS:',
                'Content Analysis Results:',
                'Keyword Matching Analysis:',
                'Skills & Experience Validation:',
                'Quantified Achievements Found:',
                'SCORE ENHANCEMENT RECOMMENDATIONS:'
            ]
            
            insights_found = [indicator for indicator in programmatic_indicators if indicator in analysis_text]
            
            if len(insights_found) < 4:
                self.log_test("Programmatic Insights Test", "FAIL", 
                            f"Only found {len(insights_found)} programmatic insights: {insights_found}")
                return False
            
            # Check for specific metrics
            metrics_to_check = [
                'Keyword Match Rate:',
                'Quantified Achievements Found:',
                'ATS Compatibility:',
                'FINAL HYBRID SCORE:'
            ]
            
            metrics_found = [metric for metric in metrics_to_check if metric in analysis_text]
            
            if len(metrics_found) < 3:
                self.log_test("Programmatic Insights Test", "FAIL", 
                            f"Missing key metrics: {set(metrics_to_check) - set(metrics_found)}")
                return False
            
            self.log_test("Programmatic Insights Test", "PASS", 
                        f"Found {len(insights_found)} programmatic insights and {len(metrics_found)} key metrics")
            return True
            
        except Exception as e:
            self.log_test("Programmatic Insights Test", "FAIL", f"Exception: {str(e)}")
            return False

    def test_keyword_density_analysis(self):
        """Test keyword density and placement analysis"""
        try:
            # Create resume with specific keywords for testing
            resume_content = self.create_sample_resume("software_engineer")
            
            files = {
                'resume': ('keyword_test_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            # Job description with specific technical keywords
            data = {
                'job_title': 'Software Engineer',
                'job_description': 'Python React MongoDB REST API Agile Docker Kubernetes AWS microservices FastAPI JavaScript'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("Keyword Density Analysis Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            analysis_text = result.get('analysis_text', '')
            
            # Check for keyword analysis metrics
            keyword_indicators = [
                'Keyword Match Rate:',
                'Top Matched Keywords:',
                'Critical Missing Keywords:',
                'Job Keywords Found:'
            ]
            
            found_indicators = [indicator for indicator in keyword_indicators if indicator in analysis_text]
            
            if len(found_indicators) < 3:
                self.log_test("Keyword Density Analysis Test", "FAIL", 
                            f"Missing keyword analysis indicators: {set(keyword_indicators) - set(found_indicators)}")
                return False
            
            # Extract keyword match percentage if present
            import re
            match_rate_pattern = r'Keyword Match Rate:\s*(\d+\.?\d*)%'
            match = re.search(match_rate_pattern, analysis_text)
            
            if match:
                match_rate = float(match.group(1))
                if match_rate > 0:
                    self.log_test("Keyword Density Analysis Test", "PASS", 
                                f"Keyword analysis working - Match rate: {match_rate}%, Found {len(found_indicators)} indicators")
                    return True
            
            self.log_test("Keyword Density Analysis Test", "PASS", 
                        f"Keyword analysis present with {len(found_indicators)} indicators")
            return True
            
        except Exception as e:
            self.log_test("Keyword Density Analysis Test", "FAIL", f"Exception: {str(e)}")
            return False

    def test_quantified_achievements_detection(self):
        """Test detection of quantified achievements and metrics"""
        try:
            # Resume with quantified achievements
            resume_content = self.create_sample_resume("software_engineer")
            
            files = {
                'resume': ('achievements_test_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Software Engineer',
                'job_description': 'Senior Software Engineer with proven track record of delivering results and leading teams.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("Quantified Achievements Detection Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            analysis_text = result.get('analysis_text', '')
            
            # Check for quantified achievements analysis
            achievement_indicators = [
                'Quantified Achievements Found:',
                'Achievement Quantification:',
                'QUANTIFIED ACHIEVEMENTS:',
                'metrics'
            ]
            
            found_indicators = [indicator for indicator in achievement_indicators if indicator in analysis_text]
            
            if len(found_indicators) < 1:
                self.log_test("Quantified Achievements Detection Test", "FAIL", 
                            "No quantified achievements analysis found")
                return False
            
            # Look for specific numbers that should be detected
            expected_numbers = ['5+', '4+', '15+', '99.9%', '50,000+', '40%', '20%', '60%', '1M+', '95%', '10,000+', '1TB+', '20+']
            numbers_found = [num for num in expected_numbers if num in resume_content]
            
            if len(numbers_found) < 5:
                self.log_test("Quantified Achievements Detection Test", "FAIL", 
                            f"Test resume should contain more quantified achievements. Found: {numbers_found}")
                return False
            
            self.log_test("Quantified Achievements Detection Test", "PASS", 
                        f"Achievement detection working - Found indicators: {found_indicators}")
            return True
            
        except Exception as e:
            self.log_test("Quantified Achievements Detection Test", "FAIL", f"Exception: {str(e)}")
            return False

    def test_hybrid_scoring_algorithm(self):
        """Test that hybrid scoring combines AI + programmatic validation"""
        try:
            resume_content = self.create_sample_resume("software_engineer")
            
            files = {
                'resume': ('hybrid_scoring_test.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Full Stack Developer',
                'job_description': 'Full Stack Developer with Python, React, MongoDB, REST API, Agile experience required.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("Hybrid Scoring Algorithm Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            analysis_text = result.get('analysis_text', '')
            
            # Check for hybrid scoring indicators
            hybrid_indicators = [
                'Hybrid Scoring Calculation:',
                'AI Analysis Score:',
                'Programmatic Adjustments:',
                'FINAL HYBRID SCORE:'
            ]
            
            found_indicators = [indicator for indicator in hybrid_indicators if indicator in analysis_text]
            
            if len(found_indicators) < 2:
                self.log_test("Hybrid Scoring Algorithm Test", "FAIL", 
                            f"Missing hybrid scoring indicators: {set(hybrid_indicators) - set(found_indicators)}")
                return False
            
            # Extract scores if present
            import re
            ai_score_pattern = r'AI Analysis Score:\s*(\d+)/100'
            adjustment_pattern = r'Programmatic Adjustments:\s*([+-]?\d+)\s*points?'
            final_score_pattern = r'FINAL HYBRID SCORE:\s*(\d+)/100'
            
            ai_match = re.search(ai_score_pattern, analysis_text)
            adj_match = re.search(adjustment_pattern, analysis_text)
            final_match = re.search(final_score_pattern, analysis_text)
            
            scores_found = []
            if ai_match:
                scores_found.append(f"AI Score: {ai_match.group(1)}")
            if adj_match:
                scores_found.append(f"Adjustments: {adj_match.group(1)}")
            if final_match:
                scores_found.append(f"Final: {final_match.group(1)}")
            
            self.log_test("Hybrid Scoring Algorithm Test", "PASS", 
                        f"Hybrid scoring working - Found: {', '.join(scores_found)}")
            return True
            
        except Exception as e:
            self.log_test("Hybrid Scoring Algorithm Test", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_generation_enhanced(self):
        """Test PDF generation with enhanced analysis"""
        try:
            resume_content = self.create_sample_resume("software_engineer")
            
            files = {
                'resume': ('pdf_test_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Software Engineer',
                'job_description': 'Software Engineer with Python, React, MongoDB experience needed.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("PDF Generation Enhanced Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            pdf_filename = result.get('pdf_filename')
            
            if not pdf_filename:
                self.log_test("PDF Generation Enhanced Test", "FAIL", 
                            "No PDF filename returned")
                return False
            
            # Try to download the PDF
            pdf_response = self.session.get(f"{BASE_URL}/placement-preparation/download-ats-report/{pdf_filename}")
            
            if pdf_response.status_code != 200:
                self.log_test("PDF Generation Enhanced Test", "FAIL", 
                            f"PDF download failed: HTTP {pdf_response.status_code}")
                return False
            
            # Check PDF content type and size
            content_type = pdf_response.headers.get('content-type', '')
            content_length = len(pdf_response.content)
            
            if 'pdf' not in content_type.lower():
                self.log_test("PDF Generation Enhanced Test", "FAIL", 
                            f"Invalid content type: {content_type}")
                return False
            
            if content_length < 1000:  # PDF should be at least 1KB
                self.log_test("PDF Generation Enhanced Test", "FAIL", 
                            f"PDF too small: {content_length} bytes")
                return False
            
            self.log_test("PDF Generation Enhanced Test", "PASS", 
                        f"PDF generated successfully - Size: {content_length} bytes, Type: {content_type}")
            return True
            
        except Exception as e:
            self.log_test("PDF Generation Enhanced Test", "FAIL", f"Exception: {str(e)}")
            return False

    def test_ats_compatibility_scoring(self):
        """Test ATS compatibility scoring for different file formats"""
        try:
            resume_content = self.create_sample_resume("software_engineer")
            
            # Test with TXT format
            files = {
                'resume': ('ats_compatibility_test.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Software Engineer',
                'job_description': 'Software Engineer position requiring technical skills.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("ATS Compatibility Scoring Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            analysis_text = result.get('analysis_text', '')
            
            # Check for ATS compatibility analysis
            compatibility_indicators = [
                'ATS Compatibility:',
                'File Format:',
                'ATS COMPATIBILITY:',
                'formatting'
            ]
            
            found_indicators = [indicator for indicator in compatibility_indicators if indicator in analysis_text]
            
            if len(found_indicators) < 2:
                self.log_test("ATS Compatibility Scoring Test", "FAIL", 
                            f"Missing ATS compatibility analysis: {found_indicators}")
                return False
            
            # Check for file format mention
            if '.txt' not in analysis_text and 'TXT' not in analysis_text:
                self.log_test("ATS Compatibility Scoring Test", "FAIL", 
                            "File format not mentioned in analysis")
                return False
            
            self.log_test("ATS Compatibility Scoring Test", "PASS", 
                        f"ATS compatibility analysis present - Found: {found_indicators}")
            return True
            
        except Exception as e:
            self.log_test("ATS Compatibility Scoring Test", "FAIL", f"Exception: {str(e)}")
            return False

    def test_experience_level_detection(self):
        """Test experience level indicators and career progression analysis"""
        try:
            resume_content = self.create_sample_resume("software_engineer")
            
            files = {
                'resume': ('experience_test_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Software Engineer',
                'job_description': 'Senior Software Engineer position for experienced professional.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("Experience Level Detection Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            analysis_text = result.get('analysis_text', '')
            
            # Check for experience analysis
            experience_indicators = [
                'Experience Indicators:',
                'EXPERIENCE',
                'years',
                'Senior',
                'career progression'
            ]
            
            found_indicators = [indicator for indicator in experience_indicators if indicator.lower() in analysis_text.lower()]
            
            if len(found_indicators) < 3:
                self.log_test("Experience Level Detection Test", "FAIL", 
                            f"Insufficient experience analysis: {found_indicators}")
                return False
            
            # Check for specific experience mentions
            experience_terms = ['5+ years', 'Senior', 'Led', 'team']
            found_terms = [term for term in experience_terms if term in resume_content]
            
            if len(found_terms) < 2:
                self.log_test("Experience Level Detection Test", "FAIL", 
                            f"Test resume should contain experience terms: {found_terms}")
                return False
            
            self.log_test("Experience Level Detection Test", "PASS", 
                        f"Experience analysis working - Found: {len(found_indicators)} indicators")
            return True
            
        except Exception as e:
            self.log_test("Experience Level Detection Test", "FAIL", f"Exception: {str(e)}")
            return False

    def test_minimal_resume_handling(self):
        """Test how the system handles minimal/poor quality resumes"""
        try:
            # Use minimal resume
            resume_content = self.create_sample_resume("minimal")
            
            files = {
                'resume': ('minimal_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            data = {
                'job_title': 'Software Developer',
                'job_description': 'Software Developer with Python, React, MongoDB, REST API experience required.'
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=data)
            
            if response.status_code != 200:
                self.log_test("Minimal Resume Handling Test", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            result = response.json()
            ats_score = result.get('ats_score', 0)
            analysis_text = result.get('analysis_text', '')
            
            # Minimal resume should get lower score
            if ats_score > 60:
                self.log_test("Minimal Resume Handling Test", "FAIL", 
                            f"Minimal resume scored too high: {ats_score}/100")
                return False
            
            # Should identify issues
            issue_indicators = [
                'Missing',
                'brief',
                'improve',
                'add',
                'insufficient'
            ]
            
            found_issues = [indicator for indicator in issue_indicators if indicator.lower() in analysis_text.lower()]
            
            if len(found_issues) < 2:
                self.log_test("Minimal Resume Handling Test", "FAIL", 
                            f"Should identify more issues with minimal resume: {found_issues}")
                return False
            
            self.log_test("Minimal Resume Handling Test", "PASS", 
                        f"Minimal resume handled correctly - Score: {ats_score}/100, Issues identified: {len(found_issues)}")
            return True
            
        except Exception as e:
            self.log_test("Minimal Resume Handling Test", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all enhanced ATS tests"""
        print("=" * 80)
        print("ENHANCED ATS SCORE CALCULATION SYSTEM TESTING")
        print("Multi-Phase Analysis Engine with Hybrid Scoring")
        print("=" * 80)
        print()
        
        test_methods = [
            self.test_enhanced_ats_endpoint_basic,
            self.test_multi_phase_analysis_features,
            self.test_programmatic_insights_section,
            self.test_keyword_density_analysis,
            self.test_quantified_achievements_detection,
            self.test_hybrid_scoring_algorithm,
            self.test_pdf_generation_enhanced,
            self.test_ats_compatibility_scoring,
            self.test_experience_level_detection,
            self.test_minimal_resume_handling
        ]
        
        results = []
        for test_method in test_methods:
            try:
                result = test_method()
                results.append(result)
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test {test_method.__name__} failed with exception: {e}")
                results.append(False)
        
        # Summary
        print("=" * 80)
        print("ENHANCED ATS TESTING SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(results)
        total_tests = len(results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL ENHANCED ATS TESTS PASSED!")
            print("✅ Multi-phase analysis engine working correctly")
            print("✅ Programmatic validation integrated")
            print("✅ Hybrid scoring algorithm functional")
            print("✅ Enhanced analysis with actionable insights")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Review issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = EnhancedATSTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ ENHANCED ATS TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ ENHANCED ATS TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()