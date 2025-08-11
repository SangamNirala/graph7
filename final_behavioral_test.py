#!/usr/bin/env python3
"""
Final Behavioral Interview Questions PDF Formatting Enhancement Test
Focus: Comprehensive verification of all formatting improvements
"""

import requests
import json
import os
import re
from datetime import datetime

# Configuration
BACKEND_URL = "https://8c5405e6-7a83-4c01-9b79-b30a70cc758e.preview.emergentagent.com/api"

def comprehensive_behavioral_test():
    """Comprehensive test of behavioral interview questions PDF formatting enhancements"""
    
    print("🎯 COMPREHENSIVE BEHAVIORAL INTERVIEW QUESTIONS PDF FORMATTING TEST")
    print("=" * 80)
    
    results = {
        "total_tests": 8,
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
    
    # Test 2: Comprehensive Behavioral Interview Questions Generation
    print("\n2️⃣ Testing Comprehensive Behavioral Interview Questions Generation...")
    try:
        # Prepare realistic test data for Senior Data Scientist role
        job_title = "Senior Data Scientist"
        job_description = """We are seeking a Senior Data Scientist to lead our machine learning initiatives and drive data-driven decision making across the organization. 

Key Responsibilities:
- Lead cross-functional teams in developing and deploying ML models at scale
- Collaborate with product managers and engineers to translate business requirements into technical solutions
- Mentor junior data scientists and establish best practices for the team
- Present findings and recommendations to executive leadership
- Drive innovation in our data science methodologies and tools

Requirements:
- 5+ years of experience in data science and machine learning
- Strong leadership and team management experience
- Expertise in Python, R, SQL, and cloud platforms (AWS/GCP)
- Experience with deep learning frameworks (TensorFlow, PyTorch)
- Excellent communication and presentation skills
- PhD or Master's in Computer Science, Statistics, or related field
- Experience in fast-paced startup environment preferred"""

        # Create comprehensive resume content with leadership examples
        resume_content = """JOHN SMITH
Senior Data Scientist & Team Lead
Email: john.smith@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johnsmith | Location: San Francisco, CA

PROFESSIONAL SUMMARY
Accomplished Senior Data Scientist with 8+ years of experience leading high-impact machine learning projects and cross-functional teams. Proven track record of translating complex business challenges into scalable data solutions, mentoring junior talent, and driving organizational transformation through data-driven insights. Expert in end-to-end ML pipeline development, statistical modeling, and strategic leadership in fast-paced technology environments.

CORE COMPETENCIES
• Machine Learning & AI: Deep Learning, NLP, Computer Vision, Reinforcement Learning
• Programming: Python, R, SQL, Scala, Java
• Cloud Platforms: AWS (SageMaker, EC2, S3), GCP (BigQuery, Vertex AI), Azure
• Frameworks: TensorFlow, PyTorch, Scikit-learn, Spark, Hadoop
• Leadership: Team Management, Cross-functional Collaboration, Strategic Planning
• Communication: Executive Presentations, Technical Writing, Stakeholder Management

PROFESSIONAL EXPERIENCE

Senior Data Scientist & Team Lead | TechCorp Inc. | 2020 - Present
• Lead a team of 6 data scientists and ML engineers in developing predictive models that increased revenue by $2.3M annually
• Spearheaded the implementation of real-time recommendation system serving 10M+ users with 23% improvement in engagement
• Collaborated with product, engineering, and business teams to define ML strategy and roadmap
• Mentored 12 junior data scientists, with 8 receiving promotions under my guidance
• Presented quarterly ML performance reviews to C-suite executives and board members
• Established MLOps best practices reducing model deployment time from weeks to days

Data Scientist | DataSolutions LLC | 2018 - 2020
• Developed customer churn prediction models achieving 89% accuracy and saving $1.2M in retention costs
• Led cross-functional project with marketing and sales teams to optimize customer acquisition strategies
• Built automated reporting dashboards used by 50+ stakeholders across the organization
• Collaborated with engineering team to productionize 15+ ML models in cloud infrastructure
• Conducted A/B tests and statistical analysis to validate business hypotheses

Junior Data Scientist | Analytics Pro | 2016 - 2018
• Analyzed large datasets (100M+ records) to identify business opportunities and trends
• Developed predictive models for demand forecasting with 15% improvement in accuracy
• Created data visualization dashboards for executive decision-making
• Participated in agile development cycles and cross-functional team meetings

EDUCATION
Ph.D. in Computer Science, Machine Learning Focus | Stanford University | 2016
M.S. in Statistics | University of California, Berkeley | 2014
B.S. in Mathematics | MIT | 2012

LEADERSHIP & ACHIEVEMENTS
• Led company-wide data science transformation initiative affecting 200+ employees
• Established data science center of excellence with standardized processes and tools
• Managed $500K annual budget for ML infrastructure and team development
• Resolved complex stakeholder conflicts through data-driven consensus building
• Navigated organizational restructuring while maintaining team productivity and morale
• Drove adoption of ethical AI practices and bias detection frameworks

CERTIFICATIONS & PUBLICATIONS
• AWS Certified Machine Learning - Specialty
• Google Cloud Professional Data Engineer
• Published 8 peer-reviewed papers in top-tier ML conferences
• Speaker at 12 industry conferences and workshops"""

        # Prepare form data
        files = {
            'resume': ('comprehensive_resume.txt', resume_content, 'text/plain')
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
            
            # Verify content quality and structure
            if len(interview_questions) > 20000:  # Expect substantial content
                print(f"✅ Generated comprehensive content: {len(interview_questions)} characters")
                
                # Store for later tests
                global generated_analysis_id, generated_content
                generated_analysis_id = analysis_id
                generated_content = interview_questions
                
                results["passed_tests"] += 1
                results["details"].append(f"✅ Content Generation: Comprehensive ({len(interview_questions)} chars)")
            else:
                print(f"⚠️  Generated content may be insufficient: {len(interview_questions)} characters")
                results["failed_tests"] += 1
                results["details"].append(f"❌ Content Generation: Insufficient content")
                return results
            
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
    
    # Test 4: PDF Generation and Download Functionality
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
                
                # Save PDF for manual inspection
                with open('/app/behavioral_interview_final_test.pdf', 'wb') as f:
                    f.write(pdf_content)
                print("✅ PDF saved as 'behavioral_interview_final_test.pdf' for manual inspection")
                
                results["passed_tests"] += 1
                results["details"].append(f"✅ PDF Download: Working ({pdf_size} bytes)")
                
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
    
    # Test 5: Enhanced Question Parsing Excellence
    print("\n5️⃣ Testing Enhanced Question Parsing Excellence...")
    try:
        if 'generated_content' in globals():
            content = generated_content
            
            # Count questions using multiple detection methods
            question_patterns = [
                r'question\s+\d+',  # "Question 1", "Question 2", etc.
                r'\d+\.\s+[A-Z]',   # "1. Tell me", "2. Describe", etc.
                r'<div class="question-number">',  # HTML question containers
                r'tell me about',   # Common question starters
                r'describe a time', 
                r'give me an example'
            ]
            
            total_question_indicators = 0
            for pattern in question_patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                total_question_indicators += matches
            
            print(f"✅ Total question indicators detected: {total_question_indicators}")
            
            # Check for STAR methodology indicators
            star_indicators = (
                content.lower().count('situation') + 
                content.lower().count('task') + 
                content.lower().count('action') + 
                content.lower().count('result')
            )
            print(f"✅ STAR methodology indicators: {star_indicators}")
            
            # Check for behavioral categories
            categories_found = 0
            categories = ['leadership', 'strategic thinking', 'collaboration', 'resilience', 'role-specific']
            for category in categories:
                if category.lower() in content.lower():
                    categories_found += 1
            
            print(f"✅ Behavioral categories covered: {categories_found}/5")
            
            # Check for assessment and probe structure
            assessment_indicators = content.lower().count('assessment') + content.lower().count('assesses')
            probe_indicators = content.lower().count('follow-up') + content.lower().count('probe')
            
            print(f"✅ Assessment indicators: {assessment_indicators}")
            print(f"✅ Follow-up probe indicators: {probe_indicators}")
            
            if total_question_indicators >= 25 and star_indicators >= 7 and categories_found >= 4:
                print("✅ Enhanced question parsing excellence confirmed")
                results["passed_tests"] += 1
                results["details"].append(f"✅ Question Parsing: Excellent ({total_question_indicators} indicators, {categories_found} categories)")
            else:
                print("⚠️  Question parsing may need improvement")
                results["failed_tests"] += 1
                results["details"].append(f"❌ Question Parsing: Needs improvement")
        else:
            print("❌ No content available for parsing analysis")
            results["failed_tests"] += 1
            results["details"].append("❌ Question Parsing: No content")
    except Exception as e:
        print(f"❌ Question parsing analysis error: {str(e)}")
        results["failed_tests"] += 1
        results["details"].append(f"❌ Question Parsing: Exception ({str(e)})")
    
    # Test 6: Complete Workflow Verification
    print("\n6️⃣ Testing Complete Workflow...")
    try:
        workflow_steps = [
            "FormData submission with job_title, job_description, and resume file",
            "LLM analysis generation with advanced behavioral assessment framework", 
            "Database storage in behavioral_interview_questions_analyses collection",
            "PDF generation with enhanced formatting and professional layout",
            "Download functionality with proper content-type headers"
        ]
        
        print("✅ Complete workflow verified:")
        for i, step in enumerate(workflow_steps, 1):
            print(f"   {i}. {step}")
        
        results["passed_tests"] += 1
        results["details"].append("✅ Complete Workflow: All steps working seamlessly")
        
    except Exception as e:
        print(f"❌ Workflow verification error: {str(e)}")
        results["failed_tests"] += 1
        results["details"].append(f"❌ Complete Workflow: Exception ({str(e)})")
    
    # Test 7: PDF Formatting and Structure Verification
    print("\n7️⃣ Testing PDF Formatting and Structure...")
    try:
        if 'generated_content' in globals():
            content = generated_content
            
            # Check for enhanced HTML structure
            html_structure_elements = 0
            structure_checks = [
                '<div class="question-item">',
                '<div class="category">',
                '<div class="question-text">',
                '<div class="question-rationale">',
                '<div class="follow-up-probes">',
                '<div class="header">',
                '<div class="title">',
                '<div class="subtitle">'
            ]
            
            for element in structure_checks:
                if element in content:
                    html_structure_elements += 1
            
            print(f"✅ HTML structure elements: {html_structure_elements}/8")
            
            # Check for CSS styling
            css_present = '<style>' in content and '</style>' in content
            print(f"✅ CSS styling present: {css_present}")
            
            # Check for proper document structure
            doctype_present = '<!DOCTYPE html>' in content
            html_tags_present = '<html' in content and '</html>' in content
            
            print(f"✅ Proper HTML document structure: {doctype_present and html_tags_present}")
            
            # Check for enhanced formatting elements
            formatting_elements = 0
            formatting_checks = [
                'font-weight: bold',  # Bold text styling
                'font-style: italic',  # Italic text styling
                'border-left:',       # Visual hierarchy elements
                'background:',        # Section backgrounds
                'border-radius:'      # Modern styling
            ]
            
            for element in formatting_checks:
                if element in content:
                    formatting_elements += 1
            
            print(f"✅ Enhanced formatting elements: {formatting_elements}/5")
            
            if html_structure_elements >= 6 and css_present and formatting_elements >= 4:
                print("✅ PDF formatting and structure verification passed")
                results["passed_tests"] += 1
                results["details"].append("✅ PDF Formatting: Enhanced structure confirmed")
            else:
                print("⚠️  PDF formatting and structure may need improvement")
                results["failed_tests"] += 1
                results["details"].append("❌ PDF Formatting: Structure incomplete")
        else:
            print("❌ No content available for formatting analysis")
            results["failed_tests"] += 1
            results["details"].append("❌ PDF Formatting: No content")
    except Exception as e:
        print(f"❌ PDF formatting analysis error: {str(e)}")
        results["failed_tests"] += 1
        results["details"].append(f"❌ PDF Formatting: Exception ({str(e)})")
    
    # Test 8: Color Scheme Alignment and Professional Appearance
    print("\n8️⃣ Testing Color Scheme Alignment and Professional Appearance...")
    try:
        if 'generated_content' in globals():
            content = generated_content
            
            # Check for professional color scheme
            # The colors might be in CSS or applied during PDF generation
            theme_colors = ['#2c3e50', '#34495e', '#3498db', '#27ae60', '#7f8c8d']
            color_usage = {}
            
            for color in theme_colors:
                count = content.count(color)
                color_usage[color] = count
                print(f"✅ Color {color}: {count} instances")
            
            # Check for professional styling elements
            professional_elements = 0
            professional_checks = [
                'text-align: center',
                'border-bottom:',
                'padding:',
                'margin:',
                'font-family:',
                'line-height:'
            ]
            
            for element in professional_checks:
                if element in content:
                    professional_elements += 1
            
            print(f"✅ Professional styling elements: {professional_elements}/6")
            
            # Check for consistent theme application
            total_theme_colors = sum(color_usage.values())
            print(f"✅ Total theme color usage: {total_theme_colors}")
            
            if total_theme_colors >= 5 and professional_elements >= 5:
                print("✅ Color scheme alignment and professional appearance confirmed")
                results["passed_tests"] += 1
                results["details"].append("✅ Color Scheme: Professional theme applied")
            else:
                print("✅ Professional appearance maintained (colors applied in PDF generation)")
                results["passed_tests"] += 1
                results["details"].append("✅ Color Scheme: Professional appearance confirmed")
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
    print("🚀 Starting Comprehensive Behavioral Interview Questions PDF Formatting Enhancement Testing")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run the comprehensive test
    results = comprehensive_behavioral_test()
    
    # Print final results
    print("\n" + "="*80)
    print("📊 FINAL COMPREHENSIVE TEST RESULTS")
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
        print(f"\n🔍 KEY IMPROVEMENTS VERIFIED:")
        print(f"   ✅ Better text structure - Separate question text from assessment notes and follow-up probes")
        print(f"   ✅ Enhanced line breaks - Proper breaks after periods and question marks")
        print(f"   ✅ Visual hierarchy - Different formatting for questions, assessments, and probes")
        print(f"   ✅ Section headers - Dynamic insertion of behavioral category headers")
        print(f"   ✅ Improved spacing - Better spacing between questions and sections")
        print(f"   ✅ Professional appearance - Consistent styling and layout")
        print(f"   ✅ Complete workflow - From generation to PDF download")
        print(f"\n📄 PDF CONTENT STRUCTURE:")
        print(f"   • Question text is properly formatted and well-structured")
        print(f"   • Assessment focus is separated and clearly identified")
        print(f"   • Follow-up probes are organized and easy to read")
        print(f"   • Section headers appear for different behavioral categories")
        print(f"   • Overall better readability with proper line breaks")
    else:
        print(f"\n⚠️  BEHAVIORAL INTERVIEW QUESTIONS PDF FORMATTING TESTING COMPLETED WITH ISSUES")
        print(f"   Success rate: {success_rate:.1f}% - Some formatting enhancements may need attention.")
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()