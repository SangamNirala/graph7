#!/usr/bin/env python3
"""
Admin Login Functionality Test
Focused test for admin authentication with password "Game@1234" 
to confirm it's working properly after fixing the backend dependency issue.
"""

import requests
import json
import time
from typing import Dict, Any

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://8a188fe1-d475-4a33-b656-a259b6527b59.preview.emergentagent.com/api"

class AdminLoginTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_backend_connectivity(self) -> bool:
        """Test basic backend connectivity"""
        try:
            # Try to reach the admin login endpoint
            response = self.session.options(f"{self.base_url}/admin/login", timeout=10)
            success = response.status_code in [200, 204, 405]  # OPTIONS might return different codes
            details = f"Status: {response.status_code}, Backend reachable"
            self.log_test("Backend Connectivity", success, details)
            return success
        except Exception as e:
            self.log_test("Backend Connectivity", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_correct_password(self) -> bool:
        """Test admin authentication with correct password 'Game@1234'"""
        try:
            payload = {"password": "Game@1234"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                try:
                    data = response.json()
                    success = data.get("success", False) == True
                    details = f"Status: {response.status_code}, Success: {data.get('success')}, Message: {data.get('message', 'N/A')}"
                except json.JSONDecodeError:
                    success = False
                    details = f"Status: {response.status_code}, Invalid JSON response: {response.text[:200]}"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Admin Login (Correct Password)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login (Correct Password)", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_wrong_password(self) -> bool:
        """Test admin authentication with wrong password"""
        try:
            payload = {"password": "WrongPassword123"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            # Should return 401 for invalid password
            success = response.status_code == 401
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Admin Login (Wrong Password)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login (Wrong Password)", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_empty_password(self) -> bool:
        """Test admin authentication with empty password"""
        try:
            payload = {"password": ""}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            # Should return 401 or 422 for empty password
            success = response.status_code in [401, 422]
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Admin Login (Empty Password)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login (Empty Password)", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_missing_password(self) -> bool:
        """Test admin authentication with missing password field"""
        try:
            payload = {}  # No password field
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            # Should return 422 for missing required field
            success = response.status_code == 422
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Admin Login (Missing Password)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login (Missing Password)", False, f"Exception: {str(e)}")
            return False
    
    def test_admin_login_old_password(self) -> bool:
        """Test admin authentication with old password 'Game@123'"""
        try:
            payload = {"password": "Game@123"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            # Should return 401 for old password
            success = response.status_code == 401
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Admin Login (Old Password)", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login (Old Password)", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all admin login tests"""
        print("=" * 70)
        print("ADMIN LOGIN FUNCTIONALITY TEST")
        print("Testing admin authentication after backend dependency fix")
        print("=" * 70)
        print()
        
        results = {}
        
        # Test backend connectivity first
        results["backend_connectivity"] = self.test_backend_connectivity()
        
        # Test correct password
        results["correct_password"] = self.test_admin_login_correct_password()
        
        # Test various invalid scenarios
        results["wrong_password"] = self.test_admin_login_wrong_password()
        results["empty_password"] = self.test_admin_login_empty_password()
        results["missing_password"] = self.test_admin_login_missing_password()
        results["old_password"] = self.test_admin_login_old_password()
        
        # Summary
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        print(f"\nAdmin Login Test Results:")
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        # Specific analysis for admin login functionality
        critical_tests = ["backend_connectivity", "correct_password"]
        critical_passed = sum(1 for test in critical_tests if results.get(test, False))
        
        if critical_passed == len(critical_tests):
            print("🎉 ADMIN LOGIN WORKING! Backend is accessible and correct password authentication works.")
        elif results.get("backend_connectivity", False):
            print("⚠️  Backend is accessible but admin login has issues.")
        else:
            print("❌ Backend connectivity issues detected.")
        
        # Check if dependency issue is resolved
        if results.get("backend_connectivity", False):
            print("✅ Backend dependency issue appears to be resolved - server is responding.")
        else:
            print("❌ Backend dependency issue may still exist - server not responding.")
        
        return results

def main():
    """Main test execution"""
    tester = AdminLoginTester()
    results = tester.run_all_tests()
    
    # Return exit code based on critical tests
    critical_tests = ["backend_connectivity", "correct_password"]
    critical_passed = all(results.get(test, False) for test in critical_tests)
    
    return 0 if critical_passed else 1

if __name__ == "__main__":
    exit(main())