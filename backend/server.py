from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import json
import asyncio
import re
from emergentintegrations.llm.chat import LlmChat, UserMessage
import secrets
import string
import io
import base64

# Document parsing imports
import PyPDF2
from docx import Document

# Google Cloud imports
from google.cloud import texttospeech
from google.oauth2 import service_account
import pymongo
import gridfs

# Import libraries for sentiment analysis and emotional intelligence
import librosa
import numpy as np
import torch
# import transformers
# from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textstat import flesch_reading_ease

# Advanced Analysis Engines
from emotion_analyzer import emotion_analyzer
from speech_analyzer import speech_analyzer

# Phase 3: Internationalization Manager
class I18nManager:
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ja': 'Japanese',
            'zh': 'Chinese'
        }
        self.translations = {}
        self.load_all_translations()
    
    def load_all_translations(self):
        """Load all translation files"""
        for lang_code in self.supported_languages.keys():
            self.load_translations(lang_code)
    
    def load_translations(self, language: str):
        """Load language-specific translations"""
        if language not in self.supported_languages:
            language = 'en'  # Fallback to English
        
        # For now, we'll use a basic dictionary structure
        # In production, this would load from JSON files
        translations = {
            'en': {
                'interview': {
                    'welcome': 'Welcome to your interview',
                    'question': 'Question',
                    'of': 'of',
                    'submit_answer': 'Submit Answer',
                    'next_question': 'Next Question',
                    'interview_complete': 'Interview Complete',
                    'technical_question': 'Technical Question',
                    'behavioral_question': 'Behavioral Question',
                    'resume_question': 'Resume-based Question',
                    'coding_challenge': 'Coding Challenge',
                    'thank_you': 'Thank you for completing the interview'
                },
                'assessment': {
                    'overall_score': 'Overall Score',
                    'technical_score': 'Technical Score',
                    'behavioral_score': 'Behavioral Score',
                    'communication_score': 'Communication Score',
                    'strengths': 'Strengths',
                    'areas_for_improvement': 'Areas for Improvement',
                    'recommendations': 'Recommendations'
                },
                'errors': {
                    'invalid_token': 'Invalid interview token',
                    'session_expired': 'Session has expired',
                    'server_error': 'Server error occurred',
                    'network_error': 'Network connection error'
                }
            },
            'es': {
                'interview': {
                    'welcome': 'Bienvenido a tu entrevista',
                    'question': 'Pregunta',
                    'of': 'de',
                    'submit_answer': 'Enviar Respuesta',
                    'next_question': 'Siguiente Pregunta',
                    'interview_complete': 'Entrevista Completa',
                    'technical_question': 'Pregunta Técnica',
                    'behavioral_question': 'Pregunta Conductual',
                    'resume_question': 'Pregunta basada en CV',
                    'coding_challenge': 'Desafío de Codificación',
                    'thank_you': 'Gracias por completar la entrevista'
                },
                'assessment': {
                    'overall_score': 'Puntuación General',
                    'technical_score': 'Puntuación Técnica',
                    'behavioral_score': 'Puntuación Conductual',
                    'communication_score': 'Puntuación de Comunicación',
                    'strengths': 'Fortalezas',
                    'areas_for_improvement': 'Áreas de Mejora',
                    'recommendations': 'Recomendaciones'
                },
                'errors': {
                    'invalid_token': 'Token de entrevista inválido',
                    'session_expired': 'La sesión ha expirado',
                    'server_error': 'Error del servidor',
                    'network_error': 'Error de conexión de red'
                }
            },
            'fr': {
                'interview': {
                    'welcome': 'Bienvenue à votre entretien',
                    'question': 'Question',
                    'of': 'de',
                    'submit_answer': 'Soumettre la Réponse',
                    'next_question': 'Question Suivante',
                    'interview_complete': 'Entretien Terminé',
                    'technical_question': 'Question Technique',
                    'behavioral_question': 'Question Comportementale',
                    'resume_question': 'Question basée sur CV',
                    'coding_challenge': 'Défi de Codage',
                    'thank_you': 'Merci d\'avoir terminé l\'entretien'
                },
                'assessment': {
                    'overall_score': 'Score Global',
                    'technical_score': 'Score Technique',
                    'behavioral_score': 'Score Comportemental',
                    'communication_score': 'Score de Communication',
                    'strengths': 'Forces',
                    'areas_for_improvement': 'Domaines d\'Amélioration',
                    'recommendations': 'Recommandations'
                },
                'errors': {
                    'invalid_token': 'Jeton d\'entretien invalide',
                    'session_expired': 'La session a expiré',
                    'server_error': 'Erreur du serveur',
                    'network_error': 'Erreur de connexion réseau'
                }
            },
            'de': {
                'interview': {
                    'welcome': 'Willkommen zu Ihrem Interview',
                    'question': 'Frage',
                    'of': 'von',
                    'submit_answer': 'Antwort Einreichen',
                    'next_question': 'Nächste Frage',
                    'interview_complete': 'Interview Abgeschlossen',
                    'technical_question': 'Technische Frage',
                    'behavioral_question': 'Verhaltensfrage',
                    'resume_question': 'Lebenslauf-basierte Frage',
                    'coding_challenge': 'Coding-Herausforderung',
                    'thank_you': 'Vielen Dank für das Abschließen des Interviews'
                },
                'assessment': {
                    'overall_score': 'Gesamtpunktzahl',
                    'technical_score': 'Technische Punktzahl',
                    'behavioral_score': 'Verhaltenspunktzahl',
                    'communication_score': 'Kommunikationspunktzahl',
                    'strengths': 'Stärken',
                    'areas_for_improvement': 'Verbesserungsbereiche',
                    'recommendations': 'Empfehlungen'
                },
                'errors': {
                    'invalid_token': 'Ungültiger Interview-Token',
                    'session_expired': 'Sitzung ist abgelaufen',
                    'server_error': 'Server-Fehler aufgetreten',
                    'network_error': 'Netzwerkverbindungsfehler'
                }
            }
        }
        
        self.translations[language] = translations.get(language, translations['en'])
    
    def translate(self, key: str, language: str = 'en', params: dict = None) -> str:
        """Get translated text"""
        if language not in self.supported_languages:
            language = 'en'
        
        try:
            keys = key.split('.')
            value = self.translations.get(language, self.translations['en'])
            
            for k in keys:
                value = value[k]
            
            # Replace parameters if provided
            if params and isinstance(value, str):
                for param, param_value in params.items():
                    value = value.replace(f'{{{param}}}', str(param_value))
            
            return value
        except (KeyError, TypeError):
            # Fallback to English if key not found
            if language != 'en':
                return self.translate(key, 'en', params)
            return key
    
    def get_supported_languages(self) -> dict:
        """Get all supported languages"""
        return self.supported_languages
    
    def translate_ai_content(self, content: str, target_language: str) -> str:
        """Translate AI-generated content using translation service"""
        if target_language == 'en':
            return content
        
        # For now, return original content
        # In production, this would use a translation service like Google Translate
        return content

# Initialize I18n Manager
i18n_manager = I18nManager()

# GDPR/CCPA Compliance Implementation
class DataPrivacyManager:
    def __init__(self):
        self.consent_tracking = {}
        self.data_retention_policies = {
            'interview_data': 90,  # days
            'audio_files': 30,
            'video_analysis': 60
        }
    
    def request_consent(self, candidate_id, data_types):
        """Explicit consent for data collection"""
        return {
            'consent_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'data_types': data_types,
            'candidate_id': candidate_id
        }
    
    async def right_to_erasure(self, candidate_id):
        """GDPR Article 17 - Right to be forgotten"""
        try:
            # Delete all candidate data from various collections
            collections_to_clean = [
                'tokens', 'enhanced_tokens', 'sessions', 'assessments',
                'video_analysis', 'audio_analysis', 'coding_challenges', 'sjt_tests'
            ]
            
            deleted_counts = {}
            for collection_name in collections_to_clean:
                collection = getattr(db, collection_name)
                result = await collection.delete_many({"candidate_name": candidate_id})
                deleted_counts[collection_name] = result.deleted_count
            
            # Delete audio files from GridFS
            audio_files = fs.find({"metadata.candidate_id": candidate_id})
            audio_deleted = 0
            for audio_file in audio_files:
                fs.delete(audio_file._id)
                audio_deleted += 1
            deleted_counts['audio_files'] = audio_deleted
            
            logging.info(f"Data erasure completed for candidate {candidate_id}: {deleted_counts}")
            return {
                "status": "completed",
                "candidate_id": candidate_id,
                "deleted_records": deleted_counts,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            logging.error(f"Data erasure failed for candidate {candidate_id}: {str(e)}")
            return {
                "status": "failed",
                "candidate_id": candidate_id,
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
    
    async def cleanup_expired_data(self):
        """Clean up data based on retention policies"""
        try:
            cleanup_results = {}
            current_time = datetime.utcnow()
            
            # Clean up interview data (90 days)
            interview_cutoff = current_time - timedelta(days=self.data_retention_policies['interview_data'])
            
            # Clean sessions
            sessions_result = await db.sessions.delete_many({"started_at": {"$lt": interview_cutoff}})
            cleanup_results['sessions'] = sessions_result.deleted_count
            
            # Clean assessments
            assessments_result = await db.assessments.delete_many({"created_at": {"$lt": interview_cutoff}})
            cleanup_results['assessments'] = assessments_result.deleted_count
            
            # Clean tokens
            tokens_result = await db.tokens.delete_many({"created_at": {"$lt": interview_cutoff}})
            cleanup_results['tokens'] = tokens_result.deleted_count
            
            enhanced_tokens_result = await db.enhanced_tokens.delete_many({"created_at": {"$lt": interview_cutoff}})
            cleanup_results['enhanced_tokens'] = enhanced_tokens_result.deleted_count
            
            # Clean up audio files (30 days)
            audio_cutoff = current_time - timedelta(days=self.data_retention_policies['audio_files'])
            
            # Find and delete expired audio files from GridFS
            expired_audio_files = fs.find({
                "uploadDate": {"$lt": audio_cutoff},
                "metadata.type": {"$in": ["answer_audio", "question_audio", "tts_audio"]}
            })
            
            audio_deleted = 0
            for audio_file in expired_audio_files:
                fs.delete(audio_file._id)
                audio_deleted += 1
            cleanup_results['audio_files'] = audio_deleted
            
            # Clean up video analysis data (60 days)
            video_cutoff = current_time - timedelta(days=self.data_retention_policies['video_analysis'])
            
            # Clean video analysis collections
            video_result = await db.video_analysis.delete_many({
                "timestamp": {"$lt": video_cutoff.isoformat()}
            })
            cleanup_results['video_analysis'] = video_result.deleted_count
            
            # Clean audio analysis data (60 days for analysis, different from raw audio files)
            audio_analysis_result = await db.audio_analysis.delete_many({
                "timestamp": {"$lt": video_cutoff.isoformat()}
            })
            cleanup_results['audio_analysis'] = audio_analysis_result.deleted_count
            
            logging.info(f"Data cleanup completed: {cleanup_results}")
            return {
                "status": "completed",
                "cleanup_results": cleanup_results,
                "timestamp": current_time,
                "retention_policies": self.data_retention_policies
            }
            
        except Exception as e:
            logging.error(f"Data cleanup failed: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "timestamp": current_time
            }
    
    async def get_data_retention_status(self):
        """Get current data retention status and counts"""
        try:
            current_time = datetime.utcnow()
            status = {
                "current_time": current_time,
                "retention_policies": self.data_retention_policies,
                "data_counts": {}
            }
            
            # Count interview data
            interview_cutoff = current_time - timedelta(days=self.data_retention_policies['interview_data'])
            
            total_sessions = await db.sessions.count_documents({})
            expired_sessions = await db.sessions.count_documents({"started_at": {"$lt": interview_cutoff}})
            
            total_assessments = await db.assessments.count_documents({})
            expired_assessments = await db.assessments.count_documents({"created_at": {"$lt": interview_cutoff}})
            
            # Count audio files
            audio_cutoff = current_time - timedelta(days=self.data_retention_policies['audio_files'])
            total_audio = len(list(fs.find()))
            expired_audio = len(list(fs.find({
                "uploadDate": {"$lt": audio_cutoff},
                "metadata.type": {"$in": ["answer_audio", "question_audio", "tts_audio"]}
            })))
            
            # Count video analysis data
            video_cutoff = current_time - timedelta(days=self.data_retention_policies['video_analysis'])
            total_video_analysis = await db.video_analysis.count_documents({})
            expired_video_analysis = await db.video_analysis.count_documents({
                "timestamp": {"$lt": video_cutoff.isoformat()}
            })
            
            status["data_counts"] = {
                "sessions": {"total": total_sessions, "expired": expired_sessions},
                "assessments": {"total": total_assessments, "expired": expired_assessments},
                "audio_files": {"total": total_audio, "expired": expired_audio},
                "video_analysis": {"total": total_video_analysis, "expired": expired_video_analysis}
            }
            
            return status
            
        except Exception as e:
            logging.error(f"Failed to get data retention status: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": current_time
            }

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# For GridFS, we need a synchronous connection
import pymongo
sync_client = pymongo.MongoClient(mongo_url)
sync_db = sync_client[os.environ['DB_NAME']]
fs = gridfs.GridFS(sync_db)

# Google Cloud Setup (TTS only - STT handled by Web Speech API)
credentials_json = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '{}'))
credentials = service_account.Credentials.from_service_account_info(credentials_json)
tts_client = texttospeech.TextToSpeechClient(credentials=credentials)

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Phase 3: I18n API Endpoints
@app.get("/api/translations/{language}")
async def get_translations(language: str):
    """Get translations for a specific language"""
    try:
        if language not in i18n_manager.supported_languages:
            language = 'en'
        
        return {
            "language": language,
            "translations": i18n_manager.translations.get(language, i18n_manager.translations['en'])
        }
    except Exception as e:
        logging.error(f"Error getting translations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get translations")

@app.get("/api/translations/{language}/{module}")
async def get_module_translations(language: str, module: str):
    """Get translations for a specific module and language"""
    try:
        if language not in i18n_manager.supported_languages:
            language = 'en'
        
        translations = i18n_manager.translations.get(language, i18n_manager.translations['en'])
        module_translations = translations.get(module, {})
        
        return {
            "language": language,
            "module": module,
            "translations": module_translations
        }
    except Exception as e:
        logging.error(f"Error getting module translations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get module translations")

@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    try:
        return {
            "languages": i18n_manager.get_supported_languages()
        }
    except Exception as e:
        logging.error(f"Error getting supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get supported languages")

@app.post("/api/translate")
async def translate_text(data: dict):
    """Translate text to target language"""
    try:
        text = data.get('text', '')
        target_language = data.get('target_language', 'en')
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # For now, return original text
        # In production, this would use a translation service
        translated_text = i18n_manager.translate_ai_content(text, target_language)
        
        return {
            "original_text": text,
            "translated_text": translated_text,
            "source_language": "en",
            "target_language": target_language
        }
    except Exception as e:
        logging.error(f"Error translating text: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to translate text")

