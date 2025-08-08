#!/usr/bin/env python3
"""
Focused Testing for Placement Preparation Resume Upload Truncation Fix
Specifically tests the 200-character truncation limit fix and full preview content
"""

import requests
import json
import os
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from docx import Document

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://3b3e66ec-f27f-42ff-b407-1f9f120f4842.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class TruncationFixTester:
    def __init__(self):
        self.test_results = []
        self.backend_url = API_BASE
        print(f"🔧 Testing Backend URL: {self.backend_url}")
        
    def log_result(self, test_name, success, details):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def create_long_resume_content(self, min_length=800):
        """Create resume content significantly longer than 200 characters"""
        content = """JANE SMITH
Senior Full Stack Developer
Email: jane.smith@techcorp.com | Phone: (555) 987-6543
LinkedIn: linkedin.com/in/janesmith | GitHub: github.com/janesmith

PROFESSIONAL SUMMARY
Highly experienced Senior Full Stack Developer with over 10 years of expertise in designing, developing, and deploying scalable web applications. Proficient in modern JavaScript frameworks, cloud technologies, and agile development methodologies. Demonstrated ability to lead cross-functional teams, mentor junior developers, and deliver high-quality software solutions that drive business growth. Strong background in both frontend and backend technologies with a passion for creating user-centric applications.

TECHNICAL EXPERTISE
Frontend Technologies: React.js, Vue.js, Angular, TypeScript, JavaScript (ES6+), HTML5, CSS3, SASS/SCSS, Bootstrap, Tailwind CSS, Material-UI, Redux, Vuex, Webpack, Vite
Backend Technologies: Node.js, Express.js, Python, Django, FastAPI, Java, Spring Boot, C#, .NET Core, PHP, Laravel
Databases: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, DynamoDB, Firebase Firestore
Cloud Platforms: Amazon Web Services (AWS), Microsoft Azure, Google Cloud Platform (GCP), Heroku, Vercel, Netlify
DevOps & Tools: Docker, Kubernetes, Jenkins, GitLab CI/CD, GitHub Actions, Terraform, Ansible, Nginx, Apache
Testing: Jest, Cypress, Selenium, PyTest, JUnit, Mocha, Chai, React Testing Library
Version Control: Git, GitHub, GitLab, Bitbucket, SVN

PROFESSIONAL EXPERIENCE

Senior Full Stack Developer | TechCorp Solutions | January 2020 - Present
• Lead development of enterprise-level web applications serving over 2 million active users
• Architected and implemented microservices infrastructure reducing system latency by 60%
• Mentored team of 8 junior and mid-level developers, conducting code reviews and technical training sessions
• Designed and developed RESTful APIs and GraphQL endpoints with 99.95% uptime
• Implemented automated CI/CD pipelines reducing deployment time from 4 hours to 15 minutes
• Collaborated with product managers, UX designers, and stakeholders to define technical requirements
• Optimized database queries and implemented caching strategies improving application performance by 45%
• Led migration from monolithic architecture to microservices, improving scalability and maintainability

Full Stack Developer | InnovateTech Startup | March 2018 - December 2019
• Developed responsive web applications using React, Node.js, and MongoDB
• Built comprehensive testing suites achieving 95% code coverage across all projects
• Integrated multiple third-party APIs including payment processors, social media platforms, and analytics tools
• Participated in agile development cycles, sprint planning, and daily standups
• Contributed to open-source projects and maintained technical documentation
• Implemented real-time features using WebSocket technology for chat and notification systems

Software Developer | Digital Solutions Inc | June 2015 - February 2018
• Developed and maintained web applications using PHP, MySQL, and jQuery
• Created automated testing scripts reducing manual testing time by 70%
• Collaborated with cross-functional teams to deliver projects on time and within budget
• Implemented responsive design principles ensuring compatibility across all devices
• Participated in code reviews and contributed to coding standards documentation

EDUCATION
Master of Science in Computer Science
Stanford University | 2013 - 2015
Specialization: Software Engineering and Distributed Systems
Thesis: "Scalable Microservices Architecture for Real-time Data Processing"
GPA: 3.9/4.0

Bachelor of Science in Computer Science
University of California, Berkeley | 2009 - 2013
Magna Cum Laude, GPA: 3.8/4.0
Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Engineering, Computer Networks

CERTIFICATIONS & ACHIEVEMENTS
• AWS Certified Solutions Architect - Professional (2023)
• Google Cloud Professional Developer (2022)
• Certified Kubernetes Administrator (CKA) (2021)
• Microsoft Azure Developer Associate (2020)
• Scrum Master Certification (2019)
• Winner of TechCorp Innovation Award 2022 for developing AI-powered recommendation system
• Speaker at React Conference 2023: "Building Scalable Frontend Architectures"
• Published article in IEEE Software Magazine: "Best Practices for Microservices Development"

NOTABLE PROJECTS
E-Commerce Platform Redesign: Led complete redesign of e-commerce platform handling 50K+ daily transactions, resulting in 35% increase in conversion rates and 40% improvement in page load times.

Real-time Collaboration Tool: Developed real-time collaboration platform similar to Slack, supporting 10K+ concurrent users with features including file sharing, video calls, and screen sharing.

AI-Powered Analytics Dashboard: Created comprehensive analytics dashboard with machine learning capabilities for predictive analysis, used by C-suite executives for strategic decision making.

Mobile-First Progressive Web App: Built PWA for retail client achieving 99% performance score on Lighthouse and increasing mobile engagement by 60%.

This resume content is intentionally comprehensive and significantly longer than 200 characters to thoroughly test the truncation fix implementation. The content should appear in full in the preview field without any truncation or ellipsis indicators, making it suitable for display in a scrollable box interface."""
        
        # Ensure content is longer than minimum required length
        while len(content) < min_length:
            content += "\n\nADDITIONAL SKILLS: Advanced proficiency in emerging technologies and continuous learning mindset."
        
        return content
    
    def create_test_files(self):
        """Create test files with long content"""
        content = self.create_long_resume_content(1000)  # Ensure at least 1000 characters
        files = []
        
        # Create TXT file
        txt_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        txt_file.write(content)
        txt_file.close()
        files.append(('txt', txt_file.name, content))
        
        # Create PDF file
        pdf_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        pdf_file.close()
        
        c = canvas.Canvas(pdf_file.name, pagesize=letter)
        width, height = letter
        lines = content.split('\n')
        y_position = height - 50
        
        for line in lines:
            if y_position < 50:
                c.showPage()
                y_position = height - 50
            
            if len(line) > 80:
                words = line.split(' ')
                current_line = ""
                for word in words:
                    if len(current_line + word) < 80:
                        current_line += word + " "
                    else:
                        if current_line:
                            c.drawString(50, y_position, current_line.strip())
                            y_position -= 15
                        current_line = word + " "
                if current_line:
                    c.drawString(50, y_position, current_line.strip())
                    y_position -= 15
            else:
                c.drawString(50, y_position, line)
                y_position -= 15
        
        c.save()
        files.append(('pdf', pdf_file.name, content))
        
        # Create DOCX file
        docx_file = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
        docx_file.close()
        
        doc = Document()
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())
        doc.save(docx_file.name)
        files.append(('docx', docx_file.name, content))
        
        return files
    
    def test_truncation_fix(self, file_type, file_path, expected_content):
        """Test the specific truncation fix for placement preparation upload"""
        try:
            with open(file_path, 'rb') as f:
                files = {'resume': (os.path.basename(file_path), f, f'application/{file_type}')}
                
                response = requests.post(
                    f"{self.backend_url}/admin/upload",
                    files=files,
                    timeout=30
                )
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get('success'):
                    self.log_result(f"Truncation Fix Test - {file_type.upper()}", False, "Upload failed")
                    return False
                
                preview_content = data.get('preview', '')
                
                # CRITICAL VERIFICATION POINTS
                verification_results = []
                
                # 1. Verify preview content is significantly longer than 200 characters
                if len(preview_content) > 200:
                    verification_results.append("✅ Preview > 200 characters")
                else:
                    verification_results.append(f"❌ Preview only {len(preview_content)} characters")
                
                # 2. Verify NO ellipsis truncation indicators
                if '...' not in preview_content:
                    verification_results.append("✅ No ellipsis indicators")
                else:
                    verification_results.append("❌ Found ellipsis indicators")
                
                # 3. Verify preview contains substantial original content
                first_100_chars = expected_content[:100].strip()
                if first_100_chars in preview_content:
                    verification_results.append("✅ Contains original content")
                else:
                    verification_results.append("❌ Missing original content")
                
                # 4. Verify content preservation ratio
                content_ratio = len(preview_content) / len(expected_content)
                if content_ratio >= 0.8:
                    verification_results.append(f"✅ Content ratio: {content_ratio:.2f}")
                else:
                    verification_results.append(f"❌ Low content ratio: {content_ratio:.2f}")
                
                # 5. Verify suitable for scrollable display (full content)
                if len(preview_content) >= 500:  # Should be substantial for scrollable display
                    verification_results.append("✅ Suitable for scrollable display")
                else:
                    verification_results.append("❌ Too short for scrollable display")
                
                # Overall success determination
                success = all('✅' in result for result in verification_results)
                
                details = f"Preview length: {len(preview_content)} chars. " + " | ".join(verification_results)
                self.log_result(f"Truncation Fix Test - {file_type.upper()}", success, details)
                
                # Additional detailed output
                print(f"   📊 Original content: {len(expected_content)} characters")
                print(f"   📊 Preview content: {len(preview_content)} characters")
                print(f"   📊 Preservation ratio: {content_ratio:.2f}")
                print(f"   🔍 Preview sample (first 100 chars): {preview_content[:100]}...")
                
                return success
                
            else:
                self.log_result(f"Truncation Fix Test - {file_type.upper()}", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result(f"Truncation Fix Test - {file_type.upper()}", False, f"Exception: {str(e)}")
            return False
    
    def cleanup_files(self, files):
        """Clean up temporary test files"""
        for file_type, file_path, content in files:
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"⚠️  Warning: Could not delete {file_type} file: {e}")
    
    def run_truncation_tests(self):
        """Run comprehensive truncation fix tests"""
        print("🚀 PLACEMENT PREPARATION RESUME UPLOAD TRUNCATION FIX TESTING")
        print("🎯 Verifying 200-character truncation limit fix and full preview content")
        print("=" * 80)
        
        # Test backend connectivity
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            if response.status_code == 200:
                self.log_result("Backend Connectivity", True, "Backend is responding")
            else:
                self.log_result("Backend Connectivity", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Backend Connectivity", False, f"Connection failed: {str(e)}")
            return False
        
        # Create test files
        test_files = self.create_test_files()
        
        try:
            # Test each file format
            for file_type, file_path, expected_content in test_files:
                print(f"\n📄 Testing {file_type.upper()} file truncation fix...")
                self.test_truncation_fix(file_type, file_path, expected_content)
            
        finally:
            # Clean up
            self.cleanup_files(test_files)
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 TRUNCATION FIX TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        # Key findings
        print("\n🔍 KEY FINDINGS:")
        print("   • Testing endpoint: /api/admin/upload (placement preparation)")
        print("   • Focus: 200-character truncation fix verification")
        print("   • Expected: Full resume content in preview field")
        print("   • Expected: No '...' ellipsis indicators")
        print("   • Expected: Content suitable for scrollable box display")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
        
        return failed_tests == 0

def main():
    """Main test execution"""
    tester = TruncationFixTester()
    success = tester.run_truncation_tests()
    
    if success:
        print("\n🎉 ALL TRUNCATION FIX TESTS PASSED!")
        print("✅ The 200-character truncation fix is working correctly.")
        print("✅ Preview field contains full resume content without truncation.")
        print("✅ Content is suitable for scrollable box display.")
    else:
        print("\n⚠️  SOME TRUNCATION FIX TESTS FAILED!")
        print("❌ The truncation fix may need additional attention.")
    
    return success

if __name__ == "__main__":
    main()