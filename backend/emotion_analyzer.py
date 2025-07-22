"""
Advanced Emotion Analysis Engine for AI Interview System
Implements facial expression, eye tracking, and sentiment analysis
"""

import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
from datetime import datetime
import base64

@dataclass
class EmotionScore:
    emotion: str
    confidence: float
    timestamp: datetime

@dataclass
class FacialMetrics:
    emotions: List[EmotionScore]
    eye_contact_score: float
    attention_level: float
    stress_indicators: Dict[str, float]
    engagement_score: float

class AdvancedEmotionAnalyzer:
    """
    Advanced emotion analysis using MediaPipe and TensorFlow
    Features:
    - Real-time facial expression recognition
    - Eye tracking and attention analysis  
    - Stress detection through micro-expressions
    - Engagement scoring
    """
    
    def __init__(self):
        # Initialize MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Initialize emotion detection model
        self.emotion_model = self._load_emotion_model()
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
        # Eye tracking landmarks (MediaPipe indices)
        self.left_eye_landmarks = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.right_eye_landmarks = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        
        # Stress indicators tracking
        self.stress_baseline = None
        self.frame_buffer = []
        self.max_buffer_size = 30  # 1 second at 30fps
        
        logging.info("Advanced Emotion Analyzer initialized")

    def _load_emotion_model(self):
        """Load pre-trained emotion recognition model"""
        try:
            # In production, load a pre-trained model
            # For now, create a placeholder model structure
            model = tf.keras.Sequential([
                tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
                tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(512, activation='relu'),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(7, activation='softmax')
            ])
            
            # In production: model.load_weights('emotion_model_weights.h5')
            logging.info("Emotion model loaded successfully")
            return model
        except Exception as e:
            logging.error(f"Failed to load emotion model: {e}")
            return None

    def analyze_frame(self, frame: np.ndarray) -> Optional[FacialMetrics]:
        """
        Analyze a single video frame for emotions and engagement
        
        Args:
            frame: Input video frame (BGR format)
            
        Returns:
            FacialMetrics object with analysis results
        """
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if not results.multi_face_landmarks:
                return None
            
            # Get first face (assuming single person interview)
            face_landmarks = results.multi_face_landmarks[0]
            
            # Extract facial metrics
            emotions = self._analyze_emotions(frame, face_landmarks)
            eye_contact_score = self._calculate_eye_contact(face_landmarks)
            attention_level = self._calculate_attention_level(face_landmarks)
            stress_indicators = self._detect_stress_indicators(face_landmarks)
            engagement_score = self._calculate_engagement_score(emotions, eye_contact_score, attention_level)
            
            return FacialMetrics(
                emotions=emotions,
                eye_contact_score=eye_contact_score,
                attention_level=attention_level,
                stress_indicators=stress_indicators,
                engagement_score=engagement_score
            )
            
        except Exception as e:
            logging.error(f"Error analyzing frame: {e}")
            return None

    def _analyze_emotions(self, frame: np.ndarray, face_landmarks) -> List[EmotionScore]:
        """Extract and classify facial expressions"""
        try:
            # Extract face region for emotion analysis
            h, w, _ = frame.shape
            
            # Get bounding box from landmarks
            x_coords = [landmark.x * w for landmark in face_landmarks.landmark]
            y_coords = [landmark.y * h for landmark in face_landmarks.landmark]
            
            x_min, x_max = int(min(x_coords)), int(max(x_coords))
            y_min, y_max = int(min(y_coords)), int(max(y_coords))
            
            # Extract face ROI
            face_roi = frame[y_min:y_max, x_min:x_max]
            
            if face_roi.size == 0:
                return [EmotionScore("neutral", 0.5, datetime.now())]
            
            # Preprocess for emotion model
            face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            face_resized = cv2.resize(face_gray, (48, 48))
            face_normalized = face_resized / 255.0
            face_input = np.expand_dims(face_normalized, axis=(0, -1))
            
            # Predict emotions (placeholder - in production use real model)
            if self.emotion_model:
                # predictions = self.emotion_model.predict(face_input, verbose=0)
                # For now, return mock predictions based on facial geometry
                predictions = self._mock_emotion_prediction(face_landmarks)
            else:
                predictions = [0.1, 0.1, 0.1, 0.4, 0.1, 0.1, 0.1]  # Mock neutral dominant
            
            # Convert to EmotionScore objects
            emotions = []
            for i, confidence in enumerate(predictions):
                if confidence > 0.1:  # Only include emotions above threshold
                    emotions.append(EmotionScore(
                        emotion=self.emotion_labels[i],
                        confidence=float(confidence),
                        timestamp=datetime.now()
                    ))
            
            return sorted(emotions, key=lambda x: x.confidence, reverse=True)
            
        except Exception as e:
            logging.error(f"Error analyzing emotions: {e}")
            return [EmotionScore("neutral", 0.5, datetime.now())]

    def _mock_emotion_prediction(self, face_landmarks) -> List[float]:
        """Mock emotion prediction based on facial geometry (replace with real model)"""
        # Calculate basic facial ratios for demo
        landmarks = face_landmarks.landmark
        
        # Mouth corner analysis for happiness
        mouth_left = landmarks[61]
        mouth_right = landmarks[291]
        mouth_center = landmarks[13]
        
        # Simple smile detection
        mouth_curve = (mouth_left.y + mouth_right.y) / 2 - mouth_center.y
        
        if mouth_curve < -0.005:  # Upward curve = smile
            return [0.05, 0.05, 0.05, 0.7, 0.05, 0.05, 0.05]  # Happy
        elif mouth_curve > 0.005:  # Downward curve = sad
            return [0.05, 0.05, 0.05, 0.05, 0.7, 0.05, 0.05]  # Sad
        else:
            return [0.1, 0.1, 0.1, 0.2, 0.1, 0.1, 0.3]  # Neutral dominant

    def _calculate_eye_contact(self, face_landmarks) -> float:
        """Calculate eye contact score based on gaze direction"""
        try:
            landmarks = face_landmarks.landmark
            
            # Get eye center points
            left_eye_center = self._get_eye_center(landmarks, self.left_eye_landmarks)
            right_eye_center = self._get_eye_center(landmarks, self.right_eye_landmarks)
            
            # Calculate average eye position
            avg_eye_x = (left_eye_center[0] + right_eye_center[0]) / 2
            avg_eye_y = (left_eye_center[1] + right_eye_center[1]) / 2
            
            # Get nose tip for reference
            nose_tip = landmarks[1]
            
            # Calculate gaze direction relative to nose
            gaze_offset_x = abs(avg_eye_x - nose_tip.x)
            gaze_offset_y = abs(avg_eye_y - nose_tip.y)
            
            # Convert to eye contact score (0-1)
            eye_contact_score = max(0, 1 - (gaze_offset_x + gaze_offset_y) * 10)
            
            return float(eye_contact_score)
            
        except Exception as e:
            logging.error(f"Error calculating eye contact: {e}")
            return 0.5

    def _get_eye_center(self, landmarks, eye_landmark_indices) -> Tuple[float, float]:
        """Calculate center point of eye from landmarks"""
        x_coords = [landmarks[i].x for i in eye_landmark_indices]
        y_coords = [landmarks[i].y for i in eye_landmark_indices]
        return (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))

    def _calculate_attention_level(self, face_landmarks) -> float:
        """Calculate attention level based on head pose and eye openness"""
        try:
            landmarks = face_landmarks.landmark
            
            # Head pose estimation using key points
            nose_tip = landmarks[1]
            chin = landmarks[175]
            forehead = landmarks[9]
            
            # Calculate head tilt and rotation
            head_tilt = abs(nose_tip.x - 0.5) * 2  # Normalized head rotation
            head_vertical = abs(nose_tip.y - 0.5) * 2  # Vertical position
            
            # Eye openness calculation
            left_eye_openness = self._calculate_eye_openness(landmarks, self.left_eye_landmarks)
            right_eye_openness = self._calculate_eye_openness(landmarks, self.right_eye_landmarks)
            avg_eye_openness = (left_eye_openness + right_eye_openness) / 2
            
            # Combine metrics for attention score
            pose_attention = max(0, 1 - head_tilt - head_vertical)
            eye_attention = avg_eye_openness
            
            attention_level = (pose_attention + eye_attention) / 2
            return float(max(0, min(1, attention_level)))
            
        except Exception as e:
            logging.error(f"Error calculating attention level: {e}")
            return 0.5

    def _calculate_eye_openness(self, landmarks, eye_landmark_indices) -> float:
        """Calculate how open an eye is"""
        try:
            # Get vertical eye landmarks
            if len(eye_landmark_indices) < 6:
                return 0.5
                
            top_indices = eye_landmark_indices[:3]
            bottom_indices = eye_landmark_indices[3:6]
            
            # Calculate average distances
            vertical_distances = []
            for i in range(3):
                top_point = landmarks[top_indices[i]]
                bottom_point = landmarks[bottom_indices[i]]
                distance = abs(top_point.y - bottom_point.y)
                vertical_distances.append(distance)
            
            avg_openness = sum(vertical_distances) / len(vertical_distances)
            # Normalize and clamp
            normalized_openness = min(1.0, avg_openness * 50)  # Scale factor
            
            return float(normalized_openness)
            
        except Exception as e:
            logging.error(f"Error calculating eye openness: {e}")
            return 0.5

    def _detect_stress_indicators(self, face_landmarks) -> Dict[str, float]:
        """Detect stress indicators from facial micro-expressions"""
        try:
            landmarks = face_landmarks.landmark
            
            # Eyebrow tension (stress indicator)
            left_eyebrow_inner = landmarks[70]
            right_eyebrow_inner = landmarks[107]
            eyebrow_distance = abs(left_eyebrow_inner.x - right_eyebrow_inner.x)
            eyebrow_tension = max(0, (0.1 - eyebrow_distance) * 10)
            
            # Jaw tension
            jaw_left = landmarks[172]
            jaw_right = landmarks[397]
            jaw_center = landmarks[175]
            jaw_tightness = abs(jaw_left.y + jaw_right.y - 2 * jaw_center.y) * 20
            
            # Eye strain
            left_eye_strain = self._calculate_eye_strain(landmarks, self.left_eye_landmarks)
            right_eye_strain = self._calculate_eye_strain(landmarks, self.right_eye_landmarks)
            avg_eye_strain = (left_eye_strain + right_eye_strain) / 2
            
            return {
                'eyebrow_tension': float(max(0, min(1, eyebrow_tension))),
                'jaw_tension': float(max(0, min(1, jaw_tightness))),
                'eye_strain': float(max(0, min(1, avg_eye_strain))),
                'overall_stress': float(max(0, min(1, (eyebrow_tension + jaw_tightness + avg_eye_strain) / 3)))
            }
            
        except Exception as e:
            logging.error(f"Error detecting stress indicators: {e}")
            return {'eyebrow_tension': 0.0, 'jaw_tension': 0.0, 'eye_strain': 0.0, 'overall_stress': 0.0}

    def _calculate_eye_strain(self, landmarks, eye_landmark_indices) -> float:
        """Calculate eye strain based on eye shape distortion"""
        try:
            # Simplified eye strain calculation
            eye_center = self._get_eye_center(landmarks, eye_landmark_indices)
            
            # Calculate variance in eye shape
            distances = []
            for idx in eye_landmark_indices:
                point = landmarks[idx]
                distance = ((point.x - eye_center[0])**2 + (point.y - eye_center[1])**2)**0.5
                distances.append(distance)
            
            variance = np.var(distances) if distances else 0
            strain_score = min(1.0, variance * 1000)  # Scale factor
            
            return float(strain_score)
            
        except Exception as e:
            logging.error(f"Error calculating eye strain: {e}")
            return 0.0

    def _calculate_engagement_score(self, emotions: List[EmotionScore], 
                                   eye_contact: float, attention: float) -> float:
        """Calculate overall engagement score"""
        try:
            # Weight positive emotions higher
            emotion_score = 0.0
            if emotions:
                for emotion in emotions:
                    if emotion.emotion in ['happy', 'surprise']:
                        emotion_score += emotion.confidence * 0.8
                    elif emotion.emotion == 'neutral':
                        emotion_score += emotion.confidence * 0.5
                    else:  # Negative emotions reduce engagement
                        emotion_score -= emotion.confidence * 0.3
            
            # Combine all factors
            engagement = (emotion_score * 0.4 + eye_contact * 0.3 + attention * 0.3)
            return float(max(0, min(1, engagement)))
            
        except Exception as e:
            logging.error(f"Error calculating engagement score: {e}")
            return 0.5

    def process_video_stream(self, video_data: str) -> Optional[Dict]:
        """
        Process base64 encoded video frame
        
        Args:
            video_data: Base64 encoded frame data
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Decode base64 to frame
            img_data = base64.b64decode(video_data.split(',')[1])
            nparr = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                return None
            
            # Analyze frame
            metrics = self.analyze_frame(frame)
            
            if metrics is None:
                return None
            
            # Convert to serializable format
            return {
                'emotions': [
                    {
                        'emotion': emotion.emotion,
                        'confidence': emotion.confidence,
                        'timestamp': emotion.timestamp.isoformat()
                    }
                    for emotion in metrics.emotions
                ],
                'eye_contact_score': metrics.eye_contact_score,
                'attention_level': metrics.attention_level,
                'stress_indicators': metrics.stress_indicators,
                'engagement_score': metrics.engagement_score,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error processing video stream: {e}")
            return None

# Global analyzer instance
emotion_analyzer = AdvancedEmotionAnalyzer()