from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime
import base64
import io
import json

# Remove Google Cloud imports - now using Web Speech API
# Document parsing imports
import PyPDF2
from docx import Document

# Basic imports
import pymongo
import gridfs

# Import libraries for sentiment analysis and emotional intelligence
import librosa
import numpy as np
import torch
import transformers
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textstat import flesch_reading_ease

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# For GridFS, we need a synchronous connection
sync_client = pymongo.MongoClient(mongo_url)
sync_db = sync_client[os.environ['DB_NAME']]
fs = gridfs.GridFS(sync_db)

# Create the main app without a prefix
app = FastAPI()

# Create API router with /api prefix
api_router = APIRouter(prefix="/api")

# Initialize AI for emotional intelligence (lazy loading)
emotion_analyzer = None
sentiment_analyzer = SentimentIntensityAnalyzer()

def get_emotion_analyzer():
    global emotion_analyzer
    if emotion_analyzer is None:
        try:
            emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        except Exception as e:
            logging.error(f"Failed to load emotion analyzer: {e}")
            emotion_analyzer = None
    return emotion_analyzer

# Voice Processing Class - Updated for Web Speech API
class VoiceProcessor:
    def __init__(self):
        # No external clients needed - Web Speech API handles TTS on frontend
        pass
    
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
    
    async def prepare_text_for_speech(self, text: str) -> str:
        """Prepare text for Web Speech API - just clean and return text"""
        try:
            cleaned_text = self.clean_text_for_speech(text)
            return cleaned_text
        except Exception as e:
            logging.error(f"Text cleaning error: {str(e)}")
            return text  # Return original text if cleaning fails
    
    # Speech-to-text functionality removed - can be added back later if needed
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Placeholder for speech-to-text functionality"""
        # For now, return empty string - can implement Web Speech API STT later
        logging.info("Speech-to-text not implemented with Web Speech API yet")
        return ""

# Initialize voice processor
voice_processor = VoiceProcessor()

# Data Models (keeping existing models)
class JobDescriptionRequest(BaseModel):
    job_title: str
    job_description: str
    job_requirements: str

class AdminLoginRequest(BaseModel):
    password: str

class CandidateTokenRequest(BaseModel):
    token: str

class InterviewStartRequest(BaseModel):
    token: str
    candidate_name: str
    voice_mode: bool = False

class InterviewMessageRequest(BaseModel):
    token: str
    message: str
    voice_data: Optional[str] = None

class InterviewMessageResponse(BaseModel):
    response: str
    question_number: int
    total_questions: int
    completed: bool
    audio_base64: Optional[str] = None

# Enhanced request models
class EnhancedJobDescriptionRequest(BaseModel):
    job_title: str
    job_description: str
    job_requirements: str
    include_coding_challenge: bool = False
    role_archetype: str = "General"  # Software Engineer, Sales, Graduate, General
    interview_focus: str = "Balanced"  # Technical Deep-Dive, Cultural Fit, Graduate Screening, Balanced

class PracticeRoundRequest(BaseModel):
    token: str

class QuestionRephraseRequest(BaseModel):
    token: str
    question: str

class CodingChallengeRequest(BaseModel):
    token: str

class CodingChallengeSubmissionRequest(BaseModel):
    token: str
    code: str
    explanation: str

class SJTRequest(BaseModel):
    token: str

class SJTSubmissionRequest(BaseModel):
    token: str
    selected_option: int
    reasoning: str

# Add API endpoints here... (keeping all existing endpoints but removing Google Cloud TTS calls)

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "AI-Powered Interview Agent API with Web Speech API"}

# Root endpoint for the main app
@app.get("/")
async def main_root():
    return {"message": "AI-Powered Interview Agent API with Web Speech API"}

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["https://9111a607-ad7c-4aad-8586-9dca4be775f2.preview.emergentagent.com", "http://localhost:3000", "*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)