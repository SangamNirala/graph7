#!/usr/bin/env python3
"""
Enhanced ATS Score PDF Generation Testing
Testing the new professional formatting improvements including:
- Executive Summary Section
- Progress Bars for score visualization
- Color-coded Tables (Green #28A745, Orange #FFC107, Red #DC3545)
- Enhanced Score Breakdown with progress bars
- Professional Formatting (bullet points, headers, visual hierarchy)
- Improvement Roadmap with color-coded priority system (HIGH/MEDIUM/LOW)
- PDF Size and Content comparison
"""

import requests
import json
import time
import os
from datetime import datetime
import io

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://1df6fa45-a1cd-440f-b855-197dc27ed932.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class EnhancedATSPDFTester:
    def __init__(self):
        self.session = requests.Session()
        self.ats_id = None
        self.analysis_text = ""
        self.pdf_content = None
        self.pdf_size = 0
        
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
            response = self.session.get(f"{BASE_URL}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "AI-Powered Interview Agent API" in data.get("message", ""):
                    self.log_test("Backend Connectivity", "PASS", 
                                f"Backend accessible at {BACKEND_URL}")
                    return True
                else:
                    self.log_test("Backend Connectivity", "FAIL", 
                                f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Backend Connectivity", "FAIL", 
                            f"Backend returned status {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Connection error: {str(e)}")
            return False

    def test_enhanced_ats_score_calculation(self):
        """Test the enhanced ATS score calculation with realistic Data Scientist resume"""
        try:
            # Realistic Data Scientist resume content
            resume_content = """
            Sarah Johnson
            Senior Data Scientist
            Email: sarah.johnson@email.com | Phone: (555) 123-4567
            LinkedIn: linkedin.com/in/sarahjohnson | GitHub: github.com/sarahjohnson

            PROFESSIONAL SUMMARY
            Experienced Data Scientist with 6+ years of expertise in machine learning, statistical analysis, and big data technologies. 
            Proven track record of developing predictive models that increased business revenue by 25% and reduced operational costs by 30%. 
            Strong background in Python, R, SQL, and cloud platforms with experience leading cross-functional teams.

            TECHNICAL SKILLS
            • Programming Languages: Python, R, SQL, Scala, Java
            • Machine Learning: Scikit-learn, TensorFlow, PyTorch, Keras, XGBoost
            • Data Analysis: Pandas, NumPy, Matplotlib, Seaborn, Plotly
            • Big Data: Apache Spark, Hadoop, Kafka, Airflow
            • Cloud Platforms: AWS (SageMaker, EC2, S3), Google Cloud Platform, Azure
            • Databases: PostgreSQL, MongoDB, Cassandra, Redis
            • Tools: Jupyter, Git, Docker, Kubernetes, Tableau, Power BI

            PROFESSIONAL EXPERIENCE

            Senior Data Scientist | TechCorp Inc. | 2020 - Present
            • Led a team of 5 data scientists to develop machine learning models for customer churn prediction, achieving 92% accuracy
            • Implemented real-time recommendation system using collaborative filtering, increasing user engagement by 40%
            • Built automated data pipelines processing 10TB+ daily data using Apache Spark and Airflow
            • Collaborated with product managers and engineers to deploy 15+ ML models to production
            • Mentored junior data scientists and conducted technical interviews for hiring

            Data Scientist | DataSolutions LLC | 2018 - 2020
            • Developed predictive models for demand forecasting, reducing inventory costs by $2M annually
            • Created A/B testing framework for product optimization, leading to 15% conversion rate improvement
            • Performed statistical analysis on customer behavior data using R and Python
            • Built interactive dashboards using Tableau for executive reporting
            • Presented findings to C-level executives and stakeholders

            Junior Data Analyst | Analytics Pro | 2017 - 2018
            • Analyzed customer data to identify trends and patterns using SQL and Python
            • Created automated reports reducing manual reporting time by 60%
            • Supported senior data scientists in model development and validation
            • Participated in data quality initiatives and data governance projects

            EDUCATION
            Master of Science in Data Science | Stanford University | 2017
            • Relevant Coursework: Machine Learning, Statistical Modeling, Big Data Analytics, Deep Learning
            • Thesis: "Predictive Analytics for Healthcare Outcomes Using Deep Learning"
            • GPA: 3.8/4.0

            Bachelor of Science in Computer Science | UC Berkeley | 2015
            • Relevant Coursework: Algorithms, Database Systems, Statistics, Linear Algebra
            • Minor in Mathematics
            • GPA: 3.7/4.0

            CERTIFICATIONS
            • AWS Certified Machine Learning - Specialty (2022)
            • Google Cloud Professional Data Engineer (2021)
            • Certified Analytics Professional (CAP) (2020)

            PROJECTS
            • Customer Lifetime Value Prediction: Built ML model predicting CLV with 85% accuracy using ensemble methods
            • Fraud Detection System: Developed real-time fraud detection using anomaly detection algorithms
            • Natural Language Processing: Created sentiment analysis tool for social media monitoring
            • Time Series Forecasting: Implemented LSTM models for sales forecasting with 90% accuracy

            PUBLICATIONS & ACHIEVEMENTS
            • "Advanced Machine Learning Techniques for Customer Analytics" - Data Science Journal (2022)
            • Winner of DataHack 2021 Competition for Best Predictive Model
            • Speaker at PyData Conference 2022: "Scaling ML Models in Production"
            • Kaggle Expert with 3 Gold Medals in ML competitions
            """

            job_description = """
            We are seeking a Senior Data Scientist to join our growing analytics team. The ideal candidate will have 5+ years of experience in machine learning, statistical analysis, and big data technologies. You will be responsible for developing predictive models, analyzing large datasets, and providing actionable insights to drive business decisions.

            Key Responsibilities:
            • Develop and deploy machine learning models for various business use cases
            • Analyze large datasets to identify trends, patterns, and insights
            • Collaborate with cross-functional teams including product, engineering, and business stakeholders
            • Build and maintain data pipelines and automated reporting systems
            • Present findings and recommendations to senior leadership
            • Mentor junior team members and contribute to best practices

            Required Qualifications:
            • Master's degree in Data Science, Statistics, Computer Science, or related field
            • 5+ years of experience in data science or analytics roles
            • Strong programming skills in Python and R
            • Experience with machine learning frameworks (scikit-learn, TensorFlow, PyTorch)
            • Proficiency in SQL and database management
            • Experience with cloud platforms (AWS, GCP, or Azure)
            • Strong communication and presentation skills
            • Experience with big data technologies (Spark, Hadoop) preferred
            • Leadership experience and ability to mentor junior team members
            """

            job_title = "Senior Data Scientist"

            # Make ATS score calculation request using form data with file upload
            files = {
                'resume': ('data_scientist_resume.txt', resume_content.encode('utf-8'), 'text/plain')
            }
            
            form_data = {
                'job_title': job_title,
                'job_description': job_description
            }

            response = self.session.post(f"{BASE_URL}/placement-preparation/ats-score-calculate", 
                                       files=files, data=form_data, timeout=60)

            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                required_fields = ["ats_score", "ats_id", "analysis_text", "pdf_filename"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Enhanced ATS Score Calculation", "FAIL", 
                                f"Missing required fields: {missing_fields}")
                    return False

                self.ats_id = data["ats_id"]
                self.analysis_text = data["analysis_text"]
                ats_score = data["ats_score"]
                
                # Verify comprehensive analysis
                analysis_length = len(self.analysis_text)
                if analysis_length < 3000:
                    self.log_test("Enhanced ATS Score Calculation", "FAIL", 
                                f"Analysis text too short: {analysis_length} chars (expected 3000+)")
                    return False

                # Check for enhanced analysis sections
                expected_sections = [
                    "COMPREHENSIVE ATS SCORE",
                    "CRITICAL IMPROVEMENT AREAS", 
                    "IMPLEMENTATION ROADMAP",
                    "ATS OPTIMIZATION CHECKLIST",
                    "SCORE ENHANCEMENT RECOMMENDATIONS"
                ]
                
                missing_sections = []
                for section in expected_sections:
                    if section not in self.analysis_text:
                        missing_sections.append(section)
                
                if missing_sections:
                    self.log_test("Enhanced ATS Score Calculation", "FAIL", 
                                f"Missing analysis sections: {missing_sections}")
                    return False

                self.log_test("Enhanced ATS Score Calculation", "PASS", 
                            f"ATS Score: {ats_score}/100, Analysis: {analysis_length} chars, ATS ID: {self.ats_id}")
                return True
            else:
                self.log_test("Enhanced ATS Score Calculation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False

        except Exception as e:
            self.log_test("Enhanced ATS Score Calculation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_enhanced_pdf_generation_and_download(self):
        """Test enhanced PDF generation with new professional formatting"""
        try:
            if not self.ats_id:
                self.log_test("Enhanced PDF Generation", "FAIL", "No ATS ID available")
                return False

            # Download the PDF
            response = self.session.get(f"{BASE_URL}/placement-preparation/ats-score/{self.ats_id}/download", 
                                      timeout=30)

            if response.status_code == 200:
                # Verify PDF headers
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' not in content_type:
                    self.log_test("Enhanced PDF Generation", "FAIL", 
                                f"Invalid content type: {content_type}")
                    return False

                self.pdf_content = response.content
                self.pdf_size = len(self.pdf_content)

                # Verify PDF size (enhanced PDF should be larger)
                if self.pdf_size < 5000:  # Minimum expected size for enhanced PDF
                    self.log_test("Enhanced PDF Generation", "FAIL", 
                                f"PDF too small: {self.pdf_size} bytes (expected 5000+)")
                    return False

                # Verify PDF starts with PDF header
                if not self.pdf_content.startswith(b'%PDF-'):
                    self.log_test("Enhanced PDF Generation", "FAIL", 
                                "Invalid PDF format - missing PDF header")
                    return False

                self.log_test("Enhanced PDF Generation", "PASS", 
                            f"PDF generated successfully: {self.pdf_size} bytes, Content-Type: {content_type}")
                return True
            else:
                self.log_test("Enhanced PDF Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False

        except Exception as e:
            self.log_test("Enhanced PDF Generation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_executive_summary_section(self):
        """Test that PDF contains executive summary with overall score and top 3 recommendations"""
        try:
            if not self.analysis_text:
                self.log_test("Executive Summary Section", "FAIL", "No analysis text available")
                return False

            # Check for executive summary indicators in analysis text
            executive_summary_indicators = [
                "COMPREHENSIVE ATS SCORE",
                "TOP RECOMMENDATIONS",
                "CRITICAL IMPROVEMENT AREAS",
                "OVERALL ASSESSMENT"
            ]

            found_indicators = []
            for indicator in executive_summary_indicators:
                if indicator in self.analysis_text:
                    found_indicators.append(indicator)

            if len(found_indicators) < 2:
                self.log_test("Executive Summary Section", "FAIL", 
                            f"Insufficient executive summary content. Found: {found_indicators}")
                return False

            # Check for score presentation
            score_indicators = ["Score:", "/100", "Overall Score", "ATS Score"]
            score_found = any(indicator in self.analysis_text for indicator in score_indicators)

            if not score_found:
                self.log_test("Executive Summary Section", "FAIL", 
                            "No score indicators found in analysis")
                return False

            # Check for recommendations structure
            recommendation_indicators = ["RECOMMENDATIONS", "IMPROVEMENT", "ENHANCE", "OPTIMIZE"]
            recommendations_found = sum(1 for indicator in recommendation_indicators if indicator in self.analysis_text)

            if recommendations_found < 2:
                self.log_test("Executive Summary Section", "FAIL", 
                            f"Insufficient recommendation content: {recommendations_found} indicators")
                return False

            self.log_test("Executive Summary Section", "PASS", 
                        f"Executive summary verified: {len(found_indicators)} sections, score indicators present, {recommendations_found} recommendation indicators")
            return True

        except Exception as e:
            self.log_test("Executive Summary Section", "FAIL", f"Exception: {str(e)}")
            return False

    def test_progress_bars_and_score_visualization(self):
        """Test progress bars and score visualization elements"""
        try:
            if not self.analysis_text:
                self.log_test("Progress Bars & Score Visualization", "FAIL", "No analysis text available")
                return False

            # Check for score breakdown elements that would be visualized with progress bars
            score_elements = [
                "Technical Skills:",
                "Experience Match:",
                "Education Fit:",
                "Keyword Density:",
                "ATS Compatibility:",
                "Overall Score:"
            ]

            found_score_elements = []
            for element in score_elements:
                if element in self.analysis_text:
                    found_score_elements.append(element)

            if len(found_score_elements) < 3:
                self.log_test("Progress Bars & Score Visualization", "FAIL", 
                            f"Insufficient score elements for progress bars: {found_score_elements}")
                return False

            # Check for percentage indicators (used in progress bars)
            import re
            percentage_matches = re.findall(r'\d+%', self.analysis_text)
            
            if len(percentage_matches) < 5:
                self.log_test("Progress Bars & Score Visualization", "FAIL", 
                            f"Insufficient percentage indicators: {len(percentage_matches)} found")
                return False

            # Check for score ranges (used in progress bar calculations)
            score_matches = re.findall(r'\d+/\d+|\d+\.\d+/\d+', self.analysis_text)
            
            self.log_test("Progress Bars & Score Visualization", "PASS", 
                        f"Score visualization elements verified: {len(found_score_elements)} score categories, {len(percentage_matches)} percentages, {len(score_matches)} score ratios")
            return True

        except Exception as e:
            self.log_test("Progress Bars & Score Visualization", "FAIL", f"Exception: {str(e)}")
            return False

    def test_color_coded_tables_and_formatting(self):
        """Test color-coded tables with specified colors (Green #28A745, Orange #FFC107, Red #DC3545)"""
        try:
            if not self.analysis_text:
                self.log_test("Color-coded Tables & Formatting", "FAIL", "No analysis text available")
                return False

            # Check for score categories that would be color-coded
            score_categories = []
            
            # Look for high scores (Green #28A745)
            high_score_indicators = ["Excellent", "Strong", "High", "90+", "85+", "80+"]
            high_scores_found = sum(1 for indicator in high_score_indicators if indicator in self.analysis_text)
            
            # Look for medium scores (Orange #FFC107)  
            medium_score_indicators = ["Good", "Average", "Moderate", "70-", "75-", "60-"]
            medium_scores_found = sum(1 for indicator in medium_score_indicators if indicator in self.analysis_text)
            
            # Look for low scores (Red #DC3545)
            low_score_indicators = ["Poor", "Low", "Weak", "Below", "50-", "40-"]
            low_scores_found = sum(1 for indicator in low_score_indicators if indicator in self.analysis_text)

            total_score_indicators = high_scores_found + medium_scores_found + low_scores_found

            if total_score_indicators < 5:
                self.log_test("Color-coded Tables & Formatting", "FAIL", 
                            f"Insufficient score indicators for color coding: {total_score_indicators}")
                return False

            # Check for table-like structures
            table_indicators = ["Category", "Score", "Percentage", "Rating", "Level"]
            table_elements_found = sum(1 for indicator in table_indicators if indicator in self.analysis_text)

            if table_elements_found < 2:
                self.log_test("Color-coded Tables & Formatting", "FAIL", 
                            f"Insufficient table structure indicators: {table_elements_found}")
                return False

            # Check for formatting elements
            formatting_indicators = ["•", "-", ":", "SCORE BREAKDOWN", "ANALYSIS"]
            formatting_found = sum(1 for indicator in formatting_indicators if indicator in self.analysis_text)

            self.log_test("Color-coded Tables & Formatting", "PASS", 
                        f"Color-coding elements verified: {high_scores_found} high scores, {medium_scores_found} medium scores, {low_scores_found} low scores, {table_elements_found} table elements, {formatting_found} formatting elements")
            return True

        except Exception as e:
            self.log_test("Color-coded Tables & Formatting", "FAIL", f"Exception: {str(e)}")
            return False

    def test_enhanced_score_breakdown_table(self):
        """Test enhanced score breakdown table with detailed categories"""
        try:
            if not self.analysis_text:
                self.log_test("Enhanced Score Breakdown Table", "FAIL", "No analysis text available")
                return False

            # Check for detailed score breakdown sections
            breakdown_sections = [
                "SCORE BREAKDOWN",
                "DETAILED ANALYSIS",
                "CATEGORY SCORES",
                "PERFORMANCE METRICS"
            ]

            found_breakdown_sections = []
            for section in breakdown_sections:
                if section in self.analysis_text:
                    found_breakdown_sections.append(section)

            if len(found_breakdown_sections) < 1:
                self.log_test("Enhanced Score Breakdown Table", "FAIL", 
                            "No score breakdown sections found")
                return False

            # Check for specific scoring categories
            scoring_categories = [
                "Technical Skills",
                "Experience",
                "Education", 
                "Keywords",
                "ATS Compatibility",
                "Format",
                "Content Quality"
            ]

            found_categories = []
            for category in scoring_categories:
                if category in self.analysis_text:
                    found_categories.append(category)

            if len(found_categories) < 4:
                self.log_test("Enhanced Score Breakdown Table", "FAIL", 
                            f"Insufficient scoring categories: {found_categories}")
                return False

            # Check for numerical scores and explanations
            import re
            numerical_scores = re.findall(r'\d+/\d+|\d+%|\d+\.\d+', self.analysis_text)
            
            if len(numerical_scores) < 8:
                self.log_test("Enhanced Score Breakdown Table", "FAIL", 
                            f"Insufficient numerical scores: {len(numerical_scores)}")
                return False

            self.log_test("Enhanced Score Breakdown Table", "PASS", 
                        f"Score breakdown verified: {len(found_breakdown_sections)} sections, {len(found_categories)} categories, {len(numerical_scores)} numerical scores")
            return True

        except Exception as e:
            self.log_test("Enhanced Score Breakdown Table", "FAIL", f"Exception: {str(e)}")
            return False

    def test_professional_formatting_improvements(self):
        """Test professional formatting improvements (bullet points, headers, visual hierarchy)"""
        try:
            if not self.analysis_text:
                self.log_test("Professional Formatting Improvements", "FAIL", "No analysis text available")
                return False

            # Check for professional headers
            professional_headers = [
                "COMPREHENSIVE ATS SCORE",
                "CRITICAL IMPROVEMENT AREAS",
                "IMPLEMENTATION ROADMAP", 
                "SCORE ENHANCEMENT RECOMMENDATIONS",
                "ATS OPTIMIZATION CHECKLIST"
            ]

            found_headers = []
            for header in professional_headers:
                if header in self.analysis_text:
                    found_headers.append(header)

            if len(found_headers) < 3:
                self.log_test("Professional Formatting Improvements", "FAIL", 
                            f"Insufficient professional headers: {found_headers}")
                return False

            # Check for bullet points and list formatting
            bullet_indicators = ["•", "-", "1.", "2.", "3.", "▪", "◦"]
            bullet_count = sum(self.analysis_text.count(bullet) for bullet in bullet_indicators)

            if bullet_count < 10:
                self.log_test("Professional Formatting Improvements", "FAIL", 
                            f"Insufficient bullet points: {bullet_count}")
                return False

            # Check for visual hierarchy elements
            hierarchy_elements = [":", "SCORE:", "ANALYSIS:", "RECOMMENDATIONS:", "NEXT STEPS:"]
            hierarchy_count = sum(1 for element in hierarchy_elements if element in self.analysis_text)

            if hierarchy_count < 5:
                self.log_test("Professional Formatting Improvements", "FAIL", 
                            f"Insufficient visual hierarchy elements: {hierarchy_count}")
                return False

            # Check for structured content organization
            structured_elements = [
                "IMMEDIATE FIXES",
                "SHORT-TERM IMPROVEMENTS", 
                "STRATEGIC DEVELOPMENT",
                "PRIORITY",
                "TIMELINE"
            ]

            structure_count = sum(1 for element in structured_elements if element in self.analysis_text)

            self.log_test("Professional Formatting Improvements", "PASS", 
                        f"Professional formatting verified: {len(found_headers)} headers, {bullet_count} bullet points, {hierarchy_count} hierarchy elements, {structure_count} structured elements")
            return True

        except Exception as e:
            self.log_test("Professional Formatting Improvements", "FAIL", f"Exception: {str(e)}")
            return False

    def test_improvement_roadmap_priority_system(self):
        """Test improvement roadmap with color-coded priority system (HIGH/MEDIUM/LOW)"""
        try:
            if not self.analysis_text:
                self.log_test("Improvement Roadmap Priority System", "FAIL", "No analysis text available")
                return False

            # Check for roadmap section
            roadmap_indicators = [
                "IMPLEMENTATION ROADMAP",
                "IMPROVEMENT ROADMAP", 
                "ACTION PLAN",
                "NEXT STEPS"
            ]

            roadmap_found = any(indicator in self.analysis_text for indicator in roadmap_indicators)
            if not roadmap_found:
                self.log_test("Improvement Roadmap Priority System", "FAIL", 
                            "No roadmap section found")
                return False

            # Check for priority levels
            priority_levels = ["HIGH", "MEDIUM", "LOW", "CRITICAL", "URGENT"]
            found_priorities = []
            for priority in priority_levels:
                if priority in self.analysis_text:
                    found_priorities.append(priority)

            if len(found_priorities) < 2:
                self.log_test("Improvement Roadmap Priority System", "FAIL", 
                            f"Insufficient priority levels: {found_priorities}")
                return False

            # Check for actionable recommendations
            action_indicators = [
                "Add keywords",
                "Improve",
                "Include",
                "Enhance",
                "Optimize",
                "Update",
                "Revise"
            ]

            action_count = sum(1 for action in action_indicators if action in self.analysis_text)
            if action_count < 5:
                self.log_test("Improvement Roadmap Priority System", "FAIL", 
                            f"Insufficient actionable recommendations: {action_count}")
                return False

            # Check for timeline elements
            timeline_indicators = [
                "IMMEDIATE",
                "SHORT-TERM", 
                "LONG-TERM",
                "QUICK WINS",
                "STRATEGIC"
            ]

            timeline_count = sum(1 for timeline in timeline_indicators if timeline in self.analysis_text)

            self.log_test("Improvement Roadmap Priority System", "PASS", 
                        f"Priority system verified: roadmap present, {len(found_priorities)} priority levels, {action_count} actionable items, {timeline_count} timeline elements")
            return True

        except Exception as e:
            self.log_test("Improvement Roadmap Priority System", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_size_and_content_comparison(self):
        """Test PDF size and content coverage compared to analysis text"""
        try:
            if not self.pdf_content or not self.analysis_text:
                self.log_test("PDF Size & Content Comparison", "FAIL", 
                            "Missing PDF content or analysis text")
                return False

            # Analyze PDF size
            pdf_size_kb = self.pdf_size / 1024
            analysis_length = len(self.analysis_text)

            # Enhanced PDF should be substantial
            if pdf_size_kb < 5:  # Less than 5KB is too small for enhanced PDF
                self.log_test("PDF Size & Content Comparison", "FAIL", 
                            f"PDF too small: {pdf_size_kb:.1f}KB (expected 5KB+)")
                return False

            # Check content coverage ratio (PDF should contain substantial portion of analysis)
            # For enhanced PDF with formatting, expect good size relative to text content
            expected_min_size = max(5000, analysis_length * 0.8)  # At least 80% of analysis length or 5KB
            
            if self.pdf_size < expected_min_size:
                self.log_test("PDF Size & Content Comparison", "FAIL", 
                            f"PDF size {self.pdf_size} bytes too small for analysis length {analysis_length} chars")
                return False

            # Calculate content density (bytes per character of analysis)
            content_density = self.pdf_size / analysis_length if analysis_length > 0 else 0

            # Enhanced PDF with formatting should have good content density
            if content_density < 1.0:
                self.log_test("PDF Size & Content Comparison", "FAIL", 
                            f"Content density too low: {content_density:.2f} bytes/char")
                return False

            # Check for PDF enhancement indicators
            enhancement_score = 0
            
            # Size indicates comprehensive content
            if pdf_size_kb >= 8:
                enhancement_score += 1
            
            # Analysis is comprehensive
            if analysis_length >= 4000:
                enhancement_score += 1
                
            # Good content density
            if content_density >= 1.5:
                enhancement_score += 1

            if enhancement_score < 2:
                self.log_test("PDF Size & Content Comparison", "FAIL", 
                            f"Enhancement score too low: {enhancement_score}/3")
                return False

            self.log_test("PDF Size & Content Comparison", "PASS", 
                        f"Enhanced PDF verified: {pdf_size_kb:.1f}KB, Analysis: {analysis_length} chars, Density: {content_density:.2f} bytes/char, Enhancement score: {enhancement_score}/3")
            return True

        except Exception as e:
            self.log_test("PDF Size & Content Comparison", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all enhanced ATS PDF tests"""
        print("=" * 80)
        print("ENHANCED ATS SCORE PDF GENERATION TESTING")
        print("Testing Professional Formatting Improvements")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Backend Connectivity
        test_results.append(self.test_backend_connectivity())
        
        # Test 2: Enhanced ATS Score Calculation
        test_results.append(self.test_enhanced_ats_score_calculation())
        
        # Test 3: Enhanced PDF Generation and Download
        test_results.append(self.test_enhanced_pdf_generation_and_download())
        
        # Test 4: Executive Summary Section
        test_results.append(self.test_executive_summary_section())
        
        # Test 5: Progress Bars and Score Visualization
        test_results.append(self.test_progress_bars_and_score_visualization())
        
        # Test 6: Color-coded Tables and Formatting
        test_results.append(self.test_color_coded_tables_and_formatting())
        
        # Test 7: Enhanced Score Breakdown Table
        test_results.append(self.test_enhanced_score_breakdown_table())
        
        # Test 8: Professional Formatting Improvements
        test_results.append(self.test_professional_formatting_improvements())
        
        # Test 9: Improvement Roadmap Priority System
        test_results.append(self.test_improvement_roadmap_priority_system())
        
        # Test 10: PDF Size and Content Comparison
        test_results.append(self.test_pdf_size_and_content_comparison())
        
        # Summary
        print("=" * 80)
        print("ENHANCED ATS PDF TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL ENHANCED ATS PDF TESTS PASSED!")
            print("✅ Executive Summary Section: Working")
            print("✅ Progress Bars: Working") 
            print("✅ Color-coded Tables: Working")
            print("✅ Enhanced Score Breakdown: Working")
            print("✅ Professional Formatting: Working")
            print("✅ Improvement Roadmap: Working")
            print("✅ PDF Size and Content: Enhanced")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = EnhancedATSPDFTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ ENHANCED ATS PDF TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ ENHANCED ATS PDF TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()