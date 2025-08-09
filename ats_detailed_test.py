#!/usr/bin/env python3
"""
Detailed ATS Score Calculator Test with Gemini API Verification
"""

import requests
import json
import os
import tempfile
from datetime import datetime

# Configuration
BACKEND_URL = "https://e143a5dd-640d-4366-979e-f44e8b4324a2.preview.emergentagent.com"
ATS_ENDPOINT = f"{BACKEND_URL}/api/placement-preparation/ats-score-calculate"

def create_comprehensive_resume():
    """Create a comprehensive resume for better Gemini API testing"""
    resume_content = """
SARAH JOHNSON
Senior Full Stack Developer & Technical Lead
📧 sarah.johnson@email.com | 📱 (555) 987-6543
🔗 LinkedIn: linkedin.com/in/sarahjohnson | 💻 GitHub: github.com/sarahjohnson
📍 San Francisco, CA

PROFESSIONAL SUMMARY
Highly accomplished Senior Full Stack Developer with 10+ years of experience building scalable web applications and leading cross-functional teams. Expert in Python, JavaScript, React, and cloud technologies with a proven track record of delivering enterprise-grade solutions that serve millions of users. Passionate about mentoring junior developers and implementing best practices for code quality and system architecture.

CORE TECHNICAL SKILLS
• Programming Languages: Python (Expert), JavaScript/TypeScript (Expert), Java (Advanced), Go (Intermediate), SQL (Expert)
• Frontend Technologies: React (Expert), Vue.js (Advanced), Angular (Intermediate), HTML5/CSS3 (Expert), Tailwind CSS, Bootstrap
• Backend Frameworks: FastAPI (Expert), Django (Expert), Node.js/Express (Advanced), Flask (Advanced), Spring Boot (Intermediate)
• Databases: PostgreSQL (Expert), MongoDB (Advanced), MySQL (Advanced), Redis (Advanced), Elasticsearch (Intermediate)
• Cloud Platforms: AWS (Expert - Solutions Architect Certified), Google Cloud Platform (Advanced), Azure (Intermediate)
• DevOps & Tools: Docker (Expert), Kubernetes (Advanced), Jenkins (Advanced), GitLab CI/CD (Expert), Terraform (Advanced)
• Testing: Jest, Pytest, Selenium, Cypress, Unit Testing, Integration Testing, TDD/BDD
• Version Control: Git, GitHub, GitLab, Bitbucket
• Monitoring: Prometheus, Grafana, ELK Stack, New Relic, DataDog

PROFESSIONAL EXPERIENCE

Senior Technical Lead | TechGiant Corp | March 2021 - Present
• Lead a team of 12 engineers across 3 product squads, delivering features for 5M+ daily active users
• Architected and implemented microservices migration from monolithic architecture, reducing deployment time by 75%
• Designed and built real-time analytics platform using Python/FastAPI, React, and AWS, processing 100M+ events daily
• Increased system performance by 60% through database optimization, caching strategies, and code refactoring
• Implemented comprehensive CI/CD pipelines using GitLab and AWS, achieving 99.9% uptime
• Mentored 8 junior developers, with 6 receiving promotions within 18 months
• Reduced infrastructure costs by 40% through cloud optimization and resource management
• Led technical interviews and hiring process, building high-performing engineering teams

Senior Full Stack Developer | InnovateStartup | June 2019 - February 2021
• Built core SaaS platform from ground up using React, FastAPI, and PostgreSQL, scaling to 100,000+ users
• Developed RESTful APIs and GraphQL endpoints serving 1M+ requests per day
• Implemented real-time features using WebSockets and Redis for collaborative editing functionality
• Created automated testing suite achieving 95% code coverage and reducing bugs by 80%
• Optimized database queries and implemented caching, improving page load times by 50%
• Collaborated with product managers and designers in agile environment, delivering 25+ major features
• Integrated third-party APIs including Stripe, SendGrid, and AWS services

Full Stack Developer | WebSolutions Inc. | August 2017 - May 2019
• Developed and maintained 15+ client web applications using Django, React, and PostgreSQL
• Built responsive frontend interfaces with modern JavaScript frameworks and CSS preprocessors
• Implemented secure authentication systems and role-based access control
• Created data visualization dashboards using D3.js and Chart.js for business intelligence
• Optimized application performance through code splitting, lazy loading, and CDN implementation
• Worked directly with clients to gather requirements and provide technical consultation

Software Developer | StartupLab | January 2015 - July 2017
• Developed web applications using Python/Django and JavaScript for various startup clients
• Built RESTful APIs and integrated with external services and payment gateways
• Implemented responsive designs and cross-browser compatibility
• Participated in code reviews and maintained high code quality standards
• Contributed to open-source projects and internal tool development

EDUCATION
Master of Science in Computer Science | Stanford University | 2014
• Specialization: Software Engineering and Distributed Systems
• GPA: 3.9/4.0 | Dean's List: 4 semesters
• Thesis: "Scalable Microservices Architecture for Real-time Data Processing"

Bachelor of Science in Computer Science | UC Berkeley | 2012
• Magna Cum Laude | GPA: 3.8/4.0
• Relevant Coursework: Data Structures, Algorithms, Database Systems, Software Engineering, Computer Networks

CERTIFICATIONS & TRAINING
• AWS Certified Solutions Architect - Professional (2023)
• AWS Certified Developer - Associate (2022)
• Google Cloud Professional Developer (2022)
• Certified Kubernetes Administrator (CKA) (2023)
• MongoDB Certified Developer (2021)
• Scrum Master Certification (2020)

NOTABLE PROJECTS

E-Commerce Platform Modernization (2023)
• Led complete rewrite of legacy e-commerce system serving 2M+ customers
• Technologies: React, FastAPI, PostgreSQL, Redis, AWS, Docker, Kubernetes
• Results: 70% improvement in page load times, 45% increase in conversion rates, 50% reduction in server costs
• Implemented advanced features: real-time inventory, personalized recommendations, multi-currency support

Real-time Collaboration Platform (2022)
• Built Slack-like collaboration tool with real-time messaging, file sharing, and video calls
• Technologies: React, Node.js, Socket.io, MongoDB, WebRTC, AWS
• Scaled to support 50,000+ concurrent users with sub-100ms message delivery
• Implemented end-to-end encryption and advanced security features

AI-Powered Analytics Dashboard (2021)
• Developed machine learning pipeline for predictive analytics and business intelligence
• Technologies: Python, TensorFlow, FastAPI, React, PostgreSQL, AWS SageMaker
• Processed 10TB+ of data daily, providing real-time insights and forecasting
• Achieved 92% prediction accuracy for customer behavior modeling

ACHIEVEMENTS & RECOGNITION
• "Technical Excellence Award" - TechGiant Corp (2023)
• "Innovation Leader of the Year" - InnovateStartup (2020)
• Speaker at PyCon 2022: "Building Scalable APIs with FastAPI"
• Open source contributor: 500+ GitHub stars across personal projects
• Technical blog with 10,000+ monthly readers
• Increased team productivity by 45% through process improvements and tooling
• Successfully delivered 50+ projects on time and within budget
• Reduced critical bugs in production by 85% through improved testing practices

LEADERSHIP & MENTORSHIP
• Mentored 15+ junior developers throughout career
• Led technical architecture decisions for $10M+ revenue products
• Established engineering best practices and coding standards
• Organized internal tech talks and knowledge sharing sessions
• Built and scaled engineering teams from 3 to 15 members

TECHNICAL WRITING & SPEAKING
• Published 25+ technical articles on Medium and personal blog
• Conference speaker at React Summit, PyCon, and AWS re:Invent
• Created internal documentation and training materials
• Contributed to technical decision-making and architecture reviews
"""
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_file.write(resume_content)
    temp_file.close()
    
    return temp_file.name

