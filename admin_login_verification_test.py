#!/usr/bin/env python3
"""
Admin Login Verification Test
Specifically tests admin login functionality with Game@1234 password
and core backend endpoints as requested in the review.
"""

import requests
import json
import time
from typing import Dict, Any

# Backend URL from frontend .env
BASE_URL = "https://65275256-099e-4a3f-b83d-fcbfb7a6d86b.preview.emergentagent.com/api"

class AdminLoginVerificationTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "status": status
        }
        self.test_results.append(result)
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
        return success
    
    def test_backend_connectivity(self) -> bool:
        """Test basic backend connectivity"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"Status: {response.status_code}, Message: {data.get('message', 'N/A')}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:100]}"
            
            return self.log_test("Backend Connectivity", success, details)
        except Exception as e:
            return self.log_test("Backend Connectivity", False, f"Exception: {str(e)}")
    
    def test_admin_login_correct_password(self) -> bool:
        """Test admin login with correct Game@1234 password"""
        try:
            payload = {"password": "Game@1234"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("success", False) == True
                details = f"Status: {response.status_code}, Success: {data.get('success')}, Message: {data.get('message', 'N/A')}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            return self.log_test("Admin Login (Game@1234)", success, details)
        except Exception as e:
            return self.log_test("Admin Login (Game@1234)", False, f"Exception: {str(e)}")
    
    def test_admin_login_incorrect_password(self) -> bool:
        """Test admin login with incorrect password - should return 401"""
        try:
            payload = {"password": "WrongPassword123"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 401
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            return self.log_test("Admin Login (Incorrect Password)", success, details)
        except Exception as e:
            return self.log_test("Admin Login (Incorrect Password)", False, f"Exception: {str(e)}")
    
    def test_admin_login_empty_password(self) -> bool:
        """Test admin login with empty password"""
        try:
            payload = {"password": ""}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 401
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            return self.log_test("Admin Login (Empty Password)", success, details)
        except Exception as e:
            return self.log_test("Admin Login (Empty Password)", False, f"Exception: {str(e)}")
    
    def test_token_generation_functionality(self) -> bool:
        """Test basic admin functionality - token generation"""
        try:
            # Create sample resume content for token generation
            import io
            resume_content = """Test Candidate
Senior Software Engineer
Email: test@example.com
Phone: (555) 123-4567

EXPERIENCE:
- 5+ years of Python development
- Expert in FastAPI and React
- Team leadership experience
- Cloud platform knowledge

