"""
Advanced Speech Analysis Engine for AI Interview System
Implements tone, pitch, pace, and sentiment analysis from audio
"""

import librosa
import numpy as np
import scipy.signal
from typing import Dict, List, Tuple, Optional
import logging
from dataclasses import dataclass
from datetime import datetime
import base64
import io
import wave

@dataclass
class SpeechMetrics:
    pitch_mean: float
    pitch_variance: float
    energy_mean: float
    energy_variance: float
    speaking_rate: float  # words per minute
    pause_frequency: float
    voice_quality: float
    confidence_level: float

@dataclass
class EmotionalTone:
    emotion: str
    confidence: float
    timestamp: datetime

@dataclass
class SpeechAnalysis:
    speech_metrics: SpeechMetrics
    emotional_tones: List[EmotionalTone]
    fluency_score: float
    clarity_score: float
    stress_indicators: Dict[str, float]
    overall_quality: float

class AdvancedSpeechAnalyzer:
    """
    Advanced speech analysis for interview assessment
    Features:
    - Pitch and tone analysis
    - Speaking rate and fluency
    - Emotional tone detection
    - Stress indicators from voice
    - Communication clarity assessment
    """
    
    def __init__(self):
        self.sample_rate = 16000
        self.frame_length = 2048
        self.hop_length = 512
        
        # Speech quality thresholds
        self.pitch_range = (80, 400)  # Hz, typical human speech range
        self.optimal_speaking_rate = (140, 180)  # words per minute
        
        # Emotion mapping (simplified)
        self.emotion_pitch_mapping = {
            'excited': (200, 300),
            'confident': (120, 200),
            'nervous': (150, 250),
            'calm': (100, 150),
            'stressed': (180, 280)
        }
        
        logging.info("Advanced Speech Analyzer initialized")

    def analyze_audio(self, audio_data: bytes) -> Optional[SpeechAnalysis]:
        """
        Analyze audio data for speech patterns and emotional content
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            SpeechAnalysis object with comprehensive analysis
        """
        try:
            # Load audio data
            audio_array = self._load_audio_from_bytes(audio_data)
            if audio_array is None or len(audio_array) < self.sample_rate:  # Less than 1 second
                return None
            
            # Extract speech features
            speech_metrics = self._extract_speech_metrics(audio_array)
            emotional_tones = self._analyze_emotional_tone(audio_array)
            fluency_score = self._calculate_fluency_score(audio_array)
            clarity_score = self._calculate_clarity_score(audio_array)
            stress_indicators = self._detect_speech_stress(audio_array)
            overall_quality = self._calculate_overall_quality(
                speech_metrics, fluency_score, clarity_score, stress_indicators
            )
            
            return SpeechAnalysis(
                speech_metrics=speech_metrics,
                emotional_tones=emotional_tones,
                fluency_score=fluency_score,
                clarity_score=clarity_score,
                stress_indicators=stress_indicators,
                overall_quality=overall_quality
            )
            
        except Exception as e:
            logging.error(f"Error analyzing audio: {e}")
            return None

    def _load_audio_from_bytes(self, audio_data: bytes) -> Optional[np.ndarray]:
        """Load audio from bytes and resample to target sample rate"""
        try:
            # Try to load as WAV first
            try:
                audio_io = io.BytesIO(audio_data)
                with wave.open(audio_io, 'rb') as wav_file:
                    frames = wav_file.readframes(-1)
                    audio_array = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
                    audio_array = audio_array / 32768.0  # Normalize to [-1, 1]
                    original_sr = wav_file.getframerate()
            except:
                # Fallback: assume raw PCM data
                audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
                audio_array = audio_array / 32768.0
                original_sr = self.sample_rate
            
            # Resample if necessary
            if original_sr != self.sample_rate:
                audio_array = librosa.resample(
                    audio_array, 
                    orig_sr=original_sr, 
                    target_sr=self.sample_rate
                )
            
            return audio_array
            
        except Exception as e:
            logging.error(f"Error loading audio: {e}")
            return None

    def _extract_speech_metrics(self, audio: np.ndarray) -> SpeechMetrics:
        """Extract basic speech characteristics"""
        try:
            # Pitch analysis
            pitches, magnitudes = librosa.piptrack(
                y=audio, 
                sr=self.sample_rate,
                threshold=0.1,
                fmin=self.pitch_range[0],
                fmax=self.pitch_range[1]
            )
            
            # Extract pitch values (remove zeros)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            pitch_mean = np.mean(pitch_values) if pitch_values else 0
            pitch_variance = np.var(pitch_values) if pitch_values else 0
            
            # Energy analysis
            frame_energy = librosa.feature.rms(
                y=audio,
                frame_length=self.frame_length,
                hop_length=self.hop_length
            )[0]
            
            energy_mean = np.mean(frame_energy)
            energy_variance = np.var(frame_energy)
            
            # Speaking rate estimation (simplified)
            speaking_rate = self._estimate_speaking_rate(audio)
            
            # Pause frequency
            pause_frequency = self._calculate_pause_frequency(audio)
            
            # Voice quality (based on spectral features)
            voice_quality = self._assess_voice_quality(audio)
            
            # Confidence level (based on pitch stability and energy)
            confidence_level = self._estimate_confidence_level(
                pitch_variance, energy_mean, speaking_rate
            )
            
            return SpeechMetrics(
                pitch_mean=float(pitch_mean),
                pitch_variance=float(pitch_variance),
                energy_mean=float(energy_mean),
                energy_variance=float(energy_variance),
                speaking_rate=float(speaking_rate),
                pause_frequency=float(pause_frequency),
                voice_quality=float(voice_quality),
                confidence_level=float(confidence_level)
            )
            
        except Exception as e:
            logging.error(f"Error extracting speech metrics: {e}")
            return SpeechMetrics(0, 0, 0, 0, 0, 0, 0, 0)

    def _estimate_speaking_rate(self, audio: np.ndarray) -> float:
        """Estimate speaking rate in words per minute"""
        try:
            # Detect speech segments using energy
            frame_energy = librosa.feature.rms(
                y=audio,
                frame_length=self.frame_length,
                hop_length=self.hop_length
            )[0]
            
            # Threshold for speech detection
            energy_threshold = np.mean(frame_energy) * 0.3
            speech_frames = frame_energy > energy_threshold
            
            # Count speech segments (approximating syllables)
            speech_changes = np.diff(speech_frames.astype(int))
            speech_onsets = np.sum(speech_changes == 1)
            
            # Convert to words per minute (rough approximation)
            duration_minutes = len(audio) / (self.sample_rate * 60)
            estimated_syllables = speech_onsets
            estimated_words = estimated_syllables / 2.5  # Average syllables per word
            speaking_rate = estimated_words / duration_minutes if duration_minutes > 0 else 0
            
            return min(300, max(60, speaking_rate))  # Clamp to reasonable range
            
        except Exception as e:
            logging.error(f"Error estimating speaking rate: {e}")
            return 150  # Default rate

    def _calculate_pause_frequency(self, audio: np.ndarray) -> float:
        """Calculate frequency of pauses in speech"""
        try:
            # Detect silent periods
            frame_energy = librosa.feature.rms(
                y=audio,
                frame_length=self.frame_length,
                hop_length=self.hop_length
            )[0]
            
            silence_threshold = np.mean(frame_energy) * 0.2
            silent_frames = frame_energy < silence_threshold
            
            # Count pause segments
            silence_changes = np.diff(silent_frames.astype(int))
            pause_count = np.sum(silence_changes == 1)
            
            # Normalize by duration
            duration_minutes = len(audio) / (self.sample_rate * 60)
            pause_frequency = pause_count / duration_minutes if duration_minutes > 0 else 0
            
            return min(20, max(0, pause_frequency))  # Clamp to reasonable range
            
        except Exception as e:
            logging.error(f"Error calculating pause frequency: {e}")
            return 2  # Default frequency

    def _assess_voice_quality(self, audio: np.ndarray) -> float:
        """Assess voice quality based on spectral features"""
        try:
            # Spectral centroid (brightness)
            spectral_centroid = librosa.feature.spectral_centroid(
                y=audio, sr=self.sample_rate
            )[0]
            
            # Spectral rolloff
            spectral_rolloff = librosa.feature.spectral_rolloff(
                y=audio, sr=self.sample_rate
            )[0]
            
            # Zero crossing rate (measure of voice quality)
            zcr = librosa.feature.zero_crossing_rate(audio)[0]
            
            # Combine metrics for quality score
            centroid_score = 1 - (np.mean(spectral_centroid) / 4000)  # Normalize
            rolloff_score = 1 - (np.mean(spectral_rolloff) / 8000)    # Normalize  
            zcr_score = 1 - np.mean(zcr) * 10  # Lower ZCR is better for voice
            
            voice_quality = (centroid_score + rolloff_score + zcr_score) / 3
            return max(0, min(1, voice_quality))
            
        except Exception as e:
            logging.error(f"Error assessing voice quality: {e}")
            return 0.5

    def _estimate_confidence_level(self, pitch_variance: float, 
                                   energy_mean: float, speaking_rate: float) -> float:
        """Estimate confidence level from speech characteristics"""
        try:
            # Stable pitch indicates confidence
            pitch_stability = 1 / (1 + pitch_variance / 100)  # Normalize variance
            
            # Adequate energy indicates confidence
            energy_score = min(1, energy_mean * 10)  # Normalize energy
            
            # Optimal speaking rate indicates confidence
            rate_optimal = 1 - abs(speaking_rate - 160) / 100  # 160 WPM is optimal
            rate_score = max(0, min(1, rate_optimal))
            
            # Combine scores
            confidence_level = (pitch_stability + energy_score + rate_score) / 3
            return max(0, min(1, confidence_level))
            
        except Exception as e:
            logging.error(f"Error estimating confidence level: {e}")
            return 0.5

    def _analyze_emotional_tone(self, audio: np.ndarray) -> List[EmotionalTone]:
        """Analyze emotional content in speech"""
        try:
            # Extract features for emotion analysis
            pitches, magnitudes = librosa.piptrack(
                y=audio, 
                sr=self.sample_rate,
                threshold=0.1,
                fmin=self.pitch_range[0],
                fmax=self.pitch_range[1]
            )
            
            # Get average pitch
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            avg_pitch = np.mean(pitch_values) if pitch_values else 150
            
            # Map pitch to emotions (simplified approach)
            emotions = []
            for emotion, (min_pitch, max_pitch) in self.emotion_pitch_mapping.items():
                if min_pitch <= avg_pitch <= max_pitch:
                    # Calculate confidence based on how well pitch matches
                    center_pitch = (min_pitch + max_pitch) / 2
                    distance = abs(avg_pitch - center_pitch)
                    max_distance = (max_pitch - min_pitch) / 2
                    confidence = 1 - (distance / max_distance)
                    
                    emotions.append(EmotionalTone(
                        emotion=emotion,
                        confidence=max(0.1, confidence),
                        timestamp=datetime.now()
                    ))
            
            # If no matches, default to neutral
            if not emotions:
                emotions.append(EmotionalTone(
                    emotion='neutral',
                    confidence=0.7,
                    timestamp=datetime.now()
                ))
            
            return sorted(emotions, key=lambda x: x.confidence, reverse=True)
            
        except Exception as e:
            logging.error(f"Error analyzing emotional tone: {e}")
            return [EmotionalTone('neutral', 0.5, datetime.now())]

    def _calculate_fluency_score(self, audio: np.ndarray) -> float:
        """Calculate speech fluency score"""
        try:
            # Factors that affect fluency:
            # 1. Consistent energy (less variation = more fluent)
            # 2. Appropriate speaking rate
            # 3. Fewer long pauses
            
            frame_energy = librosa.feature.rms(
                y=audio,
                frame_length=self.frame_length,
                hop_length=self.hop_length
            )[0]
            
            # Energy consistency
            energy_cv = np.std(frame_energy) / np.mean(frame_energy) if np.mean(frame_energy) > 0 else 1
            energy_consistency = max(0, 1 - energy_cv)
            
            # Speaking rate appropriateness
            speaking_rate = self._estimate_speaking_rate(audio)
            rate_score = 1 - abs(speaking_rate - 160) / 100  # Optimal around 160 WPM
            rate_score = max(0, min(1, rate_score))
            
            # Pause appropriateness
            pause_freq = self._calculate_pause_frequency(audio)
            pause_score = max(0, 1 - abs(pause_freq - 3) / 5)  # Optimal around 3 pauses/minute
            
            # Combine scores
            fluency_score = (energy_consistency + rate_score + pause_score) / 3
            return max(0, min(1, fluency_score))
            
        except Exception as e:
            logging.error(f"Error calculating fluency score: {e}")
            return 0.5

    def _calculate_clarity_score(self, audio: np.ndarray) -> float:
        """Calculate speech clarity score"""
        try:
            # Factors affecting clarity:
            # 1. Spectral clarity (high frequency content)
            # 2. Consistent pitch
            # 3. Adequate volume
            
            # Spectral analysis
            spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
            centroid_score = np.mean(spectral_centroid) / 2000  # Normalize
            centroid_score = max(0, min(1, centroid_score))
            
            # Pitch consistency
            pitches, magnitudes = librosa.piptrack(
                y=audio, sr=self.sample_rate, threshold=0.1
            )
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            pitch_consistency = 1 / (1 + np.var(pitch_values) / 1000) if pitch_values else 0.5
            
            # Volume adequacy
            rms_energy = librosa.feature.rms(y=audio)[0]
            volume_score = min(1, np.mean(rms_energy) * 20)  # Normalize
            
            # Combine scores
            clarity_score = (centroid_score + pitch_consistency + volume_score) / 3
            return max(0, min(1, clarity_score))
            
        except Exception as e:
            logging.error(f"Error calculating clarity score: {e}")
            return 0.5

    def _detect_speech_stress(self, audio: np.ndarray) -> Dict[str, float]:
        """Detect stress indicators in speech patterns"""
        try:
            # Stress indicators:
            # 1. High pitch variance (vocal tension)
            # 2. Rapid speaking (nervousness)
            # 3. Frequent pauses (hesitation)
            # 4. Energy fluctuations (vocal instability)
            
            # Pitch variance analysis
            pitches, magnitudes = librosa.piptrack(
                y=audio, sr=self.sample_rate, threshold=0.1
            )
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            pitch_stress = min(1, np.var(pitch_values) / 2000) if pitch_values else 0
            
            # Speaking rate stress
            speaking_rate = self._estimate_speaking_rate(audio)
            rate_stress = max(0, (speaking_rate - 200) / 100) if speaking_rate > 200 else 0
            
            # Pause frequency stress
            pause_freq = self._calculate_pause_frequency(audio)
            pause_stress = max(0, (pause_freq - 5) / 10) if pause_freq > 5 else 0
            
            # Energy fluctuation stress
            frame_energy = librosa.feature.rms(y=audio)[0]
            energy_cv = np.std(frame_energy) / np.mean(frame_energy) if np.mean(frame_energy) > 0 else 0
            energy_stress = min(1, energy_cv)
            
            # Overall stress
            overall_stress = (pitch_stress + rate_stress + pause_stress + energy_stress) / 4
            
            return {
                'vocal_tension': float(pitch_stress),
                'speaking_anxiety': float(rate_stress),
                'hesitation': float(pause_stress),
                'vocal_instability': float(energy_stress),
                'overall_stress': float(overall_stress)
            }
            
        except Exception as e:
            logging.error(f"Error detecting speech stress: {e}")
            return {
                'vocal_tension': 0.0,
                'speaking_anxiety': 0.0,
                'hesitation': 0.0,
                'vocal_instability': 0.0,
                'overall_stress': 0.0
            }

    def _calculate_overall_quality(self, speech_metrics: SpeechMetrics,
                                   fluency_score: float, clarity_score: float,
                                   stress_indicators: Dict[str, float]) -> float:
        """Calculate overall speech quality score"""
        try:
            # Weight different factors
            quality_factors = [
                speech_metrics.confidence_level * 0.25,
                speech_metrics.voice_quality * 0.20,
                fluency_score * 0.25,
                clarity_score * 0.20,
                (1 - stress_indicators['overall_stress']) * 0.10
            ]
            
            overall_quality = sum(quality_factors)
            return max(0, min(1, overall_quality))
            
        except Exception as e:
            logging.error(f"Error calculating overall quality: {e}")
            return 0.5

    def process_audio_stream(self, audio_data: bytes) -> Optional[Dict]:
        """
        Process audio stream for real-time analysis
        
        Args:
            audio_data: Raw audio bytes
            
        Returns:
            Dictionary with analysis results
        """
        try:
            analysis = self.analyze_audio(audio_data)
            
            if analysis is None:
                return None
            
            # Convert to serializable format
            return {
                'speech_metrics': {
                    'pitch_mean': analysis.speech_metrics.pitch_mean,
                    'pitch_variance': analysis.speech_metrics.pitch_variance,
                    'energy_mean': analysis.speech_metrics.energy_mean,
                    'energy_variance': analysis.speech_metrics.energy_variance,
                    'speaking_rate': analysis.speech_metrics.speaking_rate,
                    'pause_frequency': analysis.speech_metrics.pause_frequency,
                    'voice_quality': analysis.speech_metrics.voice_quality,
                    'confidence_level': analysis.speech_metrics.confidence_level
                },
                'emotional_tones': [
                    {
                        'emotion': tone.emotion,
                        'confidence': tone.confidence,
                        'timestamp': tone.timestamp.isoformat()
                    }
                    for tone in analysis.emotional_tones
                ],
                'fluency_score': analysis.fluency_score,
                'clarity_score': analysis.clarity_score,
                'stress_indicators': analysis.stress_indicators,
                'overall_quality': analysis.overall_quality,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error processing audio stream: {e}")
            return None

# Global speech analyzer instance
speech_analyzer = AdvancedSpeechAnalyzer()