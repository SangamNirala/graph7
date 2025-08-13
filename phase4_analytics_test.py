#!/usr/bin/env python3
"""
Phase 4 Analytics Backend Testing for AI Interview Platform
Tests the newly implemented Phase 4 Analytics features including:
- Executive Dashboard APIs (metrics, trends, real-time analytics, advanced reporting)
- ATS/CRM Integration APIs (Workday, Greenhouse, Lever, Salesforce)
- Advanced Video/Audio Analysis APIs (body language, engagement, speech patterns)
"""

import requests
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://aptiscore-engine.preview.emergentagent.com/api"

class Phase4AnalyticsTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.test_session_id = None
        self.test_candidate_data = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def setup_test_data(self):
        """Setup test data for analytics testing"""
        self.test_session_id = str(uuid.uuid4())
        self.test_candidate_data = {
            "candidate_id": str(uuid.uuid4()),
            "candidate_name": "John Analytics Tester",
            "job_title": "Senior Data Analyst",
            "email": "john.analytics@test.com",
            "phone": "+1-555-0123",
            "technical_score": 85,
            "behavioral_score": 78,
            "overall_score": 82,
            "overall_feedback": "Strong analytical skills with excellent communication",
            "created_at": datetime.utcnow().isoformat(),
            "company": "Analytics Corp",
            "current_title": "Data Scientist"
        }
    
    def test_admin_authentication(self) -> bool:
        """Test admin authentication for accessing analytics endpoints"""
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
                success = data.get("success", False)
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Admin Authentication for Analytics", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Authentication for Analytics", False, f"Exception: {str(e)}")
            return False
    
    # ==================== EXECUTIVE DASHBOARD TESTS ====================
    
    def test_executive_dashboard_metrics(self) -> bool:
        """Test comprehensive dashboard metrics endpoint"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/executive-dashboard/metrics",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "time_to_hire", "candidate_experience", "hiring_quality", 
                    "diversity_metrics", "cost_metrics"
                ]
                success = all(key in data for key in required_keys)
                
                # Validate data structure
                if success:
                    time_to_hire = data.get("time_to_hire", {})
                    success = all(key in time_to_hire for key in [
                        "average_time_to_hire", "median_time_to_hire", 
                        "time_distribution", "total_hires"
                    ])
            
            details = f"Status: {response.status_code}, Keys: {list(data.keys()) if success else 'N/A'}"
            self.log_test("Executive Dashboard Metrics", success, details)
            return success
        except Exception as e:
            self.log_test("Executive Dashboard Metrics", False, f"Exception: {str(e)}")
            return False
    
    def test_executive_dashboard_historical_trends(self) -> bool:
        """Test 6-month historical trends endpoint"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/executive-dashboard/historical-trends",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "time_to_hire_trend", "quality_trend", "volume_trend", 
                    "cost_trend", "diversity_trend"
                ]
                success = all(key in data for key in required_keys)
                
                # Validate trend data structure
                if success and data.get("time_to_hire_trend"):
                    trend_item = data["time_to_hire_trend"][0] if data["time_to_hire_trend"] else {}
                    success = all(key in trend_item for key in ["month", "average_time", "interview_count"])
            
            details = f"Status: {response.status_code}, Trends: {len(data.get('time_to_hire_trend', []))} months"
            self.log_test("Executive Dashboard Historical Trends", success, details)
            return success
        except Exception as e:
            self.log_test("Executive Dashboard Historical Trends", False, f"Exception: {str(e)}")
            return False
    
    def test_executive_dashboard_real_time_analytics(self) -> bool:
        """Test real-time analytics (last 24 hours) endpoint"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/executive-dashboard/real-time-analytics",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "active_interviews", "completed_today", "average_score_today",
                    "hourly_activity", "current_load"
                ]
                success = all(key in data for key in required_keys)
                
                # Validate real-time data structure
                if success:
                    hourly_activity = data.get("hourly_activity", [])
                    if hourly_activity:
                        activity_item = hourly_activity[0]
                        success = all(key in activity_item for key in ["hour", "interviews", "completions"])
            
            details = f"Status: {response.status_code}, Active: {data.get('active_interviews', 'N/A')}"
            self.log_test("Executive Dashboard Real-Time Analytics", success, details)
            return success
        except Exception as e:
            self.log_test("Executive Dashboard Real-Time Analytics", False, f"Exception: {str(e)}")
            return False
    
    def test_executive_dashboard_advanced_reporting(self) -> bool:
        """Test advanced reporting with hiring funnel and role performance"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/executive-dashboard/advanced-reporting",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "hiring_funnel", "role_performance", "focus_effectiveness",
                    "predictive_insights", "recommendations"
                ]
                success = all(key in data for key in required_keys)
                
                # Validate hiring funnel structure
                if success:
                    hiring_funnel = data.get("hiring_funnel", {})
                    success = all(key in hiring_funnel for key in [
                        "total_candidates", "interview_started", "interview_completed", "high_quality"
                    ])
            
            details = f"Status: {response.status_code}, Funnel: {data.get('hiring_funnel', {}).get('total_candidates', 'N/A')} candidates"
            self.log_test("Executive Dashboard Advanced Reporting", success, details)
            return success
        except Exception as e:
            self.log_test("Executive Dashboard Advanced Reporting", False, f"Exception: {str(e)}")
            return False
    
    # ==================== ATS/CRM INTEGRATION TESTS ====================
    
    def test_supported_systems(self) -> bool:
        """Test supported ATS/CRM systems endpoint"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/integrations/supported-systems",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                expected_systems = ["workday", "greenhouse", "lever", "salesforce"]
                systems = data.get("systems", [])
                success = all(system["name"] in expected_systems for system in systems)
                
                # Validate system structure
                if success and systems:
                    system = systems[0]
                    success = all(key in system for key in ["name", "display_name", "description", "status"])
            
            details = f"Status: {response.status_code}, Systems: {[s.get('name') for s in data.get('systems', [])]}"
            self.log_test("ATS/CRM Supported Systems", success, details)
            return success
        except Exception as e:
            self.log_test("ATS/CRM Supported Systems", False, f"Exception: {str(e)}")
            return False
    
    def test_sync_candidate_workday(self) -> bool:
        """Test syncing individual candidate to Workday"""
        try:
            response = self.session.post(
                f"{self.base_url}/admin/integrations/workday/sync-candidate",
                json=self.test_candidate_data,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("status") == "success" and 
                          "external_id" in data and 
                          data.get("system") == "workday")
            
            details = f"Status: {response.status_code}, External ID: {data.get('external_id', 'N/A') if success else 'N/A'}"
            self.log_test("Sync Candidate to Workday", success, details)
            return success
        except Exception as e:
            self.log_test("Sync Candidate to Workday", False, f"Exception: {str(e)}")
            return False
    
    def test_sync_candidate_greenhouse(self) -> bool:
        """Test syncing individual candidate to Greenhouse"""
        try:
            response = self.session.post(
                f"{self.base_url}/admin/integrations/greenhouse/sync-candidate",
                json=self.test_candidate_data,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("status") == "success" and 
                          "external_id" in data and 
                          data.get("system") == "greenhouse")
            
            details = f"Status: {response.status_code}, External ID: {data.get('external_id', 'N/A') if success else 'N/A'}"
            self.log_test("Sync Candidate to Greenhouse", success, details)
            return success
        except Exception as e:
            self.log_test("Sync Candidate to Greenhouse", False, f"Exception: {str(e)}")
            return False
    
    def test_bulk_sync_candidates(self) -> bool:
        """Test bulk syncing multiple candidates to Lever"""
        try:
            # Create multiple test candidates
            candidates = []
            for i in range(3):
                candidate = self.test_candidate_data.copy()
                candidate["candidate_id"] = str(uuid.uuid4())
                candidate["candidate_name"] = f"Bulk Test Candidate {i+1}"
                candidate["email"] = f"bulk.test{i+1}@test.com"
                candidates.append(candidate)
            
            response = self.session.post(
                f"{self.base_url}/admin/integrations/lever/bulk-sync",
                json={"candidates": candidates},
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = (data.get("total_candidates") == 3 and 
                          "successful_syncs" in data and 
                          "success_rate" in data)
            
            details = f"Status: {response.status_code}, Success Rate: {data.get('success_rate', 'N/A')}%"
            self.log_test("Bulk Sync Candidates to Lever", success, details)
            return success
        except Exception as e:
            self.log_test("Bulk Sync Candidates to Lever", False, f"Exception: {str(e)}")
            return False
    
    def test_sync_assessment_data(self) -> bool:
        """Test syncing all assessments to all systems"""
        try:
            response = self.session.post(
                f"{self.base_url}/admin/integrations/sync-assessment-data",
                json={},
                timeout=30
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("total_assessments" in data and 
                          "sync_results" in data and 
                          "summary" in data)
                
                # Validate sync results structure
                if success:
                    sync_results = data.get("sync_results", {})
                    expected_systems = ["workday", "greenhouse", "lever", "salesforce"]
                    success = all(system in sync_results for system in expected_systems)
            
            details = f"Status: {response.status_code}, Assessments: {data.get('total_assessments', 'N/A')}"
            self.log_test("Sync Assessment Data to All Systems", success, details)
            return success
        except Exception as e:
            self.log_test("Sync Assessment Data to All Systems", False, f"Exception: {str(e)}")
            return False
    
    def test_sync_history(self) -> bool:
        """Test getting synchronization history"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/integrations/sync-history",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "history" in data
                
                # Validate history structure if records exist
                if success and data.get("history"):
                    history_item = data["history"][0]
                    success = all(key in history_item for key in [
                        "system", "candidate_id", "status", "timestamp"
                    ])
            
            details = f"Status: {response.status_code}, Records: {len(data.get('history', []))}"
            self.log_test("ATS/CRM Sync History", success, details)
            return success
        except Exception as e:
            self.log_test("ATS/CRM Sync History", False, f"Exception: {str(e)}")
            return False
    
    def test_system_status(self) -> bool:
        """Test getting integration system status"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/integrations/system-status",
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = "systems" in data
                
                # Validate system status structure
                if success and data.get("systems"):
                    for system_name, system_status in data["systems"].items():
                        success = all(key in system_status for key in [
                            "status", "last_sync", "total_syncs", "success_rate"
                        ])
                        if not success:
                            break
            
            details = f"Status: {response.status_code}, Systems: {list(data.get('systems', {}).keys())}"
            self.log_test("ATS/CRM System Status", success, details)
            return success
        except Exception as e:
            self.log_test("ATS/CRM System Status", False, f"Exception: {str(e)}")
            return False
    
    # ==================== ADVANCED VIDEO/AUDIO ANALYSIS TESTS ====================
    
    def test_video_body_language_analysis(self) -> bool:
        """Test video body language analysis endpoint"""
        try:
            # Simulate video data
            video_data = {
                "session_id": self.test_session_id,
                "video_frames": ["frame1_base64", "frame2_base64", "frame3_base64"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/advanced-analysis/video/body-language",
                json=video_data,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "body_language_score", "confidence_indicators", "engagement_level",
                    "posture_analysis", "facial_expressions", "recommendations"
                ]
                success = all(key in data for key in required_keys)
            
            details = f"Status: {response.status_code}, Score: {data.get('body_language_score', 'N/A')}"
            self.log_test("Video Body Language Analysis", success, details)
            return success
        except Exception as e:
            self.log_test("Video Body Language Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_video_engagement_analysis(self) -> bool:
        """Test video engagement analysis for specific session"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/advanced-analysis/video/engagement/{self.test_session_id}",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "engagement_score", "attention_level", "eye_contact_analysis",
                    "facial_engagement", "timeline_analysis"
                ]
                success = all(key in data for key in required_keys)
            
            details = f"Status: {response.status_code}, Engagement: {data.get('engagement_score', 'N/A')}"
            self.log_test("Video Engagement Analysis", success, details)
            return success
        except Exception as e:
            self.log_test("Video Engagement Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_audio_enhancement(self) -> bool:
        """Test audio quality enhancement endpoint"""
        try:
            # Simulate audio data
            audio_data = {
                "session_id": self.test_session_id,
                "audio_data": "base64_encoded_audio_data",
                "enhancement_type": "noise_reduction",
                "quality_level": "high"
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/advanced-analysis/audio/enhance",
                json=audio_data,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "enhanced_audio", "improvement_metrics", "original_quality",
                    "enhanced_quality", "processing_time"
                ]
                success = all(key in data for key in required_keys)
            
            details = f"Status: {response.status_code}, Quality Improvement: {data.get('improvement_metrics', {}).get('quality_improvement', 'N/A')}"
            self.log_test("Audio Enhancement", success, details)
            return success
        except Exception as e:
            self.log_test("Audio Enhancement", False, f"Exception: {str(e)}")
            return False
    
    def test_speech_patterns_analysis(self) -> bool:
        """Test speech patterns analysis endpoint"""
        try:
            # Simulate speech data
            speech_data = {
                "session_id": self.test_session_id,
                "audio_data": "base64_encoded_audio_data",
                "transcript": "This is a sample transcript of the candidate's speech during the interview.",
                "analysis_type": "comprehensive"
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/advanced-analysis/audio/speech-patterns",
                json=speech_data,
                timeout=20
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "speech_rate", "pause_analysis", "vocal_variety", 
                    "clarity_score", "confidence_indicators", "emotional_tone"
                ]
                success = all(key in data for key in required_keys)
            
            details = f"Status: {response.status_code}, Speech Rate: {data.get('speech_rate', 'N/A')} WPM"
            self.log_test("Speech Patterns Analysis", success, details)
            return success
        except Exception as e:
            self.log_test("Speech Patterns Analysis", False, f"Exception: {str(e)}")
            return False
    
    def test_comprehensive_analysis_report(self) -> bool:
        """Test comprehensive analysis report for session"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/advanced-analysis/comprehensive-report/{self.test_session_id}",
                timeout=25
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "session_id", "video_analysis", "audio_analysis", 
                    "combined_insights", "recommendations", "overall_score"
                ]
                success = all(key in data for key in required_keys)
                
                # Validate nested analysis structure
                if success:
                    video_analysis = data.get("video_analysis", {})
                    audio_analysis = data.get("audio_analysis", {})
                    success = ("body_language" in video_analysis and 
                              "speech_patterns" in audio_analysis)
            
            details = f"Status: {response.status_code}, Overall Score: {data.get('overall_score', 'N/A')}"
            self.log_test("Comprehensive Analysis Report", success, details)
            return success
        except Exception as e:
            self.log_test("Comprehensive Analysis Report", False, f"Exception: {str(e)}")
            return False
    
    def test_analytics_summary(self) -> bool:
        """Test analytics summary endpoint"""
        try:
            response = self.session.get(
                f"{self.base_url}/admin/advanced-analysis/analytics-summary",
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                required_keys = [
                    "total_sessions_analyzed", "average_scores", "trend_analysis",
                    "top_insights", "system_performance"
                ]
                success = all(key in data for key in required_keys)
                
                # Validate average scores structure
                if success:
                    avg_scores = data.get("average_scores", {})
                    success = all(key in avg_scores for key in [
                        "body_language", "engagement", "speech_quality", "overall"
                    ])
            
            details = f"Status: {response.status_code}, Sessions Analyzed: {data.get('total_sessions_analyzed', 'N/A')}"
            self.log_test("Advanced Analytics Summary", success, details)
            return success
        except Exception as e:
            self.log_test("Advanced Analytics Summary", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all Phase 4 Analytics tests"""
        print("🚀 Starting Phase 4 Analytics Backend Testing")
        print("=" * 60)
        
        # Setup test data
        self.setup_test_data()
        
        # Track test results
        test_results = []
        
        # Authentication test
        test_results.append(self.test_admin_authentication())
        
        print("\n📊 EXECUTIVE DASHBOARD TESTS")
        print("-" * 40)
        test_results.append(self.test_executive_dashboard_metrics())
        test_results.append(self.test_executive_dashboard_historical_trends())
        test_results.append(self.test_executive_dashboard_real_time_analytics())
        test_results.append(self.test_executive_dashboard_advanced_reporting())
        
        print("\n🔗 ATS/CRM INTEGRATION TESTS")
        print("-" * 40)
        test_results.append(self.test_supported_systems())
        test_results.append(self.test_sync_candidate_workday())
        test_results.append(self.test_sync_candidate_greenhouse())
        test_results.append(self.test_bulk_sync_candidates())
        test_results.append(self.test_sync_assessment_data())
        test_results.append(self.test_sync_history())
        test_results.append(self.test_system_status())
        
        print("\n🎥 ADVANCED VIDEO/AUDIO ANALYSIS TESTS")
        print("-" * 40)
        test_results.append(self.test_video_body_language_analysis())
        test_results.append(self.test_video_engagement_analysis())
        test_results.append(self.test_audio_enhancement())
        test_results.append(self.test_speech_patterns_analysis())
        test_results.append(self.test_comprehensive_analysis_report())
        test_results.append(self.test_analytics_summary())
        
        # Summary
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        print("\n" + "=" * 60)
        print("📋 PHASE 4 ANALYTICS TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate == 100:
            print("🎉 All Phase 4 Analytics features are working perfectly!")
        elif success_rate >= 80:
            print("✅ Phase 4 Analytics features are mostly functional with minor issues")
        else:
            print("⚠️  Phase 4 Analytics features need attention - multiple failures detected")
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = Phase4AnalyticsTester()
    tester.run_all_tests()