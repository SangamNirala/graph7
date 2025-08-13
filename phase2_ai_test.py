#!/usr/bin/env python3
"""
Phase 2 AI Enhancement Testing
Tests the advanced AI features including:
- Bias Detection Engine with fairness analysis
- Predictive Hiring Model with ML predictions
- Personality Analyzer with Big Five traits
- Data Privacy and Retention GDPR/CCPA APIs
"""

import requests
import json
import time
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://aptitude-models.preview.emergentagent.com/api"

class Phase2AITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_session_id = None
        self.test_assessment_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def setup_test_data(self) -> bool:
        """Create test assessment data for AI enhancement testing"""
        try:
            # Create a sample assessment for testing
            sample_assessment = {
                "session_id": "test-session-ai-enhancement",
                "candidate_name": "AI Test Candidate",
                "job_title": "Senior AI Engineer",
                "technical_score": 85,
                "behavioral_score": 78,
                "overall_score": 82,
                "technical_feedback": "Strong technical skills with excellent problem-solving abilities",
                "behavioral_feedback": "Great communication and leadership potential",
                "overall_feedback": "Highly recommended candidate with strong technical and soft skills"
            }
            
            self.test_session_id = sample_assessment["session_id"]
            self.test_assessment_id = "test-assessment-ai-enhancement"
            
            return True
        except Exception as e:
            print(f"Setup failed: {str(e)}")
            return False
    
    def test_bias_detection_analysis(self) -> bool:
        """Test bias detection and fairness analysis"""
        try:
            # Test question bias analysis
            question_text = "Tell me about your technical experience and how you handle challenging situations."
            
            response = self.session.post(
                f"{self.base_url}/admin/ai-enhancement/analyze-question-bias",
                params={"question_text": question_text},
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "success" in data and
                    data.get("success") == True and
                    "bias_analysis" in data
                )
                
                if success:
                    bias_analysis = data["bias_analysis"]
                    details = f"Status: {response.status_code}, Question analyzed successfully"
                else:
                    details = f"Status: {response.status_code}, Missing required fields in response"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Bias Detection Engine", success, details)
            return success
        except Exception as e:
            self.log_test("Bias Detection Engine", False, f"Exception: {str(e)}")
            return False
    
    def test_predictive_hiring_model(self) -> bool:
        """Test ML-based hiring success prediction"""
        try:
            # First train the model
            response = self.session.post(
                f"{self.base_url}/admin/ai-enhancement/train-hiring-model",
                timeout=20
            )
            
            if response.status_code != 200:
                details = f"Model training failed - Status: {response.status_code}, Response: {response.text[:200]}"
                self.log_test("Predictive Hiring Model", False, details)
                return False
            
            # Now test prediction with a session ID (we'll use our test session)
            response = self.session.post(
                f"{self.base_url}/admin/ai-enhancement/predict-hiring-success",
                params={"session_id": self.test_session_id},
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "success" in data and
                    data.get("success") == True and
                    "prediction" in data
                )
                
                if success:
                    prediction = data["prediction"]
                    details = f"Status: {response.status_code}, Prediction generated successfully"
                else:
                    details = f"Status: {response.status_code}, Missing required prediction fields"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Predictive Hiring Model", success, details)
            return success
        except Exception as e:
            self.log_test("Predictive Hiring Model", False, f"Exception: {str(e)}")
            return False
    
    def test_personality_analysis(self) -> bool:
        """Test Big Five personality traits analysis"""
        try:
            response = self.session.post(
                f"{self.base_url}/admin/ai-enhancement/analyze-personality",
                params={"session_id": self.test_session_id},
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "success" in data and
                    data.get("success") == True and
                    "personality_analysis" in data
                )
                
                if success:
                    details = f"Status: {response.status_code}, Personality analysis completed successfully"
                else:
                    details = f"Status: {response.status_code}, Missing personality analysis"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Personality Analyzer (Big Five)", success, details)
            return success
        except Exception as e:
            self.log_test("Personality Analyzer (Big Five)", False, f"Exception: {str(e)}")
            return False
    
    def test_fairness_metrics(self) -> bool:
        """Test fairness metrics calculation"""
        try:
            response = self.session.post(
                f"{self.base_url}/admin/ai-enhancement/calculate-fairness-metrics",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "success" in data and
                    data.get("success") == True and
                    "fairness_metrics" in data
                )
                
                if success:
                    total_assessments = data.get("total_assessments_analyzed", 0)
                    details = f"Status: {response.status_code}, Fairness metrics calculated for {total_assessments} assessments"
                else:
                    details = f"Status: {response.status_code}, Missing fairness metrics"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Fairness Metrics Calculation", success, details)
            return success
        except Exception as e:
            self.log_test("Fairness Metrics Calculation", False, f"Exception: {str(e)}")
            return False
    
    def test_ml_model_training(self) -> bool:
        """Test ML model training endpoint"""
        try:
            response = self.session.post(
                f"{self.base_url}/admin/ai-enhancement/train-hiring-model",
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "success" in data and
                    data.get("success") == True and
                    "training_result" in data
                )
                
                if success:
                    details = f"Status: {response.status_code}, Model training completed successfully"
                else:
                    details = f"Status: {response.status_code}, Missing training results"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("ML Model Training", success, details)
            return success
        except Exception as e:
            self.log_test("ML Model Training", False, f"Exception: {str(e)}")
            return False
    
    def test_comprehensive_ai_analysis(self) -> bool:
        """Test comprehensive AI analysis combining all features"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/ai-enhancement/model-status",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "success" in data and
                    data.get("success") == True and
                    "models" in data
                )
                
                if success:
                    models = data["models"]
                    capabilities = data.get("capabilities", [])
                    details = f"Status: {response.status_code}, AI Models Status: {len(models)} models, {len(capabilities)} capabilities"
                else:
                    details = f"Status: {response.status_code}, Missing model status data"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("AI Enhancement Model Status", success, details)
            return success
        except Exception as e:
            self.log_test("Comprehensive AI Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_data_retention_policies(self) -> bool:
        """Test data retention policies management"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/data-privacy/policies",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "retention_policies" in data and
                    "interview_data" in data["retention_policies"] and
                    "audio_files" in data["retention_policies"]
                )
                
                if success:
                    policies = data["retention_policies"]
                    interview_days = policies["interview_data"]
                    audio_days = policies["audio_files"]
                    details = f"Status: {response.status_code}, Interview Data: {interview_days} days, Audio Files: {audio_days} days"
                else:
                    details = f"Status: {response.status_code}, Missing retention policies"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Data Retention Policies", success, details)
            return success
        except Exception as e:
            self.log_test("Data Retention Policies", False, f"Exception: {str(e)}")
            return False
    
    def test_data_retention_status(self) -> bool:
        """Test data retention status endpoint"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/data-privacy/retention-status",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "data_counts" in data and
                    "retention_policies" in data
                )
                
                if success:
                    counts = data["data_counts"]
                    details = f"Status: {response.status_code}, Sessions: {counts.get('sessions', {}).get('total', 0)}, Audio Files: {counts.get('audio_files', {}).get('total', 0)}"
                else:
                    details = f"Status: {response.status_code}, Missing retention status data"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Data Retention Status", success, details)
            return success
        except Exception as e:
            self.log_test("Data Retention Status", False, f"Exception: {str(e)}")
            return False
    
    def test_consent_tracking(self) -> bool:
        """Test consent tracking functionality"""
        try:
            payload = {
                "candidate_id": "test-candidate-consent",
                "data_types": ["interview_data", "audio_files", "video_analysis"]
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/data-privacy/request-consent",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "consent_record" in data and
                    "consent_id" in data["consent_record"] and
                    "timestamp" in data["consent_record"]
                )
                
                if success:
                    consent = data["consent_record"]
                    consent_id = consent["consent_id"]
                    details = f"Status: {response.status_code}, Consent ID: {consent_id[:8]}..., Data Types: {len(consent.get('data_types', []))}"
                else:
                    details = f"Status: {response.status_code}, Missing consent record data"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Consent Tracking", success, details)
            return success
        except Exception as e:
            self.log_test("Consent Tracking", False, f"Exception: {str(e)}")
            return False
    
    def test_right_to_erasure(self) -> bool:
        """Test GDPR Article 17 right to erasure"""
        try:
            candidate_id = "test-candidate-erasure"
            
            response = self.session.post(
                f"{self.base_url}/admin/data-privacy/right-to-erasure/{candidate_id}",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "erasure_result" in data and
                    "status" in data["erasure_result"] and
                    "deleted_records" in data["erasure_result"]
                )
                
                if success:
                    result = data["erasure_result"]
                    status = result["status"]
                    deleted = result["deleted_records"]
                    details = f"Status: {response.status_code}, Erasure Status: {status}, Collections Processed: {len(deleted)}"
                else:
                    details = f"Status: {response.status_code}, Missing erasure result data"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Right to Erasure (GDPR Article 17)", success, details)
            return success
        except Exception as e:
            self.log_test("Right to Erasure (GDPR Article 17)", False, f"Exception: {str(e)}")
            return False
    
    def test_data_cleanup(self) -> bool:
        """Test automated data cleanup functionality"""
        try:
            response = self.session.post(
                f"{self.base_url}/admin/data-privacy/cleanup-expired",
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "cleanup_result" in data and
                    "status" in data["cleanup_result"] and
                    "cleanup_results" in data["cleanup_result"]
                )
                
                if success:
                    result = data["cleanup_result"]
                    status = result["status"]
                    cleanup_results = result["cleanup_results"]
                    details = f"Status: {response.status_code}, Cleanup Status: {status}, Collections Cleaned: {len(cleanup_results)}"
                else:
                    details = f"Status: {response.status_code}, Missing cleanup result data"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Automated Data Cleanup", success, details)
            return success
        except Exception as e:
            self.log_test("Automated Data Cleanup", False, f"Exception: {str(e)}")
            return False
    
    def test_audit_trail(self) -> bool:
        """Test audit trail functionality"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/data-privacy/audit-trail",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "audit_trail" in data and
                    isinstance(data["audit_trail"], list)
                )
                
                if success:
                    trail = data["audit_trail"]
                    details = f"Status: {response.status_code}, Audit Records: {len(trail)}"
                else:
                    details = f"Status: {response.status_code}, Missing audit trail data"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Audit Trail", success, details)
            return success
        except Exception as e:
            self.log_test("Audit Trail", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all Phase 2 AI enhancement tests"""
        print("=" * 80)
        print("PHASE 2 AI ENHANCEMENT & DATA PRIVACY TESTING")
        print("Testing Advanced AI Features & GDPR/CCPA Compliance")
        print("=" * 80)
        print()
        
        # Setup test data
        if not self.setup_test_data():
            print("❌ Failed to setup test data")
            return {}
        
        results = {}
        
        # Phase 2 AI Enhancement Features
        results["bias_detection"] = self.test_bias_detection_analysis()
        results["predictive_hiring"] = self.test_predictive_hiring_model()
        results["personality_analysis"] = self.test_personality_analysis()
        results["fairness_metrics"] = self.test_fairness_metrics()
        results["ml_model_training"] = self.test_ml_model_training()
        # Update test names in results
        results["ai_model_status"] = self.test_comprehensive_ai_analysis()
        
        # Data Privacy & GDPR/CCPA Compliance
        results["data_retention_policies"] = self.test_data_retention_policies()
        results["data_retention_status"] = self.test_data_retention_status()
        results["consent_tracking"] = self.test_consent_tracking()
        results["right_to_erasure"] = self.test_right_to_erasure()
        results["data_cleanup"] = self.test_data_cleanup()
        results["audit_trail"] = self.test_audit_trail()
        
        # Summary
        print("=" * 80)
        print("PHASE 2 TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by category
        categories = {
            "AI Enhancement Features": [
                "bias_detection", "predictive_hiring", "personality_analysis",
                "fairness_metrics", "ml_model_training", "ai_model_status"
            ],
            "Data Privacy & GDPR/CCPA": [
                "data_retention_policies", "data_retention_status", "consent_tracking",
                "right_to_erasure", "data_cleanup", "audit_trail"
            ]
        }
        
        for category, test_names in categories.items():
            print(f"\n{category}:")
            for test_name in test_names:
                if test_name in results:
                    status = "✅ PASS" if results[test_name] else "❌ FAIL"
                    print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL PHASE 2 TESTS PASSED! Advanced AI features and data privacy compliance working correctly.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Most Phase 2 features are functional with minor issues.")
        else:
            print("⚠️  Multiple Phase 2 tests failed. Check the details above.")
        
        return results

def main():
    """Main test execution"""
    tester = Phase2AITester()
    results = tester.run_all_tests()
    
    # Return exit code based on results
    all_passed = all(results.values()) if results else False
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())