SKILLS:
- Python, JavaScript, TypeScript
- FastAPI, React, MongoDB
- Docker, AWS, CI/CD
- Team leadership"""
            
            files = {
                'resume_file': ('test_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Senior Backend Developer',
                'job_description': 'We are seeking a senior backend developer with strong Python and FastAPI experience.',
                'job_requirements': 'Requirements: 5+ years Python, FastAPI expertise, team leadership, cloud knowledge.'
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job",
                files=files,
                data=data,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = result.get("success", False) and "token" in result
                if success:
                    token = result["token"]
                    details = f"Status: {response.status_code}, Token Generated: {token[:8]}..., Success: {result.get('success')}"
                else:
                    details = f"Status: {response.status_code}, Missing token or success=false"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            return self.log_test("Token Generation", success, details)
        except Exception as e:
            return self.log_test("Token Generation", False, f"Exception: {str(e)}")
    
    def test_admin_reports_endpoint(self) -> bool:
        """Test admin reports endpoint accessibility"""
        try:
            response = self.session.get(f"{self.base_url}/admin/reports", timeout=10)
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "reports" in data
                details = f"Status: {response.status_code}, Reports found: {len(data.get('reports', []))}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            return self.log_test("Admin Reports Endpoint", success, details)
        except Exception as e:
            return self.log_test("Admin Reports Endpoint", False, f"Exception: {str(e)}")
    
    def test_critical_endpoints_accessibility(self) -> bool:
        """Test that all critical endpoints are accessible"""
        critical_endpoints = [
            ("/health", "GET"),
            ("/admin/login", "POST"),
            ("/admin/reports", "GET"),
            ("/candidate/validate-token", "POST"),
            ("/candidate/start-interview", "POST")
        ]
        
        accessible_count = 0
        total_endpoints = len(critical_endpoints)
        endpoint_results = []
        
        for endpoint, method in critical_endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}", timeout=5)
                else:  # POST
                    # Send minimal payload to test endpoint accessibility
                    response = self.session.post(f"{self.base_url}{endpoint}", json={}, timeout=5)
                
                # Consider endpoint accessible if it doesn't return 404 or 500
                accessible = response.status_code not in [404, 500, 502, 503]
                if accessible:
                    accessible_count += 1
                
                endpoint_results.append(f"{endpoint} ({method}): {response.status_code}")
                
            except Exception as e:
                endpoint_results.append(f"{endpoint} ({method}): Exception - {str(e)[:50]}")
        
        success = accessible_count == total_endpoints
        details = f"Accessible: {accessible_count}/{total_endpoints} endpoints. " + "; ".join(endpoint_results)
        
        return self.log_test("Critical Endpoints Accessibility", success, details)
    
    def run_verification_tests(self) -> Dict[str, Any]:
        """Run all admin login verification tests"""
        print("=" * 80)
        print("ADMIN LOGIN VERIFICATION TEST")
        print("Testing Game@1234 password authentication and core backend endpoints")
        print("=" * 80)
        print()
        
        # Run all tests
        test_methods = [
            self.test_backend_connectivity,
            self.test_admin_login_correct_password,
            self.test_admin_login_incorrect_password,
            self.test_admin_login_empty_password,
            self.test_token_generation_functionality,
            self.test_admin_reports_endpoint,
            self.test_critical_endpoints_accessibility
        ]
        
        results = {}
        for test_method in test_methods:
            test_name = test_method.__name__
            results[test_name] = test_method()
        
        # Summary
        print("=" * 80)
        print("VERIFICATION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print(f"\nTest Results:")
        for test_result in self.test_results:
            print(f"  {test_result['status']} {test_result['test_name']}")
        
        print(f"\nOVERALL RESULT: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        # Specific verification for the review requirements
        print("\n" + "=" * 80)
        print("REVIEW REQUIREMENTS VERIFICATION")
        print("=" * 80)
        
        admin_login_working = results.get("test_admin_login_correct_password", False)
        invalid_password_handled = results.get("test_admin_login_incorrect_password", False)
        token_generation_working = results.get("test_token_generation_functionality", False)
        endpoints_accessible = results.get("test_critical_endpoints_accessibility", False)
        
        print(f"✅ Admin login with Game@1234 password: {'WORKING' if admin_login_working else 'FAILED'}")
        print(f"✅ Invalid password returns 401 error: {'WORKING' if invalid_password_handled else 'FAILED'}")
        print(f"✅ Token generation functionality: {'WORKING' if token_generation_working else 'FAILED'}")
        print(f"✅ Critical endpoints accessible: {'WORKING' if endpoints_accessible else 'FAILED'}")
        
        if all([admin_login_working, invalid_password_handled, token_generation_working, endpoints_accessible]):
            print("\n🎉 ALL REVIEW REQUIREMENTS VERIFIED!")
            print("✅ Admin authentication with Game@1234 is working correctly")
            print("✅ Backend is fully operational after fixing Google AI dependency issues")
        else:
            print("\n⚠️  Some review requirements failed verification")
        
        return {
            "overall_success": passed == total,
            "passed_tests": passed,
            "total_tests": total,
            "admin_login_working": admin_login_working,
            "backend_operational": endpoints_accessible,
            "test_details": self.test_results
        }

def main():
    """Main test execution"""
    tester = AdminLoginVerificationTester()
    results = tester.run_verification_tests()
    
    # Return exit code based on results
    return 0 if results["overall_success"] else 1

if __name__ == "__main__":
    exit(main())