#!/usr/bin/env python3
"""
Detailed PDF Analysis for Rejection Reasons
Analyzing the actual PDF content to verify enhanced formatting
"""

import requests
import os
import tempfile
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://33e908ff-821c-4359-a046-0a59698e91ec.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

def analyze_latest_rejection_pdf():
    """Analyze the latest rejection reasons PDF"""
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
        latest_analysis = analyses[0]  # Assuming they're sorted by date
        analysis_id = latest_analysis.get("id")
        
        print(f"📋 Analyzing rejection analysis: {analysis_id}")
        print(f"📝 Job Title: {latest_analysis.get('job_title')}")
        print(f"📅 Created: {latest_analysis.get('created_at')}")
        
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
        
        # Save PDF for analysis
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(pdf_content)
            temp_pdf_path = temp_file.name
        
        print(f"💾 PDF saved to: {temp_pdf_path}")
        
        # Basic PDF structure analysis
        print("\n🔍 PDF STRUCTURE ANALYSIS:")
        print(f"   ✅ Starts with PDF header: {pdf_content.startswith(b'%PDF')}")
        print(f"   ✅ Contains PDF objects: {b'obj' in pdf_content}")
        print(f"   ✅ Contains streams: {b'stream' in pdf_content}")
        print(f"   ✅ Has proper ending: {b'%%EOF' in pdf_content[-100:] or b'endobj' in pdf_content[-1000:]}")
        
        # Try to extract readable text from PDF (basic approach)
        try:
            # Convert PDF bytes to string for basic text search
            pdf_text = pdf_content.decode('latin-1', errors='ignore')
            
            print("\n📝 CONTENT ANALYSIS:")
            
            # Look for key terms that should be in the rejection reasons
            key_terms = [
                "rejection", "analysis", "candidate", "requirements", "skills",
                "experience", "education", "technical", "qualifications", "gap"
            ]
            
            found_terms = []
            for term in key_terms:
                if term.lower() in pdf_text.lower():
                    found_terms.append(term)
            
            print(f"   📋 Key terms found: {len(found_terms)}/{len(key_terms)}")
            print(f"   📋 Terms: {', '.join(found_terms)}")
            
            # Look for structured content indicators
            structure_indicators = [
                "Required:", "Candidate Reality:", "Gap Impact:",
                "TECHNICAL", "EXPERIENCE", "EDUCATION", "PROGRAMMING"
            ]
            
            found_structure = []
            for indicator in structure_indicators:
                if indicator in pdf_text:
                    found_structure.append(indicator)
            
            print(f"   🏗️  Structure indicators: {len(found_structure)}/{len(structure_indicators)}")
            print(f"   🏗️  Indicators: {', '.join(found_structure)}")
            
            # Check for enhanced formatting elements (these might be encoded differently in PDF)
            formatting_elements = [
                "font", "color", "size", "bold", "italic", "header"
            ]
            
            found_formatting = []
            for element in formatting_elements:
                if element.lower() in pdf_text.lower():
                    found_formatting.append(element)
            
            print(f"   🎨 Formatting elements: {len(found_formatting)}/{len(formatting_elements)}")
            print(f"   🎨 Elements: {', '.join(found_formatting)}")
            
        except Exception as e:
            print(f"   ⚠️  Text extraction error: {e}")
        
        # Show first few lines of original content for comparison
        print("\n📄 ORIGINAL CONTENT PREVIEW:")
        original_lines = original_content.split('\n')[:10]
        for i, line in enumerate(original_lines, 1):
            if line.strip():
                print(f"   {i:2d}. {line.strip()[:80]}...")
        
        print(f"\n✅ PDF Analysis Complete!")
        print(f"📊 Summary: PDF generated successfully with {len(pdf_content)} bytes")
        print(f"📊 Content ratio: {len(pdf_content)/len(original_content):.2f}x size increase from text to PDF")
        
        # Don't delete the temp file so user can examine it if needed
        print(f"💡 PDF file available at: {temp_pdf_path}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("DETAILED PDF ANALYSIS FOR REJECTION REASONS")
    print("=" * 80)
    analyze_latest_rejection_pdf()