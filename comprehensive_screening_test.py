#!/usr/bin/env python3
"""
Comprehensive Direct Resume Screening Test
Validates the exact response format specified in the review request
"""

import requests
import json
import io

BASE_URL = "https://466a16b6-018f-40ef-a6a9-f50ebbf5d383.preview.emergentagent.com/api"

def test_response_format():
    """Test that the response format matches the expected structure from review request"""
    session = requests.Session()
    
    # Login first
    login_response = session.post(f"{BASE_URL}/admin/login", json={"password": "Game@1234"})
    if login_response.status_code != 200:
        print("❌ Admin login failed")
        return False
    
    # Get or create job requirements
    job_req_response = session.get(f"{BASE_URL}/admin/screening/job-requirements")
    if job_req_response.status_code != 200:
        print("❌ Failed to get job requirements")
        return False
    
    job_requirements = job_req_response.json().get("job_requirements", [])
    if not job_requirements:
        # Create job requirements
        create_req = {
            "job_title": "Senior Python Developer",
            "job_description": "Looking for experienced Python developer",
            "required_skills": ["Python", "FastAPI", "MongoDB"],
            "preferred_skills": ["Docker", "AWS"],
            "experience_level": "senior"
        }
        create_response = session.post(f"{BASE_URL}/admin/screening/job-requirements", json=create_req)
        if create_response.status_code != 200:
            print("❌ Failed to create job requirements")
            return False
        job_requirements_id = create_response.json()["job_requirements_id"]
    else:
        job_requirements_id = job_requirements[0]["id"]
    
    # Create test resume
    resume_content = """John Smith
Senior Python Developer
Email: john.smith@example.com

EXPERIENCE:
- 6+ years of Python development
- Expert in FastAPI and MongoDB
- Led development teams
- AWS cloud experience

SKILLS:
- Python, FastAPI, MongoDB, Docker, AWS
- Team leadership and mentoring
- Agile development practices

EDUCATION:
Master of Science in Computer Science
Tech University, 2018"""
    
    # Test the upload-and-analyze endpoint
    files = {'files': ('john_smith.txt', io.StringIO(resume_content), 'text/plain')}
    data = {
        'job_requirements_id': job_requirements_id,
        'batch_name': 'Testing Direct Screening'
    }
    
    response = session.post(f"{BASE_URL}/admin/screening/upload-and-analyze", files=files, data=data)
    
    if response.status_code != 200:
        print(f"❌ Request failed with status {response.status_code}")
        return False
    
    result = response.json()
    
    # Validate response structure according to review request
    expected_fields = [
        "success", "batch_id", "processing_summary", "screening_results", 
        "processed_candidates", "top_candidates"
    ]
    
    print("🔍 Validating Response Format:")
    print("=" * 50)
    
    # Check main fields
    for field in expected_fields:
        if field in result:
            print(f"✅ {field}: Present")
        else:
            print(f"❌ {field}: Missing")
            return False
    
    # Validate processing_summary structure
    processing = result["processing_summary"]
    processing_fields = ["total_files", "successfully_processed", "processing_rate"]
    print("\n📊 Processing Summary:")
    for field in processing_fields:
        if field in processing:
            print(f"✅ {field}: {processing[field]}")
        else:
            print(f"❌ {field}: Missing")
            return False
    
    # Validate screening_results structure
    screening = result["screening_results"]
    screening_fields = ["candidates_screened", "average_score", "high_quality_matches", "score_distribution"]
    print("\n🎯 Screening Results:")
    for field in screening_fields:
        if field in screening:
            print(f"✅ {field}: {screening[field]}")
        else:
            print(f"❌ {field}: Missing")
            return False
    
    # Validate processed_candidates structure
    if result["processed_candidates"]:
        candidate = result["processed_candidates"][0]
        candidate_fields = ["candidate_id", "filename", "name", "overall_score", "component_scores", "extracted_skills"]
        print("\n👤 Processed Candidates (first candidate):")
        for field in candidate_fields:
            if field in candidate:
                print(f"✅ {field}: {candidate[field]}")
            else:
                print(f"❌ {field}: Missing")
                return False
    
    # Validate top_candidates structure
    print(f"\n🏆 Top Candidates: {len(result['top_candidates'])} candidates")
    
    # Check if we have job requirements info
    if "job_requirements" in result:
        job_req = result["job_requirements"]
        print(f"\n📋 Job Requirements: {job_req.get('job_title', 'N/A')}")
    
    print("\n" + "=" * 50)
    print("🎉 Response format validation PASSED!")
    print(f"📈 Successfully processed {processing['successfully_processed']} out of {processing['total_files']} files")
    print(f"⭐ Average score: {screening['average_score']}")
    print(f"🎯 High quality matches: {screening['high_quality_matches']}")
    
    return True

if __name__ == "__main__":
    print("🚀 Comprehensive Direct Resume Screening Test")
    print("Testing response format against review request specifications")
    print("=" * 60)
    
    if test_response_format():
        print("\n✅ ALL VALIDATIONS PASSED!")
        print("The direct resume screening functionality meets all requirements.")
    else:
        print("\n❌ VALIDATION FAILED!")
        print("The response format does not match the expected structure.")