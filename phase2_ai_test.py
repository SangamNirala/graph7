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
BASE_URL = "https://830251f7-f1b2-4513-bd41-31754723b024.preview.emergentagent.com/api"

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
            payload = {
                "assessment_data": {
                    "session_id": self.test_session_id,
                    "candidate_responses": [
                        "I have 5 years of experience in machine learning and AI development.",
                        "I believe diversity in teams leads to better innovation and problem-solving.",
                        "My approach to leadership is collaborative and inclusive."
                    ],
                    "interview_questions": [
                        "Tell me about your technical experience.",
                        "How do you view diversity in the workplace?",
                        "Describe your leadership style."
                    ]
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/ai-enhancements/bias-detection",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "bias_analysis" in data and
                    "fairness_metrics" in data and
                    "overall_bias_score" in data["bias_analysis"]
                )
                
                if success:
                    bias_score = data["bias_analysis"]["overall_bias_score"]
                    fairness = data["fairness_metrics"]
                    details = f"Status: {response.status_code}, Bias Score: {bias_score:.3f}, Demographic Parity: {fairness.get('demographic_parity', 'N/A')}"
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
            payload = {
                "assessment_data": {
                    "technical_score": 85,
                    "behavioral_score": 78,
                    "overall_score": 82,
                    "experience_years": 5,
                    "education_level": "Masters",
                    "skills_match": 0.85,
                    "communication_score": 80,
                    "problem_solving_score": 88
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/ai-enhancements/predictive-hiring",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "prediction" in data and
                    "success_probability" in data["prediction"] and
                    "confidence_score" in data["prediction"] and
                    "risk_factors" in data["prediction"]
                )
                
                if success:
                    prediction = data["prediction"]
                    success_prob = prediction["success_probability"]
                    confidence = prediction["confidence_score"]
                    details = f"Status: {response.status_code}, Success Probability: {success_prob:.2f}, Confidence: {confidence:.2f}"
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
            payload = {
                "multimodal_data": {
                    "text_responses": [
                        "I enjoy working in teams and collaborating on complex projects.",
                        "I'm always looking for new challenges and learning opportunities.",
                        "I prefer structured approaches but can adapt when needed.",
                        "I believe in maintaining high standards and attention to detail.",
                        "I try to stay calm under pressure and help others do the same."
                    ],
                    "voice_features": {
                        "pitch_mean": 180.5,
                        "energy_mean": 0.65,
                        "speaking_rate": 150,
                        "pause_frequency": 0.3
                    },
                    "behavioral_indicators": {
                        "response_time": 2.5,
                        "question_asking": 3,
                        "elaboration_tendency": 0.7
                    }
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/ai-enhancements/personality-analysis",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "personality_profile" in data and
                    "big_five_traits" in data["personality_profile"]
                )
                
                if success:
                    traits = data["personality_profile"]["big_five_traits"]
                    required_traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
                    success = all(trait in traits for trait in required_traits)
                    
                    if success:
                        details = f"Status: {response.status_code}, Big Five Traits: O:{traits['openness']:.2f}, C:{traits['conscientiousness']:.2f}, E:{traits['extraversion']:.2f}, A:{traits['agreeableness']:.2f}, N:{traits['neuroticism']:.2f}"
                    else:
                        details = f"Status: {response.status_code}, Missing Big Five traits"
                else:
                    details = f"Status: {response.status_code}, Missing personality profile"
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
            payload = {
                "assessment_groups": [
                    {"group": "A", "scores": [85, 78, 92, 76, 88], "hired": [1, 1, 1, 0, 1]},
                    {"group": "B", "scores": [82, 80, 75, 89, 84], "hired": [1, 1, 0, 1, 1]}
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/ai-enhancements/fairness-metrics",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "fairness_analysis" in data and
                    "demographic_parity" in data["fairness_analysis"] and
                    "equalized_odds" in data["fairness_analysis"]
                )
                
                if success:
                    analysis = data["fairness_analysis"]
                    dem_parity = analysis["demographic_parity"]
                    eq_odds = analysis["equalized_odds"]
                    details = f"Status: {response.status_code}, Demographic Parity: {dem_parity:.3f}, Equalized Odds: {eq_odds:.3f}"
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
            payload = {
                "training_data": [
                    {"features": [85, 78, 5, 0.85], "outcome": 1},
                    {"features": [72, 65, 3, 0.70], "outcome": 0},
                    {"features": [90, 88, 7, 0.92], "outcome": 1},
                    {"features": [68, 70, 2, 0.65], "outcome": 0},
                    {"features": [82, 80, 4, 0.80], "outcome": 1}
                ],
                "model_type": "random_forest",
                "validation_split": 0.2
            }
            
            response = self.session.post(
                f"{self.base_url}/ai-enhancements/train-model",
                json=payload,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "training_result" in data and
                    "model_performance" in data["training_result"] and
                    "accuracy" in data["training_result"]["model_performance"]
                )
                
                if success:
                    performance = data["training_result"]["model_performance"]
                    accuracy = performance["accuracy"]
                    details = f"Status: {response.status_code}, Model Accuracy: {accuracy:.3f}"
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
            payload = {
                "session_id": self.test_session_id,
                "assessment_data": {
                    "technical_score": 85,
                    "behavioral_score": 78,
                    "overall_score": 82,
                    "candidate_responses": [
                        "I have extensive experience in AI and machine learning.",
                        "I believe in collaborative and inclusive work environments.",
                        "I'm passionate about solving complex technical challenges."
                    ],
                    "voice_features": {
                        "confidence": 0.8,
                        "enthusiasm": 0.75,
                        "clarity": 0.85
                    }
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/ai-enhancements/comprehensive-analysis",
                json=payload,
                timeout=25
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (
                    "comprehensive_analysis" in data and
                    "bias_analysis" in data["comprehensive_analysis"] and
                    "predictive_analysis" in data["comprehensive_analysis"] and
                    "personality_analysis" in data["comprehensive_analysis"]
                )
                
                if success:
                    analysis = data["comprehensive_analysis"]
                    bias_score = analysis["bias_analysis"].get("overall_bias_score", 0)
                    success_prob = analysis["predictive_analysis"].get("success_probability", 0)
                    details = f"Status: {response.status_code}, Bias Score: {bias_score:.3f}, Success Probability: {success_prob:.2f}"
                else:
                    details = f"Status: {response.status_code}, Missing comprehensive analysis components"
            else:
                details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            
            self.log_test("Comprehensive AI Analysis", success, details)
            return success
        except Exception as e:
            self.log_test("Comprehensive AI Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_data_retention_policies(self) -> bool:
        """Test data retention policies management"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/data-privacy/retention-policies",
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
                f"{self.base_url}/admin/data-privacy/consent",
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
            payload = {
                "candidate_id": "test-candidate-erasure"
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/data-privacy/erasure",
                json=payload,
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
                f"{self.base_url}/admin/data-privacy/cleanup",
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
        results["comprehensive_ai_analysis"] = self.test_comprehensive_ai_analysis()
        
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
                "fairness_metrics", "ml_model_training", "comprehensive_ai_analysis"
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