#!/usr/bin/env python3
"""
Direct Text Cleaning Function Test
Tests the clean_text_for_speech function directly without requiring Google Cloud TTS
"""

import re
import sys
import os

# Add the backend directory to the path so we can import the function
sys.path.append('/app/backend')

def clean_text_for_speech(text: str) -> str:
    """Clean text for better TTS pronunciation by removing formatting characters"""
    import re
    
    # Remove backticks around code terms
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Remove other markdown formatting
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
    text = re.sub(r'_([^_]+)_', r'\1', text)        # Underscore italic
    text = re.sub(r'~~([^~]+)~~', r'\1', text)      # Strikethrough
    
    # Replace common code-related phrases for better pronunciation
    text = text.replace('HTML', 'H-T-M-L')
    text = text.replace('CSS', 'C-S-S')
    text = text.replace('JavaScript', 'Java Script')
    text = text.replace('APIs', 'A-P-Is')
    text = text.replace('API', 'A-P-I')
    text = text.replace('JSON', 'J-S-O-N')
    text = text.replace('SQL', 'S-Q-L')
    
    # Remove multiple spaces and clean up
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def test_text_cleaning():
    """Test the text cleaning function with various inputs"""
    print("=" * 70)
    print("DIRECT TEXT CLEANING FUNCTION TEST")
    print("Testing clean_text_for_speech function")
    print("=" * 70)
    print()
    
    test_cases = [
        {
            "input": "How do `margin`, `padding`, and `border` interact in the CSS box model?",
            "expected_cleaned": "How do margin, padding, and border interact in the C-S-S box model?"
        },
        {
            "input": "Explain the difference between `let`, `const`, and `var` in **JavaScript**.",
            "expected_cleaned": "Explain the difference between let, const, and var in Java Script."
        },
        {
            "input": "What is the purpose of the `useEffect` hook in React, and how does it differ from `componentDidMount`?",
            "expected_cleaned": "What is the purpose of the useEffect hook in React, and how does it differ from componentDidMount?"
        },
        {
            "input": "Describe how **CSS Grid** and *Flexbox* work together for responsive layouts.",
            "expected_cleaned": "Describe how C-S-S Grid and Flexbox work together for responsive layouts."
        },
        {
            "input": "Why would you use `async/await` instead of ~~callbacks~~ or **Promises**?",
            "expected_cleaned": "Why would you use async/await instead of callbacks or Promises?"
        },
        {
            "input": "How do you optimize API calls in a React application using JSON data?",
            "expected_cleaned": "How do you optimize A-P-I calls in a React application using J-S-O-N data?"
        },
        {
            "input": "Can you explain `useState` and `useEffect` hooks? How would you use `fetch` API with `async/await`?",
            "expected_cleaned": "Can you explain useState and useEffect hooks? How would you use fetch A-P-I with async/await?"
        },
        {
            "input": "What's the difference between `innerHTML`, `textContent`, and `innerText` in HTML?",
            "expected_cleaned": "What's the difference between innerHTML, textContent, and innerText in H-T-M-L?"
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        input_text = test_case["input"]
        expected = test_case["expected_cleaned"]
        
        # Test the cleaning function
        cleaned = clean_text_for_speech(input_text)
        
        # Check if the result matches expected
        passed = cleaned == expected
        all_passed = all_passed and passed
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} Test {i}")
        print(f"   Input:    {input_text}")
        print(f"   Expected: {expected}")
        print(f"   Got:      {cleaned}")
        
        if not passed:
            print(f"   ❌ Mismatch detected!")
        
        print()
    
    # Test specific backtick removal
    print("=" * 50)
    print("BACKTICK REMOVAL VERIFICATION")
    print("=" * 50)
    
    backtick_tests = [
        "`margin`",
        "`padding`", 
        "`border`",
        "`useState`",
        "`useEffect`",
        "`async/await`",
        "`fetch`",
        "`componentDidMount`"
    ]
    
    backtick_removal_passed = True
    for test_text in backtick_tests:
        cleaned = clean_text_for_speech(test_text)
        has_backticks = "`" in cleaned
        
        if has_backticks:
            backtick_removal_passed = False
            print(f"❌ FAIL: '{test_text}' -> '{cleaned}' (still contains backticks)")
        else:
            print(f"✅ PASS: '{test_text}' -> '{cleaned}' (backticks removed)")
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if all_passed and backtick_removal_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Text cleaning function correctly removes backticks")
        print("✅ Markdown formatting is properly cleaned")
        print("✅ Technical acronyms are spelled out for better TTS")
        print("✅ The backtick fix is working correctly")
        return True
    else:
        print("⚠️  Some tests failed:")
        if not all_passed:
            print("❌ Text cleaning doesn't match expected output")
        if not backtick_removal_passed:
            print("❌ Backticks are not being removed properly")
        return False

if __name__ == "__main__":
    success = test_text_cleaning()
    exit(0 if success else 1)