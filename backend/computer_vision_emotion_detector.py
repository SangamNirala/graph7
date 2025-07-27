"""
Phase 3: Advanced AI & Analytics - Week 7: Open-Source AI Model Integration
Step 7.3: Computer Vision Emotion Detection

This module provides facial expression analysis during interviews using OpenCV and FER
for real-time emotion tracking, attention/engagement scoring, and privacy-compliant video analysis.
"""

import os
import logging
import cv2
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
import json
import base64
import io
from datetime import datetime, timedelta
import asyncio
from PIL import Image
import torch

# Try to import FER for emotion detection
try:
    from fer import FER
    FER_AVAILABLE = True
    logging.info("✅ FER library loaded successfully")
except ImportError as e:
    FER_AVAILABLE = False
    logging.warning(f"⚠️  FER library not available: {str(e)}")

# Import additional computer vision libraries
try:
    import imutils
    IMUTILS_AVAILABLE = True
except ImportError:
    IMUTILS_AVAILABLE = False
    logging.warning("⚠️  imutils library not available")


class ComputerVisionEmotionDetector:
    """
    Computer vision-based emotion detection system for interview analysis
    Features:
    - Real-time facial expression recognition
    - Emotion tracking over time
    - Attention and engagement scoring
    - Privacy-compliant analysis
    - Multi-face detection and analysis
    """
    
    def __init__(self):
        self.face_cascade = None
        self.emotion_detector = None
        self.emotion_history = []
        self.engagement_tracker = []
        
        # Initialize OpenCV face detection
        self._initialize_face_detection()
        
        # Initialize FER emotion detection if available
        self._initialize_emotion_detection()
        
        # Emotion categories and mapping
        self.emotion_categories = {
            'positive': ['happy', 'joy', 'excitement', 'surprise'],
            'neutral': ['neutral', 'calm'],
            'negative': ['sad', 'angry', 'fear', 'disgust'],
            'engagement': ['interested', 'focused', 'attentive'],
            'disengagement': ['bored', 'distracted', 'confused']
        }
        
        # Privacy settings
        self.privacy_mode = True  # Never store actual face images
        self.store_analysis_only = True
        
        logging.info("ComputerVisionEmotionDetector initialized")
    
    def _initialize_face_detection(self):
        """Initialize OpenCV face detection cascade"""
        try:
            # Try to load Haar cascade for face detection
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                logging.error("Failed to load face cascade classifier")
                self.face_cascade = None
            else:
                logging.info("✅ OpenCV face detection initialized")
                
        except Exception as e:
            logging.error(f"Error initializing face detection: {str(e)}")
            self.face_cascade = None
    
    def _initialize_emotion_detection(self):
        """Initialize FER emotion detection model"""
        try:
            if FER_AVAILABLE:
                # Initialize FER with MTCNN for better face detection
                self.emotion_detector = FER(mtcnn=True)
                logging.info("✅ FER emotion detection initialized")
            else:
                logging.warning("⚠️  FER not available - using basic emotion estimation")
                self.emotion_detector = None
                
        except Exception as e:
            logging.error(f"Error initializing emotion detection: {str(e)}")
            self.emotion_detector = None
    
    async def analyze_frame_emotions(self, frame_data: bytes, timestamp: datetime = None) -> Dict[str, Any]:
        """
        Analyze emotions in a single video frame
        """
        try:
            if timestamp is None:
                timestamp = datetime.utcnow()
            
            analysis = {
                "timestamp": timestamp.isoformat(),
                "faces_detected": 0,
                "emotions": {},
                "engagement_metrics": {},
                "attention_indicators": {},
                "face_quality_metrics": {},
                "privacy_compliant": True
            }
            
            # Convert bytes to OpenCV image
            image = self._bytes_to_opencv_image(frame_data)
            if image is None:
                return self._get_fallback_frame_analysis("Invalid image data")
            
            # Detect faces in the frame
            faces = self._detect_faces(image)
            analysis["faces_detected"] = len(faces)
            
            if len(faces) == 0:
                return self._get_fallback_frame_analysis("No faces detected")
            
            # Analyze each detected face
            face_analyses = []
            for i, face_region in enumerate(faces):
                face_analysis = await self._analyze_single_face(image, face_region, i)
                face_analyses.append(face_analysis)
            
            # Combine analyses from all faces (focus on primary face)
            if face_analyses:
                primary_face = max(face_analyses, key=lambda x: x.get('face_area', 0))
                analysis.update(primary_face)
            
            # Calculate frame-level metrics
            analysis["engagement_metrics"] = self._calculate_frame_engagement(face_analyses)
            analysis["attention_indicators"] = self._calculate_attention_indicators(face_analyses)
            
            return analysis
            
        except Exception as e:
            logging.error(f"Error analyzing frame emotions: {str(e)}")
            return self._get_fallback_frame_analysis(f"Analysis error: {str(e)}")
    
    def _bytes_to_opencv_image(self, frame_data: bytes) -> Optional[np.ndarray]:
        """Convert bytes data to OpenCV image format"""
        try:
            # Try different approaches to decode image
            try:
                # Method 1: Direct numpy conversion (for base64 or raw data)
                if isinstance(frame_data, str):
                    # Remove data URL prefix if present
                    if 'data:image' in frame_data:
                        frame_data = frame_data.split(',')[1]
                    # Decode base64
                    frame_data = base64.b64decode(frame_data)
                
                # Convert to numpy array
                nparr = np.frombuffer(frame_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if image is not None:
                    return image
                    
            except Exception as e:
                logging.debug(f"Method 1 failed: {str(e)}")
            
            try:
                # Method 2: PIL conversion
                pil_image = Image.open(io.BytesIO(frame_data))
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                return image
                
            except Exception as e:
                logging.debug(f"Method 2 failed: {str(e)}")
            
            return None
            
        except Exception as e:
            logging.error(f"Error converting bytes to OpenCV image: {str(e)}")
            return None
    
    def _detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect faces in the image using OpenCV"""
        try:
            faces = []
            
            if self.face_cascade is not None:
                # Convert to grayscale for face detection
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                detected_faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                
                faces = [(x, y, w, h) for (x, y, w, h) in detected_faces]
            
            return faces
            
        except Exception as e:
            logging.error(f"Error detecting faces: {str(e)}")
            return []
    
    async def _analyze_single_face(self, image: np.ndarray, face_region: Tuple[int, int, int, int], face_index: int) -> Dict[str, Any]:
        """Analyze emotions and engagement for a single detected face"""
        try:
            x, y, w, h = face_region
            face_analysis = {
                "face_index": face_index,
                "face_area": w * h,
                "face_position": {"x": x, "y": y, "width": w, "height": h},
                "emotions": {},
                "engagement_score": 0.0,
                "attention_score": 0.0,
                "face_quality": {}
            }
            
            # Extract face region
            face_roi = image[y:y+h, x:x+w]
            
            # Analyze face quality
            face_analysis["face_quality"] = self._assess_face_quality(face_roi)
            
            # Emotion detection using FER if available
            if self.emotion_detector is not None:
                emotions = await self._detect_emotions_fer(face_roi)
                face_analysis["emotions"] = emotions
            else:
                # Fallback emotion estimation
                emotions = self._estimate_emotions_basic(face_roi)
                face_analysis["emotions"] = emotions
            
            # Calculate engagement and attention scores
            face_analysis["engagement_score"] = self._calculate_face_engagement(emotions, face_analysis["face_quality"])
            face_analysis["attention_score"] = self._calculate_attention_score(face_region, image.shape)
            
            return face_analysis
            
        except Exception as e:
            logging.error(f"Error analyzing single face: {str(e)}")
            return {
                "face_index": face_index,
                "face_area": 0,
                "emotions": {"neutral": 1.0},
                "engagement_score": 0.5,
                "attention_score": 0.5,
                "error": str(e)
            }
    
    async def _detect_emotions_fer(self, face_roi: np.ndarray) -> Dict[str, float]:
        """Detect emotions using FER library"""
        try:
            if self.emotion_detector is None:
                return {"neutral": 1.0}
            
            # FER expects RGB format
            face_rgb = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
            
            # Detect emotions
            emotions = self.emotion_detector.detect_emotions(face_rgb)
            
            if emotions and len(emotions) > 0:
                # Get emotions from first detected face
                emotion_scores = emotions[0]['emotions']
                
                # Normalize scores to ensure they sum to 1.0
                total_score = sum(emotion_scores.values())
                if total_score > 0:
                    normalized_emotions = {
                        emotion: score / total_score 
                        for emotion, score in emotion_scores.items()
                    }
                else:
                    normalized_emotions = {"neutral": 1.0}
                
                return normalized_emotions
            else:
                return {"neutral": 1.0}
                
        except Exception as e:
            logging.error(f"Error in FER emotion detection: {str(e)}")
            return {"neutral": 1.0}
    
    def _estimate_emotions_basic(self, face_roi: np.ndarray) -> Dict[str, float]:
        """
        Basic emotion estimation using simple computer vision techniques
        This is a fallback when FER is not available
        """
        try:
            emotions = {"neutral": 0.7, "happy": 0.1, "sad": 0.1, "surprise": 0.05, "angry": 0.05}
            
            # Convert to grayscale
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            
            # Basic feature analysis
            height, width = gray.shape
            
            # Analyze brightness distribution (rough emotion indicators)
            brightness = np.mean(gray)
            contrast = np.std(gray)
            
            # Simple heuristics (very basic - not as accurate as proper ML models)
            if brightness > 120 and contrast > 30:
                # Brighter face with good contrast might indicate happiness
                emotions["happy"] = min(0.6, emotions["happy"] + 0.3)
                emotions["neutral"] -= 0.3
            elif brightness < 80:
                # Darker regions might indicate sadness
                emotions["sad"] = min(0.5, emotions["sad"] + 0.2)
                emotions["neutral"] -= 0.2
            
            # Ensure emotions sum to 1.0
            total = sum(emotions.values())
            emotions = {k: v/total for k, v in emotions.items()}
            
            return emotions
            
        except Exception as e:
            logging.error(f"Error in basic emotion estimation: {str(e)}")
            return {"neutral": 1.0}
    
    def _assess_face_quality(self, face_roi: np.ndarray) -> Dict[str, float]:
        """Assess the quality of detected face for reliable emotion analysis"""
        try:
            quality_metrics = {}
            
            # Face size adequacy
            height, width = face_roi.shape[:2]
            face_area = height * width
            quality_metrics["size_adequacy"] = min(1.0, face_area / 10000)  # Normalize by 100x100 pixels
            
            # Brightness check
            gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY) if len(face_roi.shape) == 3 else face_roi
            brightness = np.mean(gray)
            # Optimal brightness range is 80-180
            if 80 <= brightness <= 180:
                quality_metrics["brightness_quality"] = 1.0
            else:
                quality_metrics["brightness_quality"] = max(0.0, 1.0 - abs(brightness - 130) / 130)
            
            # Contrast check
            contrast = np.std(gray)
            quality_metrics["contrast_quality"] = min(1.0, contrast / 50)  # Normalize by expected contrast
            
            # Sharpness estimate using Laplacian variance
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            quality_metrics["sharpness"] = min(1.0, laplacian_var / 1000)  # Normalize
            
            # Overall quality score
            quality_metrics["overall_quality"] = np.mean(list(quality_metrics.values()))
            
            return quality_metrics
            
        except Exception as e:
            logging.error(f"Error assessing face quality: {str(e)}")
            return {
                "size_adequacy": 0.5,
                "brightness_quality": 0.5,
                "contrast_quality": 0.5,
                "sharpness": 0.5,
                "overall_quality": 0.5
            }
    
    def _calculate_face_engagement(self, emotions: Dict[str, float], face_quality: Dict[str, float]) -> float:
        """Calculate engagement score based on emotions and face quality"""
        try:
            # Engagement indicators
            positive_emotions = ['happy', 'surprise']
            engaged_emotions = ['happy', 'surprise', 'neutral']  # Neutral can indicate focus
            disengaged_emotions = ['sad', 'angry', 'fear', 'disgust']
            
            # Calculate engagement based on emotion distribution
            engagement_score = 0.0
            
            for emotion, score in emotions.items():
                if emotion in positive_emotions:
                    engagement_score += score * 1.0  # Full weight for positive emotions
                elif emotion in engaged_emotions:
                    engagement_score += score * 0.7  # Moderate weight for neutral engagement
                elif emotion in disengaged_emotions:
                    engagement_score -= score * 0.5  # Penalty for disengaged emotions
            
            # Adjust based on face quality (better quality = more reliable engagement score)
            quality_factor = face_quality.get("overall_quality", 0.5)
            engagement_score = engagement_score * quality_factor + 0.5 * (1 - quality_factor)
            
            # Normalize to 0-1 range
            engagement_score = max(0.0, min(1.0, engagement_score))
            
            return float(engagement_score)
            
        except Exception as e:
            logging.error(f"Error calculating face engagement: {str(e)}")
            return 0.5
    
    def _calculate_attention_score(self, face_region: Tuple[int, int, int, int], image_shape: Tuple[int, int, int]) -> float:
        """Calculate attention score based on face position and size"""
        try:
            x, y, w, h = face_region
            image_height, image_width = image_shape[:2]
            
            # Face center
            face_center_x = x + w // 2
            face_center_y = y + h // 2
            
            # Image center
            image_center_x = image_width // 2
            image_center_y = image_height // 2
            
            # Distance from center (normalized)
            distance_from_center = np.sqrt(
                ((face_center_x - image_center_x) / image_width) ** 2 +
                ((face_center_y - image_center_y) / image_height) ** 2
            )
            
            # Attention score decreases with distance from center
            center_attention = max(0.0, 1.0 - distance_from_center * 2)
            
            # Face size relative to image (larger faces generally indicate more attention)
            face_area = w * h
            image_area = image_width * image_height
            relative_face_size = face_area / image_area
            
            # Size attention score
            size_attention = min(1.0, relative_face_size * 20)  # Normalize
            
            # Combined attention score
            attention_score = (center_attention * 0.7 + size_attention * 0.3)
            
            return float(attention_score)
            
        except Exception as e:
            logging.error(f"Error calculating attention score: {str(e)}")
            return 0.5
    
    def _calculate_frame_engagement(self, face_analyses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate overall engagement metrics for the frame"""
        try:
            if not face_analyses:
                return {"overall_engagement": 0.0, "attention_level": 0.0, "emotional_positivity": 0.0}
            
            # Average engagement across all faces
            engagement_scores = [face.get("engagement_score", 0.0) for face in face_analyses]
            attention_scores = [face.get("attention_score", 0.0) for face in face_analyses]
            
            overall_engagement = np.mean(engagement_scores)
            attention_level = np.mean(attention_scores)
            
            # Calculate emotional positivity
            all_emotions = {}
            for face in face_analyses:
                emotions = face.get("emotions", {})
                for emotion, score in emotions.items():
                    all_emotions[emotion] = all_emotions.get(emotion, 0.0) + score
            
            # Normalize emotion scores
            total_emotion_score = sum(all_emotions.values())
            if total_emotion_score > 0:
                normalized_emotions = {k: v/total_emotion_score for k, v in all_emotions.items()}
            else:
                normalized_emotions = {"neutral": 1.0}
            
            # Calculate positivity
            positive_emotions = ['happy', 'surprise']
            emotional_positivity = sum(normalized_emotions.get(emotion, 0.0) for emotion in positive_emotions)
            
            return {
                "overall_engagement": float(overall_engagement),
                "attention_level": float(attention_level),
                "emotional_positivity": float(emotional_positivity),
                "dominant_emotion": max(normalized_emotions, key=normalized_emotions.get),
                "emotion_distribution": normalized_emotions
            }
            
        except Exception as e:
            logging.error(f"Error calculating frame engagement: {str(e)}")
            return {"overall_engagement": 0.5, "attention_level": 0.5, "emotional_positivity": 0.3}
    
    def _calculate_attention_indicators(self, face_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate attention indicators from face analyses"""
        try:
            if not face_analyses:
                return {"eye_contact_estimate": 0.0, "focus_stability": 0.0, "distraction_indicators": []}
            
            attention_indicators = {}
            
            # Eye contact estimation (based on face position and attention scores)
            attention_scores = [face.get("attention_score", 0.0) for face in face_analyses]
            eye_contact_estimate = np.mean(attention_scores)
            attention_indicators["eye_contact_estimate"] = float(eye_contact_estimate)
            
            # Focus stability (consistency of attention across faces)
            if len(attention_scores) > 1:
                focus_stability = 1.0 - np.std(attention_scores)
            else:
                focus_stability = 1.0  # Single face is stable by definition
            attention_indicators["focus_stability"] = float(max(0.0, focus_stability))
            
            # Distraction indicators
            distraction_indicators = []
            
            # Multiple faces might indicate distraction
            if len(face_analyses) > 1:
                distraction_indicators.append("multiple_faces_detected")
            
            # Low attention scores indicate distraction
            if eye_contact_estimate < 0.3:
                distraction_indicators.append("low_attention_score")
            
            # Poor face quality might indicate movement/distraction
            quality_scores = [face.get("face_quality", {}).get("overall_quality", 0.5) for face in face_analyses]
            avg_quality = np.mean(quality_scores)
            if avg_quality < 0.4:
                distraction_indicators.append("poor_image_quality")
            
            attention_indicators["distraction_indicators"] = distraction_indicators
            attention_indicators["distraction_level"] = len(distraction_indicators) / 3.0  # Normalize by max indicators
            
            return attention_indicators
            
        except Exception as e:
            logging.error(f"Error calculating attention indicators: {str(e)}")
            return {"eye_contact_estimate": 0.5, "focus_stability": 0.5, "distraction_indicators": [], "distraction_level": 0.0}
    
    async def analyze_video_session(self, frame_analyses: List[Dict[str, Any]], session_duration: float) -> Dict[str, Any]:
        """
        Analyze complete video session for overall emotion and engagement patterns
        """
        try:
            if not frame_analyses:
                return self._get_fallback_session_analysis("No frame analyses provided")
            
            session_analysis = {
                "session_duration": session_duration,
                "total_frames_analyzed": len(frame_analyses),
                "emotion_timeline": [],
                "engagement_timeline": [],
                "overall_metrics": {},
                "attention_patterns": {},
                "emotional_journey": {},
                "recommendations": []
            }
            
            # Extract time series data
            timestamps = []
            engagement_scores = []
            attention_scores = []
            emotion_data = []
            
            for frame in frame_analyses:
                if isinstance(frame.get("timestamp", ""), str):
                    timestamps.append(frame["timestamp"])
                
                engagement_metrics = frame.get("engagement_metrics", {})
                engagement_scores.append(engagement_metrics.get("overall_engagement", 0.0))
                attention_scores.append(engagement_metrics.get("attention_level", 0.0))
                emotion_data.append(engagement_metrics.get("emotion_distribution", {}))
            
            # Calculate overall metrics
            session_analysis["overall_metrics"] = {
                "average_engagement": float(np.mean(engagement_scores)) if engagement_scores else 0.0,
                "max_engagement": float(np.max(engagement_scores)) if engagement_scores else 0.0,
                "min_engagement": float(np.min(engagement_scores)) if engagement_scores else 0.0,
                "engagement_stability": float(1.0 - np.std(engagement_scores)) if len(engagement_scores) > 1 else 1.0,
                "average_attention": float(np.mean(attention_scores)) if attention_scores else 0.0,
                "attention_consistency": float(1.0 - np.std(attention_scores)) if len(attention_scores) > 1 else 1.0
            }
            
            # Analyze emotional journey
            session_analysis["emotional_journey"] = await self._analyze_emotional_journey(emotion_data)
            
            # Analyze attention patterns
            session_analysis["attention_patterns"] = await self._analyze_attention_patterns(attention_scores, timestamps)
            
            # Create engagement timeline (sampled for performance)
            timeline_samples = min(100, len(engagement_scores))  # Max 100 samples
            if timeline_samples > 0:
                sample_indices = np.linspace(0, len(engagement_scores) - 1, timeline_samples, dtype=int)
                session_analysis["engagement_timeline"] = [
                    {"timestamp": timestamps[i] if i < len(timestamps) else f"frame_{i}", 
                     "engagement": engagement_scores[i],
                     "attention": attention_scores[i]}
                    for i in sample_indices
                ]
            
            # Generate recommendations
            session_analysis["recommendations"] = await self._generate_video_recommendations(session_analysis)
            
            return session_analysis
            
        except Exception as e:
            logging.error(f"Error analyzing video session: {str(e)}")
            return self._get_fallback_session_analysis(f"Analysis error: {str(e)}")
    
    async def _analyze_emotional_journey(self, emotion_data: List[Dict[str, float]]) -> Dict[str, Any]:
        """Analyze how emotions change over time during the session"""
        try:
            if not emotion_data:
                return {"dominant_emotions": ["neutral"], "emotional_stability": 0.5, "emotional_peaks": []}
            
            # Aggregate emotions across all frames
            emotion_totals = {}
            for frame_emotions in emotion_data:
                for emotion, score in frame_emotions.items():
                    emotion_totals[emotion] = emotion_totals.get(emotion, 0.0) + score
            
            # Normalize and find dominant emotions
            total_emotion_score = sum(emotion_totals.values())
            if total_emotion_score > 0:
                normalized_emotions = {k: v/total_emotion_score for k, v in emotion_totals.items()}
            else:
                normalized_emotions = {"neutral": 1.0}
            
            # Find dominant emotions (top 3)
            sorted_emotions = sorted(normalized_emotions.items(), key=lambda x: x[1], reverse=True)
            dominant_emotions = [emotion for emotion, score in sorted_emotions[:3]]
            
            # Calculate emotional stability
            emotion_variances = []
            for emotion in normalized_emotions.keys():
                emotion_timeline = [frame.get(emotion, 0.0) for frame in emotion_data]
                if len(emotion_timeline) > 1:
                    emotion_variances.append(np.var(emotion_timeline))
            
            emotional_stability = 1.0 - np.mean(emotion_variances) if emotion_variances else 0.5
            
            # Identify emotional peaks (simplified)
            emotional_peaks = []
            if len(emotion_data) > 5:
                # Find frames with significantly high positive emotions
                for i, frame_emotions in enumerate(emotion_data):
                    positive_score = frame_emotions.get('happy', 0.0) + frame_emotions.get('surprise', 0.0)
                    if positive_score > 0.7:
                        emotional_peaks.append({
                            "frame_index": i,
                            "peak_type": "positive",
                            "intensity": positive_score
                        })
            
            return {
                "dominant_emotions": dominant_emotions,
                "emotion_distribution": normalized_emotions,
                "emotional_stability": float(max(0.0, emotional_stability)),
                "emotional_peaks": emotional_peaks,
                "overall_emotional_tone": dominant_emotions[0] if dominant_emotions else "neutral"
            }
            
        except Exception as e:
            logging.error(f"Error analyzing emotional journey: {str(e)}")
            return {"dominant_emotions": ["neutral"], "emotional_stability": 0.5, "emotional_peaks": []}
    
    async def _analyze_attention_patterns(self, attention_scores: List[float], timestamps: List[str]) -> Dict[str, Any]:
        """Analyze attention patterns throughout the session"""
        try:
            if not attention_scores:
                return {"attention_trend": "stable", "attention_drops": [], "peak_attention_periods": []}
            
            attention_patterns = {}
            
            # Calculate attention trend
            if len(attention_scores) > 2:
                # Simple linear trend
                x = np.arange(len(attention_scores))
                trend_slope = np.polyfit(x, attention_scores, 1)[0]
                
                if trend_slope > 0.01:
                    attention_patterns["attention_trend"] = "improving"
                elif trend_slope < -0.01:
                    attention_patterns["attention_trend"] = "declining"
                else:
                    attention_patterns["attention_trend"] = "stable"
                    
                attention_patterns["trend_strength"] = float(abs(trend_slope))
            else:
                attention_patterns["attention_trend"] = "insufficient_data"
                attention_patterns["trend_strength"] = 0.0
            
            # Identify attention drops (below 30% of max attention)
            if attention_scores:
                max_attention = max(attention_scores)
                threshold = max_attention * 0.3
                
                attention_drops = []
                for i, score in enumerate(attention_scores):
                    if score < threshold:
                        attention_drops.append({
                            "frame_index": i,
                            "attention_score": score,
                            "timestamp": timestamps[i] if i < len(timestamps) else f"frame_{i}"
                        })
                
                attention_patterns["attention_drops"] = attention_drops[:10]  # Limit to first 10
            
            # Identify peak attention periods (above 80% of max)
            if attention_scores:
                max_attention = max(attention_scores)
                threshold = max_attention * 0.8
                
                peak_periods = []
                for i, score in enumerate(attention_scores):
                    if score >= threshold:
                        peak_periods.append({
                            "frame_index": i,
                            "attention_score": score,
                            "timestamp": timestamps[i] if i < len(timestamps) else f"frame_{i}"
                        })
                
                attention_patterns["peak_attention_periods"] = peak_periods[:10]  # Limit to first 10
            
            # Overall attention quality
            avg_attention = np.mean(attention_scores)
            if avg_attention > 0.7:
                attention_patterns["overall_attention_quality"] = "excellent"
            elif avg_attention > 0.5:
                attention_patterns["overall_attention_quality"] = "good"
            elif avg_attention > 0.3:
                attention_patterns["overall_attention_quality"] = "fair"
            else:
                attention_patterns["overall_attention_quality"] = "poor"
            
            return attention_patterns
            
        except Exception as e:
            logging.error(f"Error analyzing attention patterns: {str(e)}")
            return {"attention_trend": "unknown", "attention_drops": [], "peak_attention_periods": []}
    
    async def _generate_video_recommendations(self, session_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on video analysis"""
        try:
            recommendations = []
            
            overall_metrics = session_analysis.get("overall_metrics", {})
            emotional_journey = session_analysis.get("emotional_journey", {})
            attention_patterns = session_analysis.get("attention_patterns", {})
            
            # Engagement recommendations
            avg_engagement = overall_metrics.get("average_engagement", 0.0)
            if avg_engagement < 0.5:
                recommendations.append("Work on maintaining better eye contact and facial engagement during interviews")
            
            engagement_stability = overall_metrics.get("engagement_stability", 0.0)
            if engagement_stability < 0.5:
                recommendations.append("Practice maintaining consistent engagement throughout the interview")
            
            # Attention recommendations
            avg_attention = overall_metrics.get("average_attention", 0.0)
            if avg_attention < 0.5:
                recommendations.append("Position yourself centrally in the camera frame for better attention indicators")
            
            attention_trend = attention_patterns.get("attention_trend", "stable")
            if attention_trend == "declining":
                recommendations.append("Take breaks during long interviews to maintain attention and focus")
            
            # Emotional recommendations
            dominant_emotions = emotional_journey.get("dominant_emotions", ["neutral"])
            if "sad" in dominant_emotions[:2] or "angry" in dominant_emotions[:2]:
                recommendations.append("Practice positive visualization before interviews to improve emotional state")
            
            emotional_stability = emotional_journey.get("emotional_stability", 0.5)
            if emotional_stability < 0.5:
                recommendations.append("Work on emotional regulation techniques for more stable interview performance")
            
            # Technical recommendations
            attention_drops = attention_patterns.get("attention_drops", [])
            if len(attention_drops) > len(session_analysis.get("engagement_timeline", [])) * 0.3:
                recommendations.append("Improve lighting and camera setup for better video quality")
            
            # General recommendations if no specific issues
            if not recommendations:
                recommendations.extend([
                    "Maintain your current positive interview presence",
                    "Continue practicing to build confidence",
                    "Consider using the video analysis to track improvements over time"
                ])
            
            return recommendations[:5]  # Return top 5 recommendations
            
        except Exception as e:
            logging.error(f"Error generating video recommendations: {str(e)}")
            return ["Continue practicing your interview skills", "Focus on maintaining good eye contact"]
    
    def _get_fallback_frame_analysis(self, error_message: str) -> Dict[str, Any]:
        """Return fallback analysis when frame analysis fails"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "faces_detected": 0,
            "emotions": {"neutral": 1.0},
            "engagement_metrics": {
                "overall_engagement": 0.5,
                "attention_level": 0.5,
                "emotional_positivity": 0.3,
                "dominant_emotion": "neutral"
            },
            "attention_indicators": {
                "eye_contact_estimate": 0.5,
                "focus_stability": 0.5,
                "distraction_indicators": [],
                "distraction_level": 0.0
            },
            "face_quality_metrics": {"overall_quality": 0.5},
            "privacy_compliant": True,
            "error": error_message
        }
    
    def _get_fallback_session_analysis(self, error_message: str) -> Dict[str, Any]:
        """Return fallback analysis when session analysis fails"""
        return {
            "session_duration": 0.0,
            "total_frames_analyzed": 0,
            "emotion_timeline": [],
            "engagement_timeline": [],
            "overall_metrics": {
                "average_engagement": 0.5,
                "engagement_stability": 0.5,
                "average_attention": 0.5,
                "attention_consistency": 0.5
            },
            "attention_patterns": {
                "attention_trend": "unknown",
                "overall_attention_quality": "fair"
            },
            "emotional_journey": {
                "dominant_emotions": ["neutral"],
                "emotional_stability": 0.5,
                "overall_emotional_tone": "neutral"
            },
            "recommendations": ["Video analysis temporarily unavailable"],
            "error": error_message
        }
    
    def get_detector_status(self) -> Dict[str, bool]:
        """Get status of computer vision components"""
        return {
            "opencv_available": self.face_cascade is not None,
            "fer_available": FER_AVAILABLE and self.emotion_detector is not None,
            "imutils_available": IMUTILS_AVAILABLE,
            "face_detection_ready": self.face_cascade is not None,
            "emotion_detection_ready": self.emotion_detector is not None,
            "privacy_mode": self.privacy_mode,
            "system_ready": self.face_cascade is not None or self.emotion_detector is not None
        }

# Global instance
computer_vision_detector = None

def get_emotion_detector():
    """Get or create the global emotion detector instance"""
    global computer_vision_detector
    if computer_vision_detector is None:
        computer_vision_detector = ComputerVisionEmotionDetector()
    return computer_vision_detector

# Initialize the detector when module is imported
try:
    computer_vision_detector = ComputerVisionEmotionDetector()
    logging.info("✅ ComputerVisionEmotionDetector initialized successfully")
except Exception as e:
    logging.error(f"❌ Failed to initialize ComputerVisionEmotionDetector: {str(e)}")
    computer_vision_detector = None