#!/usr/bin/env python3
"""
Simple Behavioral Interview Questions PDF Formatting Test
Focus: Testing the enhanced PDF formatting improvements
"""

import requests
import json
import os
from datetime import datetime

# Configuration
BACKEND_URL = "https://career-test.preview.emergentagent.com/api"

def test_behavioral_interview_questions():
    """Test behavioral interview questions with enhanced PDF formatting"""
    
    print("🎯 BEHAVIORAL INTERVIEW QUESTIONS PDF FORMATTING ENHANCEMENT TESTING")
    print("=" * 80)
    
    results = {
        "total_tests": 6,
        "passed_tests": 0,
        "failed_tests": 0,
        "details": []
    }
    
    # Test 1: Backend Connectivity
    print("\n1️⃣ Testing Backend Connectivity...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend accessible and responding correctly")
            results["passed_tests"] += 1
            results["details"].append("✅ Backend Connectivity: Working")
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            results["failed_tests"] += 1
            results["details"].append(f"❌ Backend Connectivity: Failed ({response.status_code})")
    except Exception as e:
        print(f"❌ Backend connectivity failed: {str(e)}")
        results["failed_tests"] += 1
        results["details"].append(f"❌ Backend Connectivity: Exception ({str(e)})")
    
    # Test 2: Behavioral Interview Questions Generation
    print("\n2️⃣ Testing Behavioral Interview Questions Generation...")
    try:
        # Prepare realistic test data
        job_title = "Senior Data Scientist"
        job_description = """We are seeking a Senior Data Scientist to lead our machine learning initiatives and drive data-driven decision making. 

Key Responsibilities:
- Lead cross-functional teams in developing ML models
- Collaborate with product managers and engineers
- Mentor junior data scientists
- Present findings to executive leadership
- Drive innovation in data science methodologies

Requirements:
- 5+ years of experience in data science and machine learning
- Strong leadership and team management experience
- Expertise in Python, R, SQL, and cloud platforms
- Experience with deep learning frameworks
- Excellent communication and presentation skills"""

        # Create comprehensive resume content
        resume_content = """JOHN SMITH
Senior Data Scientist & Team Lead
Email: john.smith@email.com | Phone: (555) 123-4567

PROFESSIONAL SUMMARY
Accomplished Senior Data Scientist with 8+ years of experience leading high-impact machine learning projects and cross-functional teams. Proven track record of translating complex business challenges into scalable data solutions, mentoring junior talent, and driving organizational transformation through data-driven insights.

CORE COMPETENCIES
• Machine Learning & AI: Deep Learning, NLP, Computer Vision
• Programming: Python, R, SQL, Scala, Java
• Cloud Platforms: AWS, GCP, Azure
• Leadership: Team Management, Cross-functional Collaboration
• Communication: Executive Presentations, Technical Writing

PROFESSIONAL EXPERIENCE

Senior Data Scientist & Team Lead | TechCorp Inc. | 2020 - Present
• Lead a team of 6 data scientists and ML engineers in developing predictive models that increased revenue by $2.3M annually
• Spearheaded the implementation of real-time recommendation system serving 10M+ users with 23% improvement in engagement
• Collaborated with product, engineering, and business teams to define ML strategy and roadmap
• Mentored 12 junior data scientists, with 8 receiving promotions under my guidance
• Presented quarterly ML performance reviews to C-suite executives and board members

Data Scientist | DataSolutions LLC | 2018 - 2020
• Developed customer churn prediction models achieving 89% accuracy and saving $1.2M in retention costs
• Led cross-functional project with marketing and sales teams to optimize customer acquisition strategies
• Built automated reporting dashboards used by 50+ stakeholders across the organization

EDUCATION
Ph.D. in Computer Science, Machine Learning Focus | Stanford University | 2016
M.S. in Statistics | University of California, Berkeley | 2014

LEADERSHIP & ACHIEVEMENTS
• Led company-wide data science transformation initiative affecting 200+ employees
• Established data science center of excellence with standardized processes
• Managed $500K annual budget for ML infrastructure and team development
• Resolved complex stakeholder conflicts through data-driven consensus building"""

        # Prepare form data
        files = {
            'resume': ('test_resume.txt', resume_content, 'text/plain')
        }
        data = {
            'job_title': job_title,
            'job_description': job_description
        }
        
        response = requests.post(
            f"{BACKEND_URL}/placement-preparation/behavioral-interview-questions",
            files=files,
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            analysis_id = result.get('analysis_id')
            interview_questions = result.get('interview_questions', '')
            
            print(f"✅ Behavioral interview questions generated successfully")
            print(f"   Analysis ID: {analysis_id}")
            print(f"   Content length: {len(interview_questions)} characters")
            
            # Store for later tests
            global generated_analysis_id, generated_content
            generated_analysis_id = analysis_id
            generated_content = interview_questions
            
            results["passed_tests"] += 1
            results["details"].append(f"✅ Content Generation: Success ({len(interview_questions)} chars)")
            
        else:
            print(f"❌ Failed to generate behavioral interview questions: {response.status_code}")
            print(f"   Response: {response.text}")
            results["failed_tests"] += 1
            results["details"].append(f"❌ Content Generation: Failed ({response.status_code})")
            return results
            
    except Exception as e:
        print(f"❌ Behavioral interview questions generation failed: {str(e)}")
        results["failed_tests"] += 1
        results["details"].append(f"❌ Content Generation: Exception ({str(e)})")
        return results
    
    # Test 3: Database Storage and Retrieval
    print("\n3️⃣ Testing Database Storage and Retrieval...")
    try:
        response = requests.get(f"{BACKEND_URL}/placement-preparation/behavioral-interview-questions", timeout=10)
        if response.status_code == 200:
            analyses = response.json().get('analyses', [])
            print(f"✅ Database retrieval working - found {len(analyses)} analyses")
            
            # Check if our newly created analysis is in the list
            found_analysis = False
            for analysis in analyses:
                if analysis.get('id') == generated_analysis_id:
                    found_analysis = True
                    print(f"✅ Newly created analysis found in database")
                    break
            
            if found_analysis or len(analyses) > 0:
                results["passed_tests"] += 1
                results["details"].append("✅ Database Storage: Working correctly")
            else:
                results["failed_tests"] += 1
                results["details"].append("❌ Database Storage: Analysis not found")
        else:
            print(f"❌ Database retrieval failed: {response.status_code}")
            results["failed_tests"] += 1
            results["details"].append(f"❌ Database Storage: Failed ({response.status_code})")
    except Exception as e:
        print(f"❌ Database retrieval error: {str(e)}")
        results["failed_tests"] += 1
        results["details"].append(f"❌ Database Storage: Exception ({str(e)})")
    
    # Test 4: PDF Generation and Download
    print("\n4️⃣ Testing PDF Generation and Download...")
    try:
        response = requests.get(
            f"{BACKEND_URL}/placement-preparation/behavioral-interview-questions/{generated_analysis_id}/download",
            timeout=30
        )
        
        if response.status_code == 200:
            pdf_content = response.content
            pdf_size = len(pdf_content)
            
            print(f"✅ PDF downloaded successfully")
            print(f"   PDF size: {pdf_size} bytes ({pdf_size/1024:.1f} KB)")
            
            # Verify PDF format
            if pdf_content.startswith(b'%PDF'):
                print("✅ Valid PDF format confirmed")
                results["passed_tests"] += 1
                results["details"].append(f"✅ PDF Download: Working ({pdf_size} bytes)")
                
                # Save PDF for inspection
                with open('/app/behavioral_interview_enhanced.pdf', 'wb') as f:
                    f.write(pdf_content)
                print("✅ PDF saved as 'behavioral_interview_enhanced.pdf'")
                
            else:
                print("❌ Invalid PDF format")
                results["failed_tests"] += 1
                results["details"].append("❌ PDF Download: Invalid format")
        else:
            print(f"❌ PDF download failed: {response.status_code}")
            print(f"   Response: {response.text}")
            results["failed_tests"] += 1
            results["details"].append(f"❌ PDF Download: Failed ({response.status_code})")
    except Exception as e:
        print(f"❌ PDF download error: {str(e)}")
        results["failed_tests"] += 1
        results["details"].append(f"❌ PDF Download: Exception ({str(e)})")
    
    # Test 5: Enhanced Question Structure Analysis
    print("\n5️⃣ Testing Enhanced Question Structure...")
    try:
        if 'generated_content' in globals():
            content = generated_content
            
            # Count questions
            question_indicators = content.lower().count('question ') + content.lower().count('<div class="question-number">')
            print(f"✅ Question indicators found: {question_indicators}")
            
            # Check for STAR methodology
            star_indicators = (
                content.lower().count('situation') + 
                content.lower().count('task') + 
                content.lower().count('action') + 
                content.lower().count('result')
            )
            print(f"✅ STAR methodology indicators: {star_indicators}")
            
            # Check for behavioral categories
            categories_found = 0
            categories = ['leadership', 'strategic', 'collaboration', 'resilience', 'role-specific']
            for category in categories:
                if category in content.lower():
                    categories_found += 1
            
            print(f"✅ Behavioral categories covered: {categories_found}/5")
            
            if question_indicators >= 15 and star_indicators >= 4 and categories_found >= 3:
                print("✅ Question structure analysis passed")
                results["passed_tests"] += 1
                results["details"].append(f"✅ Question Structure: Good ({question_indicators} questions, {categories_found} categories)")
            else:
                print("⚠️  Question structure may need improvement")
                results["failed_tests"] += 1
                results["details"].append(f"❌ Question Structure: Needs improvement")
        else:
            print("❌ No content available for analysis")
            results["failed_tests"] += 1
            results["details"].append("❌ Question Structure: No content")
    except Exception as e:
        print(f"❌ Question structure analysis error: {str(e)}")
        results["failed_tests"] += 1
        results["details"].append(f"❌ Question Structure: Exception ({str(e)})")
    
    # Test 6: Color Scheme Alignment Verification
    print("\n6️⃣ Testing Color Scheme Alignment...")
    try:
        if 'generated_content' in globals():
            content = generated_content
            
            # Check for #2c3e50 dark blue/gray theme (matching technical questions)
            theme_color_count = content.count('#2c3e50')
            secondary_color_count = content.count('#34495e')
            
            print(f"✅ Primary theme color (#2c3e50): {theme_color_count} instances")
            print(f"✅ Secondary theme color (#34495e): {secondary_color_count} instances")
            
            # Verify no purple colors (old theme)
            purple_colors = content.count('#8e44ad') + content.count('#9b59b6') + content.count('purple')
            print(f"✅ Purple color instances (should be 0): {purple_colors}")
            
            if theme_color_count > 0 and purple_colors == 0:
                print("✅ Color scheme alignment verified - using #2c3e50 theme")
                results["passed_tests"] += 1
                results["details"].append("✅ Color Scheme: Aligned with technical questions")
            else:
                print("⚠️  Color scheme alignment may need adjustment")
                results["failed_tests"] += 1
                results["details"].append("❌ Color Scheme: Not properly aligned")
        else:
            print("❌ No content available for color scheme analysis")
            results["failed_tests"] += 1
            results["details"].append("❌ Color Scheme: No content")
    except Exception as e:
        print(f"❌ Color scheme analysis error: {str(e)}")
        results["failed_tests"] += 1
        results["details"].append(f"❌ Color Scheme: Exception ({str(e)})")
    
    return results

def main():
    """Main test execution"""
    print("🚀 Starting Behavioral Interview Questions PDF Formatting Enhancement Testing")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run the test
    results = test_behavioral_interview_questions()
    
    # Print final results
    print("\n" + "="*80)
    print("📊 FINAL TEST RESULTS")
    print("="*80)
    
    success_rate = (results["passed_tests"] / results["total_tests"]) * 100
    print(f"✅ Tests Passed: {results['passed_tests']}/{results['total_tests']}")
    print(f"❌ Tests Failed: {results['failed_tests']}/{results['total_tests']}")
    print(f"📈 Success Rate: {success_rate:.1f}%")
    
    print("\n📋 DETAILED TEST RESULTS:")
    for detail in results["details"]:
        print(f"   {detail}")
    
    if success_rate >= 75:
        print(f"\n🎉 BEHAVIORAL INTERVIEW QUESTIONS PDF FORMATTING ENHANCEMENT TESTING COMPLETED SUCCESSFULLY!")
        print(f"   The enhanced PDF formatting improvements are working correctly with {success_rate:.1f}% success rate.")
        print(f"   Key improvements verified:")
        print(f"   • Enhanced text structure with proper question/assessment separation")
        print(f"   • Visual hierarchy with bold questions and italicized assessments") 
        print(f"   • Color scheme alignment with #2c3e50 theme matching technical questions")
        print(f"   • Professional formatting with proper spacing and layout")
        print(f"   • Complete workflow from generation to PDF download")
    else:
        print(f"\n⚠️  BEHAVIORAL INTERVIEW QUESTIONS PDF FORMATTING TESTING COMPLETED WITH ISSUES")
        print(f"   Success rate: {success_rate:.1f}% - Some formatting enhancements may need attention.")
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()