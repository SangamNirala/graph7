#!/usr/bin/env python3
"""
Advanced PDF Analysis for Rejection Reasons
Using PyPDF2 to properly extract and analyze PDF content
"""

import requests
import os
import tempfile
import io
from datetime import datetime
import PyPDF2

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://aptiscore-engine.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

def analyze_rejection_pdf_content():
    """Analyze rejection reasons PDF with proper text extraction"""
    session = requests.Session()
    
    try:
        # Get the latest rejection analysis
        response = session.get(f"{BASE_URL}/placement-preparation/rejection-reasons")
        
        if response.status_code != 200:
            print(f"❌ Failed to get analyses: {response.status_code}")
            return
        
        data = response.json()
        analyses = data.get("analyses", [])
        
        if not analyses:
            print("❌ No analyses found")
            return
        
        # Get the latest analysis
        latest_analysis = analyses[0]
        analysis_id = latest_analysis.get("id")
        
        print(f"📋 Analyzing rejection analysis: {analysis_id}")
        print(f"📝 Job Title: {latest_analysis.get('job_title')}")
        
        # Get original analysis content
        original_content = latest_analysis.get("rejection_reasons", "")
        print(f"📊 Original content length: {len(original_content)} characters")
        
        # Download PDF
        pdf_response = session.get(f"{BASE_URL}/placement-preparation/rejection-reasons/{analysis_id}/download")
        
        if pdf_response.status_code != 200:
            print(f"❌ Failed to download PDF: {pdf_response.status_code}")
            return
        
        pdf_content = pdf_response.content
        print(f"📄 PDF size: {len(pdf_content)} bytes")
        
        # Extract text using PyPDF2
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            
            print(f"\n📖 PDF STRUCTURE:")
            print(f"   📄 Number of pages: {len(pdf_reader.pages)}")
            
            # Extract text from all pages
            extracted_text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                extracted_text += page_text
                print(f"   📄 Page {page_num + 1}: {len(page_text)} characters")
            
            print(f"   📊 Total extracted text: {len(extracted_text)} characters")
            
            if extracted_text:
                print(f"\n📝 EXTRACTED CONTENT ANALYSIS:")
                
                # Check for key rejection reasons content
                key_terms = [
                    "rejection", "analysis", "candidate", "requirements", "skills",
                    "experience", "education", "technical", "qualifications", "gap",
                    "python", "machine learning", "data scientist"
                ]
                
                found_terms = []
                for term in key_terms:
                    if term.lower() in extracted_text.lower():
                        found_terms.append(term)
                
                print(f"   📋 Key terms found: {len(found_terms)}/{len(key_terms)}")
                print(f"   📋 Terms: {', '.join(found_terms)}")
                
                # Look for structured content
                structure_indicators = [
                    "Required:", "Candidate Reality:", "Gap Impact:",
                    "TECHNICAL", "EXPERIENCE", "EDUCATION", "PROGRAMMING",
                    "REJECTION REASONS"
                ]
                
                found_structure = []
                for indicator in structure_indicators:
                    if indicator in extracted_text:
                        found_structure.append(indicator)
                
                print(f"   🏗️  Structure indicators: {len(found_structure)}/{len(structure_indicators)}")
                print(f"   🏗️  Found: {', '.join(found_structure)}")
                
                # Count bullet points
                bullet_indicators = ["•", "-", "*", "◦"]
                total_bullets = sum(extracted_text.count(bullet) for bullet in bullet_indicators)
                print(f"   📝 Bullet points found: {total_bullets}")
                
                # Show first few lines of extracted content
                print(f"\n📄 EXTRACTED CONTENT PREVIEW:")
                extracted_lines = [line.strip() for line in extracted_text.split('\n') if line.strip()][:15]
                for i, line in enumerate(extracted_lines, 1):
                    print(f"   {i:2d}. {line[:80]}...")
                
                # Content comparison
                print(f"\n📊 CONTENT COMPARISON:")
                print(f"   📝 Original: {len(original_content)} chars")
                print(f"   📄 Extracted: {len(extracted_text)} chars")
                print(f"   📊 Coverage: {(len(extracted_text)/len(original_content)*100):.1f}%")
                
                # Enhanced formatting verification
                print(f"\n🎨 ENHANCED FORMATTING VERIFICATION:")
                
                # Check if content is properly structured
                has_title = "rejection" in extracted_text.lower() and "reasons" in extracted_text.lower()
                has_bullets = total_bullets >= 5
                has_structure = len(found_structure) >= 3
                has_content = len(extracted_text) >= 1000
                
                formatting_score = sum([has_title, has_bullets, has_structure, has_content])
                
                print(f"   📋 Has title/header: {'✅' if has_title else '❌'}")
                print(f"   📝 Has bullet points: {'✅' if has_bullets else '❌'} ({total_bullets} found)")
                print(f"   🏗️  Has structure: {'✅' if has_structure else '❌'} ({len(found_structure)} indicators)")
                print(f"   📊 Has sufficient content: {'✅' if has_content else '❌'}")
                print(f"   🎯 Formatting Score: {formatting_score}/4")
                
                if formatting_score >= 3:
                    print(f"   ✅ PDF formatting appears to be enhanced and working correctly!")
                else:
                    print(f"   ⚠️  PDF formatting may need improvement")
                
            else:
                print("   ❌ No text could be extracted from PDF")
                
        except Exception as e:
            print(f"   ❌ PDF text extraction error: {e}")
        
        # Show original content structure for comparison
        print(f"\n📄 ORIGINAL CONTENT STRUCTURE:")
        original_lines = [line.strip() for line in original_content.split('\n') if line.strip()][:10]
        for i, line in enumerate(original_lines, 1):
            print(f"   {i:2d}. {line[:80]}...")
        
        print(f"\n✅ Advanced PDF Analysis Complete!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("ADVANCED PDF ANALYSIS FOR REJECTION REASONS")
    print("=" * 80)
    analyze_rejection_pdf_content()