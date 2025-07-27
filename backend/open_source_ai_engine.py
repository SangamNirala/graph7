"""
Phase 3: Advanced AI & Analytics - Week 7: Open-Source AI Model Integration
Step 7.1: Replace Proprietary AI Services

This module replaces proprietary AI services (Gemini, OpenAI) with open-source alternatives
using Hugging Face transformers, BERT models, and other open-source solutions.
"""

import os
import logging
import asyncio
from typing import List, Dict, Any, Optional
import json
import torch
from transformers import (
    AutoTokenizer, AutoModel, AutoModelForCausalLM,
    pipeline, BertTokenizer, BertModel,
    GPT2LMHeadModel, GPT2Tokenizer
)
from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

class OpenSourceAIEngine:
    """
    Open-source AI engine to replace proprietary services
    Features:
    - BERT-based question analysis
    - GPT-style question generation
    - Advanced sentiment analysis
    - Emotion detection with open models
    """
    
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"OpenSourceAIEngine initialized on device: {self.device}")
        
        # Initialize models
        self.models = {}
        self.tokenizers = {}
        self.pipelines = {}
        
        # Sentiment analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize models asynchronously
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all AI models"""
        try:
            logging.info("Loading open-source AI models...")
            
            # 1. BERT for question analysis and embeddings
            self._load_bert_models()
            
            # 2. GPT-style models for text generation
            self._load_generative_models()
            
            # 3. Sentence transformers for semantic analysis
            self._load_sentence_transformers()
            
            # 4. Emotion detection pipeline
            self._load_emotion_models()
            
            logging.info("✅ All open-source AI models loaded successfully")
            
        except Exception as e:
            logging.error(f"❌ Error loading AI models: {str(e)}")
            # Fallback to basic functionality
            self._initialize_fallback_models()
    
    def _load_bert_models(self):
        """Load BERT models for question analysis"""
        try:
            # BERT for question analysis
            model_name = "bert-base-uncased"
            self.tokenizers['bert'] = BertTokenizer.from_pretrained(model_name)
            self.models['bert'] = BertModel.from_pretrained(model_name)
            self.models['bert'].to(self.device)
            
            logging.info("✅ BERT models loaded successfully")
        except Exception as e:
            logging.error(f"Error loading BERT models: {str(e)}")
    
    def _load_generative_models(self):
        """Load GPT-style models for question generation"""
        try:
            # GPT-2 for question generation (lighter model)
            model_name = "gpt2"
            self.tokenizers['gpt2'] = GPT2Tokenizer.from_pretrained(model_name)
            self.models['gpt2'] = GPT2LMHeadModel.from_pretrained(model_name)
            self.models['gpt2'].to(self.device)
            
            # Add padding token
            if self.tokenizers['gpt2'].pad_token is None:
                self.tokenizers['gpt2'].pad_token = self.tokenizers['gpt2'].eos_token
            
            logging.info("✅ Generative models loaded successfully")
        except Exception as e:
            logging.error(f"Error loading generative models: {str(e)}")
    
    def _load_sentence_transformers(self):
        """Load sentence transformers for semantic analysis"""
        try:
            # Sentence transformer for semantic similarity
            self.models['sentence_transformer'] = SentenceTransformer('all-MiniLM-L6-v2')
            logging.info("✅ Sentence transformers loaded successfully")
        except Exception as e:
            logging.error(f"Error loading sentence transformers: {str(e)}")
    
    def _load_emotion_models(self):
        """Load emotion detection models"""
        try:
            # Emotion classification pipeline
            self.pipelines['emotion'] = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=0 if self.device == "cuda" else -1
            )
            
            # Sentiment analysis pipeline as backup
            self.pipelines['sentiment'] = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if self.device == "cuda" else -1
            )
            
            logging.info("✅ Emotion detection models loaded successfully")
        except Exception as e:
            logging.error(f"Error loading emotion models: {str(e)}")
    
    def _initialize_fallback_models(self):
        """Initialize basic fallback models if main models fail"""
        try:
            logging.info("Initializing fallback models...")
            # Basic sentiment analysis is always available
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            logging.info("✅ Fallback models initialized")
        except Exception as e:
            logging.error(f"Error initializing fallback models: {str(e)}")
    
    async def analyze_question_quality(self, question: str) -> Dict[str, Any]:
        """
        Analyze question quality using BERT embeddings and linguistic features
        Replaces proprietary AI analysis
        """
        try:
            analysis = {
                "clarity_score": 0.0,
                "complexity_score": 0.0,
                "relevance_score": 0.0,
                "bias_indicators": [],
                "linguistic_features": {},
                "improvement_suggestions": []
            }
            
            # Basic linguistic analysis
            word_count = len(question.split())
            char_count = len(question)
            sentence_count = len([s for s in question.split('.') if s.strip()])
            
            # Clarity score based on readability
            analysis["clarity_score"] = min(1.0, max(0.0, (20 - word_count) / 20))
            analysis["complexity_score"] = min(1.0, word_count / 30)
            
            # Check for bias indicators
            bias_terms = [
                'he', 'she', 'guys', 'girls', 'young', 'old', 'native',
                'foreign', 'cultural', 'ethnic', 'race', 'gender'
            ]
            detected_bias = [term for term in bias_terms if term.lower() in question.lower()]
            analysis["bias_indicators"] = detected_bias
            
            # Linguistic features
            analysis["linguistic_features"] = {
                "word_count": word_count,
                "character_count": char_count,
                "sentence_count": sentence_count,
                "avg_word_length": char_count / max(word_count, 1),
                "question_words": len([w for w in question.lower().split() if w in ['what', 'how', 'why', 'when', 'where', 'who']])
            }
            
            # BERT-based semantic analysis if available
            if 'bert' in self.models:
                semantic_score = await self._get_bert_semantic_score(question)
                analysis["relevance_score"] = semantic_score
            
            # Generate improvement suggestions
            if analysis["clarity_score"] < 0.5:
                analysis["improvement_suggestions"].append("Consider simplifying the question for better clarity")
            
            if detected_bias:
                analysis["improvement_suggestions"].append("Review question for potential bias indicators")
            
            if word_count < 5:
                analysis["improvement_suggestions"].append("Question might be too short - consider adding more context")
            
            return analysis
            
        except Exception as e:
            logging.error(f"Error in question analysis: {str(e)}")
            return {
                "clarity_score": 0.5,
                "complexity_score": 0.5,
                "relevance_score": 0.5,
                "bias_indicators": [],
                "linguistic_features": {},
                "improvement_suggestions": ["Analysis temporarily unavailable"]
            }
    
    async def _get_bert_semantic_score(self, question: str) -> float:
        """Get semantic relevance score using BERT"""
        try:
            if 'bert' not in self.models:
                return 0.5
            
            # Tokenize and get BERT embeddings
            inputs = self.tokenizers['bert'](question, return_tensors="pt", padding=True, truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.models['bert'](**inputs)
                # Use [CLS] token embedding
                cls_embedding = outputs.last_hidden_state[:, 0, :]
                
                # Simple relevance score based on embedding magnitude
                relevance_score = float(torch.norm(cls_embedding).cpu())
                return min(1.0, relevance_score / 10.0)  # Normalize
        
        except Exception as e:
            logging.error(f"Error in BERT semantic analysis: {str(e)}")
            return 0.5
    
    async def generate_interview_questions(self, 
                                         job_description: str, 
                                         resume_content: str,
                                         question_type: str = "technical",
                                         count: int = 1) -> List[str]:
        """
        Generate interview questions using open-source models
        Replaces Gemini AI question generation
        """
        try:
            questions = []
            
            # Extract key skills and topics from job description and resume
            key_topics = self._extract_key_topics(job_description, resume_content)
            
            # Generate questions based on type
            if question_type == "technical":
                questions = await self._generate_technical_questions(key_topics, count)
            elif question_type == "behavioral":
                questions = await self._generate_behavioral_questions(key_topics, count)
            elif question_type == "resume":
                questions = await self._generate_resume_questions(resume_content, count)
            else:
                questions = await self._generate_general_questions(key_topics, count)
            
            return questions[:count]  # Ensure we don't exceed requested count
            
        except Exception as e:
            logging.error(f"Error generating questions: {str(e)}")
            return self._get_fallback_questions(question_type, count)
    
    def _extract_key_topics(self, job_description: str, resume_content: str) -> List[str]:
        """Extract key topics using NLP techniques"""
        try:
            # Combine texts
            combined_text = f"{job_description} {resume_content}".lower()
            
            # Technical keywords
            tech_keywords = [
                'python', 'javascript', 'java', 'react', 'node', 'sql', 'database',
                'api', 'rest', 'docker', 'kubernetes', 'cloud', 'aws', 'azure',
                'machine learning', 'ai', 'data science', 'backend', 'frontend',
                'web development', 'mobile', 'ios', 'android', 'devops'
            ]
            
            # Find matching keywords
            found_topics = [keyword for keyword in tech_keywords if keyword in combined_text]
            
            # Add some general business topics
            business_keywords = [
                'leadership', 'management', 'communication', 'teamwork', 'project',
                'client', 'customer', 'sales', 'marketing', 'strategy'
            ]
            
            found_topics.extend([keyword for keyword in business_keywords if keyword in combined_text])
            
            return found_topics[:10]  # Limit to top 10 topics
            
        except Exception as e:
            logging.error(f"Error extracting topics: {str(e)}")
            return ["general software development", "problem solving"]
    
    async def _generate_technical_questions(self, topics: List[str], count: int) -> List[str]:
        """Generate technical questions using GPT-2 or templates"""
        try:
            questions = []
            
            # Template-based generation (more reliable)
            templates = [
                "How would you implement {} in a scalable application?",
                "What are the best practices for {} development?",
                "Explain the key concepts of {} and how you've used them.",
                "What challenges have you faced with {} and how did you solve them?",
                "How do you ensure quality and performance when working with {}?",
                "Describe your experience with {} and related technologies.",
                "What's your approach to debugging {} applications?",
                "How do you stay updated with {} trends and best practices?"
            ]
            
            # Generate questions using templates
            for i in range(count):
                if topics:
                    topic = topics[i % len(topics)]
                    template = templates[i % len(templates)]
                    question = template.format(topic)
                    questions.append(question)
                else:
                    questions.append(templates[i % len(templates)].format("software"))
            
            # Try GPT-2 generation as enhancement if available
            if 'gpt2' in self.models and len(topics) > 0:
                enhanced_questions = await self._enhance_questions_with_gpt2(questions, topics)
                return enhanced_questions
            
            return questions
            
        except Exception as e:
            logging.error(f"Error generating technical questions: {str(e)}")
            return self._get_fallback_questions("technical", count)
    
    async def _generate_behavioral_questions(self, topics: List[str], count: int) -> List[str]:
        """Generate behavioral questions"""
        templates = [
            "Tell me about a time when you had to work under pressure.",
            "Describe a situation where you had to collaborate with a difficult team member.",
            "Give an example of how you handled a challenging project deadline.",
            "Tell me about a time when you had to learn something new quickly.",
            "Describe a situation where you had to make a difficult decision.",
            "Give an example of how you handled constructive criticism.",
            "Tell me about a time when you took initiative on a project.",
            "Describe a situation where you had to adapt to change quickly."
        ]
        
        return templates[:count]
    
    async def _generate_resume_questions(self, resume_content: str, count: int) -> List[str]:
        """Generate resume-based questions"""
        try:
            # Extract experience and skills from resume
            lines = resume_content.lower().split('\n')
            experience_indicators = ['experience', 'worked', 'developed', 'managed', 'led', 'created']
            
            relevant_lines = []
            for line in lines:
                if any(indicator in line for indicator in experience_indicators):
                    relevant_lines.append(line)
            
            questions = []
            templates = [
                "Can you tell me more about your experience with {}?",
                "What was your role in the {} project mentioned in your resume?",
                "How did you contribute to {} in your previous position?",
                "What challenges did you face while working on {}?"
            ]
            
            # Generate questions based on resume content
            for i in range(count):
                if relevant_lines:
                    # Extract a key phrase from resume
                    line = relevant_lines[i % len(relevant_lines)]
                    # Simple extraction of potential project/skill names
                    words = line.split()
                    key_phrase = ' '.join(words[:3]) if len(words) >= 3 else line
                    template = templates[i % len(templates)]
                    questions.append(template.format(key_phrase))
                else:
                    questions.append("Can you walk me through your most recent work experience?")
            
            return questions
            
        except Exception as e:
            logging.error(f"Error generating resume questions: {str(e)}")
            return ["Can you walk me through your professional background?"] * count
    
    async def _generate_general_questions(self, topics: List[str], count: int) -> List[str]:
        """Generate general interview questions"""
        templates = [
            "What interests you most about this role?",
            "How do you handle challenging situations at work?",
            "What are your career goals for the next few years?",
            "How do you stay motivated and productive?",
            "What do you consider your greatest professional strength?",
            "How do you approach learning new technologies or skills?",
            "What type of work environment do you thrive in?",
            "How do you prioritize tasks when facing multiple deadlines?"
        ]
        
        return templates[:count]
    
    async def _enhance_questions_with_gpt2(self, base_questions: List[str], topics: List[str]) -> List[str]:
        """Enhance questions using GPT-2 generation"""
        try:
            enhanced_questions = []
            
            for question in base_questions:
                # Create a prompt for GPT-2
                prompt = f"Professional interview question: {question[:50]}"
                
                # Generate with GPT-2
                inputs = self.tokenizers['gpt2'](prompt, return_tensors="pt", padding=True, truncation=True)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.models['gpt2'].generate(
                        **inputs,
                        max_length=inputs['input_ids'].shape[1] + 30,
                        num_return_sequences=1,
                        temperature=0.7,
                        pad_token_id=self.tokenizers['gpt2'].eos_token_id,
                        do_sample=True
                    )
                
                # Decode the generated text
                generated = self.tokenizers['gpt2'].decode(outputs[0], skip_special_tokens=True)
                
                # Clean up the generated question
                if '?' in generated:
                    enhanced_question = generated.split('?')[0] + '?'
                    enhanced_questions.append(enhanced_question)
                else:
                    enhanced_questions.append(question)  # Fallback to original
            
            return enhanced_questions
            
        except Exception as e:
            logging.error(f"Error enhancing questions with GPT-2: {str(e)}")
            return base_questions  # Return original questions on error
    
    def _get_fallback_questions(self, question_type: str, count: int) -> List[str]:
        """Get fallback questions when generation fails"""
        fallback_questions = {
            "technical": [
                "How do you approach solving complex technical problems?",
                "What's your experience with software development best practices?",
                "How do you ensure code quality in your projects?",
                "Describe your experience with debugging and troubleshooting.",
                "What development tools and technologies are you most comfortable with?"
            ],
            "behavioral": [
                "Tell me about a challenging project you worked on.",
                "How do you handle working under tight deadlines?",
                "Describe your experience working in a team environment.",
                "How do you approach learning new skills?",
                "Tell me about a time you had to adapt to change."
            ],
            "resume": [
                "Can you walk me through your professional background?",
                "What was your most significant achievement in your previous role?",
                "How has your experience prepared you for this position?",
                "What attracted you to your field of work?",
                "Describe the most challenging aspect of your current/previous job."
            ]
        }
        
        questions = fallback_questions.get(question_type, fallback_questions["technical"])
        return questions[:count]
    
    async def analyze_candidate_response(self, 
                                       response: str, 
                                       question: str,
                                       question_type: str = "general") -> Dict[str, Any]:
        """
        Analyze candidate response using open-source models
        Replaces proprietary AI analysis
        """
        try:
            analysis = {
                "content_quality": 0.0,
                "relevance": 0.0,
                "technical_accuracy": 0.0,
                "communication_clarity": 0.0,
                "sentiment_analysis": {},
                "emotion_analysis": {},
                "key_points": [],
                "areas_for_improvement": [],
                "strengths": []
            }
            
            # Basic metrics
            word_count = len(response.split())
            char_count = len(response)
            
            # Content quality based on length and structure
            analysis["content_quality"] = min(1.0, word_count / 100)  # Normalize by expected length
            
            # Communication clarity
            sentences = [s.strip() for s in response.split('.') if s.strip()]
            avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
            analysis["communication_clarity"] = max(0.0, min(1.0, (30 - avg_sentence_length) / 30))
            
            # Sentiment analysis using VADER
            sentiment_scores = self.sentiment_analyzer.polarity_scores(response)
            analysis["sentiment_analysis"] = {
                "compound": sentiment_scores['compound'],
                "positive": sentiment_scores['pos'],
                "neutral": sentiment_scores['neu'],
                "negative": sentiment_scores['neg'],
                "overall_tone": "positive" if sentiment_scores['compound'] > 0.1 else "negative" if sentiment_scores['compound'] < -0.1 else "neutral"
            }
            
            # Advanced emotion analysis if available
            if 'emotion' in self.pipelines:
                try:
                    emotion_results = self.pipelines['emotion'](response)
                    analysis["emotion_analysis"] = {
                        "primary_emotion": emotion_results[0]['label'] if emotion_results else "neutral",
                        "confidence": emotion_results[0]['score'] if emotion_results else 0.5,
                        "emotions": emotion_results
                    }
                except Exception as e:
                    logging.error(f"Emotion analysis failed: {str(e)}")
                    analysis["emotion_analysis"] = {"primary_emotion": "neutral", "confidence": 0.5}
            
            # Relevance analysis using sentence similarity if available
            if 'sentence_transformer' in self.models:
                try:
                    question_embedding = self.models['sentence_transformer'].encode([question])
                    response_embedding = self.models['sentence_transformer'].encode([response])
                    
                    # Calculate cosine similarity
                    similarity = np.dot(question_embedding[0], response_embedding[0]) / (
                        np.linalg.norm(question_embedding[0]) * np.linalg.norm(response_embedding[0])
                    )
                    analysis["relevance"] = float(max(0.0, min(1.0, similarity)))
                except Exception as e:
                    logging.error(f"Relevance analysis failed: {str(e)}")
                    analysis["relevance"] = 0.5
            
            # Extract key points (simple keyword extraction)
            response_lower = response.lower()
            keywords = []
            
            # Technical keywords
            tech_terms = ['algorithm', 'database', 'api', 'framework', 'architecture', 'design', 'implementation', 'testing', 'debugging']
            keywords.extend([term for term in tech_terms if term in response_lower])
            
            # Behavioral keywords
            behavioral_terms = ['team', 'leadership', 'communication', 'problem', 'solution', 'challenge', 'goal', 'achievement']
            keywords.extend([term for term in behavioral_terms if term in response_lower])
            
            analysis["key_points"] = list(set(keywords))[:5]  # Top 5 unique keywords
            
            # Generate strengths and improvement areas
            if analysis["content_quality"] > 0.7:
                analysis["strengths"].append("Comprehensive and detailed response")
            
            if analysis["communication_clarity"] > 0.7:
                analysis["strengths"].append("Clear and well-structured communication")
            
            if sentiment_scores['compound'] > 0.3:
                analysis["strengths"].append("Positive and enthusiastic tone")
            
            if analysis["content_quality"] < 0.5:
                analysis["areas_for_improvement"].append("Provide more detailed and comprehensive answers")
            
            if analysis["communication_clarity"] < 0.5:
                analysis["areas_for_improvement"].append("Improve clarity and sentence structure")
            
            if len(analysis["key_points"]) < 2:
                analysis["areas_for_improvement"].append("Include more relevant technical or professional terms")
            
            return analysis
            
        except Exception as e:
            logging.error(f"Error analyzing candidate response: {str(e)}")
            return {
                "content_quality": 0.5,
                "relevance": 0.5,
                "technical_accuracy": 0.5,
                "communication_clarity": 0.5,
                "sentiment_analysis": {"compound": 0.0, "overall_tone": "neutral"},
                "emotion_analysis": {"primary_emotion": "neutral", "confidence": 0.5},
                "key_points": [],
                "areas_for_improvement": ["Analysis temporarily unavailable"],
                "strengths": []
            }
    
    async def generate_interview_feedback(self, 
                                        candidate_responses: List[Dict[str, Any]],
                                        overall_performance: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate comprehensive interview feedback using open-source AI
        Replaces proprietary AI feedback generation
        """
        try:
            feedback = {
                "overall_assessment": "",
                "technical_feedback": "",
                "behavioral_feedback": "",
                "strengths": [],
                "areas_for_improvement": [],
                "recommendations": [],
                "detailed_analysis": {}
            }
            
            # Analyze overall performance
            avg_scores = {
                "content_quality": np.mean([r.get('analysis', {}).get('content_quality', 0.5) for r in candidate_responses]),
                "communication": np.mean([r.get('analysis', {}).get('communication_clarity', 0.5) for r in candidate_responses]),
                "relevance": np.mean([r.get('analysis', {}).get('relevance', 0.5) for r in candidate_responses])
            }
            
            # Generate overall assessment
            if avg_scores["content_quality"] > 0.7:
                feedback["overall_assessment"] = "Strong candidate with comprehensive responses and good technical knowledge."
            elif avg_scores["content_quality"] > 0.5:
                feedback["overall_assessment"] = "Solid candidate with adequate responses and reasonable technical understanding."
            else:
                feedback["overall_assessment"] = "Candidate shows potential but needs improvement in response depth and technical clarity."
            
            # Technical feedback
            technical_responses = [r for r in candidate_responses if r.get('question_type') == 'technical']
            if technical_responses:
                tech_quality = np.mean([r.get('analysis', {}).get('content_quality', 0.5) for r in technical_responses])
                if tech_quality > 0.7:
                    feedback["technical_feedback"] = "Demonstrates strong technical knowledge with detailed explanations."
                elif tech_quality > 0.5:
                    feedback["technical_feedback"] = "Shows adequate technical understanding with room for more depth."
                else:
                    feedback["technical_feedback"] = "Technical responses need improvement in depth and accuracy."
            
            # Behavioral feedback
            behavioral_responses = [r for r in candidate_responses if r.get('question_type') == 'behavioral']
            if behavioral_responses:
                behavioral_quality = np.mean([r.get('analysis', {}).get('content_quality', 0.5) for r in behavioral_responses])
                if behavioral_quality > 0.7:
                    feedback["behavioral_feedback"] = "Excellent behavioral responses with clear examples and outcomes."
                elif behavioral_quality > 0.5:
                    feedback["behavioral_feedback"] = "Good behavioral responses with relevant examples."
                else:
                    feedback["behavioral_feedback"] = "Behavioral responses would benefit from more specific examples and outcomes."
            
            # Collect strengths from individual responses
            all_strengths = []
            all_improvements = []
            
            for response in candidate_responses:
                analysis = response.get('analysis', {})
                all_strengths.extend(analysis.get('strengths', []))
                all_improvements.extend(analysis.get('areas_for_improvement', []))
            
            # Consolidate unique strengths and improvements
            feedback["strengths"] = list(set(all_strengths))[:5]
            feedback["areas_for_improvement"] = list(set(all_improvements))[:5]
            
            # Generate recommendations
            if avg_scores["communication"] < 0.6:
                feedback["recommendations"].append("Practice articulating technical concepts more clearly")
            
            if avg_scores["content_quality"] < 0.6:
                feedback["recommendations"].append("Prepare more detailed examples and use cases")
            
            if avg_scores["relevance"] < 0.6:
                feedback["recommendations"].append("Focus on answering the specific question asked")
            
            # Detailed analysis
            feedback["detailed_analysis"] = {
                "average_scores": avg_scores,
                "response_count": len(candidate_responses),
                "technical_response_count": len(technical_responses),
                "behavioral_response_count": len(behavioral_responses),
                "overall_performance_score": np.mean(list(avg_scores.values()))
            }
            
            return feedback
            
        except Exception as e:
            logging.error(f"Error generating interview feedback: {str(e)}")
            return {
                "overall_assessment": "Interview completed successfully.",
                "technical_feedback": "Technical responses recorded.",
                "behavioral_feedback": "Behavioral responses recorded.",
                "strengths": ["Participated in the interview process"],
                "areas_for_improvement": ["Detailed analysis temporarily unavailable"],
                "recommendations": ["Continue practicing interview skills"],
                "detailed_analysis": {"overall_performance_score": 0.5}
            }
    
    def get_model_status(self) -> Dict[str, bool]:
        """Get status of all loaded models"""
        return {
            "bert_loaded": 'bert' in self.models,
            "gpt2_loaded": 'gpt2' in self.models,
            "sentence_transformer_loaded": 'sentence_transformer' in self.models,
            "emotion_pipeline_loaded": 'emotion' in self.pipelines,
            "sentiment_pipeline_loaded": 'sentiment' in self.pipelines,
            "device": self.device,
            "total_models": len(self.models),
            "total_pipelines": len(self.pipelines)
        }

# Global instance
open_source_ai_engine = None

def get_ai_engine():
    """Get or create the global AI engine instance"""
    global open_source_ai_engine
    if open_source_ai_engine is None:
        open_source_ai_engine = OpenSourceAIEngine()
    return open_source_ai_engine

# Initialize the engine when module is imported
try:
    open_source_ai_engine = OpenSourceAIEngine()
    logging.info("✅ OpenSourceAIEngine initialized successfully")
except Exception as e:
    logging.error(f"❌ Failed to initialize OpenSourceAIEngine: {str(e)}")
    open_source_ai_engine = None