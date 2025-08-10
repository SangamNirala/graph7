#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Placement Preparation Resume Preview Functionality
Testing the resume upload and preview implementation for Resume Analysis section
"""

import requests
import json
import os
import tempfile
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://d608964e-3bc2-49ac-82ce-24fb220fc6c6.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class ResumePreviewTester:
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test(self, test_name, passed, details=""):
        """Log test results"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = f"{status}: {test_name}"
        if details:
            result += f" - {details}"
        
        self.test_results.append(result)
        print(result)
        
    def create_test_resume_files(self):
        """Create test resume files in different formats"""
        test_files = {}
        
        # Sample resume content (realistic and substantial)
        resume_content = """JANE SMITH
Senior Software Engineer
Email: jane.smith@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/janesmith | GitHub: github.com/janesmith

PROFESSIONAL SUMMARY
Experienced Senior Software Engineer with 8+ years of expertise in full-stack development, 
cloud architecture, and team leadership. Proven track record of delivering scalable web 
applications using modern technologies including React, Node.js, Python, and AWS. 
Strong background in agile methodologies, code review processes, and mentoring junior developers.

TECHNICAL SKILLS
• Programming Languages: JavaScript, Python, TypeScript, Java, C++
• Frontend Technologies: React, Vue.js, Angular, HTML5, CSS3, SASS, Bootstrap
• Backend Technologies: Node.js, Express.js, Django, Flask, Spring Boot
• Databases: PostgreSQL, MongoDB, MySQL, Redis, DynamoDB
• Cloud Platforms: AWS (EC2, S3, Lambda, RDS), Azure, Google Cloud Platform
• DevOps Tools: Docker, Kubernetes, Jenkins, GitLab CI/CD, Terraform
• Version Control: Git, GitHub, GitLab, Bitbucket
• Testing: Jest, Cypress, Selenium, PyTest, JUnit
• Other: RESTful APIs, GraphQL, Microservices, Agile/Scrum

PROFESSIONAL EXPERIENCE

Senior Software Engineer | TechCorp Solutions | 2020 - Present
• Led development of a customer-facing web application serving 100K+ daily active users
• Architected and implemented microservices infrastructure reducing system latency by 40%
• Mentored team of 5 junior developers, conducting code reviews and technical training sessions
• Collaborated with product managers and designers to deliver features on time and within budget
• Implemented automated testing strategies increasing code coverage from 60% to 95%
• Optimized database queries and caching strategies improving application performance by 35%

Software Engineer | InnovateTech Inc. | 2018 - 2020
• Developed and maintained multiple React-based web applications for e-commerce platform
• Built RESTful APIs using Node.js and Express.js handling 10M+ requests per day
• Integrated third-party payment systems including Stripe, PayPal, and Square
• Participated in agile development process with 2-week sprint cycles
• Contributed to open-source projects and internal developer tools
• Reduced bug reports by 50% through implementation of comprehensive testing suite

Junior Software Developer | StartupXYZ | 2016 - 2018
• Developed responsive web interfaces using HTML5, CSS3, and JavaScript
• Assisted in migration from monolithic architecture to microservices
• Participated in daily standups, sprint planning, and retrospective meetings
• Gained experience with version control systems and collaborative development workflows
• Contributed to documentation and knowledge sharing initiatives

EDUCATION
Bachelor of Science in Computer Science | University of Technology | 2016
• Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Engineering
• Senior Project: Developed a machine learning-based recommendation system
• GPA: 3.8/4.0, Dean's List (4 semesters)

CERTIFICATIONS
• AWS Certified Solutions Architect - Associate (2021)
• Certified Scrum Master (CSM) (2020)
• Google Cloud Professional Developer (2019)

PROJECTS
E-Commerce Platform Redesign (2021)
• Led frontend redesign using React and TypeScript improving user engagement by 25%
• Implemented responsive design supporting mobile, tablet, and desktop devices
• Integrated analytics tracking and A/B testing framework

Real-Time Chat Application (2020)
• Built scalable chat application using Socket.io, Node.js, and MongoDB
• Implemented user authentication, message encryption, and file sharing features
• Deployed on AWS using Docker containers and load balancers

ACHIEVEMENTS
• Increased team productivity by 30% through implementation of automated deployment pipeline
• Reduced customer support tickets by 40% through improved error handling and user experience
• Recognized as "Employee of the Quarter" for outstanding technical contributions (Q3 2021)
• Speaker at TechConf 2021: "Building Scalable Web Applications with Modern JavaScript"

LANGUAGES
• English (Native)
• Spanish (Conversational)
• French (Basic)

INTERESTS
• Open source contributions, technical blogging, hiking, photography, chess"""

        # Create TXT file
        txt_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        txt_file.write(resume_content)
        txt_file.close()
        test_files['txt'] = txt_file.name
        
        # For PDF and DOCX, we'll create simple text files with appropriate extensions
        # In a real scenario, these would be proper binary files
        pdf_file = tempfile.NamedTemporaryFile(mode='w', suffix='.pdf', delete=False, encoding='utf-8')
        pdf_file.write(resume_content)  # Simplified for testing
        pdf_file.close()
        test_files['pdf'] = pdf_file.name
        
        docx_file = tempfile.NamedTemporaryFile(mode='w', suffix='.docx', delete=False, encoding='utf-8')
        docx_file.write(resume_content)  # Simplified for testing
        docx_file.close()
        test_files['docx'] = docx_file.name
        
        return test_files, resume_content
    
    def cleanup_test_files(self, test_files):
        """Clean up temporary test files"""
        for file_path in test_files.values():
            try:
                os.unlink(file_path)
            except:
                pass
    
    def test_backend_connectivity(self):
        """Test basic backend connectivity"""
        try:
            response = requests.get(f"{API_BASE}/health", timeout=10)
            if response.status_code in [200, 404, 405]:  # 404/405 means server is responding
                self.log_test("Backend Connectivity", True, f"Status: {response.status_code}")
                return True
            else:
                self.log_test("Backend Connectivity", False, f"Unexpected status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Connectivity", False, f"Connection error: {str(e)}")
            return False
    
    def test_resume_upload_endpoint(self, file_path, file_type, expected_content):
        """Test resume upload endpoint with specific file type"""
        try:
            with open(file_path, 'rb') as f:
                files = {'resume': (f"test_resume.{file_type}", f, 'application/octet-stream')}
                
                response = requests.post(
                    f"{API_BASE}/admin/upload",
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                required_fields = ['success', 'preview', 'full_text', 'filename', 'message']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(f"{file_type.upper()} Upload Response Structure", False, 
                                f"Missing fields: {missing_fields}")
                    return False
                
                # Check preview content
                preview_content = data.get('preview', '')
                preview_length = len(preview_content)
                
                # Verify preview is not truncated (should be substantial content)
                if preview_length < 200:
                    self.log_test(f"{file_type.upper()} Upload Preview Length", False, 
                                f"Preview too short: {preview_length} chars")
                    return False
                
                # Check for truncation indicators
                has_ellipsis = '...' in preview_content[-10:]  # Check end of content
                if has_ellipsis:
                    self.log_test(f"{file_type.upper()} Upload Truncation Check", False, 
                                "Found truncation indicators")
                    return False
                
                # Verify content preservation
                full_text = data.get('full_text', '')
                content_ratio = len(preview_content) / len(full_text) if full_text else 0
                
                if content_ratio < 0.9:  # Should preserve at least 90% of content
                    self.log_test(f"{file_type.upper()} Upload Content Preservation", False, 
                                f"Content ratio: {content_ratio:.2f}")
                    return False
                
                self.log_test(f"{file_type.upper()} File Upload", True, 
                            f"Preview length: {preview_length} chars, Content ratio: {content_ratio:.2f}")
                return True
                
            else:
                error_detail = "Unknown error"
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', str(error_data))
                except:
                    error_detail = response.text[:100]
                
                self.log_test(f"{file_type.upper()} File Upload", False, 
                            f"Status: {response.status_code}, Error: {error_detail}")
                return False
                
        except Exception as e:
            self.log_test(f"{file_type.upper()} File Upload", False, f"Exception: {str(e)}")
            return False
    
    def test_preview_content_quality(self, file_path, file_type):
        """Test the quality and completeness of preview content"""
        try:
            with open(file_path, 'rb') as f:
                files = {'resume': (f"test_resume.{file_type}", f, 'application/octet-stream')}
                
                response = requests.post(
                    f"{API_BASE}/admin/upload",
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                preview_content = data.get('preview', '')
                
                # Check for key resume sections
                key_sections = ['PROFESSIONAL SUMMARY', 'TECHNICAL SKILLS', 'PROFESSIONAL EXPERIENCE', 'EDUCATION']
                found_sections = sum(1 for section in key_sections if section in preview_content)
                
                if found_sections >= 3:  # Should find most key sections
                    self.log_test(f"{file_type.upper()} Preview Content Quality", True, 
                                f"Found {found_sections}/{len(key_sections)} key sections")
                    return True
                else:
                    self.log_test(f"{file_type.upper()} Preview Content Quality", False, 
                                f"Only found {found_sections}/{len(key_sections)} key sections")
                    return False
            else:
                self.log_test(f"{file_type.upper()} Preview Content Quality", False, 
                            f"Upload failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test(f"{file_type.upper()} Preview Content Quality", False, f"Exception: {str(e)}")
            return False
    
    def test_scrollable_display_suitability(self, file_path, file_type):
        """Test if preview content is suitable for scrollable display"""
        try:
            with open(file_path, 'rb') as f:
                files = {'resume': (f"test_resume.{file_type}", f, 'application/octet-stream')}
                
                response = requests.post(
                    f"{API_BASE}/admin/upload",
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                preview_content = data.get('preview', '')
                
                # Check line breaks and formatting
                line_count = preview_content.count('\n')
                has_proper_formatting = line_count > 10  # Should have multiple lines
                
                # Check content length suitable for scrolling
                is_scrollable_length = len(preview_content) > 1000  # Should be substantial
                
                if has_proper_formatting and is_scrollable_length:
                    self.log_test(f"{file_type.upper()} Scrollable Display Suitability", True, 
                                f"Lines: {line_count}, Length: {len(preview_content)} chars")
                    return True
                else:
                    self.log_test(f"{file_type.upper()} Scrollable Display Suitability", False, 
                                f"Lines: {line_count}, Length: {len(preview_content)} chars")
                    return False
            else:
                self.log_test(f"{file_type.upper()} Scrollable Display Suitability", False, 
                            f"Upload failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test(f"{file_type.upper()} Scrollable Display Suitability", False, f"Exception: {str(e)}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all comprehensive tests for resume preview functionality"""
        print("=" * 80)
        print("🧪 COMPREHENSIVE RESUME PREVIEW FUNCTIONALITY TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"API Base: {API_BASE}")
        print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Test 1: Backend Connectivity
        print("📡 Testing Backend Connectivity...")
        if not self.test_backend_connectivity():
            print("❌ Backend connectivity failed. Stopping tests.")
            return self.generate_summary()
        
        # Create test files
        print("\n📄 Creating Test Resume Files...")
        test_files, expected_content = self.create_test_resume_files()
        
        try:
            # Test 2: Resume Upload Functionality for Multiple Formats
            print("\n📤 Testing Resume Upload Functionality...")
            for file_type in ['txt', 'pdf', 'docx']:
                if file_type in test_files:
                    self.test_resume_upload_endpoint(test_files[file_type], file_type, expected_content)
            
            # Test 3: Preview Content Quality
            print("\n🔍 Testing Preview Content Quality...")
            for file_type in ['txt', 'pdf', 'docx']:
                if file_type in test_files:
                    self.test_preview_content_quality(test_files[file_type], file_type)
            
            # Test 4: Scrollable Display Suitability
            print("\n📜 Testing Scrollable Display Suitability...")
            for file_type in ['txt', 'pdf', 'docx']:
                if file_type in test_files:
                    self.test_scrollable_display_suitability(test_files[file_type], file_type)
            
        finally:
            # Cleanup
            self.cleanup_test_files(test_files)
        
        return self.generate_summary()
    
    def generate_summary(self):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        for result in self.test_results:
            print(result)
        
        print("\n" + "=" * 80)
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"📈 OVERALL RESULTS: {self.passed_tests}/{self.total_tests} tests passed ({success_rate:.1f}% success rate)")
        
        if success_rate >= 90:
            print("🎉 EXCELLENT: Resume preview functionality is working perfectly!")
        elif success_rate >= 75:
            print("✅ GOOD: Resume preview functionality is mostly working with minor issues.")
        elif success_rate >= 50:
            print("⚠️  MODERATE: Resume preview functionality has some significant issues.")
        else:
            print("❌ CRITICAL: Resume preview functionality has major problems.")
        
        print("=" * 80)
        
        return {
            'total_tests': self.total_tests,
            'passed_tests': self.passed_tests,
            'success_rate': success_rate,
            'results': self.test_results
        }

def main():
    """Main test execution function"""
    tester = ResumePreviewTester()
    results = tester.run_comprehensive_tests()
    
    # Return appropriate exit code
    if results['success_rate'] >= 75:
        exit(0)  # Success
    else:
        exit(1)  # Failure

if __name__ == "__main__":
    main()