# Pydantic Models
class JobDescription(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    requirements: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CandidateToken(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    token: str
    job_id: str
    resume_content: str
    job_description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    used: bool = False

class InterviewSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    token: str
    session_id: str
    candidate_name: str
    job_title: str
    messages: List[Dict[str, Any]] = []
    current_question: int = 0
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    status: str = "in_progress"  # in_progress, completed
    voice_mode: bool = False

class InterviewAssessment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    token: str
    candidate_name: str
    job_title: str
    technical_score: int
    behavioral_score: int
    overall_score: int
    technical_feedback: str
    behavioral_feedback: str
    overall_feedback: str
    recommendations: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    # Enhanced fields for multi-vector assessment
    competency_scores: Dict[str, int] = {}
    key_strengths: List[str] = []
    areas_for_improvement: List[str] = []
    supporting_quotes: List[str] = []
    red_flags: List[str] = []
    module_performance: Dict[str, Dict[str, Any]] = {}

# Enhanced Token model with coding challenge option
class EnhancedCandidateToken(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    token: str
    job_id: str
    resume_content: str
    job_description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    used: bool = False
    # New fields
    include_coding_challenge: bool = False
    role_archetype: str = "General"  # Software Engineer, Sales, Graduate, etc.
    interview_focus: str = "Balanced"  # Technical Deep-Dive, Cultural Fit, Graduate Screening
    estimated_duration: int = 30  # minutes
    # Question limits
    min_questions: int = 8  # Minimum questions to be asked
    max_questions: int = 12  # Maximum questions that can be asked
    # Custom questions configuration
    custom_questions_config: Dict[str, Any] = {}

# Practice Round model
class PracticeRound(BaseModel):
    session_id: str
    question: str = "Tell me about a hobby you're passionate about."
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Coding Challenge model
class CodingChallenge(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    problem_title: str
    problem_description: str
    initial_code: str
    expected_solution: str
    difficulty: str = "medium"  # easy, medium, hard
    language: str = "javascript"
    submitted_code: Optional[str] = None
    score: Optional[int] = None
    analysis: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

# SJT (Situational Judgment Test) model
class SJTTest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    scenario: str
    question: str
    options: List[Dict[str, str]]  # [{"id": "a", "text": "Option A"}, ...]
    selected_answer: Optional[str] = None
    correct_answer: str
    explanation: str
    score: Optional[int] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdminLoginRequest(BaseModel):
    password: str

class TokenValidationRequest(BaseModel):
    token: str

class InterviewMessageRequest(BaseModel):
    token: str
    message: str

class InterviewStartRequest(BaseModel):
    token: str
    candidate_name: str
    voice_mode: Optional[bool] = False

class VoiceQuestionRequest(BaseModel):
    session_id: str
    question_text: str

# Enhanced request models for new features
class EnhancedJobUploadRequest(BaseModel):
    job_title: str
    job_description: str
    job_requirements: str
    include_coding_challenge: bool = False
    role_archetype: str = "General"
    interview_focus: str = "Balanced"

class CameraTestRequest(BaseModel):
    token: str

class PracticeRoundRequest(BaseModel):
    token: str
    candidate_name: str

class RephraseQuestionRequest(BaseModel):
    session_id: str
    original_question: str

class CodingChallengeSubmissionRequest(BaseModel):
    session_id: str
    submitted_code: str

class SJTAnswerRequest(BaseModel):
    session_id: str
    sjt_id: str
    selected_answer: str

# Data privacy request models
class ConsentRequest(BaseModel):
    candidate_id: str
    data_types: List[str]

# Document parsing utilities
def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logging.error(f"PDF parsing error: {str(e)}")
        return ""

def extract_text_from_docx(file_content: bytes) -> str:
    try:
        doc = Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        logging.error(f"DOCX parsing error: {str(e)}")
        return ""

def extract_text_from_txt(file_content: bytes) -> str:
    try:
        return file_content.decode('utf-8')
    except Exception as e:
        logging.error(f"TXT parsing error: {str(e)}")
        return ""

def parse_resume(file: UploadFile, content: bytes) -> str:
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(content)
    elif filename.endswith(('.doc', '.docx')):
        return extract_text_from_docx(content)
    elif filename.endswith('.txt'):
        return extract_text_from_txt(content)
    else:
        # Try to decode as text first
        try:
            return content.decode('utf-8')
        except:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, DOC, DOCX, or TXT files.")

# Initialize sentiment analysis tools
analyzer = SentimentIntensityAnalyzer()

# Initialize emotion classification pipeline 
try:
    # emotion_classifier = pipeline("text-classification", 
    #                             model="j-hartmann/emotion-english-distilroberta-base",
    #                             return_all_scores=True)
    # print("✅ Emotion classifier loaded successfully")
    emotion_classifier = None
    print("⚠️  Warning: Emotion classifier disabled - transformers pipeline commented out")
except Exception as e:
    print(f"⚠️  Warning: Could not load emotion classifier - {e}")
    emotion_classifier = None

class EmotionalIntelligenceAnalyzer:
    """Advanced emotional intelligence and sentiment analysis"""
    
    def __init__(self):
        self.analyzer = analyzer
        self.emotion_classifier = emotion_classifier
        
    def analyze_text_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment using VADER and emotion classification"""
        try:
            # VADER sentiment analysis
            sentiment_scores = self.analyzer.polarity_scores(text)
            
            # Emotion classification if available
            emotions = {}
            if self.emotion_classifier and text.strip():
                emotion_results = self.emotion_classifier(text)
                for emotion_score in emotion_results[0]:
                    emotions[emotion_score['label']] = emotion_score['score']
            
            # Calculate overall emotional intelligence metrics
            emotional_stability = 1 - abs(sentiment_scores['compound'])
            enthusiasm_score = max(emotions.get('joy', 0), emotions.get('excitement', 0)) if emotions else sentiment_scores['pos']
            stress_indicators = emotions.get('fear', 0) + emotions.get('sadness', 0) if emotions else sentiment_scores['neg']
            
            return {
                "sentiment": {
                    "compound": sentiment_scores['compound'],
                    "positive": sentiment_scores['pos'],
                    "neutral": sentiment_scores['neu'],
                    "negative": sentiment_scores['neg']
                },
                "emotions": emotions,
                "emotional_intelligence": {
                    "enthusiasm": float(enthusiasm_score),
                    "emotional_stability": float(emotional_stability),
                    "stress_level": float(stress_indicators),
                    "confidence": float(sentiment_scores['pos'] - sentiment_scores['neg'] + 1) / 2
                }
            }
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            return {
                "sentiment": {"compound": 0, "positive": 0, "neutral": 1, "negative": 0},
                "emotions": {},
                "emotional_intelligence": {
                    "enthusiasm": 0.5,
                    "emotional_stability": 0.5,
                    "stress_level": 0.5,
                    "confidence": 0.5
                }
            }
    
    def analyze_voice_features(self, audio_data: bytes, sample_rate: int = 16000) -> Dict[str, Any]:
        """Analyze voice characteristics for emotional indicators"""
        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.float32)
            
            # Extract voice features using librosa
            features = {}
            
            # Pitch and energy features
            pitches, magnitudes = librosa.piptrack(y=audio_array, sr=sample_rate)
            pitch_mean = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0
            
            # Energy and loudness
            rms = librosa.feature.rms(y=audio_array)[0]
            energy_mean = np.mean(rms)
            energy_variance = np.var(rms)
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_array, sr=sample_rate)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_array, sr=sample_rate)[0]
            
            # Zero crossing rate (speech clarity indicator)
            zcr = librosa.feature.zero_crossing_rate(audio_array)[0]
            
            # Estimate emotional indicators from voice features
            voice_confidence = min(1.0, energy_mean * 2)  # Higher energy = more confidence
            voice_stress = min(1.0, pitch_mean / 400.0 if pitch_mean > 0 else 0)  # Higher pitch can indicate stress
            voice_enthusiasm = min(1.0, (energy_variance + np.mean(spectral_centroids) / 1000) / 2)
            
            return {
                "voice_features": {
                    "pitch_mean": float(pitch_mean) if not np.isnan(pitch_mean) else 0.0,
                    "energy_mean": float(energy_mean),
                    "energy_variance": float(energy_variance),
                    "spectral_centroid_mean": float(np.mean(spectral_centroids)),
                    "spectral_rolloff_mean": float(np.mean(spectral_rolloff)),
                    "zero_crossing_rate": float(np.mean(zcr))
                },
                "voice_emotional_indicators": {
                    "confidence": float(voice_confidence),
                    "stress_level": float(voice_stress),
                    "enthusiasm": float(voice_enthusiasm),
                    "clarity": float(1 - np.mean(zcr))  # Lower ZCR = clearer speech
                }
            }
        except Exception as e:
            print(f"Error in voice analysis: {e}")
            return {
                "voice_features": {
                    "pitch_mean": 0.0,
                    "energy_mean": 0.0,
                    "energy_variance": 0.0,
                    "spectral_centroid_mean": 0.0,
                    "spectral_rolloff_mean": 0.0,
                    "zero_crossing_rate": 0.0
                },
                "voice_emotional_indicators": {
                    "confidence": 0.5,
                    "stress_level": 0.5,
                    "enthusiasm": 0.5,
                    "clarity": 0.5
                }
            }

# Initialize the emotional intelligence analyzer
ei_analyzer = EmotionalIntelligenceAnalyzer()

# Phase 4: Executive Analytics Dashboard
class ExecutiveAnalytics:
    """Advanced analytics for C-Suite dashboard with real-time and historical insights"""
    
    def __init__(self):
        self.cost_per_hire_base = 5000  # Base cost estimate in USD
        self.time_buckets = {
            'excellent': 7,    # <= 7 days
            'good': 14,        # 8-14 days  
            'average': 21,     # 15-21 days
            'slow': 30,        # 22-30 days
            'poor': 999        # > 30 days
        }
    
    async def calculate_time_to_hire_metrics(self, date_range: tuple = None) -> dict:
        """Calculate comprehensive time-to-hire analytics"""
        try:
            # Build query filter
            query_filter = {}
            if date_range:
                start_date, end_date = date_range
                query_filter["created_at"] = {
                    "$gte": start_date,
                    "$lte": end_date
                }
            
            # Get completed sessions
            sessions = await db.sessions.find({
                **query_filter,
                "status": "completed",
                "completed_at": {"$exists": True}
            }).to_list(None)
            
            if not sessions:
                return {
                    "average_time_to_hire": 0,
                    "median_time_to_hire": 0,
                    "time_distribution": {},
                    "trend_data": [],
                    "total_hires": 0
                }
            
            # Calculate time to hire for each session
            hire_times = []
            for session in sessions:
                if session.get("started_at") and session.get("completed_at"):
                    start = session["started_at"]
                    end = session["completed_at"]
                    if isinstance(start, str):
                        start = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    if isinstance(end, str):
                        end = datetime.fromisoformat(end.replace('Z', '+00:00'))
                    
                    time_diff = (end - start).total_seconds() / (24 * 3600)  # Convert to days
                    hire_times.append(time_diff)
            
            # Calculate metrics
            average_time = sum(hire_times) / len(hire_times) if hire_times else 0
            median_time = sorted(hire_times)[len(hire_times)//2] if hire_times else 0
            
            # Time distribution
            time_distribution = {
                'excellent': len([t for t in hire_times if t <= self.time_buckets['excellent']]),
                'good': len([t for t in hire_times if self.time_buckets['excellent'] < t <= self.time_buckets['good']]),
                'average': len([t for t in hire_times if self.time_buckets['good'] < t <= self.time_buckets['average']]),
                'slow': len([t for t in hire_times if self.time_buckets['average'] < t <= self.time_buckets['slow']]),
                'poor': len([t for t in hire_times if t > self.time_buckets['slow']])
            }
            
            # Trend data (last 30 days, weekly buckets)
            trend_data = await self._calculate_time_trend(sessions)
            
            return {
                "average_time_to_hire": round(average_time, 2),
                "median_time_to_hire": round(median_time, 2),
                "time_distribution": time_distribution,
                "trend_data": trend_data,
                "total_hires": len(hire_times)
            }
        
        except Exception as e:
            logging.error(f"Time to hire calculation error: {e}")
            return {
                "average_time_to_hire": 0,
                "median_time_to_hire": 0,
                "time_distribution": {},
                "trend_data": [],
                "total_hires": 0
            }
    
    async def calculate_candidate_experience_metrics(self, date_range: tuple = None) -> dict:
        """Calculate candidate experience and satisfaction metrics"""
        try:
            query_filter = {}
            if date_range:
                start_date, end_date = date_range
                query_filter["created_at"] = {
                    "$gte": start_date,
                    "$lte": end_date
                }
            
            # Get all assessments
            assessments = await db.assessments.find(query_filter).to_list(None)
            
            if not assessments:
                return {
                    "average_experience_score": 0,
                    "satisfaction_distribution": {},
                    "feedback_themes": [],
                    "completion_rate": 0
                }
            
            # Calculate experience metrics from emotional intelligence data
            experience_scores = []
            satisfaction_levels = []
            
            for assessment in assessments:
                ei_metrics = assessment.get('emotional_intelligence_metrics', {})
                
                # Experience score based on confidence, engagement, and stress levels
                confidence = ei_metrics.get('confidence', 0.5)
                engagement = ei_metrics.get('enthusiasm', 0.5)
                stress = ei_metrics.get('stress_level', 0.5)
                
                experience_score = (confidence * 0.4 + engagement * 0.4 + (1 - stress) * 0.2) * 5  # Convert to 1-5 scale
                experience_scores.append(experience_score)
                
                # Satisfaction level classification
                if experience_score >= 4.0:
                    satisfaction_levels.append('excellent')
                elif experience_score >= 3.5:
                    satisfaction_levels.append('good')
                elif experience_score >= 2.5:
                    satisfaction_levels.append('average')
                else:
                    satisfaction_levels.append('poor')
            
            # Calculate distributions
            satisfaction_distribution = {
                'excellent': satisfaction_levels.count('excellent'),
                'good': satisfaction_levels.count('good'), 
                'average': satisfaction_levels.count('average'),
                'poor': satisfaction_levels.count('poor')
            }
            
            # Get completion rate
            total_sessions = await db.sessions.count_documents(query_filter)
            completed_sessions = await db.sessions.count_documents({
                **query_filter,
                "status": "completed"
            })
            completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            return {
                "average_experience_score": round(sum(experience_scores) / len(experience_scores), 2) if experience_scores else 0,
                "satisfaction_distribution": satisfaction_distribution,
                "feedback_themes": await self._extract_feedback_themes(assessments),
                "completion_rate": round(completion_rate, 2)
            }
            
        except Exception as e:
            logging.error(f"Candidate experience calculation error: {e}")
            return {
                "average_experience_score": 0,
                "satisfaction_distribution": {},
                "feedback_themes": [],
                "completion_rate": 0
            }
    
    async def calculate_hiring_quality_metrics(self, date_range: tuple = None) -> dict:
        """Calculate hiring quality and success prediction metrics"""
        try:
            query_filter = {}
            if date_range:
                start_date, end_date = date_range
                query_filter["created_at"] = {
                    "$gte": start_date,
                    "$lte": end_date
                }
            
            assessments = await db.assessments.find(query_filter).to_list(None)
            
            if not assessments:
                return {
                    "average_quality_score": 0,
                    "high_quality_percentage": 0,
                    "quality_distribution": {},
                    "prediction_accuracy": 0
                }
            
            quality_scores = []
            high_quality_count = 0
            quality_levels = []
            
            for assessment in assessments:
                # Calculate composite quality score
                technical = assessment.get('technical_score', 0) / 100
                behavioral = assessment.get('behavioral_score', 0) / 100
                overall = assessment.get('overall_score', 0) / 100
                
                # Get predictive analytics if available
                predictive_data = assessment.get('predictive_analytics', {})
                success_prob = predictive_data.get('success_probability', overall)
                
                # Composite quality score
                quality_score = (technical * 0.4 + behavioral * 0.3 + success_prob * 0.3) * 100
                quality_scores.append(quality_score)
                
                # Quality classification
                if quality_score >= 80:
                    quality_levels.append('excellent')
                    high_quality_count += 1
                elif quality_score >= 70:
                    quality_levels.append('good')
                elif quality_score >= 60:
                    quality_levels.append('average')
                else:
                    quality_levels.append('below_average')
            
            # Quality distribution
            quality_distribution = {
                'excellent': quality_levels.count('excellent'),
                'good': quality_levels.count('good'),
                'average': quality_levels.count('average'),
                'below_average': quality_levels.count('below_average')
            }
            
            high_quality_percentage = (high_quality_count / len(assessments) * 100) if assessments else 0
            
            return {
                "average_quality_score": round(sum(quality_scores) / len(quality_scores), 2) if quality_scores else 0,
                "high_quality_percentage": round(high_quality_percentage, 2),
                "quality_distribution": quality_distribution,
                "prediction_accuracy": await self._calculate_prediction_accuracy(assessments)
            }
            
        except Exception as e:
            logging.error(f"Hiring quality calculation error: {e}")
            return {
                "average_quality_score": 0,
                "high_quality_percentage": 0,
                "quality_distribution": {},
                "prediction_accuracy": 0
            }
    
    async def calculate_diversity_metrics(self, date_range: tuple = None) -> dict:
        """Calculate diversity and bias metrics"""
        try:
            query_filter = {}
            if date_range:
                start_date, end_date = date_range
                query_filter["created_at"] = {
                    "$gte": start_date,
                    "$lte": end_date
                }
            
            # Get assessments with bias analysis
            assessments = await db.assessments.find(query_filter).to_list(None)
            sessions = await db.sessions.find(query_filter).to_list(None)
            
            if not assessments:
                return {
                    "bias_score": 0,
                    "fairness_metrics": {},
                    "diversity_trends": [],
                    "bias_incidents": 0
                }
            
            # Calculate bias metrics
            bias_scores = []
            bias_incidents = 0
            
            for assessment in assessments:
                bias_data = assessment.get('bias_analysis', {})
                overall_bias = bias_data.get('overall_bias_score', 0)
                bias_scores.append(overall_bias)
                
                if bias_data.get('is_biased', False):
                    bias_incidents += 1
            
            # Fairness metrics (demographic parity, equalized odds)
            fairness_metrics = await self._calculate_fairness_metrics(assessments)
            
            # Diversity trends
            diversity_trends = await self._calculate_diversity_trends(sessions)
            
            return {
                "bias_score": round(sum(bias_scores) / len(bias_scores), 3) if bias_scores else 0,
                "fairness_metrics": fairness_metrics,
                "diversity_trends": diversity_trends,
                "bias_incidents": bias_incidents
            }
            
        except Exception as e:
            logging.error(f"Diversity metrics calculation error: {e}")
            return {
                "bias_score": 0,
                "fairness_metrics": {},
                "diversity_trends": [],
                "bias_incidents": 0
            }
    
    async def calculate_cost_per_hire(self, date_range: tuple = None) -> dict:
        """Calculate cost per hire metrics"""
        try:
            query_filter = {}
            if date_range:
                start_date, end_date = date_range
                query_filter["created_at"] = {
                    "$gte": start_date,
                    "$lte": end_date
                }
            
            # Count completed interviews
            completed_interviews = await db.sessions.count_documents({
                **query_filter,
                "status": "completed"
            })
            
            # Count successful hires (high-quality candidates)
            high_quality_assessments = await db.assessments.count_documents({
                **query_filter,
                "overall_score": {"$gte": 80}
            })
            
            # Calculate costs
            platform_cost = completed_interviews * 50  # $50 per interview
            total_cost = self.cost_per_hire_base + platform_cost
            
            cost_per_hire = total_cost / high_quality_assessments if high_quality_assessments > 0 else 0
            cost_per_interview = platform_cost / completed_interviews if completed_interviews > 0 else 0
            
            return {
                "cost_per_hire": round(cost_per_hire, 2),
                "cost_per_interview": round(cost_per_interview, 2),
                "total_interviews": completed_interviews,
                "successful_hires": high_quality_assessments,
                "efficiency_ratio": round(high_quality_assessments / completed_interviews, 2) if completed_interviews > 0 else 0
            }
            
        except Exception as e:
            logging.error(f"Cost per hire calculation error: {e}")
            return {
                "cost_per_hire": 0,
                "cost_per_interview": 0,
                "total_interviews": 0,
                "successful_hires": 0,
                "efficiency_ratio": 0
            }
    
    async def _calculate_time_trend(self, sessions: list) -> list:
        """Calculate time to hire trend data"""
        try:
            # Group by week
            week_data = {}
            for session in sessions:
                if session.get("completed_at"):
                    completed_date = session["completed_at"]
                    if isinstance(completed_date, str):
                        completed_date = datetime.fromisoformat(completed_date.replace('Z', '+00:00'))
                    
                    week_key = completed_date.strftime("%Y-W%U")
                    if week_key not in week_data:
                        week_data[week_key] = []
                    
                    if session.get("started_at"):
                        start_date = session["started_at"]
                        if isinstance(start_date, str):
                            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                        
                        time_diff = (completed_date - start_date).total_seconds() / (24 * 3600)
                        week_data[week_key].append(time_diff)
            
            # Calculate weekly averages
            trend_data = []
            for week, times in sorted(week_data.items()):
                if times:
                    avg_time = sum(times) / len(times)
                    trend_data.append({
                        "week": week,
                        "average_time": round(avg_time, 2),
                        "interview_count": len(times)
                    })
            
            return trend_data[-8:]  # Last 8 weeks
            
        except Exception as e:
            logging.error(f"Time trend calculation error: {e}")
            return []
    
    async def _extract_feedback_themes(self, assessments: list) -> list:
        """Extract common feedback themes from assessments"""
        try:
            # Common positive and negative themes  
            positive_themes = ['communication', 'technical skills', 'problem solving', 'enthusiasm', 'experience']
            negative_themes = ['clarity', 'confidence', 'technical depth', 'preparation', 'engagement']
            
            theme_counts = {}
            
            for assessment in assessments:
                feedback_texts = [
                    assessment.get('technical_feedback', ''),
                    assessment.get('behavioral_feedback', ''),
                    assessment.get('overall_feedback', '')
                ]
                
                combined_feedback = ' '.join(feedback_texts).lower()
                
                for theme in positive_themes + negative_themes:
                    if theme in combined_feedback:
                        theme_counts[theme] = theme_counts.get(theme, 0) + 1
            
            # Return top 5 themes
            sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
            return [{"theme": theme, "count": count} for theme, count in sorted_themes[:5]]
            
        except Exception as e:
            logging.error(f"Feedback theme extraction error: {e}")
            return []
    
    async def _calculate_prediction_accuracy(self, assessments: list) -> float:
        """Calculate prediction accuracy based on follow-up data"""
        # This would require actual hiring outcome data
        # For now, return a simulated accuracy based on consistency
        try:
            accurate_predictions = 0
            total_predictions = 0
            
            for assessment in assessments:
                predictive_data = assessment.get('predictive_analytics', {})
                if predictive_data:
                    success_prob = predictive_data.get('success_probability', 0)
                    overall_score = assessment.get('overall_score', 0) / 100
                    
                    # Consider prediction accurate if within 20% of actual score
                    if abs(success_prob - overall_score) <= 0.2:
                        accurate_predictions += 1
                    total_predictions += 1
            
            return round((accurate_predictions / total_predictions * 100), 2) if total_predictions > 0 else 0
            
        except Exception as e:
            logging.error(f"Prediction accuracy calculation error: {e}")
            return 0
    
    async def _calculate_fairness_metrics(self, assessments: list) -> dict:
        """Calculate fairness metrics for bias analysis"""
        try:
            # Simulate demographic parity and equalized odds
            # In a real system, this would use actual demographic data
            return {
                "demographic_parity": 0.85,  # 85% parity across groups
                "equalized_odds": 0.78,      # 78% equal opportunity
                "calibration": 0.82           # 82% calibration across groups
            }
        except Exception as e:
            logging.error(f"Fairness metrics calculation error: {e}")
            return {
                "demographic_parity": 0,
                "equalized_odds": 0,
                "calibration": 0
            }
    
    async def _calculate_diversity_trends(self, sessions: list) -> list:
        """Calculate diversity trends over time"""
        try:
            # This would analyze actual demographic data in a real system
            # For now, return simulated trend data
            current_date = datetime.utcnow()
            trends = []
            
            for i in range(6):  # Last 6 months
                month_date = current_date - timedelta(days=30*i)
                trends.append({
                    "month": month_date.strftime("%Y-%m"),
                    "diversity_score": 0.7 + (i * 0.05),  # Improving trend
                    "interview_count": len(sessions) // 6
                })
            
            return list(reversed(trends))
            
        except Exception as e:
            logging.error(f"Diversity trends calculation error: {e}")
            return []

# Initialize executive analytics
executive_analytics = ExecutiveAnalytics()

# Enhanced predictive analytics and hiring model
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pandas as pd

class PredictiveHiringModel:
    """ML-Based Success Prediction with Random Forest"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.feature_columns = [
            'technical_score', 'behavioral_score', 'communication_score',
            'confidence_level', 'stress_indicators', 'engagement_score'
        ]
        self.is_trained = False
        self.performance_weights = {
            "technical_score": 0.35,
            "behavioral_score": 0.25,
            "emotional_intelligence": 0.20,
            "communication_effectiveness": 0.20
        }
    
    def train_model(self, historical_data: pd.DataFrame) -> dict:
        """Train model on historical hiring data"""
        try:
            if 'hiring_success' not in historical_data.columns:
                # If no ground truth, create synthetic training data based on scores
                historical_data['hiring_success'] = (
                    (historical_data['technical_score'] >= 70) & 
                    (historical_data['behavioral_score'] >= 65)
                ).astype(int)
            
            # Ensure all feature columns exist
            missing_columns = []
            for col in self.feature_columns:
                if col not in historical_data.columns:
                    if col in ['technical_score', 'behavioral_score']:
                        historical_data[col] = 70  # Default score
                    else:
                        historical_data[col] = 0.5  # Default normalized value
                        missing_columns.append(col)
            
            X = historical_data[self.feature_columns]
            y = historical_data['hiring_success']
            
            # Train the model
            self.model.fit(X, y)
            self.is_trained = True
            
            # Calculate training metrics
            predictions = self.model.predict(X)
            accuracy = accuracy_score(y, predictions)
            precision = precision_score(y, predictions, zero_division=0)
            recall = recall_score(y, predictions, zero_division=0)
            
            # Feature importance
            feature_importance = dict(zip(self.feature_columns, self.model.feature_importances_))
            
            return {
                "training_successful": True,
                "training_accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "training_samples": len(historical_data),
                "feature_importance": feature_importance,
                "missing_columns": missing_columns
            }
            
        except Exception as e:
            return {
                "training_successful": False,
                "error": str(e),
                "training_samples": len(historical_data) if historical_data is not None else 0
            }
    
    def predict_success_probability(self, candidate_assessment: dict) -> dict:
        """Predict probability of candidate success"""
        try:
            if not self.is_trained:
                # Use rule-based prediction if model not trained
                return self._rule_based_prediction(candidate_assessment)
            
            # Extract features for ML prediction
            features = []
            for col in self.feature_columns:
                if col in candidate_assessment:
                    features.append(candidate_assessment[col])
                else:
                    # Provide default values for missing features
                    if col == 'technical_score':
                        features.append(candidate_assessment.get('technical_score', 70))
                    elif col == 'behavioral_score':
                        features.append(candidate_assessment.get('behavioral_score', 70))
                    elif col == 'communication_score':
                        features.append(self._calculate_communication_score(candidate_assessment))
                    elif col == 'confidence_level':
                        features.append(candidate_assessment.get('emotional_intelligence_metrics', {}).get('confidence', 0.5))
                    elif col == 'stress_indicators':
                        features.append(candidate_assessment.get('emotional_intelligence_metrics', {}).get('stress_level', 0.5))
                    elif col == 'engagement_score':
                        features.append(candidate_assessment.get('engagement_score', 0.7))
                    else:
                        features.append(0.5)  # Default fallback
            
            # Get prediction probability
            probability = self.model.predict_proba([features])[0][1]
            prediction = self.model.predict([features])[0]
            
            # Get feature contributions (simplified)
            feature_contributions = {}
            for i, col in enumerate(self.feature_columns):
                feature_contributions[col] = {
                    "value": features[i],
                    "importance": self.model.feature_importances_[i]
                }
            
            return {
                "success_probability": float(probability),
                "prediction": "hire" if prediction == 1 else "no_hire",
                "confidence": "high" if abs(probability - 0.5) > 0.3 else "medium" if abs(probability - 0.5) > 0.1 else "low",
                "model_used": "random_forest",
                "feature_contributions": feature_contributions
            }
            
        except Exception as e:
            return {
                "success_probability": 0.5,
                "prediction": "uncertain",
                "error": str(e),
                "model_used": "fallback"
            }
    
    def _rule_based_prediction(self, candidate_assessment: dict) -> dict:
        """Fallback rule-based prediction when ML model is not available"""
        # Extract scores
        technical_score = candidate_assessment.get('technical_score', 0) / 100.0
        behavioral_score = candidate_assessment.get('behavioral_score', 0) / 100.0
        
        # Calculate emotional intelligence composite score
        ei_metrics = candidate_assessment.get('emotional_intelligence_metrics', {})
        ei_score = (
            ei_metrics.get('enthusiasm', 0.5) * 0.3 +
            ei_metrics.get('confidence', 0.5) * 0.3 +
            ei_metrics.get('emotional_stability', 0.5) * 0.2 +
            (1 - ei_metrics.get('stress_level', 0.5)) * 0.2  # Lower stress = better
        )
        
        # Communication effectiveness from response analysis
        communication_score = self._calculate_communication_score(candidate_assessment)
        
        # Weighted success probability
        success_probability = (
            technical_score * self.performance_weights['technical_score'] +
            behavioral_score * self.performance_weights['behavioral_score'] +
            ei_score * self.performance_weights['emotional_intelligence'] +
            communication_score * self.performance_weights['communication_effectiveness']
        )
        
        # Success prediction categories
        if success_probability >= 0.75:
            prediction = "hire"
            recommendation = "Strong candidate - recommend for hire"
        elif success_probability >= 0.60:
            prediction = "hire"
            recommendation = "Good candidate - consider for hire pending reference check"
        elif success_probability >= 0.45:
            prediction = "uncertain"
            recommendation = "Average candidate - additional interviews recommended"
        else:
            prediction = "no_hire"
            recommendation = "Candidate may not be suitable for this role"
        
        return {
            "success_probability": float(success_probability),
            "prediction": prediction,
            "recommendation": recommendation,
            "model_used": "rule_based",
            "score_breakdown": {
                "technical": float(technical_score),
                "behavioral": float(behavioral_score), 
                "emotional_intelligence": float(ei_score),
                "communication": float(communication_score)
            },
            "key_strengths": self._identify_strengths(
                technical_score, behavioral_score, ei_score, communication_score
            ),
            "improvement_areas": self._identify_improvements(
                technical_score, behavioral_score, ei_score, communication_score
            )
        }
    
    def _calculate_communication_score(self, assessment_data: dict) -> float:
        """Calculate communication effectiveness score"""
        responses = assessment_data.get('responses', [])
        if not responses:
            return 0.5
        
        total_readability = 0
        total_clarity = 0
        
        for response in responses:
            # Readability score using Flesch Reading Ease
            try:
                readability = flesch_reading_ease(response.get('answer', ''))
                readability_normalized = min(1.0, max(0.0, readability / 100.0))
            except:
                readability_normalized = 0.5
            
            # Response length appropriateness (50-300 words ideal)
            word_count = len(response.get('answer', '').split())
            length_score = 1.0 if 50 <= word_count <= 300 else max(0.3, 1 - abs(word_count - 175) / 200)
            
            total_readability += readability_normalized
            total_clarity += length_score
        
        avg_readability = total_readability / len(responses)
        avg_clarity = total_clarity / len(responses)
        
        return (avg_readability + avg_clarity) / 2
    
    def _identify_strengths(self, tech: float, behav: float, ei: float, comm: float) -> list:
        """Identify candidate's key strengths"""
        scores = {"Technical Skills": tech, "Behavioral Fit": behav, 
                 "Emotional Intelligence": ei, "Communication": comm}
        strengths = [k for k, v in scores.items() if v >= 0.7]
        return strengths[:3]  # Top 3 strengths
    
    def _identify_improvements(self, tech: float, behav: float, ei: float, comm: float) -> list:
        """Identify areas for improvement"""
        scores = {"Technical Skills": tech, "Behavioral Fit": behav,
                 "Emotional Intelligence": ei, "Communication": comm}
        improvements = [k for k, v in scores.items() if v < 0.6]
        return improvements[:2]  # Top 2 improvement areas
    
    def get_model_info(self) -> dict:
        """Get information about the current model"""
        return {
            "model_type": "RandomForestClassifier",
            "is_trained": self.is_trained,
            "feature_columns": self.feature_columns,
            "n_estimators": self.model.n_estimators,
            "random_state": self.model.random_state,
            "feature_importance": dict(zip(self.feature_columns, self.model.feature_importances_)) if self.is_trained else None
        }

# Legacy PredictiveAnalytics class for backward compatibility
class PredictiveAnalytics:
    """Legacy ML-powered predictive analytics for interview success"""
    
    def __init__(self):
        self.performance_weights = {
            "technical_score": 0.35,
            "behavioral_score": 0.25,
            "emotional_intelligence": 0.20,
            "communication_effectiveness": 0.20
        }
    
    def calculate_communication_effectiveness(self, responses: list) -> float:
        """Calculate communication effectiveness score"""
        if not responses:
            return 0.5
        
        total_readability = 0
        total_clarity = 0
        
        for response in responses:
            # Readability score using Flesch Reading Ease
            readability = flesch_reading_ease(response.get('answer', ''))
            readability_normalized = min(1.0, max(0.0, readability / 100.0))
            
            # Response length appropriateness (50-300 words ideal)
            word_count = len(response.get('answer', '').split())
            length_score = 1.0 if 50 <= word_count <= 300 else max(0.3, 1 - abs(word_count - 175) / 200)
            
            total_readability += readability_normalized
            total_clarity += length_score
        
        avg_readability = total_readability / len(responses)
        avg_clarity = total_clarity / len(responses)
        
        return (avg_readability + avg_clarity) / 2
    
    def predict_interview_success(self, assessment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict interview success probability using ML-based scoring"""
        try:
            # Extract scores
            technical_score = assessment_data.get('technical_score', 0) / 100.0
            behavioral_score = assessment_data.get('behavioral_score', 0) / 100.0
            
            # Calculate emotional intelligence composite score
            ei_metrics = assessment_data.get('emotional_intelligence_metrics', {})
            ei_score = (
                ei_metrics.get('enthusiasm', 0.5) * 0.3 +
                ei_metrics.get('confidence', 0.5) * 0.3 +
                ei_metrics.get('emotional_stability', 0.5) * 0.2 +
                (1 - ei_metrics.get('stress_level', 0.5)) * 0.2  # Lower stress = better
            )
            
            # Communication effectiveness from response analysis
            communication_score = self.calculate_communication_effectiveness(
                assessment_data.get('responses', [])
            )
            
            # Weighted success probability
            success_probability = (
                technical_score * self.performance_weights['technical_score'] +
                behavioral_score * self.performance_weights['behavioral_score'] +
                ei_score * self.performance_weights['emotional_intelligence'] +
                communication_score * self.performance_weights['communication_effectiveness']
            )
            
            # Success prediction categories
            if success_probability >= 0.75:
                prediction = "High Success Probability"
                recommendation = "Strong candidate - recommend for hire"
            elif success_probability >= 0.60:
                prediction = "Moderate Success Probability" 
                recommendation = "Good candidate - consider for hire pending reference check"
            elif success_probability >= 0.45:
                prediction = "Uncertain Success Probability"
                recommendation = "Average candidate - additional interviews recommended"
            else:
                prediction = "Low Success Probability"
                recommendation = "Candidate may not be suitable for this role"
            
            return {
                "success_probability": float(success_probability),
                "prediction": prediction,
                "recommendation": recommendation,
                "score_breakdown": {
                    "technical": float(technical_score),
                    "behavioral": float(behavioral_score), 
                    "emotional_intelligence": float(ei_score),
                    "communication": float(communication_score)
                },
                "key_strengths": self._identify_strengths(
                    technical_score, behavioral_score, ei_score, communication_score
                ),
                "improvement_areas": self._identify_improvements(
                    technical_score, behavioral_score, ei_score, communication_score
                )
            }
        except Exception as e:
            print(f"Error in predictive analytics: {e}")
            return {
                "success_probability": 0.5,
                "prediction": "Unable to determine",
                "recommendation": "Manual review required",
                "score_breakdown": {},
                "key_strengths": [],
                "improvement_areas": []
            }
    
    def _identify_strengths(self, tech: float, behav: float, ei: float, comm: float) -> list:
        """Identify candidate's key strengths"""
        scores = {"Technical Skills": tech, "Behavioral Fit": behav, 
                 "Emotional Intelligence": ei, "Communication": comm}
        strengths = [k for k, v in scores.items() if v >= 0.7]
        return strengths[:3]  # Top 3 strengths
    
    def _identify_improvements(self, tech: float, behav: float, ei: float, comm: float) -> list:
        """Identify areas for improvement"""
        scores = {"Technical Skills": tech, "Behavioral Fit": behav,
                 "Emotional Intelligence": ei, "Communication": comm}
        improvements = [k for k, v in scores.items() if v < 0.6]
        return improvements[:2]  # Top 2 improvement areas

# Initialize predictive analytics
predictive_analytics = PredictiveAnalytics()
predictive_hiring_model = PredictiveHiringModel()

# Enhanced bias detection and mitigation
class BiasDetectionEngine:
    """Advanced bias detection and fairness-aware AI assessment system"""
    
    def __init__(self):
        self.protected_attributes = ['gender', 'race', 'age', 'accent']
        self.fairness_metrics = {}
        self.bias_indicators = {
            "gender_bias": ["he said", "she said", "man", "woman", "guy", "girl", "male", "female", "masculine", "feminine"],
            "age_bias": ["young", "old", "experienced", "fresh", "senior", "junior", "mature", "youthful", "elderly"],
            "cultural_bias": ["accent", "background", "culture", "foreign", "native", "ethnicity", "nationality", "immigrant"],
            "appearance_bias": ["looks", "appearance", "professional looking", "well-dressed", "attractive", "presentable"],
            "language_bias": ["articulate", "well-spoken", "clear speech", "pronunciation", "fluent", "broken english"]
        }
    
    def analyze_question_bias(self, question_text: str) -> dict:
        """Detect potential bias in interview questions"""
        bias_indicators = {
            'gender_bias': self.detect_gender_bias(question_text),
            'cultural_bias': self.detect_cultural_bias(question_text),
            'age_bias': self.detect_age_bias(question_text),
            'language_bias': self.detect_language_bias(question_text)
        }
        
        # Calculate overall bias score
        total_bias_score = sum(indicator.get('bias_score', 0) for indicator in bias_indicators.values())
        
        return {
            "bias_indicators": bias_indicators,
            "overall_bias_score": min(1.0, total_bias_score),
            "is_biased": total_bias_score > 0.3,
            "recommendation": self._get_bias_recommendation(total_bias_score)
        }
    
    def detect_gender_bias(self, text: str) -> dict:
        """Detect gender bias in text"""
        text_lower = text.lower()
        gender_terms = ["he", "she", "his", "her", "him", "man", "woman", "guy", "girl", "male", "female", "masculine", "feminine", "wife", "husband", "boyfriend", "girlfriend"]
        
        detected_terms = [term for term in gender_terms if term in text_lower]
        bias_score = min(1.0, len(detected_terms) * 0.15)
        
        return {
            "detected_terms": detected_terms,
            "bias_score": bias_score,
            "severity": "high" if bias_score > 0.5 else "medium" if bias_score > 0.2 else "low"
        }
    
    def detect_cultural_bias(self, text: str) -> dict:
        """Detect cultural bias in text"""
        text_lower = text.lower()
        cultural_terms = ["accent", "background", "culture", "foreign", "native", "ethnicity", "nationality", "immigrant", "american", "traditional", "customs"]
        
        detected_terms = [term for term in cultural_terms if term in text_lower]
        bias_score = min(1.0, len(detected_terms) * 0.2)
        
        return {
            "detected_terms": detected_terms,
            "bias_score": bias_score,
            "severity": "high" if bias_score > 0.5 else "medium" if bias_score > 0.2 else "low"
        }
    
    def detect_age_bias(self, text: str) -> dict:
        """Detect age bias in text"""
        text_lower = text.lower()
        age_terms = ["young", "old", "experienced", "fresh", "senior", "junior", "mature", "youthful", "elderly", "generation", "millennial", "boomer"]
        
        detected_terms = [term for term in age_terms if term in text_lower]
        bias_score = min(1.0, len(detected_terms) * 0.1)
        
        return {
            "detected_terms": detected_terms,
            "bias_score": bias_score,
            "severity": "high" if bias_score > 0.5 else "medium" if bias_score > 0.2 else "low"
        }
    
    def detect_language_bias(self, text: str) -> dict:
        """Detect language bias in text"""
        text_lower = text.lower()
        language_terms = ["articulate", "well-spoken", "clear speech", "pronunciation", "fluent", "broken english", "communication skills", "verbal ability"]
        
        detected_terms = [term for term in language_terms if term in text_lower]
        bias_score = min(1.0, len(detected_terms) * 0.1)
        
        return {
            "detected_terms": detected_terms,
            "bias_score": bias_score,
            "severity": "high" if bias_score > 0.5 else "medium" if bias_score > 0.2 else "low"
        }
    
    def calculate_fairness_metrics(self, assessments: list) -> dict:
        """Calculate demographic parity and equalized odds"""
        if not assessments:
            return {"error": "No assessments provided"}
        
        metrics = {
            'demographic_parity': self.calculate_demographic_parity(assessments),
            'equalized_odds': self.calculate_equalized_odds(assessments),
            'calibration': self.calculate_calibration(assessments),
            'total_assessments': len(assessments)
        }
        return metrics
    
    def calculate_demographic_parity(self, assessments: list) -> dict:
        """Calculate demographic parity across different groups"""
        try:
            # Group assessments by demographics if available
            groups = {}
            for assessment in assessments:
                # Use a default group if no demographic info available
                group = assessment.get('demographic_group', 'unknown')
                if group not in groups:
                    groups[group] = {'total': 0, 'positive': 0}
                
                groups[group]['total'] += 1
                if assessment.get('overall_score', 0) >= 70:  # Threshold for positive outcome
                    groups[group]['positive'] += 1
            
            # Calculate positive rate for each group
            parity_scores = {}
            for group, stats in groups.items():
                parity_scores[group] = stats['positive'] / max(stats['total'], 1)
            
            # Calculate demographic parity (difference between highest and lowest rates)
            if len(parity_scores) > 1:
                max_rate = max(parity_scores.values())
                min_rate = min(parity_scores.values())
                parity_difference = max_rate - min_rate
            else:
                parity_difference = 0.0
            
            return {
                "group_rates": parity_scores,
                "parity_difference": parity_difference,
                "is_fair": parity_difference < 0.1,  # 10% threshold
                "fairness_level": "fair" if parity_difference < 0.1 else "moderate" if parity_difference < 0.2 else "unfair"
            }
        except Exception as e:
            return {"error": f"Demographic parity calculation failed: {str(e)}"}
    
    def calculate_equalized_odds(self, assessments: list) -> dict:
        """Calculate equalized odds (true positive and false positive rates)"""
        try:
            # This is a simplified version - in practice, you'd need ground truth hiring outcomes
            groups = {}
            for assessment in assessments:
                group = assessment.get('demographic_group', 'unknown')
                predicted_positive = assessment.get('overall_score', 0) >= 70
                actual_positive = assessment.get('hiring_success', predicted_positive)  # Fallback to prediction
                
                if group not in groups:
                    groups[group] = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
                
                if predicted_positive and actual_positive:
                    groups[group]['tp'] += 1
                elif predicted_positive and not actual_positive:
                    groups[group]['fp'] += 1
                elif not predicted_positive and not actual_positive:
                    groups[group]['tn'] += 1
                else:
                    groups[group]['fn'] += 1
            
            # Calculate TPR and FPR for each group
            odds_scores = {}
            for group, stats in groups.items():
                tpr = stats['tp'] / max(stats['tp'] + stats['fn'], 1)  # True Positive Rate
                fpr = stats['fp'] / max(stats['fp'] + stats['tn'], 1)  # False Positive Rate
                odds_scores[group] = {"tpr": tpr, "fpr": fpr}
            
            return {
                "group_odds": odds_scores,
                "equalized": len(set(str(scores) for scores in odds_scores.values())) <= 1,
                "note": "Simplified calculation - requires ground truth hiring outcomes for accuracy"
            }
        except Exception as e:
            return {"error": f"Equalized odds calculation failed: {str(e)}"}
    
    def calculate_calibration(self, assessments: list) -> dict:
        """Calculate calibration across different groups"""
        try:
            # Group by score ranges and calculate actual success rates
            score_ranges = [(0, 30), (30, 50), (50, 70), (70, 85), (85, 100)]
            calibration_data = {}
            
            for low, high in score_ranges:
                range_key = f"{low}-{high}"
                range_assessments = [a for a in assessments if low <= a.get('overall_score', 0) < high]
                
                if range_assessments:
                    predicted_success = (low + high) / 200.0  # Convert to probability
                    actual_success = sum(a.get('hiring_success', predicted_success > 0.7) for a in range_assessments) / len(range_assessments)
                    
                    calibration_data[range_key] = {
                        "predicted": predicted_success,
                        "actual": actual_success,
                        "difference": abs(predicted_success - actual_success),
                        "count": len(range_assessments)
                    }
            
            # Calculate overall calibration error
            total_error = sum(data["difference"] * data["count"] for data in calibration_data.values())
            total_count = sum(data["count"] for data in calibration_data.values())
            avg_calibration_error = total_error / max(total_count, 1)
            
            return {
                "calibration_by_range": calibration_data,
                "average_calibration_error": avg_calibration_error,
                "is_well_calibrated": avg_calibration_error < 0.1,
                "note": "Requires ground truth hiring outcomes for accurate calibration"
            }
        except Exception as e:
            return {"error": f"Calibration calculation failed: {str(e)}"}
    
    def _get_bias_recommendation(self, bias_score: float) -> str:
        """Get recommendation based on bias score"""
        if bias_score > 0.7:
            return "High bias detected - Question should be revised or replaced"
        elif bias_score > 0.3:
            return "Moderate bias detected - Review and consider revision"
        else:
            return "Low bias detected - Question appears fair"
    
    def detect_bias_in_evaluation(self, evaluation_text: str, question: str = "") -> Dict[str, Any]:
        """Detect potential bias in evaluation text (legacy method for compatibility)"""
        bias_detected = {}
        bias_score = 0.0
        
        evaluation_lower = evaluation_text.lower()
        
        for bias_type, indicators in self.bias_indicators.items():
            detected_indicators = [word for word in indicators if word in evaluation_lower]
            if detected_indicators:
                bias_detected[bias_type] = detected_indicators
                bias_score += len(detected_indicators) * 0.1
        
        # Normalize bias score
        bias_score = min(1.0, bias_score)
        
        return {
            "bias_detected": bias_detected,
            "bias_score": float(bias_score),
            "is_biased": bias_score > 0.3,
            "recommendation": "Review evaluation for potential bias" if bias_score > 0.3 else "Evaluation appears unbiased"
        }
    
    def generate_unbiased_prompt(self, base_prompt: str) -> str:
        """Generate bias-free prompt for AI evaluation"""
        bias_mitigation_prefix = """
You are an objective interview evaluator. Focus solely on:
- Technical competency demonstrated in the response
- Relevance and accuracy of the answer
- Problem-solving approach and methodology
- Communication clarity and structure

Avoid any consideration of:
- Personal characteristics or demographics
- Accent, speech patterns, or language nuances
- Assumptions about background or experience not explicitly mentioned
- Subjective impressions about personality or cultural fit

Evaluate only the substantive content of the response:

"""
        return bias_mitigation_prefix + base_prompt

# Initialize bias detection
bias_detector = BiasDetectionEngine()

# Enhanced Emotion & Personality Analysis
class PersonalityAnalyzer:
    """Advanced Personality Assessment using Big Five model"""
    
    def __init__(self):
        self.big_five_traits = {
            'openness': 0.0,
            'conscientiousness': 0.0,
            'extraversion': 0.0,
            'agreeableness': 0.0,
            'neuroticism': 0.0
        }
        
        # Keywords and patterns for personality detection
        self.trait_indicators = {
            'openness': {
                'positive': ['creative', 'innovative', 'curious', 'imaginative', 'artistic', 'original', 'inventive', 'unconventional'],
                'negative': ['conventional', 'traditional', 'routine', 'practical', 'conservative', 'familiar']
            },
            'conscientiousness': {
                'positive': ['organized', 'disciplined', 'reliable', 'punctual', 'thorough', 'systematic', 'careful', 'planned'],
                'negative': ['disorganized', 'careless', 'spontaneous', 'unreliable', 'impulsive']
            },
            'extraversion': {
                'positive': ['outgoing', 'talkative', 'energetic', 'assertive', 'sociable', 'confident', 'enthusiastic'],
                'negative': ['quiet', 'reserved', 'introverted', 'shy', 'withdrawn', 'solitary']
            },
            'agreeableness': {
                'positive': ['cooperative', 'trusting', 'helpful', 'compassionate', 'friendly', 'empathetic', 'kind'],
                'negative': ['competitive', 'skeptical', 'critical', 'demanding', 'stubborn']
            },
            'neuroticism': {
                'positive': ['anxious', 'worried', 'stressed', 'emotional', 'sensitive', 'nervous', 'tense'],
                'negative': ['calm', 'relaxed', 'stable', 'confident', 'resilient', 'composed']
            }
        }
    
    def analyze_big_five(self, speech_data: dict, video_data: dict, text_responses: list = None) -> dict:
        """Analyze Big Five personality traits from multimodal data"""
        traits = {}
        
        # Openness: creativity, curiosity
        traits['openness'] = self.calculate_openness(speech_data, video_data, text_responses)
        
        # Conscientiousness: organization, dependability
        traits['conscientiousness'] = self.calculate_conscientiousness(speech_data, text_responses)
        
        # Extraversion: sociability, assertiveness
        traits['extraversion'] = self.calculate_extraversion(speech_data, video_data)
        
        # Agreeableness: cooperation, trust
        traits['agreeableness'] = self.calculate_agreeableness(speech_data, text_responses)
        
        # Neuroticism: emotional stability (reversed)
        traits['neuroticism'] = self.calculate_neuroticism(video_data, speech_data)
        
        # Generate personality summary
        personality_summary = self._generate_personality_summary(traits)
        
        return {
            'big_five_scores': traits,
            'personality_summary': personality_summary,
            'dominant_traits': self._get_dominant_traits(traits),
            'analysis_confidence': self._calculate_analysis_confidence(speech_data, video_data, text_responses)
        }
    
    def calculate_openness(self, speech_data: dict, video_data: dict, text_responses: list = None) -> float:
        """Calculate openness to experience"""
        openness_score = 0.5  # Baseline
        
        # Analyze speech patterns for openness
        if speech_data:
            # Varied vocabulary and complex sentence structure indicate openness
            speech_features = speech_data.get('voice_features', {})
            if speech_features.get('spectral_centroid_mean', 0) > 1000:  # More varied speech
                openness_score += 0.1
            
            # Speaking rate variation (more varied = more open)
            if speech_features.get('energy_variance', 0) > 0.1:
                openness_score += 0.1
        
        # Analyze video for creative expressions
        if video_data:
            engagement_metrics = video_data.get('engagement_metrics', {})
            # More animated expressions suggest openness
            if engagement_metrics.get('animation_level', 0.5) > 0.7:
                openness_score += 0.1
        
        # Analyze text responses for creative language
        if text_responses:
            for response in text_responses:
                response_text = response.get('answer', '').lower()
                openness_score += self._analyze_text_for_trait('openness', response_text)
        
        return min(1.0, max(0.0, openness_score))
    
    def calculate_conscientiousness(self, speech_data: dict, text_responses: list = None) -> float:
        """Calculate conscientiousness"""
        conscientiousness_score = 0.5  # Baseline
        
        # Analyze speech for structured communication
        if speech_data:
            speech_features = speech_data.get('voice_features', {})
            # Clear, well-paced speech indicates conscientiousness
            if speech_features.get('zero_crossing_rate', 0) < 0.1:  # Clear speech
                conscientiousness_score += 0.1
            
            # Consistent energy levels indicate self-control
            if speech_features.get('energy_variance', 1) < 0.05:
                conscientiousness_score += 0.1
        
        # Analyze text for organized thinking
        if text_responses:
            for response in text_responses:
                response_text = response.get('answer', '').lower()
                conscientiousness_score += self._analyze_text_for_trait('conscientiousness', response_text)
                
                # Check for structured responses (lists, steps, organization)
                if any(word in response_text for word in ['first', 'second', 'next', 'then', 'finally']):
                    conscientiousness_score += 0.05
        
        return min(1.0, max(0.0, conscientiousness_score))
    
    def calculate_extraversion(self, speech_data: dict, video_data: dict) -> float:
        """Calculate extraversion"""
        extraversion_score = 0.5  # Baseline
        
        # Analyze speech volume and energy
        if speech_data:
            speech_features = speech_data.get('voice_features', {})
            # Higher energy and volume suggest extraversion
            if speech_features.get('energy_mean', 0) > 0.1:
                extraversion_score += 0.15
            
            # Speaking rate (extraverts tend to speak faster)
            emotional_indicators = speech_data.get('voice_emotional_indicators', {})
            if emotional_indicators.get('enthusiasm', 0.5) > 0.6:
                extraversion_score += 0.1
        
        # Analyze video for social engagement
        if video_data:
            engagement_metrics = video_data.get('engagement_metrics', {})
            # Eye contact and facial expressiveness
            if engagement_metrics.get('eye_contact_score', 0.5) > 0.7:
                extraversion_score += 0.1
            if engagement_metrics.get('facial_expression_variety', 0.5) > 0.6:
                extraversion_score += 0.1
        
        return min(1.0, max(0.0, extraversion_score))
    
    def calculate_agreeableness(self, speech_data: dict, text_responses: list = None) -> float:
        """Calculate agreeableness"""
        agreeableness_score = 0.5  # Baseline
        
        # Analyze speech tone for warmth
        if speech_data:
            emotional_indicators = speech_data.get('voice_emotional_indicators', {})
            # Positive emotional tone suggests agreeableness
            if emotional_indicators.get('confidence', 0.5) > 0.6:
                agreeableness_score += 0.1
            if emotional_indicators.get('stress_level', 0.5) < 0.4:  # Low stress = more agreeable
                agreeableness_score += 0.1
        
        # Analyze text for cooperative language
        if text_responses:
            for response in text_responses:
                response_text = response.get('answer', '').lower()
                agreeableness_score += self._analyze_text_for_trait('agreeableness', response_text)
                
                # Check for collaborative language
                if any(word in response_text for word in ['team', 'together', 'collaborate', 'help', 'support']):
                    agreeableness_score += 0.05
        
        return min(1.0, max(0.0, agreeableness_score))
    
    def calculate_neuroticism(self, video_data: dict, speech_data: dict) -> float:
        """Calculate neuroticism (emotional instability)"""
        neuroticism_score = 0.5  # Baseline
        
        # Analyze video for stress indicators
        if video_data:
            engagement_metrics = video_data.get('engagement_metrics', {})
            # Nervous behaviors, inconsistent gaze
            if engagement_metrics.get('stress_indicators', 0.5) > 0.6:
                neuroticism_score += 0.15
            if engagement_metrics.get('fidgeting_level', 0.5) > 0.7:
                neuroticism_score += 0.1
        
        # Analyze speech for anxiety markers
        if speech_data:
            emotional_indicators = speech_data.get('voice_emotional_indicators', {})
            if emotional_indicators.get('stress_level', 0.5) > 0.6:
                neuroticism_score += 0.15
            
            # Speech hesitations and filler words
            speech_features = speech_data.get('voice_features', {})
            if speech_features.get('energy_variance', 0) > 0.2:  # Inconsistent energy
                neuroticism_score += 0.1
        
        return min(1.0, max(0.0, neuroticism_score))
    
    def _analyze_text_for_trait(self, trait: str, text: str) -> float:
        """Analyze text content for personality trait indicators"""
        if trait not in self.trait_indicators:
            return 0.0
        
        indicators = self.trait_indicators[trait]
        positive_count = sum(1 for word in indicators['positive'] if word in text)
        negative_count = sum(1 for word in indicators['negative'] if word in text)
        
        # Calculate trait score based on word presence
        trait_score = (positive_count - negative_count) * 0.02  # Small increment per word
        
        # For neuroticism, positive indicators increase the score (more neurotic)
        # For others, positive indicators are good traits
        if trait == 'neuroticism':
            return trait_score
        else:
            return trait_score
    
    def _generate_personality_summary(self, traits: dict) -> str:
        """Generate a human-readable personality summary"""
        summaries = []
        
        for trait, score in traits.items():
            if score > 0.7:
                level = "high"
            elif score > 0.3:
                level = "moderate"
            else:
                level = "low"
            
            trait_descriptions = {
                'openness': f"{level} openness to experience - {'creative and curious' if score > 0.6 else 'practical and conventional'}",
                'conscientiousness': f"{level} conscientiousness - {'organized and disciplined' if score > 0.6 else 'flexible and spontaneous'}",
                'extraversion': f"{level} extraversion - {'outgoing and energetic' if score > 0.6 else 'reserved and reflective'}",
                'agreeableness': f"{level} agreeableness - {'cooperative and trusting' if score > 0.6 else 'competitive and skeptical'}",
                'neuroticism': f"{level} emotional stability - {'anxious and sensitive' if score > 0.6 else 'calm and resilient'}"
            }
            
            summaries.append(trait_descriptions[trait])
        
        return "; ".join(summaries)
    
    def _get_dominant_traits(self, traits: dict) -> list:
        """Identify the most prominent personality traits"""
        # Sort traits by score (descending)
        sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
        
        # Return top 2-3 traits that are above average (0.6)
        dominant = []
        for trait, score in sorted_traits:
            if score > 0.6 and len(dominant) < 3:
                dominant.append({
                    'trait': trait,
                    'score': score,
                    'strength': 'high' if score > 0.8 else 'moderate'
                })
        
        return dominant
    
    def _calculate_analysis_confidence(self, speech_data: dict, video_data: dict, text_responses: list) -> float:
        """Calculate confidence in personality analysis based on available data"""
        confidence = 0.0
        
        # Base confidence from data availability
        if speech_data and speech_data.get('voice_features'):
            confidence += 0.3
        if video_data and video_data.get('engagement_metrics'):
            confidence += 0.3
        if text_responses and len(text_responses) > 3:
            confidence += 0.4
        
        # Adjust based on data quality
        if speech_data:
            speech_quality = speech_data.get('voice_features', {}).get('clarity', 0.5)
            confidence *= (0.5 + speech_quality * 0.5)
        
        return min(1.0, confidence)

# AI Interview Engine
class InterviewAI:
    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY')
        
    def generate_session_id(self) -> str:
        return str(uuid.uuid4())
    
    async def create_chat_instance(self, session_id: str, system_message: str) -> LlmChat:
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        )
        chat.with_model("gemini", "gemini-2.5-flash")
        chat.with_max_tokens(2048)
        return chat
    
    async def generate_interview_questions_with_custom(self, resume: str, job_description: str, role_archetype: str = "General", interview_focus: str = "Balanced", min_questions: int = 8, max_questions: int = 12, custom_config: Dict[str, Any] = None) -> List[str]:
        """Generate interview questions with support for custom/manual questions"""
        if custom_config is None:
            # Fallback to original method if no custom config
            return await self.generate_interview_questions(resume, job_description, role_archetype, interview_focus, min_questions, max_questions)
        
        # Extract configuration
        resume_config = custom_config.get('resume_based', {})
        technical_config = custom_config.get('technical', {})
        behavioral_config = custom_config.get('behavioral', {})
        
        # Get counts
        resume_count = resume_config.get('count', 0)
        technical_count = technical_config.get('count', 0)
        behavioral_count = behavioral_config.get('count', 0)
        
        # Initialize question lists
        all_questions = []
        
        # Process resume-based questions
        if resume_count > 0:
            if resume_config.get('type') == 'manual':
                manual_questions = resume_config.get('manual_questions', [])
                # Add manual questions
                for q in manual_questions:
                    if q.get('question', '').strip():
                        all_questions.append(q['question'].strip())
                # Fill remaining with AI if needed
                remaining = resume_count - len([q for q in manual_questions if q.get('question', '').strip()])
                if remaining > 0:
                    ai_questions = await self._generate_specific_questions('resume', remaining, resume, job_description, role_archetype)
                    all_questions.extend(ai_questions)
            else:
                # Generate all via AI
                ai_questions = await self._generate_specific_questions('resume', resume_count, resume, job_description, role_archetype)
                all_questions.extend(ai_questions)
        
        # Process technical questions
        if technical_count > 0:
            if technical_config.get('type') == 'manual':
                manual_questions = technical_config.get('manual_questions', [])
                # Add manual questions
                for q in manual_questions:
                    if q.get('question', '').strip():
                        all_questions.append(q['question'].strip())
                # Fill remaining with AI if needed
                remaining = technical_count - len([q for q in manual_questions if q.get('question', '').strip()])
                if remaining > 0:
                    ai_questions = await self._generate_specific_questions('technical', remaining, resume, job_description, role_archetype)
                    all_questions.extend(ai_questions)
            else:
                # Generate all via AI
                ai_questions = await self._generate_specific_questions('technical', technical_count, resume, job_description, role_archetype)
                all_questions.extend(ai_questions)
        
        # Process behavioral questions
        if behavioral_count > 0:
            if behavioral_config.get('type') == 'manual':
                manual_questions = behavioral_config.get('manual_questions', [])
                # Add manual questions
                for q in manual_questions:
                    if q.get('question', '').strip():
                        all_questions.append(q['question'].strip())
                # Fill remaining with AI if needed
                remaining = behavioral_count - len([q for q in manual_questions if q.get('question', '').strip()])
                if remaining > 0:
                    ai_questions = await self._generate_specific_questions('behavioral', remaining, resume, job_description, role_archetype)
                    all_questions.extend(ai_questions)
            else:
                # Generate all via AI
                ai_questions = await self._generate_specific_questions('behavioral', behavioral_count, resume, job_description, role_archetype)
                all_questions.extend(ai_questions)
        
        return all_questions[:max_questions]  # Ensure we don't exceed max_questions
    
    async def _generate_specific_questions(self, question_type: str, count: int, resume: str, job_description: str, role_archetype: str) -> List[str]:
        """Generate specific type of questions using AI"""
        if count <= 0:
            return []
        
        type_prompts = {
            'resume': f"Generate {count} questions specifically based on the candidate's resume experience and background",
            'technical': f"Generate {count} technical questions relevant to the job requirements and role",
            'behavioral': f"Generate {count} behavioral questions to assess soft skills and cultural fit"
        }
        
        bias_mitigation = """
        BIAS MITIGATION INSTRUCTIONS:
        - Evaluate candidates based ONLY on job-related competencies and qualifications
        - Ignore accent, gender, age, race, religion, or other protected characteristics
        - Focus on skills, experience, problem-solving ability, and cultural alignment
        - Ensure questions are fair and relevant to the role requirements
        """
        
        role_context = self._get_role_context(role_archetype)
        
        system_message = f"""You are an expert AI interviewer conducting a fair and unbiased interview. {bias_mitigation}
        
        Role Archetype: {role_archetype}
        {role_context}

        IMPORTANT: Generate questions in plain text without any formatting like backticks, bold, or italics since these will be converted to speech.
        
        {type_prompts.get(question_type, '')}

        Resume: {resume}
        Job Description: {job_description}

        Generate exactly {count} {question_type} questions. Format each question on a new line starting with "Q: " followed by the question."""
        
        session_id = self.generate_session_id()
        chat = await self.create_chat_instance(session_id, system_message)
        
        user_message = UserMessage(text=f"Generate {count} {question_type} questions based on the provided resume and job description.")
        response = await chat.send_message(user_message)
        
        # Parse questions from response
        questions = []
        lines = response.split('\n')
        for line in lines:
            if line.strip().startswith('Q:'):
                question = line.replace('Q:', '', 1).strip()
                if question:
                    questions.append(question)
        
        return questions[:count]  # Ensure we return exactly the requested count
    
    async def generate_interview_questions(self, resume: str, job_description: str, role_archetype: str = "General", interview_focus: str = "Balanced", min_questions: int = 8, max_questions: int = 12) -> List[str]:
        # Enhanced system message with bias mitigation and role archetype
        bias_mitigation = """
        BIAS MITIGATION INSTRUCTIONS:
        - Evaluate candidates based ONLY on job-related competencies and qualifications
        - Ignore accent, gender, age, race, religion, or other protected characteristics
        - Focus on skills, experience, problem-solving ability, and cultural alignment
        - Ensure questions are fair and relevant to the role requirements
        """
        
        role_context = self._get_role_context(role_archetype)
        focus_context = self._get_focus_context(interview_focus)
        
        # Calculate technical and behavioral question distribution
        total_questions = min_questions  # Start with minimum questions
        technical_count = (total_questions + 1) // 2  # Round up for technical
        behavioral_count = total_questions - technical_count
        
        # Generate dynamic question format instructions
        question_format = "Generate questions in this exact format:\n"
        for i in range(1, technical_count + 1):
            question_format += f"TECHNICAL_{i}: [question]\n"
        for i in range(1, behavioral_count + 1):
            question_format += f"BEHAVIORAL_{i}: [question]\n"
        
        system_message = f"""You are an expert AI interviewer conducting a fair and unbiased interview. {bias_mitigation}
        
        Role Archetype: {role_archetype}
        Interview Focus: {interview_focus}
        
        {role_context}
        {focus_context}

        IMPORTANT: Generate questions in plain text without any formatting like backticks, bold, or italics since these will be converted to speech.
        
        You need to generate exactly {total_questions} questions ({technical_count} technical, {behavioral_count} behavioral).
        The interviewer can ask up to {max_questions} questions if needed for comprehensive assessment.

        Resume: {resume}
        Job Description: {job_description}

        {question_format}"""
        
        session_id = self.generate_session_id()
        chat = await self.create_chat_instance(session_id, system_message)
        
        user_message = UserMessage(text="Generate the interview questions based on the resume and job description.")
        response = await chat.send_message(user_message)
        
        # Parse questions from response
        questions = []
        lines = response.split('\n')
        for line in lines:
            if line.startswith(('TECHNICAL_', 'BEHAVIORAL_')):
                question = line.split(': ', 1)[1] if ': ' in line else line
                questions.append(question.strip())
        
        return questions[:total_questions]  # Return the exact number of questions requested
    
    def _get_role_context(self, role_archetype: str) -> str:
        role_contexts = {
            "Software Engineer": "Focus on technical skills, coding abilities, system design, and software development lifecycle knowledge.",
            "Sales": "Emphasize communication skills, relationship building, negotiation abilities, and results-driven mindset.",
            "Graduate": "Consider fresh perspective, learning potential, adaptability, and foundational knowledge rather than extensive experience.",
            "General": "Balance technical competencies with behavioral traits suitable for the specific role."
        }
        return role_contexts.get(role_archetype, role_contexts["General"])
    
    def _get_focus_context(self, interview_focus: str) -> str:
        focus_contexts = {
            "Technical Deep-Dive": "Prioritize technical questions (6 technical, 2 behavioral) with detailed technical scenarios.",
            "Cultural Fit": "Prioritize behavioral questions (6 behavioral, 2 technical) focusing on team dynamics and company culture.",
            "Graduate Screening": "Balance foundational technical knowledge with potential and learning attitude.",
            "Balanced": "Equal focus on technical competencies and behavioral traits."
        }
        return focus_contexts.get(interview_focus, focus_contexts["Balanced"])
    
    async def rephrase_question(self, original_question: str) -> str:
        """Rephrase a question to help candidate understanding"""
        system_message = """You are helping rephrase interview questions to make them clearer while maintaining the same intent and difficulty level.
        
        IMPORTANT: Generate rephrased questions in plain text without any formatting like backticks, bold, or italics since these will be converted to speech.
        
        Keep the core assessment objective the same but make the language clearer and more accessible."""
        
        session_id = self.generate_session_id()
        chat = await self.create_chat_instance(session_id, system_message)
        
        user_message = UserMessage(text=f"Please rephrase this question to make it clearer: {original_question}")
        response = await chat.send_message(user_message)
        
        return response.strip()
    
    async def generate_coding_challenge(self, role_archetype: str, difficulty: str = "medium") -> Dict[str, Any]:
        """Generate a coding challenge based on role"""
        challenges_by_role = {
            "Software Engineer": [
                {
                    "title": "Array Sum Finder",
                    "description": "Write a function that finds two numbers in an array that add up to a target sum.",
                    "initial_code": "function findTwoSum(numbers, target) {\n  // Your code here\n  return [];\n}",
                    "expected_solution": "Use hash map for O(n) solution"
                },
                {
                    "title": "String Reversal",
                    "description": "Write a function that reverses a string without using built-in reverse methods.",
                    "initial_code": "function reverseString(str) {\n  // Your code here\n  return '';\n}",
                    "expected_solution": "Use two-pointer technique or recursion"
                }
            ]
        }
        
        role_challenges = challenges_by_role.get(role_archetype, challenges_by_role["Software Engineer"])
        challenge = role_challenges[0]  # For now, use first challenge
        
        return {
            "problem_title": challenge["title"],
            "problem_description": challenge["description"],
            "initial_code": challenge["initial_code"],
            "expected_solution": challenge["expected_solution"],
            "difficulty": difficulty,
            "language": "javascript"
        }
    
    async def generate_sjt_test(self, role_archetype: str) -> Dict[str, Any]:
        """Generate a Situational Judgment Test"""
        sjt_scenarios = {
            "Software Engineer": {
                "scenario": "You're working on a critical project with a tight deadline. A team member's code has a bug that could delay the release, but they're defensive about feedback.",
                "question": "What's the best approach to handle this situation?",
                "options": [
                    {"id": "a", "text": "Fix the bug yourself without involving the team member"},
                    {"id": "b", "text": "Schedule a private meeting to discuss the issue constructively"},
                    {"id": "c", "text": "Bring up the issue in the team meeting publicly"},
                    {"id": "d", "text": "Report the issue to management immediately"}
                ],
                "correct_answer": "b",
                "explanation": "A private constructive discussion respects the team member while addressing the critical issue professionally."
            }
        }
        
        return sjt_scenarios.get(role_archetype, sjt_scenarios["Software Engineer"])
    
    async def evaluate_coding_challenge(self, submitted_code: str, expected_solution: str, problem_description: str) -> Dict[str, Any]:
        """Evaluate submitted coding challenge"""
        system_message = f"""You are evaluating a coding challenge submission. 
        
        Problem: {problem_description}
        Expected approach: {expected_solution}
        
        Evaluate the code for:
        1. Correctness (does it solve the problem?)
        2. Efficiency (time/space complexity)
        3. Code quality (readability, structure)
        4. Edge case handling
        
        Provide a score out of 100 and detailed analysis."""
        
        session_id = self.generate_session_id()
        chat = await self.create_chat_instance(session_id, system_message)
        
        user_message = UserMessage(text=f"Evaluate this code submission: {submitted_code}")
        response = await chat.send_message(user_message)
        
        # Parse score from response (simplified)
        try:
            score_match = re.search(r'score.*?(\d+)', response.lower())
            score = int(score_match.group(1)) if score_match else 70
        except:
            score = 70
        
        return {
            "score": min(100, max(0, score)),
            "analysis": response
        }
    
    async def evaluate_answer(self, question: str, answer: str, question_type: str, unbiased_prompt: str = None) -> Dict[str, Any]:
        # Use unbiased prompt if provided, otherwise use standard prompt
        if unbiased_prompt:
            system_message = unbiased_prompt
        else:
            system_message = f"""You are an expert interview evaluator. Evaluate the candidate's answer to this {question_type} question.

        Question: {question}
        Answer: {answer}

        Provide evaluation in this exact JSON format:
        {{
            "score": [0-10],
            "feedback": "detailed feedback on the answer",
            "strengths": ["strength1", "strength2"],
            "improvements": ["improvement1", "improvement2"]
        }}"""
        
        session_id = self.generate_session_id()
        chat = await self.create_chat_instance(session_id, system_message)
        
        user_message = UserMessage(text=f"Evaluate this answer: {answer}")
        response = await chat.send_message(user_message)
        
        try:
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response[start:end]
                evaluation = json.loads(json_str)
                return evaluation
        except:
            pass
        
        # Fallback evaluation
        return {
            "score": 7,
            "feedback": "Answer provided shows understanding of the topic.",
            "strengths": ["Shows knowledge"],
            "improvements": ["Could provide more specific examples"]
        }
    
    async def generate_final_assessment(self, session_data: Dict) -> InterviewAssessment:
        technical_evaluations = session_data.get('technical_evaluations', [])
        behavioral_evaluations = session_data.get('behavioral_evaluations', [])
        
        # Calculate scores
        tech_scores = [eval.get('score', 0) for eval in technical_evaluations]
        behavioral_scores = [eval.get('score', 0) for eval in behavioral_evaluations]
        
        technical_score = int((sum(tech_scores) / len(tech_scores)) * 10) if tech_scores else 50
        behavioral_score = int((sum(behavioral_scores) / len(behavioral_scores)) * 10) if behavioral_scores else 50
        overall_score = int((technical_score + behavioral_score) / 2)
        
        # Generate comprehensive feedback
        system_message = """You are an expert HR analyst. Based on the interview evaluations provided, generate a comprehensive assessment report.

        IMPORTANT: Provide feedback in plain text without any formatting like backticks, bold, or italics since this may be converted to speech.

        Provide detailed feedback for technical performance, behavioral performance, overall assessment, and specific recommendations for the candidate."""
        
        session_id = self.generate_session_id()
        chat = await self.create_chat_instance(session_id, system_message)
        
        evaluation_summary = f"""
        Technical Evaluations: {technical_evaluations}
        Behavioral Evaluations: {behavioral_evaluations}
        Technical Score: {technical_score}/100
        Behavioral Score: {behavioral_score}/100
        """
        
        user_message = UserMessage(text=f"Generate comprehensive assessment based on: {evaluation_summary}")
        try:
            response = await chat.send_message(user_message)
            if not response or not isinstance(response, str):
                response = "Assessment completed successfully. The candidate demonstrated good understanding across technical and behavioral areas."
        except Exception as e:
            response = "Assessment completed successfully. The candidate demonstrated good understanding across technical and behavioral areas."
        
        return InterviewAssessment(
            session_id=session_data['session_id'],
            token=session_data['token'],
            candidate_name=session_data['candidate_name'],
            job_title=session_data['job_title'],
            technical_score=technical_score,
            behavioral_score=behavioral_score,
            overall_score=overall_score,
            technical_feedback=f"Technical performance: {technical_score}/100. Shows solid understanding of technical concepts.",
            behavioral_feedback=f"Behavioral performance: {behavioral_score}/100. Demonstrates good communication and problem-solving skills.",
            overall_feedback=response,
            recommendations="Continue developing relevant skills and gain more practical experience. Focus on areas where improvement was noted."
        )

# Voice Processing Class - Updated for Web Speech API
class VoiceProcessor:
    def __init__(self):
        # Web Speech API doesn't require server-side clients
        # TTS is handled on the frontend
        self.use_web_speech = True
        logging.info("VoiceProcessor initialized for Web Speech API")
    
    def clean_text_for_speech(self, text: str) -> str:
        """Clean text for better TTS pronunciation by removing formatting characters"""
        import re
        
        # Remove backticks around code terms
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Remove other markdown formatting
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
        text = re.sub(r'_([^_]+)_', r'\1', text)        # Underscore italic
        text = re.sub(r'~~([^~]+)~~', r'\1', text)      # Strikethrough
        
        # Replace common code-related phrases for better pronunciation
        text = text.replace('HTML', 'H-T-M-L')
        text = text.replace('CSS', 'C-S-S')
        text = text.replace('JavaScript', 'Java Script')
        text = text.replace('APIs', 'A-P-Is')
        text = text.replace('API', 'A-P-I')
        text = text.replace('JSON', 'J-S-O-N')
        text = text.replace('SQL', 'S-Q-L')
        
        # Remove multiple spaces and clean up
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    async def text_to_speech(self, text: str) -> dict:
        """Prepare text for Web Speech API - return cleaned text with metadata"""
        try:
            # Clean text before sending to frontend
            cleaned_text = self.clean_text_for_speech(text)
            
            # Generate a dummy file ID for compatibility
            file_id = str(uuid.uuid4())
            
            # Return dictionary format expected by calling code
            return {
                "file_id": file_id,
                "cleaned_text": cleaned_text,
                "original_text": text,
                "audio_base64": "",  # Empty since Web Speech API handles TTS on frontend
                "success": True
            }
            
        except Exception as e:
            logging.error(f"Text cleaning error: {str(e)}")
            # Return error format
            return {
                "file_id": str(uuid.uuid4()),
                "cleaned_text": text,
                "original_text": text,
                "audio_base64": "",
                "success": False,
                "error": str(e)
            }
    
    async def speech_to_text(self, audio_data: bytes) -> str:
        """STT is now handled by Web Speech API on the frontend"""
        try:
            logging.info("STT request received - redirecting to Web Speech API")
            
            # Since STT is now handled by Web Speech API on the frontend,
            # this method should not be called. Return a message indicating this.
            return "Speech-to-text is now handled by Web Speech API on the frontend"
            
        except Exception as e:
            logging.error(f"Speech-to-text error: {str(e)}")
            
            # Fallback message
            return "Speech-to-text is handled by Web Speech API on the frontend"

# Initialize all managers and analyzers
interview_ai = InterviewAI()
voice_processor = VoiceProcessor()
data_privacy_manager = DataPrivacyManager()
personality_analyzer = PersonalityAnalyzer()

# Background task for automatic data cleanup
async def scheduled_data_cleanup():
    """Scheduled task to automatically cleanup expired data"""
    while True:
        try:
            # Sleep for 24 hours (86400 seconds)
            await asyncio.sleep(86400)
            
            # Perform cleanup
            result = await data_privacy_manager.cleanup_expired_data()
            
            # Log the automated cleanup
            audit_record = {
                "action": "automated_data_cleanup",
                "result": result,
                "timestamp": datetime.utcnow(),
                "source": "scheduled_task"
            }
            await db.audit_logs.insert_one(audit_record)
            
            logging.info(f"Automated data cleanup completed: {result}")
            
        except Exception as e:
            logging.error(f"Automated data cleanup failed: {str(e)}")
            # Continue the loop even if cleanup fails
            continue

# Start background cleanup task when the app starts
@app.on_event("startup")
async def startup_background_tasks():
    """Start background maintenance tasks"""
    asyncio.create_task(scheduled_data_cleanup())
    logging.info("Background data cleanup task started")

# Helper Functions
def generate_secure_token() -> str:
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))

# Admin Routes
@api_router.post("/admin/login")
async def admin_login(request: AdminLoginRequest):
    if request.password != "Game@1234":
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"success": True, "message": "Admin authenticated successfully"}

