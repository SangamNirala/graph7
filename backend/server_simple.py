from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form
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
from google.cloud import texttospeech, speech
from google.oauth2 import service_account
import pymongo
import gridfs

# Simplified sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

# Google Cloud Setup
credentials_json = json.loads(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '{}'))
credentials = service_account.Credentials.from_service_account_info(credentials_json)
tts_client = texttospeech.TextToSpeechClient(credentials=credentials)
stt_client = speech.SpeechClient(credentials=credentials)

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

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

class EnhancedCandidateToken(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    token: str
    job_id: str
    resume_content: str
    job_description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    used: bool = False
    include_coding_challenge: bool = False
    role_archetype: str = "General"
    interview_focus: str = "Balanced"
    estimated_duration: int = 30
    min_questions: int = 8
    max_questions: int = 12

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
    status: str = "in_progress"
    voice_mode: bool = False

class AdminLoginRequest(BaseModel):
    password: str

class TokenValidationRequest(BaseModel):
    token: str

class InterviewStartRequest(BaseModel):
    token: str
    candidate_name: str
    voice_mode: Optional[bool] = False

class InterviewMessageRequest(BaseModel):
    token: str
    message: str

class CameraTestRequest(BaseModel):
    token: str

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
        try:
            return content.decode('utf-8')
        except:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF, DOC, DOCX, or TXT files.")

# Initialize sentiment analysis tools
analyzer = SentimentIntensityAnalyzer()

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
    
    async def generate_interview_questions(self, resume: str, job_description: str, role_archetype: str = "General", interview_focus: str = "Balanced", min_questions: int = 8, max_questions: int = 12) -> List[str]:
        role_context = self._get_role_context(role_archetype)
        focus_context = self._get_focus_context(interview_focus)
        
        total_questions = min_questions
        technical_count = (total_questions + 1) // 2
        behavioral_count = total_questions - technical_count
        
        question_format = "Generate questions in this exact format:\n"
        for i in range(1, technical_count + 1):
            question_format += f"TECHNICAL_{i}: [question]\n"
        for i in range(1, behavioral_count + 1):
            question_format += f"BEHAVIORAL_{i}: [question]\n"
        
        system_message = f"""You are an expert AI interviewer conducting a fair and unbiased interview.
        
        Role Archetype: {role_archetype}
        Interview Focus: {interview_focus}
        
        {role_context}
        {focus_context}

        IMPORTANT: Generate questions in plain text without any formatting like backticks, bold, or italics since these will be converted to speech.
        
        You need to generate exactly {total_questions} questions ({technical_count} technical, {behavioral_count} behavioral).

        Resume: {resume}
        Job Description: {job_description}

        {question_format}"""
        
        session_id = self.generate_session_id()
        chat = await self.create_chat_instance(session_id, system_message)
        
        user_message = UserMessage(text="Generate the interview questions based on the resume and job description.")
        response = await chat.send_message(user_message)
        
        questions = []
        lines = response.split('\n')
        for line in lines:
            if line.startswith(('TECHNICAL_', 'BEHAVIORAL_')):
                question = line.split(': ', 1)[1] if ': ' in line else line
                questions.append(question.strip())
        
        return questions[:total_questions]
    
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
    
    async def evaluate_answer(self, question: str, answer: str, question_type: str) -> Dict[str, Any]:
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
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response[start:end]
                evaluation = json.loads(json_str)
                return evaluation
        except:
            pass
        
        return {
            "score": 7,
            "feedback": "Answer provided shows understanding of the topic.",
            "strengths": ["Shows knowledge"],
            "improvements": ["Could provide more specific examples"]
        }

# Voice Processing Class
class VoiceProcessor:
    def __init__(self):
        self.use_web_speech = True
        logging.info("VoiceProcessor initialized for Web Speech API")
    
    def clean_text_for_speech(self, text: str) -> str:
        """Clean text for better TTS pronunciation by removing formatting characters"""
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        text = re.sub(r'~~([^~]+)~~', r'\1', text)
        
        text = text.replace('HTML', 'H-T-M-L')
        text = text.replace('CSS', 'C-S-S')
        text = text.replace('JavaScript', 'Java Script')
        text = text.replace('APIs', 'A-P-Is')
        text = text.replace('API', 'A-P-I')
        text = text.replace('JSON', 'J-S-O-N')
        text = text.replace('SQL', 'S-Q-L')
        
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    async def text_to_speech(self, text: str) -> str:
        """Prepare text for Web Speech API - return cleaned text instead of audio"""
        try:
            cleaned_text = self.clean_text_for_speech(text)
            return cleaned_text
        except Exception as e:
            logging.error(f"Text cleaning error: {str(e)}")
            return text

# Initialize engines
interview_ai = InterviewAI()
voice_processor = VoiceProcessor()

# Helper Functions
def generate_secure_token() -> str:
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin Routes
@api_router.post("/admin/login")
async def admin_login(request: AdminLoginRequest):
    if request.password != "Game@1234":
        raise HTTPException(status_code=401, detail="Invalid password")
    return {"success": True, "message": "Admin authenticated successfully"}

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
    resume_file: UploadFile = File(...)
):
    resume_content = await resume_file.read()
    try:
        resume_text = parse_resume(resume_file, resume_content)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from resume file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Resume parsing failed: {str(e)}")
    
    job_data = JobDescription(
        title=job_title,
        description=job_description,
        requirements=job_requirements
    )
    await db.jobs.insert_one(job_data.dict())
    
    token = generate_secure_token()
    
    token_data = EnhancedCandidateToken(
        token=token,
        job_id=job_data.id,
        resume_content=resume_text,
        job_description=f"{job_title}\n\n{job_description}\n\n{job_requirements}",
        include_coding_challenge=include_coding_challenge,
        role_archetype=role_archetype,
        interview_focus=interview_focus,
        min_questions=min_questions,
        max_questions=max_questions
    )
    await db.enhanced_tokens.insert_one(token_data.dict())
    
    base_duration = max_questions * 3
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

