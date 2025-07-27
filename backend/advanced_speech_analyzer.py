"""
Phase 3: Advanced AI & Analytics - Week 7: Open-Source AI Model Integration
Step 7.2: Advanced Speech Analysis

This module provides professional-grade voice assessment using open-source libraries
for speech feature extraction, emotion recognition, pace and clarity analysis.
"""

import os
import logging
import numpy as np
import librosa
import torch
from typing import Dict, Any, List, Tuple, Optional
import json
from datetime import datetime
import io
import base64
import wave
import struct
from pydub import AudioSegment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import scipy.signal
from scipy.stats import kurtosis, skew
import math

class AdvancedSpeechAnalyzer:
    """
    Advanced speech analysis for professional-grade voice assessment
    Features:
    - Multi-modal speech feature extraction
    - Speech emotion recognition
    - Pace and clarity analysis
    - Confidence scoring system
    - Voice quality assessment
    """
    
    def __init__(self):
        self.sample_rate = 16000  # Standard sample rate for speech analysis
        self.frame_length = 2048
        self.hop_length = 512
        
        # Initialize sentiment analyzer for transcript analysis
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Speech quality thresholds
        self.quality_thresholds = {
            'excellent': {'clarity': 0.8, 'pace': 0.8, 'confidence': 0.8},
            'good': {'clarity': 0.6, 'pace': 0.6, 'confidence': 0.6},
            'average': {'clarity': 0.4, 'pace': 0.4, 'confidence': 0.4},
            'poor': {'clarity': 0.0, 'pace': 0.0, 'confidence': 0.0}
        }
        
        logging.info("AdvancedSpeechAnalyzer initialized successfully")
    
    async def analyze_speech_comprehensive(self, 
                                         audio_data: bytes, 
                                         transcript: str = "",
                                         sample_rate: int = 16000) -> Dict[str, Any]:
        """
        Comprehensive speech analysis combining multiple techniques
        """
        try:
            analysis = {
                "acoustic_features": {},
                "prosodic_features": {},
                "speech_quality": {},
                "emotion_analysis": {},
                "confidence_scoring": {},
                "pace_analysis": {},
                "clarity_analysis": {},
                "overall_assessment": {},
                "recommendations": []
            }
            
            # Convert audio data to numpy array
            audio_array = self._convert_audio_to_array(audio_data, sample_rate)
            
            if audio_array is None or len(audio_array) == 0:
                return self._get_fallback_analysis("Invalid or empty audio data")
            
            # 1. Extract acoustic features
            analysis["acoustic_features"] = await self._extract_acoustic_features(audio_array, sample_rate)
            
            # 2. Extract prosodic features (rhythm, stress, intonation)
            analysis["prosodic_features"] = await self._extract_prosodic_features(audio_array, sample_rate)
            
            # 3. Assess speech quality
            analysis["speech_quality"] = await self._assess_speech_quality(audio_array, sample_rate)
            
            # 4. Emotion analysis from voice
            analysis["emotion_analysis"] = await self._analyze_speech_emotion(audio_array, transcript, sample_rate)
            
            # 5. Confidence scoring
            analysis["confidence_scoring"] = await self._calculate_confidence_score(analysis)
            
            # 6. Pace analysis
            analysis["pace_analysis"] = await self._analyze_speech_pace(audio_array, transcript, sample_rate)
            
            # 7. Clarity analysis
            analysis["clarity_analysis"] = await self._analyze_speech_clarity(audio_array, sample_rate)
            
            # 8. Overall assessment and recommendations
            analysis["overall_assessment"] = await self._generate_overall_assessment(analysis)
            analysis["recommendations"] = await self._generate_recommendations(analysis)
            
            return analysis
            
        except Exception as e:
            logging.error(f"Error in comprehensive speech analysis: {str(e)}")
            return self._get_fallback_analysis(f"Analysis error: {str(e)}")
    
    def _convert_audio_to_array(self, audio_data: bytes, sample_rate: int) -> Optional[np.ndarray]:
        """Convert audio bytes to numpy array"""
        try:
            # Try different audio format conversions
            try:
                # Try as WAV data first
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
                audio_array = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
                
                # Convert to mono if stereo
                if audio_segment.channels == 2:
                    audio_array = audio_array.reshape((-1, 2))
                    audio_array = np.mean(audio_array, axis=1)
                
                # Normalize
                audio_array = audio_array / np.max(np.abs(audio_array)) if np.max(np.abs(audio_array)) > 0 else audio_array
                
                return audio_array
                
            except:
                # Try as raw PCM data
                audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
                audio_array = audio_array / 32768.0  # Normalize 16-bit PCM
                return audio_array
                
        except Exception as e:
            logging.error(f"Error converting audio to array: {str(e)}")
            return None
    
    async def _extract_acoustic_features(self, audio_array: np.ndarray, sample_rate: int) -> Dict[str, Any]:
        """
        Extract comprehensive acoustic features from speech
        """
        try:
            features = {}
            
            # 1. Fundamental frequency (F0) - pitch
            f0, voiced_flag, voiced_probs = librosa.pyin(
                audio_array, 
                fmin=librosa.note_to_hz('C2'), 
                fmax=librosa.note_to_hz('C7'),
                sr=sample_rate
            )
            
            # Clean F0 (remove NaN values)
            f0_clean = f0[~np.isnan(f0)]
            
            if len(f0_clean) > 0:
                features["pitch"] = {
                    "mean_f0": float(np.mean(f0_clean)),
                    "std_f0": float(np.std(f0_clean)),
                    "min_f0": float(np.min(f0_clean)),
                    "max_f0": float(np.max(f0_clean)),
                    "f0_range": float(np.max(f0_clean) - np.min(f0_clean)),
                    "voiced_percentage": float(np.sum(voiced_flag) / len(voiced_flag))
                }
            else:
                features["pitch"] = {
                    "mean_f0": 0.0, "std_f0": 0.0, "min_f0": 0.0, 
                    "max_f0": 0.0, "f0_range": 0.0, "voiced_percentage": 0.0
                }
            
            # 2. Energy and intensity
            rms = librosa.feature.rms(y=audio_array, frame_length=self.frame_length, hop_length=self.hop_length)[0]
            features["energy"] = {
                "mean_rms": float(np.mean(rms)),
                "std_rms": float(np.std(rms)),
                "energy_variance": float(np.var(rms)),
                "dynamic_range": float(np.max(rms) - np.min(rms))
            }
            
            # 3. Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_array, sr=sample_rate)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_array, sr=sample_rate)[0]
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_array, sr=sample_rate)[0]
            zero_crossing_rate = librosa.feature.zero_crossing_rate(audio_array)[0]
            
            features["spectral"] = {
                "mean_spectral_centroid": float(np.mean(spectral_centroids)),
                "std_spectral_centroid": float(np.std(spectral_centroids)),
                "mean_spectral_rolloff": float(np.mean(spectral_rolloff)),
                "mean_spectral_bandwidth": float(np.mean(spectral_bandwidth)),
                "mean_zcr": float(np.mean(zero_crossing_rate)),
                "std_zcr": float(np.std(zero_crossing_rate))
            }
            
            # 4. MFCCs (Mel-frequency cepstral coefficients)
            mfccs = librosa.feature.mfcc(y=audio_array, sr=sample_rate, n_mfcc=13)
            features["mfcc"] = {
                f"mfcc_{i}": {"mean": float(np.mean(mfccs[i])), "std": float(np.std(mfccs[i]))}
                for i in range(13)
            }
            
            # 5. Chroma features (harmonic content)
            chroma = librosa.feature.chroma_stft(y=audio_array, sr=sample_rate)
            features["chroma"] = {
                "mean_chroma": [float(np.mean(chroma[i])) for i in range(12)],
                "chroma_variance": float(np.var(chroma))
            }
            
            return features
            
        except Exception as e:
            logging.error(f"Error extracting acoustic features: {str(e)}")
            return {"error": str(e)}
    
    async def _extract_prosodic_features(self, audio_array: np.ndarray, sample_rate: int) -> Dict[str, Any]:
        """
        Extract prosodic features (rhythm, stress, intonation patterns)
        """
        try:
            features = {}
            
            # 1. Speech rate estimation
            # Detect speech segments using energy thresholding
            rms = librosa.feature.rms(y=audio_array, frame_length=self.frame_length, hop_length=self.hop_length)[0]
            energy_threshold = np.mean(rms) * 0.3
            speech_frames = rms > energy_threshold
            
            total_frames = len(speech_frames)
            speech_frame_count = np.sum(speech_frames)
            speech_ratio = speech_frame_count / total_frames if total_frames > 0 else 0
            
            # Estimate speech rate (syllables per second)
            duration = len(audio_array) / sample_rate
            estimated_syllables = self._estimate_syllables(audio_array, sample_rate)
            speech_rate = estimated_syllables / duration if duration > 0 else 0
            
            features["rhythm"] = {
                "speech_rate_sps": float(speech_rate),  # syllables per second
                "speech_ratio": float(speech_ratio),
                "estimated_syllables": int(estimated_syllables),
                "duration": float(duration)
            }
            
            # 2. Stress patterns (based on energy and pitch variations)
            f0, _, _ = librosa.pyin(audio_array, fmin=50, fmax=400, sr=sample_rate)
            f0_clean = f0[~np.isnan(f0)]
            
            if len(f0_clean) > 10:
                # Calculate stress indicators
                pitch_variation = np.std(f0_clean) / np.mean(f0_clean) if np.mean(f0_clean) > 0 else 0
                energy_variation = np.std(rms) / np.mean(rms) if np.mean(rms) > 0 else 0
                
                features["stress"] = {
                    "pitch_variation_coefficient": float(pitch_variation),
                    "energy_variation_coefficient": float(energy_variation),
                    "stress_level": float((pitch_variation + energy_variation) / 2)
                }
            else:
                features["stress"] = {
                    "pitch_variation_coefficient": 0.0,
                    "energy_variation_coefficient": 0.0,
                    "stress_level": 0.0
                }
            
            # 3. Intonation patterns
            if len(f0_clean) > 5:
                # Calculate intonation trends
                f0_trend = np.polyfit(range(len(f0_clean)), f0_clean, 1)[0]  # Linear trend
                f0_curvature = np.mean(np.diff(f0_clean, 2))  # Curvature
                
                features["intonation"] = {
                    "pitch_trend": float(f0_trend),
                    "pitch_curvature": float(f0_curvature),
                    "intonation_range": float(np.max(f0_clean) - np.min(f0_clean)),
                    "intonation_variability": float(np.std(np.diff(f0_clean)))
                }
            else:
                features["intonation"] = {
                    "pitch_trend": 0.0,
                    "pitch_curvature": 0.0,
                    "intonation_range": 0.0,
                    "intonation_variability": 0.0
                }
            
            return features
            
        except Exception as e:
            logging.error(f"Error extracting prosodic features: {str(e)}")
            return {"error": str(e)}
    
    def _estimate_syllables(self, audio_array: np.ndarray, sample_rate: int) -> int:
        """
        Estimate number of syllables in speech using energy peaks
        """
        try:
            # Apply low-pass filter to smooth the energy contour
            nyquist = sample_rate // 2
            cutoff = 20  # Hz
            b, a = scipy.signal.butter(2, cutoff / nyquist, btype='low')
            
            # Get energy contour
            rms = librosa.feature.rms(y=audio_array, frame_length=2048, hop_length=512)[0]
            
            # Smooth the energy contour
            rms_smooth = scipy.signal.filtfilt(b, a, rms)
            
            # Find peaks in energy (potential syllable centers)
            # Dynamic threshold based on energy distribution
            energy_threshold = np.mean(rms_smooth) + 0.1 * np.std(rms_smooth)
            
            # Find peaks
            peaks, _ = scipy.signal.find_peaks(rms_smooth, height=energy_threshold, distance=10)
            
            return len(peaks)
            
        except Exception as e:
            logging.error(f"Error estimating syllables: {str(e)}")
            # Fallback: estimate based on duration (average 2 syllables per second)
            duration = len(audio_array) / sample_rate
            return max(1, int(duration * 2))
    
    async def _assess_speech_quality(self, audio_array: np.ndarray, sample_rate: int) -> Dict[str, Any]:
        """
        Assess overall speech quality using multiple metrics
        """
        try:
            quality = {}
            
            # 1. Signal-to-noise ratio estimation
            # Use spectral subtraction method
            stft = librosa.stft(audio_array, n_fft=2048, hop_length=512)
            magnitude = np.abs(stft)
            
            # Estimate noise floor (bottom 10% of magnitude spectrum)
            noise_floor = np.percentile(magnitude, 10, axis=1, keepdims=True)
            signal_power = np.mean(magnitude ** 2)
            noise_power = np.mean(noise_floor ** 2)
            
            snr = 10 * np.log10(signal_power / max(noise_power, 1e-10))
            quality["snr_db"] = float(snr)
            
            # 2. Spectral quality measures
            # Spectral flatness (measure of noisiness)
            spectral_flatness = librosa.feature.spectral_flatness(y=audio_array)[0]
            quality["spectral_flatness"] = float(np.mean(spectral_flatness))
            
            # 3. Harmonic-to-noise ratio
            f0, voiced_flag, voiced_probs = librosa.pyin(audio_array, fmin=50, fmax=400, sr=sample_rate)
            if np.any(voiced_flag):
                # Simple HNR estimation
                voiced_segments = audio_array[voiced_flag]
                if len(voiced_segments) > 0:
                    harmonic_power = np.var(voiced_segments)
                    total_power = np.var(audio_array)
                    noise_power = total_power - harmonic_power
                    hnr = 10 * np.log10(harmonic_power / max(noise_power, 1e-10))
                    quality["hnr_db"] = float(hnr)
                else:
                    quality["hnr_db"] = 0.0
            else:
                quality["hnr_db"] = 0.0
            
            # 4. Overall quality score (0-1)
            # Normalize and combine metrics
            snr_score = min(1.0, max(0.0, (snr + 10) / 30))  # Normalize SNR (-10 to 20 dB)
            hnr_score = min(1.0, max(0.0, (quality["hnr_db"] + 5) / 25))  # Normalize HNR (-5 to 20 dB)
            flatness_score = 1.0 - min(1.0, quality["spectral_flatness"] * 10)  # Lower flatness is better
            
            quality["overall_quality_score"] = float((snr_score + hnr_score + flatness_score) / 3)
            
            # 5. Quality classification
            if quality["overall_quality_score"] > 0.8:
                quality["quality_rating"] = "excellent"
            elif quality["overall_quality_score"] > 0.6:
                quality["quality_rating"] = "good"
            elif quality["overall_quality_score"] > 0.4:
                quality["quality_rating"] = "average"
            else:
                quality["quality_rating"] = "poor"
            
            return quality
            
        except Exception as e:
            logging.error(f"Error assessing speech quality: {str(e)}")
            return {
                "snr_db": 10.0,
                "spectral_flatness": 0.5,
                "hnr_db": 10.0,
                "overall_quality_score": 0.5,
                "quality_rating": "average",
                "error": str(e)
            }
    
    async def _analyze_speech_emotion(self, audio_array: np.ndarray, transcript: str, sample_rate: int) -> Dict[str, Any]:
        """
        Analyze emotions from speech using acoustic features
        """
        try:
            emotion_analysis = {}
            
            # 1. Acoustic emotion indicators
            # Extract features that correlate with emotions
            f0, _, _ = librosa.pyin(audio_array, fmin=50, fmax=400, sr=sample_rate)
            f0_clean = f0[~np.isnan(f0)]
            
            rms = librosa.feature.rms(y=audio_array)[0]
            spectral_centroid = librosa.feature.spectral_centroid(y=audio_array, sr=sample_rate)[0]
            zcr = librosa.feature.zero_crossing_rate(audio_array)[0]
            
            # Emotion feature extraction
            if len(f0_clean) > 0:
                pitch_mean = np.mean(f0_clean)
                pitch_std = np.std(f0_clean)
                pitch_range = np.max(f0_clean) - np.min(f0_clean)
            else:
                pitch_mean = pitch_std = pitch_range = 0.0
            
            energy_mean = np.mean(rms)
            energy_std = np.std(rms)
            spectral_mean = np.mean(spectral_centroid)
            zcr_mean = np.mean(zcr)
            
            # Emotion classification based on acoustic features
            # These are simplified rules based on research literature
            emotions_scores = {}
            
            # Excitement/Happiness: Higher pitch, higher energy, more variation
            excitement_score = min(1.0, (
                (pitch_mean / 200.0) * 0.3 +  # Higher pitch
                (energy_mean * 10) * 0.3 +     # Higher energy
                (pitch_std / 50.0) * 0.4       # More pitch variation
            ))
            emotions_scores["excitement"] = float(excitement_score)
            
            # Confidence: Stable pitch, moderate energy, low variation
            confidence_score = min(1.0, (
                (energy_mean * 8) * 0.4 +           # Moderate-high energy
                (1.0 - min(1.0, pitch_std / 30.0)) * 0.4 +  # Stable pitch
                (1.0 - min(1.0, zcr_mean * 20)) * 0.2       # Clear speech
            ))
            emotions_scores["confidence"] = float(confidence_score)
            
            # Nervousness/Anxiety: Unstable pitch, variable energy
            nervousness_score = min(1.0, (
                (pitch_std / 40.0) * 0.4 +      # Pitch instability
                (energy_std * 15) * 0.3 +       # Energy variation
                (zcr_mean * 15) * 0.3           # Voice breaks
            ))
            emotions_scores["nervousness"] = float(nervousness_score)
            
            # Calmness: Stable pitch, moderate energy, smooth delivery
            calmness_score = min(1.0, (
                (1.0 - min(1.0, pitch_std / 25.0)) * 0.4 +  # Stable pitch
                (1.0 - abs(energy_mean - 0.1) * 10) * 0.3 + # Moderate energy
                (1.0 - energy_std * 20) * 0.3               # Stable energy
            ))
            emotions_scores["calmness"] = float(calmness_score)
            
            # Determine primary emotion
            primary_emotion = max(emotions_scores, key=emotions_scores.get)
            primary_score = emotions_scores[primary_emotion]
            
            emotion_analysis["acoustic_emotions"] = {
                "primary_emotion": primary_emotion,
                "confidence": primary_score,
                "emotion_scores": emotions_scores,
                "acoustic_features": {
                    "pitch_mean": float(pitch_mean),
                    "pitch_std": float(pitch_std),
                    "pitch_range": float(pitch_range),
                    "energy_mean": float(energy_mean),
                    "energy_std": float(energy_std),
                    "spectral_centroid_mean": float(spectral_mean),
                    "zcr_mean": float(zcr_mean)
                }
            }
            
            # 2. Text-based emotion analysis (if transcript available)
            if transcript:
                sentiment_scores = self.sentiment_analyzer.polarity_scores(transcript)
                emotion_analysis["text_emotions"] = {
                    "sentiment_compound": sentiment_scores['compound'],
                    "positive": sentiment_scores['pos'],
                    "neutral": sentiment_scores['neu'],
                    "negative": sentiment_scores['neg'],
                    "overall_sentiment": "positive" if sentiment_scores['compound'] > 0.1 else "negative" if sentiment_scores['compound'] < -0.1 else "neutral"
                }
            
            # 3. Combined emotion assessment
            emotion_analysis["combined_assessment"] = {
                "overall_emotion": primary_emotion,
                "emotion_confidence": primary_score,
                "emotional_stability": 1.0 - nervousness_score,
                "engagement_level": (excitement_score + confidence_score) / 2
            }
            
            return emotion_analysis
            
        except Exception as e:
            logging.error(f"Error in speech emotion analysis: {str(e)}")
            return {
                "acoustic_emotions": {
                    "primary_emotion": "neutral",
                    "confidence": 0.5,
                    "emotion_scores": {"neutral": 0.5}
                },
                "combined_assessment": {
                    "overall_emotion": "neutral",
                    "emotion_confidence": 0.5,
                    "emotional_stability": 0.5,
                    "engagement_level": 0.5
                },
                "error": str(e)
            }
    
    async def _calculate_confidence_score(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive confidence score based on all analysis
        """
        try:
            confidence_factors = {}
            
            # 1. Acoustic confidence indicators
            acoustic_features = analysis.get("acoustic_features", {})
            
            # Voice stability (low pitch variation indicates confidence)
            pitch_info = acoustic_features.get("pitch", {})
            if pitch_info.get("mean_f0", 0) > 0:
                pitch_stability = 1.0 - min(1.0, pitch_info.get("std_f0", 0) / pitch_info.get("mean_f0", 1))
                confidence_factors["pitch_stability"] = float(pitch_stability)
            else:
                confidence_factors["pitch_stability"] = 0.5
            
            # Energy consistency (confident speakers maintain steady energy)
            energy_info = acoustic_features.get("energy", {})
            if energy_info.get("mean_rms", 0) > 0:
                energy_consistency = 1.0 - min(1.0, energy_info.get("std_rms", 0) / energy_info.get("mean_rms", 1))
                confidence_factors["energy_consistency"] = float(energy_consistency)
            else:
                confidence_factors["energy_consistency"] = 0.5
            
            # 2. Speech quality contribution
            speech_quality = analysis.get("speech_quality", {})
            quality_score = speech_quality.get("overall_quality_score", 0.5)
            confidence_factors["speech_quality"] = float(quality_score)
            
            # 3. Prosodic confidence indicators
            prosodic_features = analysis.get("prosodic_features", {})
            
            # Speech rate (moderate rate indicates confidence)
            rhythm_info = prosodic_features.get("rhythm", {})
            speech_rate = rhythm_info.get("speech_rate_sps", 3.0)  # syllables per second
            # Optimal range is 3-5 syllables per second
            if 3.0 <= speech_rate <= 5.0:
                rate_confidence = 1.0
            else:
                rate_confidence = max(0.0, 1.0 - abs(speech_rate - 4.0) / 4.0)
            confidence_factors["speech_rate_confidence"] = float(rate_confidence)
            
            # Stress level (lower stress indicates more confidence)
            stress_info = prosodic_features.get("stress", {})
            stress_level = stress_info.get("stress_level", 0.5)
            stress_confidence = 1.0 - min(1.0, stress_level)
            confidence_factors["stress_confidence"] = float(stress_confidence)
            
            # 4. Emotion-based confidence
            emotion_analysis = analysis.get("emotion_analysis", {})
            acoustic_emotions = emotion_analysis.get("acoustic_emotions", {})
            emotion_scores = acoustic_emotions.get("emotion_scores", {})
            
            # Confidence from emotion analysis
            emotion_confidence = emotion_scores.get("confidence", 0.5)
            nervousness = emotion_scores.get("nervousness", 0.5)
            emotion_confidence_score = emotion_confidence - nervousness
            confidence_factors["emotional_confidence"] = float(max(0.0, min(1.0, emotion_confidence_score)))
            
            # 5. Combined confidence score
            weights = {
                "pitch_stability": 0.2,
                "energy_consistency": 0.15,
                "speech_quality": 0.15,
                "speech_rate_confidence": 0.15,
                "stress_confidence": 0.2,
                "emotional_confidence": 0.15
            }
            
            overall_confidence = sum(
                confidence_factors.get(factor, 0.5) * weight 
                for factor, weight in weights.items()
            )
            
            # Confidence level classification
            if overall_confidence > 0.8:
                confidence_level = "very_confident"
            elif overall_confidence > 0.6:
                confidence_level = "confident"
            elif overall_confidence > 0.4:
                confidence_level = "somewhat_confident"
            else:
                confidence_level = "not_confident"
            
            return {
                "overall_confidence_score": float(overall_confidence),
                "confidence_level": confidence_level,
                "confidence_factors": confidence_factors,
                "confidence_percentage": float(overall_confidence * 100)
            }
            
        except Exception as e:
            logging.error(f"Error calculating confidence score: {str(e)}")
            return {
                "overall_confidence_score": 0.5,
                "confidence_level": "somewhat_confident",
                "confidence_factors": {},
                "confidence_percentage": 50.0,
                "error": str(e)
            }
    
    async def _analyze_speech_pace(self, audio_array: np.ndarray, transcript: str, sample_rate: int) -> Dict[str, Any]:
        """
        Analyze speech pace and rhythm
        """
        try:
            pace_analysis = {}
            
            # Duration and basic metrics
            duration = len(audio_array) / sample_rate
            pace_analysis["total_duration"] = float(duration)
            
            # Syllable count estimation
            estimated_syllables = self._estimate_syllables(audio_array, sample_rate)
            pace_analysis["estimated_syllables"] = int(estimated_syllables)
            
            # Speech rate (syllables per second)
            speech_rate = estimated_syllables / duration if duration > 0 else 0
            pace_analysis["speech_rate_sps"] = float(speech_rate)
            
            # Word rate (if transcript available)
            if transcript:
                word_count = len(transcript.split())
                words_per_minute = (word_count / duration) * 60 if duration > 0 else 0
                pace_analysis["words_per_minute"] = float(words_per_minute)
                pace_analysis["word_count"] = int(word_count)
            else:
                # Estimate words from syllables (average 1.3 syllables per word)
                estimated_words = estimated_syllables / 1.3
                words_per_minute = (estimated_words / duration) * 60 if duration > 0 else 0
                pace_analysis["words_per_minute"] = float(words_per_minute)
                pace_analysis["word_count"] = int(estimated_words)
            
            # Pace evaluation
            wpm = pace_analysis["words_per_minute"]
            if 130 <= wpm <= 160:
                pace_rating = "optimal"
                pace_score = 1.0
            elif 110 <= wpm < 130 or 160 < wpm <= 180:
                pace_rating = "good"
                pace_score = 0.8
            elif 90 <= wpm < 110 or 180 < wpm <= 200:
                pace_rating = "acceptable"
                pace_score = 0.6
            elif wpm < 90:
                pace_rating = "too_slow"
                pace_score = max(0.0, wpm / 90 * 0.4)
            else:  # wpm > 200
                pace_rating = "too_fast"
                pace_score = max(0.0, 0.4 - (wpm - 200) / 100 * 0.4)
            
            pace_analysis["pace_rating"] = pace_rating
            pace_analysis["pace_score"] = float(pace_score)
            
            # Rhythm analysis (pause patterns)
            # Detect silence/pause segments
            rms = librosa.feature.rms(y=audio_array, frame_length=2048, hop_length=512)[0]
            silence_threshold = np.mean(rms) * 0.1
            silence_frames = rms < silence_threshold
            
            # Count pause segments
            pause_segments = []
            in_pause = False
            pause_start = 0
            
            frame_duration = 512 / sample_rate  # Duration of each frame
            
            for i, is_silent in enumerate(silence_frames):
                if is_silent and not in_pause:
                    in_pause = True
                    pause_start = i
                elif not is_silent and in_pause:
                    in_pause = False
                    pause_duration = (i - pause_start) * frame_duration
                    if pause_duration > 0.1:  # Only count pauses longer than 100ms
                        pause_segments.append(pause_duration)
            
            pace_analysis["pause_analysis"] = {
                "pause_count": len(pause_segments),
                "total_pause_time": float(sum(pause_segments)),
                "average_pause_duration": float(np.mean(pause_segments)) if pause_segments else 0.0,
                "pause_percentage": float(sum(pause_segments) / duration * 100) if duration > 0 else 0.0
            }
            
            return pace_analysis
            
        except Exception as e:
            logging.error(f"Error analyzing speech pace: {str(e)}")
            return {
                "total_duration": 1.0,
                "estimated_syllables": 10,
                "speech_rate_sps": 3.0,
                "words_per_minute": 150.0,
                "word_count": 10,
                "pace_rating": "acceptable",
                "pace_score": 0.6,
                "pause_analysis": {"pause_count": 0, "total_pause_time": 0.0, "average_pause_duration": 0.0, "pause_percentage": 0.0},
                "error": str(e)
            }
    
    async def _analyze_speech_clarity(self, audio_array: np.ndarray, sample_rate: int) -> Dict[str, Any]:
        """
        Analyze speech clarity and articulation
        """
        try:
            clarity_analysis = {}
            
            # 1. Spectral clarity metrics
            # High-frequency content indicates clear consonants
            stft = librosa.stft(audio_array, n_fft=2048, hop_length=512)
            magnitude = np.abs(stft)
            
            # Frequency bands
            freqs = librosa.fft_frequencies(sr=sample_rate, n_fft=2048)
            
            # High-frequency energy (2-8 kHz) - important for speech clarity
            hf_start = np.argmax(freqs >= 2000)
            hf_end = np.argmax(freqs >= 8000) if np.any(freqs >= 8000) else len(freqs)
            
            hf_energy = np.mean(magnitude[hf_start:hf_end, :])
            total_energy = np.mean(magnitude)
            
            hf_ratio = hf_energy / max(total_energy, 1e-10)
            clarity_analysis["high_frequency_ratio"] = float(hf_ratio)
            
            # 2. Spectral tilt (measure of voice quality)
            # Negative tilt indicates healthy voice
            spectral_slope = []
            for frame in range(magnitude.shape[1]):
                spectrum = magnitude[:, frame]
                if np.sum(spectrum) > 0:
                    # Calculate spectral tilt as slope of log spectrum
                    log_spectrum = np.log(spectrum + 1e-10)
                    slope = np.polyfit(range(len(log_spectrum)), log_spectrum, 1)[0]
                    spectral_slope.append(slope)
            
            avg_spectral_tilt = np.mean(spectral_slope) if spectral_slope else 0.0
            clarity_analysis["spectral_tilt"] = float(avg_spectral_tilt)
            
            # 3. Formant clarity (simplified)
            # Use spectral peaks as rough formant estimates
            spectrum_avg = np.mean(magnitude, axis=1)
            peaks, _ = scipy.signal.find_peaks(spectrum_avg, height=np.max(spectrum_avg) * 0.1)
            
            formant_clarity = len(peaks) / 5.0  # Normalize by expected number of formants
            clarity_analysis["formant_clarity"] = float(min(1.0, formant_clarity))
            
            # 4. Zero crossing rate (articulation clarity)
            zcr = librosa.feature.zero_crossing_rate(audio_array)[0]
            zcr_mean = np.mean(zcr)
            zcr_std = np.std(zcr)
            
            # Moderate ZCR with variation indicates good articulation
            optimal_zcr = 0.05  # Typical value for clear speech
            zcr_score = 1.0 - min(1.0, abs(zcr_mean - optimal_zcr) / optimal_zcr)
            
            clarity_analysis["articulation"] = {
                "zcr_mean": float(zcr_mean),
                "zcr_std": float(zcr_std),
                "articulation_score": float(zcr_score)
            }
            
            # 5. Overall clarity score
            # Combine different clarity metrics
            clarity_components = {
                "spectral_clarity": min(1.0, hf_ratio * 5),  # High-frequency content
                "voice_quality": min(1.0, max(0.0, 1.0 + avg_spectral_tilt / 0.01)),  # Spectral tilt
                "formant_definition": formant_clarity,
                "articulation_quality": zcr_score
            }
            
            weights = {"spectral_clarity": 0.3, "voice_quality": 0.3, "formant_definition": 0.2, "articulation_quality": 0.2}
            
            overall_clarity = sum(
                clarity_components[component] * weight 
                for component, weight in weights.items()
            )
            
            clarity_analysis["clarity_components"] = clarity_components
            clarity_analysis["overall_clarity_score"] = float(overall_clarity)
            
            # Clarity rating
            if overall_clarity > 0.8:
                clarity_rating = "excellent"
            elif overall_clarity > 0.6:
                clarity_rating = "good"
            elif overall_clarity > 0.4:
                clarity_rating = "fair"
            else:
                clarity_rating = "poor"
            
            clarity_analysis["clarity_rating"] = clarity_rating
            clarity_analysis["clarity_percentage"] = float(overall_clarity * 100)
            
            return clarity_analysis
            
        except Exception as e:
            logging.error(f"Error analyzing speech clarity: {str(e)}")
            return {
                "high_frequency_ratio": 0.2,
                "spectral_tilt": -0.01,
                "formant_clarity": 0.6,
                "articulation": {"zcr_mean": 0.05, "zcr_std": 0.02, "articulation_score": 0.6},
                "clarity_components": {"spectral_clarity": 0.6, "voice_quality": 0.6, "formant_definition": 0.6, "articulation_quality": 0.6},
                "overall_clarity_score": 0.6,
                "clarity_rating": "fair",
                "clarity_percentage": 60.0,
                "error": str(e)
            }
    
    async def _generate_overall_assessment(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate overall speech assessment
        """
        try:
            # Extract key scores
            speech_quality = analysis.get("speech_quality", {}).get("overall_quality_score", 0.5)
            confidence_score = analysis.get("confidence_scoring", {}).get("overall_confidence_score", 0.5)
            pace_score = analysis.get("pace_analysis", {}).get("pace_score", 0.6)
            clarity_score = analysis.get("clarity_analysis", {}).get("overall_clarity_score", 0.6)
            
            # Calculate weighted overall score
            weights = {
                "speech_quality": 0.25,
                "confidence": 0.30,
                "pace": 0.25,
                "clarity": 0.20
            }
            
            overall_score = (
                speech_quality * weights["speech_quality"] +
                confidence_score * weights["confidence"] +
                pace_score * weights["pace"] +
                clarity_score * weights["clarity"]
            )
            
            # Overall rating
            if overall_score > 0.8:
                overall_rating = "excellent"
                description = "Outstanding speech performance with professional-level delivery"
            elif overall_score > 0.65:
                overall_rating = "good"
                description = "Strong speech performance with minor areas for improvement"
            elif overall_score > 0.5:
                overall_rating = "average"
                description = "Acceptable speech performance with several areas for improvement"
            else:
                overall_rating = "needs_improvement"
                description = "Speech performance requires significant improvement"
            
            return {
                "overall_score": float(overall_score),
                "overall_rating": overall_rating,
                "description": description,
                "component_scores": {
                    "speech_quality": float(speech_quality),
                    "confidence": float(confidence_score),
                    "pace": float(pace_score),
                    "clarity": float(clarity_score)
                },
                "score_percentage": float(overall_score * 100)
            }
            
        except Exception as e:
            logging.error(f"Error generating overall assessment: {str(e)}")
            return {
                "overall_score": 0.5,
                "overall_rating": "average",
                "description": "Speech analysis completed with basic metrics",
                "component_scores": {"speech_quality": 0.5, "confidence": 0.5, "pace": 0.5, "clarity": 0.5},
                "score_percentage": 50.0,
                "error": str(e)
            }
    
    async def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """
        Generate personalized recommendations based on analysis
        """
        try:
            recommendations = []
            
            # Speech quality recommendations
            speech_quality = analysis.get("speech_quality", {})
            if speech_quality.get("overall_quality_score", 0.5) < 0.6:
                recommendations.append("Improve audio setup and environment to reduce background noise")
            
            if speech_quality.get("snr_db", 10) < 15:
                recommendations.append("Find a quieter environment for better audio quality")
            
            # Confidence recommendations
            confidence_scoring = analysis.get("confidence_scoring", {})
            confidence_score = confidence_scoring.get("overall_confidence_score", 0.5)
            
            if confidence_score < 0.6:
                recommendations.append("Practice speaking with more confidence and steady voice")
            
            confidence_factors = confidence_scoring.get("confidence_factors", {})
            if confidence_factors.get("pitch_stability", 0.5) < 0.5:
                recommendations.append("Work on maintaining steady pitch throughout your speech")
            
            if confidence_factors.get("stress_confidence", 0.5) < 0.5:
                recommendations.append("Try relaxation techniques to reduce vocal stress")
            
            # Pace recommendations
            pace_analysis = analysis.get("pace_analysis", {})
            pace_rating = pace_analysis.get("pace_rating", "acceptable")
            
            if pace_rating == "too_fast":
                recommendations.append("Slow down your speech rate for better comprehension")
            elif pace_rating == "too_slow":
                recommendations.append("Increase your speech rate slightly for more engagement")
            
            wpm = pace_analysis.get("words_per_minute", 150)
            if wpm < 120:
                recommendations.append("Practice speaking at a more natural conversational pace")
            elif wpm > 180:
                recommendations.append("Take more pauses and speak more deliberately")
            
            # Clarity recommendations
            clarity_analysis = analysis.get("clarity_analysis", {})
            clarity_score = clarity_analysis.get("overall_clarity_score", 0.6)
            
            if clarity_score < 0.6:
                recommendations.append("Focus on clear articulation and pronunciation")
            
            clarity_components = clarity_analysis.get("clarity_components", {})
            if clarity_components.get("articulation_quality", 0.6) < 0.5:
                recommendations.append("Practice consonant articulation exercises")
            
            if clarity_components.get("spectral_clarity", 0.6) < 0.5:
                recommendations.append("Speak with more energy and projection")
            
            # Emotion and engagement recommendations
            emotion_analysis = analysis.get("emotion_analysis", {})
            combined_assessment = emotion_analysis.get("combined_assessment", {})
            
            engagement_level = combined_assessment.get("engagement_level", 0.5)
            if engagement_level < 0.5:
                recommendations.append("Show more enthusiasm and energy in your voice")
            
            emotional_stability = combined_assessment.get("emotional_stability", 0.5)
            if emotional_stability < 0.5:
                recommendations.append("Work on emotional regulation and composure during speech")
            
            # General recommendations if no specific issues found
            if not recommendations:
                recommendations.extend([
                    "Continue practicing to maintain your current speech quality",
                    "Consider recording yourself regularly to track improvements",
                    "Focus on connecting with your audience through voice modulation"
                ])
            
            return recommendations[:5]  # Return top 5 recommendations
            
        except Exception as e:
            logging.error(f"Error generating recommendations: {str(e)}")
            return [
                "Continue practicing your speech and presentation skills",
                "Record yourself regularly to monitor improvements",
                "Focus on clear communication and audience engagement"
            ]
    
    def _get_fallback_analysis(self, error_message: str) -> Dict[str, Any]:
        """
        Return fallback analysis when main analysis fails
        """
        return {
            "acoustic_features": {"error": error_message},
            "prosodic_features": {"error": error_message},
            "speech_quality": {
                "overall_quality_score": 0.5,
                "quality_rating": "average",
                "snr_db": 10.0,
                "hnr_db": 10.0,
                "spectral_flatness": 0.5
            },
            "emotion_analysis": {
                "acoustic_emotions": {
                    "primary_emotion": "neutral",
                    "confidence": 0.5,
                    "emotion_scores": {"neutral": 0.5}
                },
                "combined_assessment": {
                    "overall_emotion": "neutral",
                    "emotion_confidence": 0.5,
                    "emotional_stability": 0.5,
                    "engagement_level": 0.5
                }
            },
            "confidence_scoring": {
                "overall_confidence_score": 0.5,
                "confidence_level": "somewhat_confident",
                "confidence_percentage": 50.0
            },
            "pace_analysis": {
                "words_per_minute": 150.0,
                "pace_rating": "acceptable",
                "pace_score": 0.6
            },
            "clarity_analysis": {
                "overall_clarity_score": 0.6,
                "clarity_rating": "fair",
                "clarity_percentage": 60.0
            },
            "overall_assessment": {
                "overall_score": 0.5,
                "overall_rating": "average",
                "description": "Basic speech analysis completed",
                "score_percentage": 50.0
            },
            "recommendations": ["Analysis temporarily unavailable - please try again"],
            "error": error_message
        }

# Global instance
advanced_speech_analyzer = None

def get_speech_analyzer():
    """Get or create the global speech analyzer instance"""
    global advanced_speech_analyzer
    if advanced_speech_analyzer is None:
        advanced_speech_analyzer = AdvancedSpeechAnalyzer()
    return advanced_speech_analyzer

# Initialize the analyzer when module is imported
try:
    advanced_speech_analyzer = AdvancedSpeechAnalyzer()
    logging.info("✅ AdvancedSpeechAnalyzer initialized successfully")
except Exception as e:
    logging.error(f"❌ Failed to initialize AdvancedSpeechAnalyzer: {str(e)}")
    advanced_speech_analyzer = None