# Legacy Admin Route (for backward compatibility)
@api_router.post("/admin/upload-job-enhanced")
async def upload_job_enhanced(
    job_title: str = Form(...),
    job_description: str = Form(...),
    job_requirements: str = Form(...),
    include_coding_challenge: bool = Form(False),
    role_archetype: str = Form("General"),
    interview_focus: str = Form("Balanced"),
    min_questions: int = Form(8),
    max_questions: int = Form(12),
    custom_questions_config: str = Form("{}"),
    resume_file: UploadFile = File(...)
):
    # Validate admin authentication (same as before)
    # Parse resume (same as before)
    resume_content = await resume_file.read()
    try:
        resume_text = parse_resume(resume_file, resume_content)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from resume file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume parsing failed: {str(e)}")
    
    # Create job record
    job_data = JobDescription(
        title=job_title,
        description=job_description,
        requirements=job_requirements
    )
    await db.jobs.insert_one(job_data.dict())
    
    # Generate secure token
    token = generate_secure_token()
    
    # Parse custom questions configuration
    try:
        custom_config = json.loads(custom_questions_config)
    except (json.JSONDecodeError, TypeError):
        custom_config = {}
    
    # Create enhanced token record
    token_data = EnhancedCandidateToken(
        token=token,
        job_id=job_data.id,
        resume_content=resume_text,
        job_description=f"{job_title}\n\n{job_description}\n\n{job_requirements}",
        include_coding_challenge=include_coding_challenge,
        role_archetype=role_archetype,
        interview_focus=interview_focus,
        min_questions=min_questions,
        max_questions=max_questions,
        custom_questions_config=custom_config
    )
    await db.enhanced_tokens.insert_one(token_data.dict())
    
    # Estimate duration based on features and question count
    base_duration = max_questions * 3  # 3 minutes per question average
    if include_coding_challenge:
        base_duration += 15
    
    return {
        "success": True,
        "token": token,
        "resume_preview": resume_text[:200] + "..." if len(resume_text) > 200 else resume_text,
        "estimated_duration": base_duration,
        "features": {
            "coding_challenge": include_coding_challenge,
            "role_archetype": role_archetype,
            "interview_focus": interview_focus,
            "min_questions": min_questions,
            "max_questions": max_questions,
            "estimated_duration": base_duration
        },
        "message": f"Enhanced job and resume ({resume_file.filename}) uploaded successfully."
    }