# Candidate Routes
@api_router.post("/candidate/validate-token")
async def validate_token(request: TokenValidationRequest):
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

@api_router.post("/candidate/camera-test")
async def camera_test(request: CameraTestRequest):
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

@api_router.post("/candidate/start-interview")
async def start_interview(request: InterviewStartRequest):
    token_data = await db.enhanced_tokens.find_one({"token": request.token})
    is_enhanced = True
    
    if not token_data:
        token_data = await db.tokens.find_one({"token": request.token})
        is_enhanced = False
    
    if not token_data or token_data.get('used', False):
        raise HTTPException(status_code=401, detail="Invalid or used token")
    
    job_data = await db.jobs.find_one({"id": token_data['job_id']})
    
    if is_enhanced:
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
            token_data['job_description']
        )
    
    session_id = str(uuid.uuid4())
    
    # Calculate technical and behavioral counts
    total_questions = len(questions)
    technical_count = (total_questions + 1) // 2
    behavioral_count = total_questions - technical_count
    
    session_data = InterviewSession(
        token=request.token,
        session_id=session_id,
        candidate_name=request.candidate_name,
        job_title=job_data['title'] if job_data else "Software Developer",
        voice_mode=request.voice_mode or False
    )
    
    session_dict = session_data.dict()
    session_dict['questions'] = questions
    session_dict['total_questions'] = total_questions
    session_dict['technical_count'] = technical_count
    session_dict['behavioral_count'] = behavioral_count
    session_dict['is_enhanced'] = is_enhanced
    
    await db.sessions.insert_one(session_dict)
    
    # Mark token as used
    if is_enhanced:
        await db.enhanced_tokens.update_one(
            {"token": request.token},
            {"$set": {"used": True}}
        )
    else:
        await db.tokens.update_one(
            {"token": request.token},
            {"$set": {"used": True}}
        )
    
    first_question = questions[0] if questions else "Tell me about yourself."
    
    response_data = {
        "session_id": session_id,
        "first_question": first_question,
        "question_number": 1,
        "total_questions": total_questions,
        "voice_mode": request.voice_mode or False,
        "is_enhanced": is_enhanced
    }
    
    if request.voice_mode:
        try:
            cleaned_question = await voice_processor.text_to_speech(first_question)
            response_data["question_text"] = cleaned_question
        except Exception as e:
            logging.error(f"Text cleaning failed: {str(e)}")
            response_data["question_text"] = first_question
    
    return response_data

@api_router.post("/candidate/send-message")
async def send_message(request: InterviewMessageRequest):
    session = await db.sessions.find_one({"token": request.token})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    questions = session.get('questions', [])
    current_question_num = session.get('current_question', 0)
    total_questions = len(questions)
    
    if current_question_num >= total_questions:
        return {"completed": True, "message": "Interview completed"}
    
    # Get current question and determine type
    current_question = questions[current_question_num]
    technical_count = session.get('technical_count', (total_questions + 1) // 2)
    question_type = "technical" if current_question_num < technical_count else "behavioral"
    
    # Evaluate the answer
    evaluation = await interview_ai.evaluate_answer(current_question, request.message, question_type)
    
    # Store the message and evaluation
    message_data = {
        "question": current_question,
        "answer": request.message,
        "question_number": current_question_num + 1,
        "question_type": question_type,
        "evaluation": evaluation,
        "timestamp": datetime.utcnow()
    }
    
    await db.sessions.update_one(
        {"token": request.token},
        {
            "$push": {"messages": message_data},
            "$set": {"current_question": current_question_num + 1}
        }
    )
    
    # Check if interview is completed
    if current_question_num + 1 >= total_questions:
        await db.sessions.update_one(
            {"token": request.token},
            {"$set": {"status": "completed", "completed_at": datetime.utcnow()}}
        )
        return {"completed": True, "message": "Interview completed successfully"}
    
    # Get next question
    next_question = questions[current_question_num + 1]
    
    response_data = {
        "next_question": next_question,
        "question_number": current_question_num + 2,
        "total_questions": total_questions,
        "completed": False
    }
    
    if session.get('voice_mode'):
        try:
            cleaned_question = await voice_processor.text_to_speech(next_question)
            response_data["question_text"] = cleaned_question
        except Exception as e:
            logging.error(f"Text cleaning failed: {str(e)}")
            response_data["question_text"] = next_question
    
    return response_data

# Include the router
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)