def test_comprehensive_ats_analysis():
    """Test ATS analysis with comprehensive resume to trigger full Gemini analysis"""
    print("🔬 COMPREHENSIVE ATS ANALYSIS TEST")
    print("=" * 60)
    
    # Detailed job description to match the comprehensive resume
    job_title = "Senior Full Stack Developer - Technical Lead"
    job_description = """
We are seeking an exceptional Senior Full Stack Developer to join our engineering leadership team and drive technical excellence across our platform.

ROLE OVERVIEW:
As a Senior Full Stack Developer and Technical Lead, you will architect scalable solutions, mentor engineering teams, and lead the development of mission-critical applications serving millions of users globally.

KEY RESPONSIBILITIES:
• Lead technical architecture and design decisions for complex, distributed systems
• Mentor and guide a team of 8-12 engineers across multiple product areas
• Drive technical excellence through code reviews, best practices, and engineering standards
• Collaborate with product managers, designers, and stakeholders to deliver high-impact features
• Optimize system performance, scalability, and reliability for enterprise-grade applications
• Implement and maintain CI/CD pipelines and DevOps best practices
• Participate in technical interviews and help build world-class engineering teams

REQUIRED TECHNICAL SKILLS:
• 8+ years of professional software development experience
• Expert-level proficiency in Python and JavaScript/TypeScript
• Deep experience with modern frontend frameworks (React, Vue.js, or Angular)
• Strong backend development skills with FastAPI, Django, or Node.js
• Extensive experience with cloud platforms (AWS, GCP, or Azure)
• Proficiency with containerization (Docker) and orchestration (Kubernetes)
• Experience with both SQL (PostgreSQL, MySQL) and NoSQL (MongoDB, Redis) databases
• Strong understanding of microservices architecture and distributed systems
• Experience with CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
• Knowledge of monitoring and observability tools (Prometheus, Grafana, ELK Stack)

PREFERRED QUALIFICATIONS:
• Master's degree in Computer Science or related field
• AWS/GCP/Azure certifications (Solutions Architect, Developer, or equivalent)
• Experience with machine learning and data processing pipelines
• Track record of scaling applications to millions of users
• Open source contributions and technical writing experience
• Conference speaking or technical leadership experience
• Experience with performance optimization and system architecture
• Knowledge of security best practices and compliance requirements

LEADERSHIP REQUIREMENTS:
• Proven experience leading and mentoring engineering teams
• Strong communication skills and ability to work with cross-functional teams
• Experience with agile development methodologies
• Track record of delivering complex projects on time and within budget
• Ability to make technical decisions and drive consensus across teams
• Experience with hiring and building high-performing engineering teams

WHAT WE OFFER:
• Competitive salary range: $180,000 - $250,000 + equity
• Comprehensive health, dental, and vision insurance
• Flexible work arrangements (remote-friendly)
• Professional development budget and conference attendance
• Stock options and performance bonuses
• Collaborative and innovative work environment
• Opportunity to work on cutting-edge technology at scale

COMPANY CULTURE:
We value technical excellence, continuous learning, and collaborative problem-solving. Our engineering team is passionate about building products that make a real impact on millions of users worldwide.
"""
    
    # Create comprehensive resume file
    resume_file_path = create_comprehensive_resume()
    
    try:
        print(f"📋 Job Title: {job_title}")
        print(f"📄 Resume File: {os.path.basename(resume_file_path)}")
        print(f"📊 Job Description Length: {len(job_description)} characters")
        print(f"📊 Resume Content Length: {os.path.getsize(resume_file_path)} bytes")
        print()
        
        # Prepare multipart form data
        with open(resume_file_path, 'rb') as resume_file:
            files = {
                'resume': ('sarah_johnson_resume.txt', resume_file, 'text/plain')
            }
            data = {
                'job_title': job_title,
                'job_description': job_description
            }
            
            print("🚀 Sending Comprehensive ATS Analysis Request...")
            print("   This may take 30-60 seconds for full Gemini API analysis...")
            print()
            
            # Make the request with longer timeout for Gemini processing
            response = requests.post(ATS_ENDPOINT, files=files, data=data, timeout=120)
            
            print(f"📊 Response Status: {response.status_code}")
            print()
            
            if response.status_code == 200:
                result = response.json()
                print("✅ COMPREHENSIVE ATS ANALYSIS SUCCESSFUL!")
                print("=" * 60)
                
                ats_score = result.get('ats_score', 0)
                analysis_text = result.get('analysis_text', '')
                
                print(f"🆔 ATS ID: {result.get('ats_id', 'N/A')}")
                print(f"📊 ATS Score: {ats_score}/100")
                print(f"📄 PDF Filename: {result.get('pdf_filename', 'N/A')}")
                print(f"📝 Analysis Length: {len(analysis_text)} characters")
                print()
                
                # Check if this is full Gemini analysis or fallback
                is_full_analysis = "Due to API limitations" not in analysis_text
                gemini_indicators = [
                    "KEYWORD ANALYSIS:",
                    "EXPERIENCE EVALUATION:",
                    "TECHNICAL COMPETENCY:",
                    "COMPREHENSIVE ATS SCORE:",
                    "PRIMARY ADVANTAGES:",
                    "CRITICAL GAP IDENTIFICATION:"
                ]
                
                gemini_score = sum(1 for indicator in gemini_indicators if indicator in analysis_text)
                
                print("🤖 GEMINI API ANALYSIS VERIFICATION:")
                print(f"   Full Analysis: {'✅ Yes' if is_full_analysis else '❌ No (Fallback used)'}")
                print(f"   Gemini Indicators Found: {gemini_score}/{len(gemini_indicators)}")
                print(f"   Analysis Depth: {'✅ Comprehensive' if gemini_score >= 4 else '❌ Basic'}")
                print()
                
                if is_full_analysis and gemini_score >= 4:
                    print("🎯 DETAILED ANALYSIS BREAKDOWN:")
                    print("-" * 50)
                    
                    # Extract key sections from the analysis
                    sections = analysis_text.split('\n')
                    current_section = ""
                    
                    for line in sections[:30]:  # Show first 30 lines
                        if any(indicator in line for indicator in gemini_indicators):
                            current_section = line.strip()
                            print(f"📋 {current_section}")
                        elif line.strip() and current_section:
                            print(f"   {line.strip()}")
                    
                    print("-" * 50)
                
                # Test PDF download
                if result.get('pdf_filename'):
                    ats_id = result.get('ats_id')
                    pdf_url = f"{BACKEND_URL}/api/placement-preparation/ats-score/{ats_id}/download"
                    
                    print(f"📥 Testing PDF Download...")
                    pdf_response = requests.get(pdf_url, timeout=30)
                    
                    if pdf_response.status_code == 200:
                        print(f"✅ PDF Download Successful - Size: {len(pdf_response.content)} bytes")
                        
                        # Save PDF for inspection
                        pdf_path = f"/tmp/ats_test_report_{ats_id[:8]}.pdf"
                        with open(pdf_path, 'wb') as f:
                            f.write(pdf_response.content)
                        print(f"📄 PDF saved to: {pdf_path}")
                    else:
                        print(f"❌ PDF Download Failed - Status: {pdf_response.status_code}")
                
                return {
                    'success': True,
                    'ats_score': ats_score,
                    'full_gemini_analysis': is_full_analysis,
                    'gemini_indicators': gemini_score,
                    'analysis_length': len(analysis_text)
                }
                
            else:
                print(f"❌ ATS ANALYSIS FAILED!")
                print(f"   Status Code: {response.status_code}")
                print(f"   Response: {response.text}")
                return {'success': False, 'error': response.text}
                
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return {'success': False, 'error': str(e)}
    finally:
        # Clean up temporary file
        try:
            os.unlink(resume_file_path)
        except:
            pass

if __name__ == "__main__":
    print("🔬 DETAILED ATS SCORE CALCULATOR TESTING")
    print("=" * 60)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    result = test_comprehensive_ats_analysis()
    
    print("\n" + "=" * 60)
    if result.get('success'):
        print("🎉 COMPREHENSIVE ATS TESTING COMPLETED!")
        print("✅ Key Results:")
        print(f"   • ATS Score Generated: {result.get('ats_score', 'N/A')}/100")
        print(f"   • Full Gemini Analysis: {'Yes' if result.get('full_gemini_analysis') else 'No'}")
        print(f"   • Analysis Indicators: {result.get('gemini_indicators', 0)}/6")
        print(f"   • Analysis Length: {result.get('analysis_length', 0)} characters")
        
        if result.get('full_gemini_analysis'):
            print("🤖 Gemini API is working correctly with comprehensive analysis!")
        else:
            print("⚠️  Using fallback analysis - Gemini API may have issues")
    else:
        print("❌ COMPREHENSIVE ATS TESTING FAILED!")
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    print("=" * 60)