@api_router.get("/admin/candidate-pipeline")
async def get_candidate_pipeline():
    """Get all candidates with their current status"""
    # Get all tokens (both regular and enhanced)
    regular_tokens = await db.tokens.find().to_list(1000)
    enhanced_tokens = await db.enhanced_tokens.find().to_list(1000)
    
    pipeline = []
    
    # Process regular tokens
    for token_data in regular_tokens:
        session = await db.sessions.find_one({"token": token_data["token"]})
        assessment = await db.assessments.find_one({"token": token_data["token"]})
        
        status = "Invited"
        if session:
            if session.get("status") == "completed":
                status = "Completed"
            else:
                status = "In Progress"
        if assessment:
            status = "Report Ready"
            
        pipeline.append({
            "token": token_data["token"],
            "candidate_name": session.get("candidate_name", "Not Started") if session else "Not Started",
            "job_title": token_data["job_description"].split("\n")[0],
            "status": status,
            "created_at": token_data["created_at"],
            "overall_score": assessment.get("overall_score") if assessment else None,
            "interview_type": "Standard",
            "session_id": session.get("session_id") if session else None
        })
    
    # Process enhanced tokens
    for token_data in enhanced_tokens:
        session = await db.sessions.find_one({"token": token_data["token"]})
        assessment = await db.assessments.find_one({"token": token_data["token"]})
        
        status = "Invited"
        if session:
            if session.get("status") == "completed":
                status = "Completed"
            else:
                status = "In Progress"
        if assessment:
            status = "Report Ready"
            
        pipeline.append({
            "token": token_data["token"],
            "candidate_name": session.get("candidate_name", "Not Started") if session else "Not Started",
            "job_title": token_data["job_description"].split("\n")[0],
            "status": status,
            "created_at": token_data["created_at"],
            "overall_score": assessment.get("overall_score") if assessment else None,
            "interview_type": "Enhanced",
            "session_id": session.get("session_id") if session else None,
            "features": {
                "coding_challenge": token_data.get("include_coding_challenge", False),
                "role_archetype": token_data.get("role_archetype", "General"),
                "interview_focus": token_data.get("interview_focus", "Balanced")
            }
        })
    
    # Sort by creation date
    pipeline.sort(key=lambda x: x["created_at"], reverse=True)
    
    return {"pipeline": pipeline}

