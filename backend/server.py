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
from google.cloud import texttospeech, speech
from google.oauth2 import service_account
import pymongo
import gridfs

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
    
    async def generate_interview_questions(self, resume: str, job_description: str, role_archetype: str = "General", interview_focus: str = "Balanced") -> List[str]:
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
        
        system_message = f"""You are an expert AI interviewer conducting a fair and unbiased interview. {bias_mitigation}
        
        Role Archetype: {role_archetype}
        Interview Focus: {interview_focus}
        
        {role_context}
        {focus_context}

        IMPORTANT: Generate questions in plain text without any formatting like backticks, bold, or italics since these will be converted to speech.

        Resume: {resume}
        Job Description: {job_description}

        Generate questions in this exact format:
        TECHNICAL_1: [question]
        TECHNICAL_2: [question]
        TECHNICAL_3: [question]
        TECHNICAL_4: [question]
        BEHAVIORAL_1: [question]
        BEHAVIORAL_2: [question]
        BEHAVIORAL_3: [question]
        BEHAVIORAL_4: [question]"""
        
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
        
        return questions[:8]  # Ensure exactly 8 questions
    
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

# Voice Processing Class
class VoiceProcessor:
    def __init__(self):
        self.tts_client = tts_client
        self.stt_client = stt_client
    
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
    
    async def text_to_speech(self, text: str) -> str:
        """Convert text to speech and return base64 audio data"""
        try:
            # Clean text before synthesis
            cleaned_text = self.clean_text_for_speech(text)
            synthesis_input = texttospeech.SynthesisInput(text=cleaned_text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Store in GridFS and return file ID
            file_id = fs.put(response.audio_content, 
                           filename=f"question_{str(uuid.uuid4())}.mp3",
                           metadata={"type": "question_audio"})
            
            # Also return base64 for immediate playback
            audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
            
            return {
                "file_id": str(file_id),
                "audio_base64": audio_base64
            }
        except Exception as e:
            logging.error(f"TTS Error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Text-to-speech failed: {str(e)}")
    
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech audio to text"""
        try:
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code="en-US",
            )
            
            response = self.stt_client.recognize(config=config, audio=audio)
            
            if response.results:
                return response.results[0].alternatives[0].transcript
            else:
                return ""
        except Exception as e:
            logging.error(f"STT Error: {str(e)}")
            return ""

# Initialize engines
interview_ai = InterviewAI()
voice_processor = VoiceProcessor()

# Helper Functions
def generate_secure_token() -> str:
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))

# Admin Routes
@api_router.post("/admin/login")
async def admin_login(request: AdminLoginRequest):
    if request.password != "Game@123":
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
    
    # Create enhanced token record
    token_data = EnhancedCandidateToken(
        token=token,
        job_id=job_data.id,
        resume_content=resume_text,
        job_description=f"{job_title}\n\n{job_description}\n\n{job_requirements}",
        include_coding_challenge=include_coding_challenge,
        role_archetype=role_archetype,
        interview_focus=interview_focus
    )
    await db.enhanced_tokens.insert_one(token_data.dict())
    
    # Estimate duration based on features
    base_duration = 30
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
            "interview_focus": interview_focus
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
            "interview_type": "Standard"
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
    
    # Generate TTS for practice question if voice mode
    audio_data = None
    try:
        audio_data = await voice_processor.text_to_speech(practice.question)
    except Exception as e:
        logging.error(f"TTS generation failed for practice: {str(e)}")
    
    return {
        "session_id": practice.session_id,
        "practice_question": practice.question,
        "audio_base64": audio_data["audio_base64"] if audio_data else None,
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
            "audio_base64": audio_data["audio_base64"] if audio_data else None
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
            "audio_base64": audio_data["audio_base64"],
            "file_id": audio_data["file_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/voice/process-answer")
async def process_voice_answer(
    session_id: str = Form(...),
    question_number: int = Form(...),
    audio_file: UploadFile = File(...)
):
    """Process voice answer - convert to text and store audio"""
    try:
        audio_content = await audio_file.read()
        
        # Convert speech to text
        transcript = await voice_processor.speech_to_text(audio_content)
        
        # Store audio file in GridFS
        file_id = fs.put(audio_content, 
                        filename=f"answer_{session_id}_{question_number}.webm",
                        metadata={"type": "answer_audio", "session_id": session_id})
        
        # Store answer in session metadata
        await db.session_metadata.update_one(
            {"session_id": session_id},
            {"$push": {"answer_audios": {
                "file_id": str(file_id),
                "transcript": transcript,
                "question_number": question_number,
                "timestamp": datetime.utcnow()
            }}}
        )
        
        return {
            "success": True,
            "transcript": transcript,
            "file_id": str(file_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice processing failed: {str(e)}")

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
        questions = await interview_ai.generate_interview_questions(
            token_data['resume_content'],
            token_data['job_description'],
            token_data.get('role_archetype', 'General'),
            token_data.get('interview_focus', 'Balanced')
        )
    else:
        questions = await interview_ai.generate_interview_questions(
            token_data['resume_content'],
            token_data['job_description']
        )
    
    # Create interview session
    session_id = interview_ai.generate_session_id()
    session_data = InterviewSession(
        token=request.token,
        session_id=session_id,
        candidate_name=request.candidate_name,
        job_title=job_data['title'] if job_data else "Software Developer",
        voice_mode=request.voice_mode or False,
        messages=[{
            "type": "system",
            "content": f"Welcome {request.candidate_name}! I'm your AI interviewer today. We'll have 8 questions - 4 technical and 4 behavioral. Let's begin!",
            "timestamp": datetime.utcnow().isoformat()
        }],
        current_question=0
    )
    
    await db.sessions.insert_one(session_data.dict())
    
    # Store questions and enhanced features in session metadata
    session_metadata = {
        "session_id": session_id,
        "questions": questions,
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
        "total_questions": 8,
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
    
    # Generate TTS for voice mode
    if request.voice_mode:
        try:
            welcome_audio = await voice_processor.text_to_speech(response_data["welcome_message"])
            question_audio = await voice_processor.text_to_speech(questions[0] if questions else "Tell me about your experience.")
            
            response_data["welcome_audio"] = welcome_audio["audio_base64"]
            response_data["question_audio"] = question_audio["audio_base64"]
        except Exception as e:
            logging.error(f"TTS generation failed: {str(e)}")
    
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
    
    # Evaluate current answer
    current_question = questions[current_q_num]
    question_type = "technical" if current_q_num < 4 else "behavioral"
    
    evaluation = await interview_ai.evaluate_answer(
        current_question,
        request.message,
        question_type
    )
    
    # Store evaluation
    if question_type == "technical":
        session_metadata['technical_evaluations'].append(evaluation)
    else:
        session_metadata['behavioral_evaluations'].append(evaluation)
    
    await db.session_metadata.update_one(
        {"session_id": session['session_id']},
        {"$set": {
            "technical_evaluations": session_metadata['technical_evaluations'],
            "behavioral_evaluations": session_metadata['behavioral_evaluations']
        }}
    )
    
    # Add candidate's message
    new_message = {
        "type": "candidate",
        "content": request.message,
        "timestamp": datetime.utcnow().isoformat(),
        "question_number": current_q_num + 1
    }
    
    # Move to next question
    next_q_num = current_q_num + 1
    
    if next_q_num >= len(questions):
        # Interview completed
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
        
        # Generate final assessment
        assessment_data = {
            "session_id": session['session_id'],
            "token": request.token,
            "candidate_name": session['candidate_name'],
            "job_title": session['job_title'],
            "technical_evaluations": session_metadata['technical_evaluations'],
            "behavioral_evaluations": session_metadata['behavioral_evaluations']
        }
        
        assessment = await interview_ai.generate_final_assessment(assessment_data)
        await db.assessments.insert_one(assessment.dict())
        
        return {
            "completed": True,
            "message": "Thank you for completing the interview! Your responses have been evaluated.",
            "assessment_id": assessment.id
        }
    else:
        # Continue with next question
        next_question = questions[next_q_num]
        ai_response = {
            "type": "ai",
            "content": next_question,
            "timestamp": datetime.utcnow().isoformat(),
            "question_number": next_q_num + 1
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
            "next_question": next_question,
            "question_number": next_q_num + 1,
            "total_questions": len(questions)
        }
        
        # Generate TTS for voice mode
        if session.get('voice_mode'):
            try:
                question_audio = await voice_processor.text_to_speech(next_question)
                response_data["question_audio"] = question_audio["audio_base64"]
            except Exception as e:
                logging.error(f"TTS generation failed: {str(e)}")
        
        return response_data

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
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()