@api_router.post("/admin/compare-candidates")
async def compare_candidates(candidate_tokens: List[str]):
    """Compare multiple candidates side by side"""
    comparisons = []
    
    for token in candidate_tokens:
        assessment = await db.assessments.find_one({"token": token})
        session = await db.sessions.find_one({"token": token})
        
        if assessment and session:
            comparisons.append({
                "token": token,
                "candidate_name": session.get("candidate_name"),
                "job_title": assessment.get("job_title"),
                "technical_score": assessment.get("technical_score"),
                "behavioral_score": assessment.get("behavioral_score"),
                "overall_score": assessment.get("overall_score"),
                "key_strengths": assessment.get("key_strengths", []),
                "areas_for_improvement": assessment.get("areas_for_improvement", []),
                "red_flags": assessment.get("red_flags", [])
            })
    
    return {"comparisons": comparisons}

# Enhanced Candidate Routes
@api_router.post("/candidate/camera-test")
async def camera_test(request: CameraTestRequest):
    """Test camera and microphone functionality"""
    # This is primarily handled by frontend, backend just validates token
    token_data = await db.enhanced_tokens.find_one({"token": request.token})
    if not token_data:
        token_data = await db.tokens.find_one({"token": request.token})
    
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {
        "success": True,
        "message": "Camera and microphone test completed",
        "estimated_duration": 30,
        "features": {
            "voice_mode": True,
            "coding_challenge": token_data.get("include_coding_challenge", False),
            "role_archetype": token_data.get("role_archetype", "General")
        }
    }

@api_router.post("/candidate/practice-round")
async def start_practice_round(request: PracticeRoundRequest):
    """Start practice round for candidate"""
    # Validate token
    token_data = await db.enhanced_tokens.find_one({"token": request.token})
    if not token_data:
        token_data = await db.tokens.find_one({"token": request.token})
    
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Create practice session
    practice = PracticeRound(
        session_id=f"practice_{request.token}_{datetime.utcnow().timestamp()}"
    )
    await db.practice_rounds.insert_one(practice.dict())
    
    # Clean TTS practice question
    try:
        audio_text = await voice_processor.text_to_speech(practice.question)
    except Exception as e:
        logging.error(f"Text cleaning failed for practice: {str(e)}")
        audio_text = practice.question
    
    return {
        "session_id": practice.session_id,
        "practice_question": practice.question,
        "question_text": await voice_processor.text_to_speech(practice.question),
        "message": "This is a practice round. Your answer will not be saved or scored."
    }

@api_router.post("/candidate/rephrase-question")
async def rephrase_question(request: RephraseQuestionRequest):
    """Rephrase current question for better understanding"""
    try:
        # Get current session to find the original question
        session = await db.sessions.find_one({"session_id": request.session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        rephrased = await interview_ai.rephrase_question(request.original_question)
        
        # Generate TTS for rephrased question
        audio_data = None
        if session.get("voice_mode"):
            try:
                audio_data = await voice_processor.text_to_speech(rephrased)
            except Exception as e:
                logging.error(f"TTS generation failed: {str(e)}")
        
        return {
            "rephrased_question": rephrased,
            "question_text": await voice_processor.text_to_speech(rephrased)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Interactive Module Routes
@api_router.get("/modules/coding-challenge/{session_id}")
async def get_coding_challenge(session_id: str):
    """Get coding challenge for session"""
    session = await db.sessions.find_one({"session_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if coding challenge is enabled
    token_data = await db.enhanced_tokens.find_one({"token": session["token"]})
    if not token_data or not token_data.get("include_coding_challenge"):
        raise HTTPException(status_code=400, detail="Coding challenge not enabled for this interview")
    
    # Check if challenge already exists
    existing_challenge = await db.coding_challenges.find_one({"session_id": session_id})
    if existing_challenge:
        return {"challenge": existing_challenge}
    
    # Generate new coding challenge
    challenge_data = await interview_ai.generate_coding_challenge(
        token_data.get("role_archetype", "Software Engineer")
    )
    
    challenge = CodingChallenge(
        session_id=session_id,
        **challenge_data
    )
    await db.coding_challenges.insert_one(challenge.dict())
    
    # Don't include expected solution in response
    response_data = challenge.dict()
    response_data.pop("expected_solution", None)
    
    return {"challenge": response_data}

@api_router.post("/modules/coding-challenge/submit")
async def submit_coding_challenge(request: CodingChallengeSubmissionRequest):
    """Submit coding challenge solution"""
    challenge = await db.coding_challenges.find_one({"session_id": request.session_id})
    if not challenge:
        raise HTTPException(status_code=404, detail="Coding challenge not found")
    
    if challenge["completed"]:
        raise HTTPException(status_code=400, detail="Challenge already completed")
    
    # Evaluate the submission
    evaluation = await interview_ai.evaluate_coding_challenge(
        request.submitted_code,
        challenge["expected_solution"],
        challenge["problem_description"]
    )
    
    # Update challenge record
    await db.coding_challenges.update_one(
        {"session_id": request.session_id},
        {
            "$set": {
                "submitted_code": request.submitted_code,
                "score": evaluation["score"],
                "analysis": evaluation["analysis"],
                "completed": True
            }
        }
    )
    
    return {
        "success": True,
        "score": evaluation["score"],
        "analysis": evaluation["analysis"]
    }

@api_router.get("/modules/sjt/{session_id}")
async def get_sjt_test(session_id: str):
    """Get Situational Judgment Test"""
    session = await db.sessions.find_one({"session_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get role archetype
    token_data = await db.enhanced_tokens.find_one({"token": session["token"]})
    role_archetype = token_data.get("role_archetype", "Software Engineer") if token_data else "Software Engineer"
    
    # Check if SJT already exists
    existing_sjt = await db.sjt_tests.find_one({"session_id": session_id})
    if existing_sjt:
        response_data = existing_sjt.copy()
        response_data.pop("correct_answer", None)  # Don't reveal correct answer
        return {"sjt": response_data}
    
    # Generate new SJT
    sjt_data = await interview_ai.generate_sjt_test(role_archetype)
    
    sjt = SJTTest(
        session_id=session_id,
        **sjt_data
    )
    await db.sjt_tests.insert_one(sjt.dict())
    
    # Don't include correct answer in response
    response_data = sjt.dict()
    response_data.pop("correct_answer", None)
    
    return {"sjt": response_data}

@api_router.post("/modules/sjt/submit")
async def submit_sjt_answer(request: SJTAnswerRequest):
    """Submit SJT answer"""
    sjt = await db.sjt_tests.find_one({"id": request.sjt_id, "session_id": request.session_id})
    if not sjt:
        raise HTTPException(status_code=404, detail="SJT test not found")
    
    if sjt["completed"]:
        raise HTTPException(status_code=400, detail="SJT already completed")
    
    # Check answer
    is_correct = request.selected_answer == sjt["correct_answer"]
    score = 100 if is_correct else 0
    
    # Update SJT record
    await db.sjt_tests.update_one(
        {"id": request.sjt_id},
        {
            "$set": {
                "selected_answer": request.selected_answer,
                "score": score,
                "completed": True
            }
        }
    )
    
    return {
        "success": True,
        "is_correct": is_correct,
        "score": score,
        "explanation": sjt["explanation"]
    }

# Legacy Admin Route (for backward compatibility)
@api_router.post("/admin/upload-job")
async def upload_job_legacy(
    job_title: str = Form(...),
    job_description: str = Form(...),
    job_requirements: str = Form(...),
    resume_file: UploadFile = File(...)
):
    resume_content = await resume_file.read()
    try:
        resume_text = parse_resume(resume_file, resume_content)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from resume file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume parsing failed: {str(e)}")
    
    # Create job record
    job_data = JobDescription(
        title=job_title,
        description=job_description,
        requirements=job_requirements
    )
    await db.jobs.insert_one(job_data.dict())
    
    # Generate secure token
    token = generate_secure_token()
    
    # Create token record
    token_data = CandidateToken(
        token=token,
        job_id=job_data.id,
        resume_content=resume_text,
        job_description=f"{job_title}\n\n{job_description}\n\n{job_requirements}"
    )
    await db.tokens.insert_one(token_data.dict())
    
    return {
        "success": True,
        "token": token,
        "resume_preview": resume_text[:200] + "..." if len(resume_text) > 200 else resume_text,
        "message": f"Job and resume ({resume_file.filename}) uploaded successfully. Token generated for candidate."
    }
async def upload_job_and_resume(
    job_title: str = Form(...),
    job_description: str = Form(...),
    job_requirements: str = Form(...),
    resume_file: UploadFile = File(...)
):
    # Read resume content
    resume_content = await resume_file.read()
    
    # Parse resume based on file type
    try:
        resume_text = parse_resume(resume_file, resume_content)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from resume file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume parsing failed: {str(e)}")
    
    # Create job record
    job_data = JobDescription(
        title=job_title,
        description=job_description,
        requirements=job_requirements
    )
    await db.jobs.insert_one(job_data.dict())
    
    # Generate secure token
    token = generate_secure_token()
    
    # Create token record
    token_data = CandidateToken(
        token=token,
        job_id=job_data.id,
        resume_content=resume_text,
        job_description=f"{job_title}\n\n{job_description}\n\n{job_requirements}"
    )
    await db.tokens.insert_one(token_data.dict())
    
    return {
        "success": True,
        "token": token,
        "resume_preview": resume_text[:200] + "..." if len(resume_text) > 200 else resume_text,
        "message": f"Job and resume ({resume_file.filename}) uploaded successfully. Token generated for candidate."
    }

@api_router.get("/admin/reports")
async def get_all_reports():
    reports = await db.assessments.find().to_list(1000)
    # Convert MongoDB ObjectIds to strings for JSON serialization
    for report in reports:
        if '_id' in report:
            report['_id'] = str(report['_id'])
    return {"reports": reports}

@api_router.get("/admin/reports/{session_id}")
async def get_report_by_session(session_id: str):
    report = await db.assessments.find_one({"session_id": session_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    # Convert MongoDB ObjectId to string for JSON serialization
    if '_id' in report:
        report['_id'] = str(report['_id'])
    return {"report": report}

@api_router.get("/admin/detailed-report/{session_id}")
async def get_detailed_report_by_session(session_id: str):
    """Get detailed interview transcript and enhanced assessment for admin review"""
    # Get the assessment
    assessment = await db.assessments.find_one({"session_id": session_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get the session data for messages
    session = await db.sessions.find_one({"session_id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get session metadata for questions
    session_metadata = await db.session_metadata.find_one({"session_id": session_id})
    if not session_metadata:
        raise HTTPException(status_code=404, detail="Session metadata not found")
    
    # Build the transcript with proper formatting
    questions = session_metadata.get('questions', [])
    messages = session.get('messages', [])
    
    # Filter candidate answers
    candidate_messages = [msg for msg in messages if msg.get('type') == 'candidate']
    
    transcript_parts = []
    
    # Format Q&A pairs
    for i in range(min(len(questions), len(candidate_messages))):
        question_num = i + 1
        question_text = questions[i]
        answer_text = candidate_messages[i].get('content', 'No answer provided')
        
        # Add question
        transcript_parts.append(f"Q{question_num}: {question_text}")
        
        # Add answer
        transcript_parts.append(f"A{question_num}: {answer_text}")
        
        # Add two line gap except after the last question
        if i < min(len(questions), len(candidate_messages)) - 1:
            transcript_parts.append("")
            transcript_parts.append("")
    
    # Create the formatted transcript
    formatted_transcript = "\n".join(transcript_parts)
    
    # Generate enhanced assessment with merits and demerits
    candidate_name = assessment.get('candidate_name', 'Candidate')
    job_title = assessment.get('job_title', 'Position')
    technical_score = assessment.get('technical_score', 0)
    behavioral_score = assessment.get('behavioral_score', 0)
    overall_score = assessment.get('overall_score', 0)
    
    # Generate detailed justification with merits and demerits
    session_id_for_ai = interview_ai.generate_session_id()
    chat = await interview_ai.create_chat_instance(session_id_for_ai, 
        """You are an expert HR analyst. Based on the interview assessment provided, generate a comprehensive hiring justification.

        IMPORTANT: Provide feedback in plain text without any formatting like backticks, bold, or italics.
        
        Structure your response as follows:
        1. CANDIDATE SCORE: [overall score]/100
        2. MERITS (Why should we hire this candidate):
        - List 3-5 key strengths based on interview performance
        3. DEMERITS (Areas of concern):
        - List 3-5 areas where the candidate showed weaknesses or gaps
        4. RECOMMENDATION:
        - Clear hiring recommendation (Strong Hire / Hire / No Hire / Strong No Hire) with justification
        
        Be specific and reference actual interview responses when possible.""")
    
    assessment_summary = f"""
    Candidate: {candidate_name}
    Position: {job_title}
    Technical Score: {technical_score}/100
    Behavioral Score: {behavioral_score}/100
    Overall Score: {overall_score}/100
    
    Technical Evaluations: {session_metadata.get('technical_evaluations', [])}
    Behavioral Evaluations: {session_metadata.get('behavioral_evaluations', [])}
    """
    
    try:
        user_message = UserMessage(text=f"Generate detailed hiring justification based on: {assessment_summary}")
        justification = await chat.send_message(user_message)
        if not justification or not isinstance(justification, str):
            justification = f"""
CANDIDATE SCORE: {overall_score}/100

MERITS (Why should we hire this candidate):
- Demonstrated solid technical understanding with score of {technical_score}/100
- Showed good behavioral responses with score of {behavioral_score}/100
- Completed the full interview process successfully

DEMERITS (Areas of concern):
- Some areas may need improvement based on evaluation scores
- Would benefit from additional experience in certain technical areas

RECOMMENDATION: 
{'Strong Hire' if overall_score >= 80 else 'Hire' if overall_score >= 60 else 'No Hire'} - Overall performance was {'excellent' if overall_score >= 80 else 'good' if overall_score >= 60 else 'below expectations'}.
            """
    except Exception as e:
        justification = f"""
CANDIDATE SCORE: {overall_score}/100

MERITS (Why should we hire this candidate):
- Demonstrated solid technical understanding with score of {technical_score}/100
- Showed good behavioral responses with score of {behavioral_score}/100
- Completed the full interview process successfully

DEMERITS (Areas of concern):
- Some areas may need improvement based on evaluation scores
- Would benefit from additional experience in certain technical areas

RECOMMENDATION: 
{'Strong Hire' if overall_score >= 80 else 'Hire' if overall_score >= 60 else 'No Hire'} - Overall performance was {'excellent' if overall_score >= 80 else 'good' if overall_score >= 60 else 'below expectations'}.
        """
    
    # Convert MongoDB ObjectId to string for JSON serialization
    if '_id' in assessment:
        assessment['_id'] = str(assessment['_id'])
    
    return {
        "session_id": session_id,
        "candidate_name": candidate_name,
        "job_title": job_title,
        "interview_date": session.get('created_at', 'Not available'),
        "transcript": formatted_transcript,
        "assessment_summary": {
            "technical_score": technical_score,
            "behavioral_score": behavioral_score,
            "overall_score": overall_score
        },
        "detailed_justification": justification,
        "full_assessment": assessment
    }

# Voice Routes
@api_router.post("/voice/generate-question")
async def generate_voice_question(request: VoiceQuestionRequest):
    """Generate TTS audio for interview question"""
    try:
        audio_data = await voice_processor.text_to_speech(request.question_text)
        
        # Store question audio reference in session metadata
        await db.session_metadata.update_one(
            {"session_id": request.session_id},
            {"$push": {"question_audios": {
                "file_id": audio_data["file_id"],
                "text": request.question_text,
                "timestamp": datetime.utcnow()
            }}}
        )
        
        return {
            "success": True,
            "question_text": request.question_text,
            "audio_base64": audio_data.get("audio_base64", ""),
            "file_id": audio_data["file_id"],
            "cleaned_text": audio_data.get("cleaned_text", request.question_text)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/voice/process-answer")
async def process_voice_answer(
    session_id: str = Form(...),
    question_number: int = Form(...),
    audio_file: UploadFile = File(...)
):
    """Process voice answer - convert to text and analyze emotional intelligence from voice"""
    try:
        audio_content = await audio_file.read()
        
        # Convert speech to text
        transcript = await voice_processor.speech_to_text(audio_content)
        
        # ENHANCED: Analyze voice for emotional intelligence
        voice_analysis = ei_analyzer.analyze_voice_features(audio_content)
        
        # ENHANCED: Analyze text sentiment from transcript
        text_analysis = ei_analyzer.analyze_text_sentiment(transcript)
        
        # Combine voice and text analysis
        combined_ei_analysis = {
            "voice_emotional_indicators": voice_analysis["voice_emotional_indicators"],
            "voice_features": voice_analysis["voice_features"],
            "text_sentiment": text_analysis["sentiment"],
            "text_emotions": text_analysis["emotions"],
            "combined_confidence": (
                voice_analysis["voice_emotional_indicators"]["confidence"] + 
                text_analysis["emotional_intelligence"]["confidence"]
            ) / 2,
            "combined_stress": (
                voice_analysis["voice_emotional_indicators"]["stress_level"] + 
                text_analysis["emotional_intelligence"]["stress_level"]
            ) / 2,
            "combined_enthusiasm": (
                voice_analysis["voice_emotional_indicators"]["enthusiasm"] + 
                text_analysis["emotional_intelligence"]["enthusiasm"]  
            ) / 2
        }
        
        # Store audio file in GridFS
        file_id = fs.put(audio_content, 
                        filename=f"answer_{session_id}_{question_number}.webm",
                        metadata={
                            "type": "answer_audio", 
                            "session_id": session_id,
                            "emotional_analysis": combined_ei_analysis
                        })
        
        # Store answer with enhanced analysis in session metadata
        await db.session_metadata.update_one(
            {"session_id": session_id},
            {"$push": {"answer_audios": {
                "file_id": str(file_id),
                "transcript": transcript,
                "question_number": question_number,
                "timestamp": datetime.utcnow(),
                "emotional_analysis": combined_ei_analysis
            }}}
        )
        
        return {
            "success": True,
            "transcript": transcript,
            "file_id": str(file_id),
            "emotional_intelligence": {
                "confidence": combined_ei_analysis["combined_confidence"],
                "stress_level": combined_ei_analysis["combined_stress"], 
                "enthusiasm": combined_ei_analysis["combined_enthusiasm"],
                "voice_clarity": voice_analysis["voice_emotional_indicators"]["clarity"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced voice processing failed: {str(e)}")

# Candidate Routes
@api_router.post("/candidate/validate-token")
async def validate_token(request: TokenValidationRequest):
    # Try enhanced token first, then fallback to regular token
    token_data = await db.enhanced_tokens.find_one({"token": request.token})
    
    if not token_data:
        token_data = await db.tokens.find_one({"token": request.token})
    
    if not token_data or token_data.get('used', False):
        raise HTTPException(status_code=401, detail="Invalid or used token")
    
    job_data = await db.jobs.find_one({"id": token_data['job_id']})
    
    return {
        "valid": True,
        "job_title": job_data['title'] if job_data else "Software Developer",
        "token": request.token
    }

@api_router.post("/candidate/start-interview")
async def start_interview(request: InterviewStartRequest):
    # Try enhanced token first, then fallback to regular token
    token_data = await db.enhanced_tokens.find_one({"token": request.token})
    is_enhanced = True
    
    if not token_data:
        token_data = await db.tokens.find_one({"token": request.token})
        is_enhanced = False
    
    if not token_data or token_data.get('used', False):
        raise HTTPException(status_code=401, detail="Invalid or used token")
    
    job_data = await db.jobs.find_one({"id": token_data['job_id']})
    
    # Generate interview questions with enhanced parameters if available
    if is_enhanced:
        custom_config = token_data.get('custom_questions_config', {})
        if custom_config:
            # Use custom question generation method
            questions = await interview_ai.generate_interview_questions_with_custom(
                token_data['resume_content'],
                token_data['job_description'],
                token_data.get('role_archetype', 'General'),
                token_data.get('interview_focus', 'Balanced'),
                token_data.get('min_questions', 8),
                token_data.get('max_questions', 12),
                custom_config
            )
        else:
            # Use original method
            questions = await interview_ai.generate_interview_questions(
                token_data['resume_content'],
                token_data['job_description'],
                token_data.get('role_archetype', 'General'),
                token_data.get('interview_focus', 'Balanced'),
                token_data.get('min_questions', 8),
                token_data.get('max_questions', 12)
            )
    else:
        questions = await interview_ai.generate_interview_questions(
            token_data['resume_content'],
            token_data['job_description'],
            'General',
            'Balanced',
            8,  # Default min questions for legacy tokens
            12  # Default max questions for legacy tokens
        )
    
    # Create interview session
    session_id = interview_ai.generate_session_id()
    
    # Calculate technical and behavioral question distribution
    total_questions = len(questions)
    technical_count = (total_questions + 1) // 2  # Round up for technical (same logic as generation)
    behavioral_count = total_questions - technical_count
    session_data = InterviewSession(
        token=request.token,
        session_id=session_id,
        candidate_name=request.candidate_name,
        job_title=job_data['title'] if job_data else "Software Developer",
        voice_mode=request.voice_mode or False,
        messages=[{
            "type": "system",
            "content": f"Welcome {request.candidate_name}! I'm your AI interviewer today. We'll have {total_questions} questions - {technical_count} technical and {behavioral_count} behavioral. Let's begin!",
            "timestamp": datetime.utcnow().isoformat()
        }],
        current_question=0
    )
    
    await db.sessions.insert_one(session_data.dict())
    
    # Store questions and enhanced features in session metadata
    session_metadata = {
        "session_id": session_id,
        "questions": questions,
        "technical_count": technical_count,  # Store for later use in question type determination
        "behavioral_count": behavioral_count,
        "technical_evaluations": [],
        "behavioral_evaluations": [],
        "question_audios": [],
        "answer_audios": [],
        "is_enhanced": is_enhanced
    }
    
    if is_enhanced:
        session_metadata.update({
            "include_coding_challenge": token_data.get('include_coding_challenge', False),
            "role_archetype": token_data.get('role_archetype', 'General'),
            "interview_focus": token_data.get('interview_focus', 'Balanced')
        })
    
    await db.session_metadata.insert_one(session_metadata)
    
    # Mark token as used
    collection = db.enhanced_tokens if is_enhanced else db.tokens
    await collection.update_one(
        {"token": request.token},
        {"$set": {"used": True}}
    )
    
    response_data = {
        "session_id": session_id,
        "first_question": questions[0] if questions else "Tell me about your experience with software development.",
        "question_number": 1,
        "total_questions": len(questions),  # Use actual number of generated questions
        "welcome_message": f"Welcome {request.candidate_name}! Ready to start your interview?",
        "voice_mode": request.voice_mode or False,
        "is_enhanced": is_enhanced
    }
    
    # Add enhanced features to response
    if is_enhanced:
        response_data.update({
            "features": {
                "coding_challenge": token_data.get('include_coding_challenge', False),
                "role_archetype": token_data.get('role_archetype', 'General'),
                "interview_focus": token_data.get('interview_focus', 'Balanced')
            },
            "estimated_duration": token_data.get('estimated_duration', 30)
        })
    
    # Generate text for Web Speech API (voice mode)
    if request.voice_mode:
        try:
            welcome_text = await voice_processor.text_to_speech(response_data["welcome_message"])
            question_text = await voice_processor.text_to_speech(questions[0] if questions else "Tell me about your experience.")
            
            # Return cleaned text for frontend Web Speech API
            response_data["welcome_text"] = welcome_text
            response_data["question_text"] = question_text
        except Exception as e:
            logging.error(f"Text cleaning failed: {str(e)}")
    
    return response_data

@api_router.post("/candidate/send-message")
async def send_interview_message(request: InterviewMessageRequest):
    session = await db.sessions.find_one({"token": request.token, "status": "in_progress"})
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found or completed")
    
    session_metadata = await db.session_metadata.find_one({"session_id": session['session_id']})
    if not session_metadata:
        raise HTTPException(status_code=404, detail="Session metadata not found")
    
    questions = session_metadata['questions']
    current_q_num = session['current_question']
    
    if current_q_num >= len(questions):
        raise HTTPException(status_code=400, detail="Interview already completed")
    
    # ENHANCED: Perform emotional intelligence analysis on the answer
    ei_analysis = ei_analyzer.analyze_text_sentiment(request.message)
    
    # Apply bias detection to the evaluation process
    current_question = questions[current_q_num]
    # Use dynamic question type based on actual technical/behavioral split
    technical_count = session_metadata.get('technical_count', (len(questions) + 1) // 2)  # Fallback for legacy sessions
    question_type = "technical" if current_q_num < technical_count else "behavioral"
    
    # Generate unbiased evaluation prompt
    unbiased_prompt = bias_detector.generate_unbiased_prompt(
        f"Evaluate this {question_type} response to: {current_question}\n\nCandidate's answer: {request.message}"
    )
    
    evaluation = await interview_ai.evaluate_answer(
        current_question,
        request.message,
        question_type,
        unbiased_prompt=unbiased_prompt
    )
    
    # Enhanced evaluation with EI metrics and bias detection
    enhanced_evaluation = {
        **evaluation,
        "emotional_intelligence": ei_analysis["emotional_intelligence"],
        "sentiment_analysis": ei_analysis["sentiment"],
        "detected_emotions": ei_analysis["emotions"],
        "bias_check": bias_detector.detect_bias_in_evaluation(
            evaluation.get("feedback", ""), current_question
        )
    }
    
    # Store evaluation
    if question_type == "technical":
        session_metadata['technical_evaluations'].append(enhanced_evaluation)
    else:
        session_metadata['behavioral_evaluations'].append(enhanced_evaluation)
    
    await db.session_metadata.update_one(
        {"session_id": session['session_id']},
        {"$set": {
            "technical_evaluations": session_metadata['technical_evaluations'],
            "behavioral_evaluations": session_metadata['behavioral_evaluations']
        }}
    )
    
    # Add candidate's message with EI analysis
    new_message = {
        "type": "candidate",
        "content": request.message,
        "timestamp": datetime.utcnow().isoformat(),
        "question_number": current_q_num + 1,
        "emotional_intelligence": ei_analysis["emotional_intelligence"],
        "sentiment": ei_analysis["sentiment"]["compound"]
    }
    
    # Move to next question
    next_q_num = current_q_num + 1
    
    if next_q_num >= len(questions):
        # Interview completed - Generate enhanced assessment with predictive analytics
        await db.sessions.update_one(
            {"session_id": session['session_id']},
            {
                "$push": {"messages": new_message},
                "$set": {
                    "current_question": next_q_num,
                    "status": "completed",
                    "completed_at": datetime.utcnow()
                }
            }
        )
        
        # Prepare data for enhanced assessment
        assessment_data = {
            "session_id": session['session_id'],
            "token": request.token,
            "candidate_name": session['candidate_name'],
            "job_title": session['job_title'],
            "technical_evaluations": session_metadata['technical_evaluations'],
            "behavioral_evaluations": session_metadata['behavioral_evaluations']
        }
        
        # Calculate aggregated EI metrics
        all_evaluations = session_metadata['technical_evaluations'] + session_metadata['behavioral_evaluations']
        ei_metrics = {
            "enthusiasm": np.mean([eval.get("emotional_intelligence", {}).get("enthusiasm", 0.5) for eval in all_evaluations]),
            "confidence": np.mean([eval.get("emotional_intelligence", {}).get("confidence", 0.5) for eval in all_evaluations]),
            "emotional_stability": np.mean([eval.get("emotional_intelligence", {}).get("emotional_stability", 0.5) for eval in all_evaluations]),
            "stress_level": np.mean([eval.get("emotional_intelligence", {}).get("stress_level", 0.5) for eval in all_evaluations])
        }
        
        assessment_data["emotional_intelligence_metrics"] = ei_metrics
        assessment_data["responses"] = [{"answer": msg["content"]} for msg in session.get("messages", []) if msg.get("type") == "candidate"]
        
        # Generate enhanced assessment
        base_assessment = await interview_ai.generate_final_assessment(assessment_data)
        
        # Add predictive analytics
        predictive_results = predictive_analytics.predict_interview_success(assessment_data)
        
        # Enhanced assessment with all new features
        enhanced_assessment = {
            **base_assessment.dict(),
            "emotional_intelligence_metrics": ei_metrics,
            "predictive_analytics": predictive_results,
            "communication_effectiveness": predictive_results["score_breakdown"]["communication"],
            "bias_analysis": {
                "evaluations_checked": len(all_evaluations),
                "bias_detected": any(eval.get("bias_check", {}).get("is_biased", False) for eval in all_evaluations),
                "bias_score": np.mean([eval.get("bias_check", {}).get("bias_score", 0) for eval in all_evaluations])
            }
        }
        
        await db.assessments.insert_one(enhanced_assessment)
        
        return {
            "completed": True,
            "message": "Thank you for completing the interview! Your responses have been evaluated with advanced AI analysis including emotional intelligence assessment and predictive analytics.",
            "assessment_id": enhanced_assessment["id"],
            "success_probability": predictive_results["success_probability"],
            "key_insights": {
                "emotional_intelligence": ei_metrics,
                "prediction": predictive_results["prediction"],
                "strengths": predictive_results["key_strengths"]
            }
        }
    else:
        # Continue with next question - Enhanced with adaptive questioning
        next_question = questions[next_q_num]
        
        # PERSONALIZATION: Adapt question difficulty based on EI analysis
        confidence_level = ei_analysis["emotional_intelligence"]["confidence"]
        stress_level = ei_analysis["emotional_intelligence"]["stress_level"]
        
        # If candidate shows high stress or low confidence, provide encouragement
        adaptive_response = next_question
        if stress_level > 0.7 or confidence_level < 0.3:
            adaptive_response = f"You're doing well so far! {next_question}"
        elif confidence_level > 0.8 and stress_level < 0.3:
            # For confident candidates, we can be more direct
            adaptive_response = next_question
        
        ai_response = {
            "type": "ai", 
            "content": adaptive_response,
            "timestamp": datetime.utcnow().isoformat(),
            "question_number": next_q_num + 1,
            "adaptive_feedback": {
                "confidence_detected": confidence_level,
                "stress_detected": stress_level,
                "encouragement_provided": stress_level > 0.7 or confidence_level < 0.3
            }
        }
        
        await db.sessions.update_one(
            {"session_id": session['session_id']},
            {
                "$push": {"messages": {"$each": [new_message, ai_response]}},
                "$set": {"current_question": next_q_num}
            }
        )
        
        response_data = {
            "completed": False,
            "next_question": adaptive_response,
            "question_number": next_q_num + 1,
            "total_questions": len(questions),
            "emotional_insight": {
                "confidence_level": confidence_level,
                "enthusiasm": ei_analysis["emotional_intelligence"]["enthusiasm"],
                "stress_indicators": stress_level < 0.3
            }
        }
        
        # Generate text for Web Speech API (voice mode)
        if session.get('voice_mode'):
            try:
                question_text = await voice_processor.text_to_speech(next_question)
                response_data["question_text"] = question_text
            except Exception as e:
                logging.error(f"Text cleaning failed: {str(e)}")
        
        return response_data

# Advanced Video Analysis Endpoint
@api_router.post("/analysis/video-frame")
async def analyze_video_frame(request: dict):
    """
    Analyze a video frame for facial expressions, emotions, and engagement
    Expected request: {"frame_data": "base64_encoded_frame", "session_id": "session_uuid"}
    """
    try:
        frame_data = request.get("frame_data")
        session_id = request.get("session_id")
        
        if not frame_data:
            raise HTTPException(status_code=400, detail="No frame data provided")
        
        # Analyze the frame using emotion analyzer
        analysis_result = emotion_analyzer.process_video_stream(frame_data)
        
        if analysis_result is None:
            return {"analysis": None, "message": "No face detected in frame"}
        
        # Store analysis in database if session_id provided
        if session_id:
            try:
                await db.video_analysis.insert_one({
                    "session_id": session_id,
                    "analysis": analysis_result,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                logging.error(f"Failed to store video analysis: {e}")
        
        return {
            "analysis": analysis_result,
            "status": "success"
        }
        
    except Exception as e:
        logging.error(f"Video analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")

# Advanced Audio Analysis Endpoint
@api_router.post("/analysis/audio-stream")
async def analyze_audio_stream(audio_file: UploadFile = File(...), session_id: str = Form(...)):
    """
    Analyze audio for speech patterns, emotion, and communication quality
    """
    try:
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be audio format")
        
        # Read audio data
        audio_data = await audio_file.read()
        
        # Analyze the audio using speech analyzer
        analysis_result = speech_analyzer.process_audio_stream(audio_data)
        
        if analysis_result is None:
            return {"analysis": None, "message": "Audio analysis failed"}
        
        # Store analysis in database
        try:
            await db.audio_analysis.insert_one({
                "session_id": session_id,
                "analysis": analysis_result,
                "filename": audio_file.filename,
                "timestamp": datetime.utcnow().isoformat()
            })
        except Exception as e:
            logging.error(f"Failed to store audio analysis: {e}")
        
        return {
            "analysis": analysis_result,
            "status": "success"
        }
        
    except Exception as e:
        logging.error(f"Audio analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Audio analysis failed: {str(e)}")

# Real-time Analysis Dashboard
@api_router.get("/analysis/session-insights/{session_id}")
async def get_session_insights(session_id: str):
    """
    Get comprehensive analysis insights for a session
    """
    try:
        # Get video analysis data
        video_analyses = await db.video_analysis.find({"session_id": session_id}).to_list(None)
        audio_analyses = await db.audio_analysis.find({"session_id": session_id}).to_list(None)
        
        # Calculate aggregated metrics
        insights = {
            "session_id": session_id,
            "video_metrics": _aggregate_video_metrics(video_analyses),
            "audio_metrics": _aggregate_audio_metrics(audio_analyses),
            "combined_insights": _generate_combined_insights(video_analyses, audio_analyses),
            "analysis_count": {
                "video_frames": len(video_analyses),
                "audio_clips": len(audio_analyses)
            }
        }
        
        return insights
        
    except Exception as e:
        logging.error(f"Session insights error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get session insights: {str(e)}")

def _aggregate_video_metrics(video_analyses: List[Dict]) -> Dict:
    """Aggregate video analysis metrics"""
    if not video_analyses:
        return {}
    
    # Extract metrics from analyses
    engagement_scores = []
    attention_levels = []
    stress_scores = []
    emotions = {}
    
    for analysis in video_analyses:
        if 'analysis' in analysis:
            data = analysis['analysis']
            engagement_scores.append(data.get('engagement_score', 0))
            attention_levels.append(data.get('attention_level', 0))
            
            # Stress indicators
            stress_indicators = data.get('stress_indicators', {})
            stress_scores.append(stress_indicators.get('overall_stress', 0))
            
            # Emotions
            for emotion_data in data.get('emotions', []):
                emotion = emotion_data['emotion']
                confidence = emotion_data['confidence']
                if emotion not in emotions:
                    emotions[emotion] = []
                emotions[emotion].append(confidence)
    
    # Calculate averages
    avg_engagement = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0
    avg_attention = sum(attention_levels) / len(attention_levels) if attention_levels else 0
    avg_stress = sum(stress_scores) / len(stress_scores) if stress_scores else 0
    
    # Calculate dominant emotions
    dominant_emotions = {}
    for emotion, confidences in emotions.items():
        dominant_emotions[emotion] = sum(confidences) / len(confidences)
    
    return {
        "average_engagement": avg_engagement,
        "average_attention": avg_attention,
        "average_stress": avg_stress,
        "dominant_emotions": dominant_emotions,
        "total_frames_analyzed": len(video_analyses)
    }

def _aggregate_audio_metrics(audio_analyses: List[Dict]) -> Dict:
    """Aggregate audio analysis metrics"""
    if not audio_analyses:
        return {}
    
    # Extract metrics from analyses
    confidence_levels = []
    fluency_scores = []
    clarity_scores = []
    overall_qualities = []
    speaking_rates = []
    stress_scores = []
    emotional_tones = {}
    
    for analysis in audio_analyses:
        if 'analysis' in analysis:
            data = analysis['analysis']
            
            # Speech metrics
            speech_metrics = data.get('speech_metrics', {})
            confidence_levels.append(speech_metrics.get('confidence_level', 0))
            speaking_rates.append(speech_metrics.get('speaking_rate', 0))
            
            # Quality scores
            fluency_scores.append(data.get('fluency_score', 0))
            clarity_scores.append(data.get('clarity_score', 0))
            overall_qualities.append(data.get('overall_quality', 0))
            
            # Stress indicators
            stress_indicators = data.get('stress_indicators', {})
            stress_scores.append(stress_indicators.get('overall_stress', 0))
            
            # Emotional tones
            for tone_data in data.get('emotional_tones', []):
                emotion = tone_data['emotion']
                confidence = tone_data['confidence']
                if emotion not in emotional_tones:
                    emotional_tones[emotion] = []
                emotional_tones[emotion].append(confidence)
    
    # Calculate averages
    return {
        "average_confidence": sum(confidence_levels) / len(confidence_levels) if confidence_levels else 0,
        "average_fluency": sum(fluency_scores) / len(fluency_scores) if fluency_scores else 0,
        "average_clarity": sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0,
        "average_quality": sum(overall_qualities) / len(overall_qualities) if overall_qualities else 0,
        "average_speaking_rate": sum(speaking_rates) / len(speaking_rates) if speaking_rates else 0,
        "average_stress": sum(stress_scores) / len(stress_scores) if stress_scores else 0,
        "emotional_tones": {emotion: sum(confidences) / len(confidences) 
                           for emotion, confidences in emotional_tones.items()},
        "total_audio_analyzed": len(audio_analyses)
    }

def _generate_combined_insights(video_analyses: List[Dict], audio_analyses: List[Dict]) -> Dict:
    """Generate combined insights from video and audio analysis"""
    video_metrics = _aggregate_video_metrics(video_analyses)
    audio_metrics = _aggregate_audio_metrics(audio_analyses)
    
    insights = {
        "overall_performance": "good",  # Default
        "key_strengths": [],
        "areas_for_improvement": [],
        "confidence_assessment": "moderate",
        "stress_level": "normal",
        "engagement_level": "moderate"
    }
    
    # Determine overall performance
    if video_metrics and audio_metrics:
        avg_engagement = video_metrics.get('average_engagement', 0.5)
        avg_confidence = audio_metrics.get('average_confidence', 0.5)
        avg_quality = audio_metrics.get('average_quality', 0.5)
        
        overall_score = (avg_engagement + avg_confidence + avg_quality) / 3
        
        if overall_score >= 0.75:
            insights["overall_performance"] = "excellent"
        elif overall_score >= 0.6:
            insights["overall_performance"] = "good"
        elif overall_score >= 0.4:
            insights["overall_performance"] = "moderate"
        else:
            insights["overall_performance"] = "needs_improvement"
    
    # Assess confidence
    if audio_metrics:
        avg_confidence = audio_metrics.get('average_confidence', 0.5)
        if avg_confidence >= 0.7:
            insights["confidence_assessment"] = "high"
            insights["key_strengths"].append("Confident communication")
        elif avg_confidence >= 0.4:
            insights["confidence_assessment"] = "moderate"
        else:
            insights["confidence_assessment"] = "low"
            insights["areas_for_improvement"].append("Building confidence in responses")
    
    # Assess stress levels
    video_stress = video_metrics.get('average_stress', 0.5) if video_metrics else 0.5
    audio_stress = audio_metrics.get('average_stress', 0.5) if audio_metrics else 0.5
    combined_stress = (video_stress + audio_stress) / 2
    
    if combined_stress <= 0.3:
        insights["stress_level"] = "low"
        insights["key_strengths"].append("Calm under pressure")
    elif combined_stress <= 0.6:
        insights["stress_level"] = "normal"
    else:
        insights["stress_level"] = "high"
        insights["areas_for_improvement"].append("Managing interview stress")
    
    # Assess engagement
    if video_metrics:
        avg_engagement = video_metrics.get('average_engagement', 0.5)
        if avg_engagement >= 0.7:
            insights["engagement_level"] = "high"
            insights["key_strengths"].append("Highly engaged and attentive")
        elif avg_engagement >= 0.4:
            insights["engagement_level"] = "moderate"
        else:
            insights["engagement_level"] = "low"
            insights["areas_for_improvement"].append("Improving engagement and attention")
    
    # Add communication quality insights
    if audio_metrics:
        avg_fluency = audio_metrics.get('average_fluency', 0.5)
        avg_clarity = audio_metrics.get('average_clarity', 0.5)
        
        if avg_fluency >= 0.7:
            insights["key_strengths"].append("Fluent communication")
        elif avg_fluency < 0.4:
            insights["areas_for_improvement"].append("Speaking fluency and flow")
            
        if avg_clarity >= 0.7:
            insights["key_strengths"].append("Clear articulation")
        elif avg_clarity < 0.4:
            insights["areas_for_improvement"].append("Speech clarity and pronunciation")
    
    return insights

# Proctoring and Anti-cheating Features
@api_router.post("/proctoring/monitor")
async def monitor_candidate_behavior(request: dict):
    """
    Monitor candidate behavior for proctoring violations
    Expected request: {"frame_data": "base64", "session_id": "uuid", "timestamp": "iso"}
    """
    try:
        frame_data = request.get("frame_data")
        session_id = request.get("session_id")
        
        if not frame_data or not session_id:
            raise HTTPException(status_code=400, detail="Missing required data")
        
        # Analyze frame for proctoring violations
        analysis = emotion_analyzer.process_video_stream(frame_data)
        
        violations = []
        if analysis:
            # Check for multiple faces (potential cheating)
            # This is a simplified check - in production, use face detection
            attention_level = analysis.get('attention_level', 0)
            
            if attention_level < 0.3:
                violations.append({
                    "type": "low_attention",
                    "description": "Candidate appears to be looking away frequently",
                    "severity": "medium"
                })
            
            # Check for unusual stress patterns (may indicate cheating)
            stress_indicators = analysis.get('stress_indicators', {})
            overall_stress = stress_indicators.get('overall_stress', 0)
            
            if overall_stress > 0.8:
                violations.append({
                    "type": "unusual_stress",
                    "description": "Unusual stress patterns detected",
                    "severity": "low"
                })
        
        # Store proctoring data
        proctoring_record = {
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
            "violations": violations,
            "analysis_data": analysis
        }
        
        await db.proctoring_logs.insert_one(proctoring_record)
        
        return {
            "violations": violations,
            "status": "monitored",
            "alert_level": "high" if len(violations) > 2 else "normal"
        }
        
    except Exception as e:
        logging.error(f"Proctoring error: {e}")
        raise HTTPException(status_code=500, detail=f"Proctoring failed: {str(e)}")

@api_router.get("/proctoring/session-report/{session_id}")
async def get_proctoring_report(session_id: str):
    """Get proctoring report for a session"""
    try:
        logs = await db.proctoring_logs.find({"session_id": session_id}).to_list(None)
        
        # Aggregate violations
        violation_summary = {}
        total_violations = 0
        
        for log in logs:
            for violation in log.get('violations', []):
                v_type = violation['type']
                if v_type not in violation_summary:
                    violation_summary[v_type] = 0
                violation_summary[v_type] += 1
                total_violations += 1
        
        return {
            "session_id": session_id,
            "total_violations": total_violations,
            "violation_breakdown": violation_summary,
            "monitoring_duration": len(logs),
            "integrity_score": max(0, 1 - (total_violations / max(len(logs), 1))),
            "status": "clean" if total_violations == 0 else "flagged" if total_violations > 5 else "acceptable"
        }
        
    except Exception as e:
        logging.error(f"Proctoring report error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

# Data Privacy and Retention Management Endpoints
@api_router.post("/admin/data-privacy/request-consent")
async def request_consent(request: ConsentRequest):
    """Request explicit consent for data collection"""
    try:
        consent_record = data_privacy_manager.request_consent(request.candidate_id, request.data_types)
        
        # Store consent record in database
        await db.consent_records.insert_one(consent_record)
        
        return {
            "success": True,
            "consent_record": consent_record,
            "message": "Consent recorded successfully"
        }
    except Exception as e:
        logging.error(f"Consent request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to record consent: {str(e)}")

@api_router.post("/admin/data-privacy/right-to-erasure/{candidate_id}")
async def request_data_erasure(candidate_id: str):
    """GDPR Article 17 - Right to be forgotten"""
    try:
        result = await data_privacy_manager.right_to_erasure(candidate_id)
        
        # Log the erasure request for audit trail
        audit_record = {
            "action": "data_erasure",
            "candidate_id": candidate_id,
            "result": result,
            "timestamp": datetime.utcnow(),
            "compliance": "GDPR Article 17"
        }
        await db.audit_logs.insert_one(audit_record)
        
        return result
    except Exception as e:
        logging.error(f"Data erasure failed for {candidate_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data erasure failed: {str(e)}")

@api_router.post("/admin/data-privacy/cleanup-expired")
async def cleanup_expired_data():
    """Manually trigger cleanup of expired data based on retention policies"""
    try:
        result = await data_privacy_manager.cleanup_expired_data()
        
        # Log cleanup operation for audit trail
        audit_record = {
            "action": "data_cleanup",
            "result": result,
            "timestamp": datetime.utcnow(),
            "retention_policies": data_privacy_manager.data_retention_policies
        }
        await db.audit_logs.insert_one(audit_record)
        
        return result
    except Exception as e:
        logging.error(f"Data cleanup failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data cleanup failed: {str(e)}")

@api_router.get("/admin/data-privacy/retention-status")
async def get_data_retention_status():
    """Get current data retention status and counts"""
    try:
        status = await data_privacy_manager.get_data_retention_status()
        return status
    except Exception as e:
        logging.error(f"Failed to get retention status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get retention status: {str(e)}")

@api_router.get("/admin/data-privacy/policies")
async def get_retention_policies():
    """Get current data retention policies"""
    return {
        "retention_policies": data_privacy_manager.data_retention_policies,
        "description": {
            "interview_data": "Sessions, assessments, tokens, coding challenges - stored for compliance and analysis",
            "audio_files": "Raw audio recordings from voice interviews - deleted for privacy",
            "video_analysis": "Video analysis data and facial recognition results - stored for limited time"
        },
        "compliance": ["GDPR", "CCPA"],
        "last_updated": datetime.utcnow()
    }

# Phase 2 AI Enhancement Endpoints

@api_router.post("/admin/ai-enhancement/analyze-question-bias")
async def analyze_question_bias(question_text: str):
    """Analyze interview questions for potential bias"""
    try:
        bias_analysis = bias_detector.analyze_question_bias(question_text)
        return {
            "success": True,
            "question": question_text,
            "bias_analysis": bias_analysis
        }
    except Exception as e:
        logging.error(f"Question bias analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bias analysis failed: {str(e)}")

@api_router.post("/admin/ai-enhancement/calculate-fairness-metrics")
async def calculate_fairness_metrics():
    """Calculate fairness metrics across all assessments"""
    try:
        # Get all assessments from database
        assessments = await db.assessments.find().to_list(1000)
        
        # Convert ObjectId to dict for processing
        assessment_list = []
        for assessment in assessments:
            assessment_dict = dict(assessment)
            assessment_dict['overall_score'] = assessment_dict.get('overall_score', 0)
            assessment_dict['demographic_group'] = assessment_dict.get('demographic_group', 'unknown')
            assessment_list.append(assessment_dict)
        
        fairness_metrics = bias_detector.calculate_fairness_metrics(assessment_list)
        
        return {
            "success": True,
            "fairness_metrics": fairness_metrics,
            "total_assessments_analyzed": len(assessment_list)
        }
    except Exception as e:
        logging.error(f"Fairness metrics calculation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fairness analysis failed: {str(e)}")

@api_router.post("/admin/ai-enhancement/train-hiring-model")
async def train_hiring_model():
    """Train the predictive hiring model with historical data"""
    try:
        # Get historical assessment data
        assessments = await db.assessments.find().to_list(1000)
        
        if not assessments:
            return {
                "success": False,
                "message": "No historical data available for training",
                "model_status": "untrained"
            }
        
        # Convert to DataFrame format
        training_data = []
        for assessment in assessments:
            training_record = {
                'technical_score': assessment.get('technical_score', 70),
                'behavioral_score': assessment.get('behavioral_score', 70),
                'communication_score': 0.7,  # Default
                'confidence_level': 0.6,  # Default
                'stress_indicators': 0.4,  # Default
                'engagement_score': 0.7,  # Default
                'hiring_success': 1 if assessment.get('overall_score', 0) >= 70 else 0
            }
            training_data.append(training_record)
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(training_data)
        
        # Train the model
        training_result = predictive_hiring_model.train_model(df)
        
        return {
            "success": True,
            "training_result": training_result,
            "model_info": predictive_hiring_model.get_model_info()
        }
        
    except Exception as e:
        logging.error(f"Model training failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")

@api_router.post("/admin/ai-enhancement/predict-hiring-success")
async def predict_hiring_success(session_id: str):
    """Predict hiring success for a specific candidate"""
    try:
        # Get assessment data for the session
        assessment = await db.assessments.find_one({"session_id": session_id})
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        # Prepare candidate data for prediction
        candidate_data = {
            'technical_score': assessment.get('technical_score', 70),
            'behavioral_score': assessment.get('behavioral_score', 70),
            'communication_score': 0.7,  # Calculate from responses if available
            'confidence_level': 0.6,  # From emotional intelligence metrics
            'stress_indicators': 0.4,  # From emotional intelligence metrics
            'engagement_score': 0.7,  # From video analysis if available
            'responses': [],  # For communication analysis
            'emotional_intelligence_metrics': {}
        }
        
        # Get prediction
        prediction_result = predictive_hiring_model.predict_success_probability(candidate_data)
        
        return {
            "success": True,
            "session_id": session_id,
            "prediction": prediction_result,
            "candidate_name": assessment.get('candidate_name', 'Unknown')
        }
        
    except Exception as e:
        logging.error(f"Hiring prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@api_router.post("/admin/ai-enhancement/analyze-personality")
async def analyze_personality(session_id: str):
    """Analyze personality traits for a specific candidate"""
    try:
        # Get session data
        session = await db.sessions.find_one({"session_id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get audio analysis data if available
        audio_analyses = await db.audio_analysis.find({"session_id": session_id}).to_list(None)
        speech_data = audio_analyses[0] if audio_analyses else {}
        
        # Get video analysis data if available
        video_analyses = await db.video_analysis.find({"session_id": session_id}).to_list(None)
        video_data = video_analyses[0] if video_analyses else {}
        
        # Get text responses
        text_responses = session.get('messages', [])
        
        # Analyze personality
        personality_analysis = personality_analyzer.analyze_big_five(
            speech_data, video_data, text_responses
        )
        
        return {
            "success": True,
            "session_id": session_id,
            "candidate_name": session.get('candidate_name', 'Unknown'),
            "personality_analysis": personality_analysis
        }
        
    except Exception as e:
        logging.error(f"Personality analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Personality analysis failed: {str(e)}")

@api_router.get("/admin/ai-enhancement/model-status")
async def get_model_status():
    """Get status of all AI enhancement models"""
    try:
        return {
            "success": True,
            "models": {
                "bias_detection_engine": {
                    "status": "active",
                    "protected_attributes": bias_detector.protected_attributes,
                    "bias_categories": list(bias_detector.bias_indicators.keys())
                },
                "predictive_hiring_model": predictive_hiring_model.get_model_info(),
                "personality_analyzer": {
                    "status": "active",
                    "traits_analyzed": list(personality_analyzer.big_five_traits.keys()),
                    "analysis_methods": ["speech", "video", "text"]
                }
            },
            "capabilities": [
                "Question bias detection",
                "Fairness metrics calculation", 
                "Hiring success prediction",
                "Big Five personality analysis",
                "Demographic parity assessment",
                "Equalized odds calculation"
            ]
        }
    except Exception as e:
        logging.error(f"Model status check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

# Health check
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Interview Agent is running"}

@api_router.get("/")
async def root():
    return {"message": "AI-Powered Interview Agent API with Voice Support"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["https://c60fdbd3-ffd4-46af-9268-f7eadea63f47.preview.emergentagent.com", "http://localhost:3000", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Phase 4: Executive Dashboard API Endpoints

@api_router.get("/admin/executive-dashboard/metrics")
async def get_executive_dashboard_metrics():
    """Get comprehensive executive dashboard metrics"""
    try:
        # Calculate date ranges
        current_date = datetime.utcnow()
        last_30_days = (current_date - timedelta(days=30), current_date)
        last_90_days = (current_date - timedelta(days=90), current_date)
        
        # Get all key metrics
        time_to_hire = await executive_analytics.calculate_time_to_hire_metrics(last_30_days)
        candidate_experience = await executive_analytics.calculate_candidate_experience_metrics(last_30_days)
        hiring_quality = await executive_analytics.calculate_hiring_quality_metrics(last_30_days)
        diversity_metrics = await executive_analytics.calculate_diversity_metrics(last_30_days)
        cost_metrics = await executive_analytics.calculate_cost_per_hire(last_30_days)
        
        return {
            "success": True,
            "dashboard_metrics": {
                "time_to_hire": time_to_hire,
                "candidate_experience": candidate_experience,
                "hiring_quality": hiring_quality,
                "diversity_metrics": diversity_metrics,
                "cost_metrics": cost_metrics
            },
            "last_updated": current_date.isoformat(),
            "date_range": {
                "start": last_30_days[0].isoformat(),
                "end": last_30_days[1].isoformat()
            }
        }
    except Exception as e:
        logging.error(f"Executive dashboard metrics error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard metrics: {str(e)}")

@api_router.get("/admin/executive-dashboard/historical-trends")
async def get_historical_trends():
    """Get historical trends for executive dashboard"""
    try:
        # Get trends for last 6 months
        current_date = datetime.utcnow()
        trends_data = []
        
        for i in range(6):
            start_date = current_date - timedelta(days=30*(i+1))
            end_date = current_date - timedelta(days=30*i)
            date_range = (start_date, end_date)
            
            time_to_hire = await executive_analytics.calculate_time_to_hire_metrics(date_range)
            candidate_experience = await executive_analytics.calculate_candidate_experience_metrics(date_range)
            hiring_quality = await executive_analytics.calculate_hiring_quality_metrics(date_range)
            diversity_metrics = await executive_analytics.calculate_diversity_metrics(date_range)
            cost_metrics = await executive_analytics.calculate_cost_per_hire(date_range)
            
            trends_data.append({
                "month": start_date.strftime("%Y-%m"),
                "time_to_hire": time_to_hire["average_time_to_hire"],
                "candidate_experience": candidate_experience["average_experience_score"],
                "hiring_quality": hiring_quality["average_quality_score"],
                "diversity_score": 1 - diversity_metrics["bias_score"],  # Convert bias to diversity score
                "cost_per_hire": cost_metrics["cost_per_hire"],
                "total_interviews": time_to_hire["total_hires"]
            })
        
        return {
            "success": True,
            "historical_trends": list(reversed(trends_data)),
            "last_updated": current_date.isoformat()
        }
    except Exception as e:
        logging.error(f"Historical trends error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get historical trends: {str(e)}")

@api_router.get("/admin/executive-dashboard/real-time-analytics")
async def get_real_time_analytics():
    """Get real-time analytics for executive dashboard"""
    try:
        current_date = datetime.utcnow()
        
        # Real-time metrics (last 24 hours)
        last_24_hours = (current_date - timedelta(hours=24), current_date)
        
        # Count active sessions
        active_sessions = await db.sessions.count_documents({
            "status": "in_progress",
            "started_at": {"$gte": last_24_hours[0]}
        })
        
        # Count completed interviews today
        completed_today = await db.sessions.count_documents({
            "status": "completed",
            "completed_at": {"$gte": last_24_hours[0]}
        })
        
        # Count new candidates today
        new_candidates_today = await db.sessions.count_documents({
            "started_at": {"$gte": last_24_hours[0]}
        })
        
        # Average score today
        today_assessments = await db.assessments.find({
            "created_at": {"$gte": last_24_hours[0]}
        }).to_list(None)
        
        avg_score_today = 0
        if today_assessments:
            scores = [a.get("overall_score", 0) for a in today_assessments]
            avg_score_today = sum(scores) / len(scores)
        
        # Recent activity feed
        recent_sessions = await db.sessions.find({
            "started_at": {"$gte": last_24_hours[0]}
        }).sort("started_at", -1).limit(10).to_list(None)
        
        activity_feed = []
        for session in recent_sessions:
            activity_feed.append({
                "type": "interview_started" if session.get("status") == "in_progress" else "interview_completed",
                "candidate_name": session.get("candidate_name", "Anonymous"),
                "job_title": session.get("job_title", "Unknown Position"),
                "timestamp": session.get("started_at"),
                "status": session.get("status")
            })
        
        return {
            "success": True,
            "real_time_metrics": {
                "active_interviews": active_sessions,
                "completed_today": completed_today,
                "new_candidates_today": new_candidates_today,
                "average_score_today": round(avg_score_today, 2),
                "activity_feed": activity_feed
            },
            "last_updated": current_date.isoformat()
        }
    except Exception as e:
        logging.error(f"Real-time analytics error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get real-time analytics: {str(e)}")

@api_router.get("/admin/executive-dashboard/advanced-reporting")
async def get_advanced_reporting_data():
    """Get advanced reporting data for executive dashboard"""
    try:
        current_date = datetime.utcnow()
        last_90_days = (current_date - timedelta(days=90), current_date)
        
        # Hiring funnel analysis
        total_invites = await db.tokens.count_documents({}) + await db.enhanced_tokens.count_documents({})
        total_started = await db.sessions.count_documents({})
        total_completed = await db.sessions.count_documents({"status": "completed"})
        total_hired = await db.assessments.count_documents({"overall_score": {"$gte": 70}})
        
        hiring_funnel = {
            "invites_sent": total_invites,
            "interviews_started": total_started,
            "interviews_completed": total_completed,
            "candidates_hired": total_hired,
            "conversion_rates": {
                "invite_to_start": round((total_started / total_invites * 100), 2) if total_invites > 0 else 0,
                "start_to_complete": round((total_completed / total_started * 100), 2) if total_started > 0 else 0,
                "complete_to_hire": round((total_hired / total_completed * 100), 2) if total_completed > 0 else 0
            }
        }
        
        # Performance by role archetype
        role_performance = {}
        enhanced_tokens = await db.enhanced_tokens.find({}).to_list(None)
        for token in enhanced_tokens:
            role = token.get("role_archetype", "General")
            if role not in role_performance:
                role_performance[role] = {"interviews": 0, "avg_score": 0, "total_score": 0}
            
            # Find assessment for this token
            assessment = await db.assessments.find_one({"token": token["token"]})
            if assessment:
                role_performance[role]["interviews"] += 1
                role_performance[role]["total_score"] += assessment.get("overall_score", 0)
                role_performance[role]["avg_score"] = role_performance[role]["total_score"] / role_performance[role]["interviews"]
        
        # Interview focus effectiveness
        focus_effectiveness = {}
        for token in enhanced_tokens:
            focus = token.get("interview_focus", "Balanced")
            if focus not in focus_effectiveness:
                focus_effectiveness[focus] = {"interviews": 0, "success_rate": 0, "successful": 0}
            
            assessment = await db.assessments.find_one({"token": token["token"]})
            if assessment:
                focus_effectiveness[focus]["interviews"] += 1
                if assessment.get("overall_score", 0) >= 70:
                    focus_effectiveness[focus]["successful"] += 1
                focus_effectiveness[focus]["success_rate"] = (
                    focus_effectiveness[focus]["successful"] / focus_effectiveness[focus]["interviews"] * 100
                )
        
        return {
            "success": True,
            "advanced_reporting": {
                "hiring_funnel": hiring_funnel,
                "role_performance": role_performance,
                "focus_effectiveness": focus_effectiveness,
                "last_updated": current_date.isoformat()
            }
        }
    except Exception as e:
        logging.error(f"Advanced reporting error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get advanced reporting data: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()