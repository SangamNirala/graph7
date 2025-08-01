"""
Phase 2: AI-Powered Screening & Shortlisting Engine
This module implements intelligent resume analysis, candidate scoring, and automated shortlisting
"""

import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import json
from typing import List, Dict, Any, Optional, Tuple
import asyncio
import logging
from datetime import datetime
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os

# Initialize NLP models
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("English model not found. Please install: python -m spacy download en_core_web_sm")
    nlp = None

# Initialize NLTK
try:
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

class AIResumeAnalysisEngine:
    """AI-powered resume analysis and skills extraction engine"""
    
    def __init__(self):
        self.technical_skills_database = {
            # Programming Languages
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
                'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'shell', 'bash',
                'powershell', 'perl', 'lua', 'dart', 'objective-c', 'vb.net', 'f#', 'clojure', 'haskell'
            ],
            
            # Web Frameworks & Technologies
            'web_frameworks': [
                'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt.js', 'gatsby', 'express',
                'fastapi', 'flask', 'django', 'spring', 'laravel', 'symfony', 'rails', 'asp.net',
                'node.js', 'jquery', 'bootstrap', 'tailwind', 'sass', 'less'
            ],
            
            # Databases
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb',
                'sqlite', 'oracle', 'mssql', 'mariadb', 'neo4j', 'firebase', 'supabase', 'couchbase'
            ],
            
            # Cloud & DevOps
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins',
                'gitlab', 'github actions', 'circleci', 'travis ci', 'helm', 'prometheus', 'grafana',
                'nginx', 'apache', 'linux', 'ubuntu', 'centos', 'rhel'
            ],
            
            # AI/ML
            'ai_ml': [
                'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'keras', 'opencv',
                'natural language processing', 'computer vision', 'deep learning', 'machine learning',
                'neural networks', 'transformers', 'huggingface', 'langchain', 'openai', 'llm'
            ],
            
            # Mobile Development
            'mobile': [
                'react native', 'flutter', 'ionic', 'xamarin', 'android development', 'ios development',
                'swift ui', 'jetpack compose', 'cordova'
            ],
            
            # Tools & Technologies
            'tools': [
                'git', 'jira', 'confluence', 'slack', 'postman', 'insomnia', 'figma', 'adobe xd',
                'photoshop', 'illustrator', 'sketch', 'vscode', 'intellij', 'eclipse', 'vim'
            ]
        }
        
        # Role level indicators
        self.experience_indicators = {
            'entry': ['junior', 'entry', 'associate', 'graduate', 'trainee', 'intern', '0-2 years', '1 year', '2 years'],
            'mid': ['mid', 'intermediate', 'developer', 'engineer', '3-5 years', '4 years', '5 years', '3 years'],
            'senior': ['senior', 'sr', 'lead', 'principal', '5+ years', '6 years', '7 years', '8 years', '5-8 years'],
            'executive': ['manager', 'director', 'vp', 'cto', 'ceo', 'head of', 'chief', '10+ years', '9+ years']
        }
        
        # Common degree patterns
        self.education_patterns = {
            'bachelor': ['b.s.', 'b.a.', 'bs', 'ba', 'bachelor', 'undergraduate'],
            'master': ['m.s.', 'm.a.', 'ms', 'ma', 'master', 'mba', 'm.tech', 'mtech'],
            'phd': ['ph.d.', 'phd', 'doctorate', 'doctoral']
        }
        
    async def extract_skills_from_resume(self, resume_content: str) -> List[Dict[str, Any]]:
        """Extract technical skills from resume content with confidence scores"""
        extracted_skills = []
        resume_lower = resume_content.lower()
        
        # Extract skills using pattern matching and spaCy NER
        for category, skills_list in self.technical_skills_database.items():
            for skill in skills_list:
                # Check for exact matches and variations
                skill_patterns = [
                    skill,
                    skill.replace('.', ''),
                    skill.replace(' ', ''),
                    skill.replace('-', ''),
                    skill.replace('_', ' ')
                ]
                
                confidence = 0.0
                contexts = []
                
                for pattern in skill_patterns:
                    if pattern.lower() in resume_lower:
                        # Calculate confidence based on context and frequency
                        matches = re.findall(rf'\b{re.escape(pattern.lower())}\b', resume_lower)
                        frequency = len(matches)
                        
                        # Extract context around skill mentions
                        for match in re.finditer(rf'\b{re.escape(pattern.lower())}\b', resume_lower):
                            start = max(0, match.start() - 50)
                            end = min(len(resume_lower), match.end() + 50)
                            context = resume_content[start:end].strip()
                            contexts.append(context)
                        
                        # Determine confidence based on context keywords
                        context_text = ' '.join(contexts).lower()
                        base_confidence = min(0.8, 0.3 + (frequency * 0.1))
                        
                        # Boost confidence for stronger context indicators
                        if any(keyword in context_text for keyword in ['experience', 'years', 'proficient', 'expert', 'advanced']):
                            base_confidence += 0.15
                        if any(keyword in context_text for keyword in ['project', 'developed', 'built', 'implemented']):
                            base_confidence += 0.1
                        
                        confidence = max(confidence, min(base_confidence, 0.95))
                
                if confidence > 0.3:  # Only include skills with reasonable confidence
                    extracted_skills.append({
                        'skill': skill,
                        'category': category,
                        'confidence': round(confidence, 2),
                        'frequency': frequency,
                        'contexts': contexts[:3]  # Limit contexts for storage
                    })
        
        # Sort by confidence score
        extracted_skills.sort(key=lambda x: x['confidence'], reverse=True)
        return extracted_skills
    
    async def analyze_experience_level(self, resume_content: str) -> Dict[str, Any]:
        """Analyze experience level and career progression"""
        resume_lower = resume_content.lower()
        
        # Extract years of experience
        years_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*in',
            r'over\s*(\d+)\s*years?',
            r'more\s*than\s*(\d+)\s*years?'
        ]
        
        max_years = 0
        for pattern in years_patterns:
            matches = re.findall(pattern, resume_lower)
            for match in matches:
                years = int(match.replace('+', ''))
                max_years = max(max_years, years)
        
        # Analyze role progression
        role_level_scores = {level: 0 for level in self.experience_indicators.keys()}
        
        for level, indicators in self.experience_indicators.items():
            for indicator in indicators:
                count = len(re.findall(rf'\b{re.escape(indicator)}\b', resume_lower))
                role_level_scores[level] += count
        
        # Determine primary experience level
        primary_level = max(role_level_scores, key=role_level_scores.get)
        
        # If we found explicit years, adjust the level accordingly
        if max_years > 0:
            if max_years <= 2:
                primary_level = 'entry'
            elif max_years <= 5:
                primary_level = 'mid'
            elif max_years <= 8:
                primary_level = 'senior'
            else:
                primary_level = 'executive'
        
        return {
            'experience_level': primary_level,
            'years_of_experience': max_years,
            'level_confidence': role_level_scores[primary_level] / (sum(role_level_scores.values()) + 1),
            'role_indicators': role_level_scores
        }
    
    async def parse_education(self, resume_content: str) -> List[Dict[str, Any]]:
        """Parse education information from resume"""
        education_entries = []
        resume_lower = resume_content.lower()
        
        # Look for degree patterns
        for degree_level, patterns in self.education_patterns.items():
            for pattern in patterns:
                # Find degree mentions with context
                degree_pattern = rf'{re.escape(pattern)}[^.]*?(?:in|of)\s+([^.,\n]+)'
                matches = re.finditer(degree_pattern, resume_lower)
                
                for match in matches:
                    field_of_study = match.group(1).strip()
                    
                    # Extract year if present
                    year_pattern = r'(19|20)\d{2}'
                    context = resume_content[max(0, match.start()-100):match.end()+100]
                    year_match = re.search(year_pattern, context)
                    graduation_year = year_match.group() if year_match else None
                    
                    education_entries.append({
                        'degree_level': degree_level,
                        'field_of_study': field_of_study,
                        'graduation_year': graduation_year,
                        'raw_text': match.group().strip()
                    })
        
        return education_entries
    
    async def enhanced_skills_extraction_with_ai(self, resume_content: str) -> Dict[str, Any]:
        """Use AI to enhance skills extraction with semantic understanding"""
        try:
            # Create LLM chat instance for Gemini
            chat = LlmChat(
                api_key=os.environ.get("GEMINI_API_KEY"),
                provider="gemini",
                model="gemini-1.5-flash"
            )
            
            prompt = f"""
            Analyze the following resume and extract technical skills with high accuracy:
            
            Resume Content:
            {resume_content[:3000]}  # Limit content to avoid token limits
            
            Please extract:
            1. Programming languages and their proficiency level
            2. Frameworks and libraries
            3. Databases and data technologies
            4. Cloud platforms and DevOps tools
            5. Years of experience for each major skill area
            
            Return the analysis in JSON format with this structure:
            {{
                "technical_skills": [
                    {{"skill": "Python", "category": "programming", "proficiency": "expert", "years": 5}},
                    {{"skill": "React", "category": "frontend", "proficiency": "advanced", "years": 3}}
                ],
                "summary": "Brief summary of technical expertise"
            }}
            """
            
            response = await chat.send_message(UserMessage(content=prompt))
            
            # Parse AI response
            try:
                # Extract JSON from response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    ai_analysis = json.loads(response[json_start:json_end])
                    return ai_analysis
            except json.JSONDecodeError:
                logging.warning("Failed to parse AI response as JSON")
                
        except Exception as e:
            logging.error(f"AI-enhanced skills extraction failed: {e}")
        
        # Fallback to basic extraction
        return {"technical_skills": [], "summary": "AI analysis unavailable"}

class SmartScoringSystem:
    """Multi-dimensional candidate scoring system"""
    
    def __init__(self):
        self.default_weights = {
            'skills_match': 0.4,
            'experience_level': 0.3,
            'education_fit': 0.2,
            'career_progression': 0.1
        }
    
    async def score_candidate_against_job(self, 
                                        candidate_profile: Dict[str, Any],
                                        job_requirements: Dict[str, Any],
                                        custom_weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """Score a candidate against specific job requirements"""
        
        weights = custom_weights or self.default_weights
        scores = {}
        
        # 1. Skills Match Score
        scores['skills_match'] = await self._calculate_skills_match_score(
            candidate_profile, job_requirements
        )
        
        # 2. Experience Level Score
        scores['experience_level'] = await self._calculate_experience_score(
            candidate_profile, job_requirements
        )
        
        # 3. Education Fit Score
        scores['education_fit'] = await self._calculate_education_score(
            candidate_profile, job_requirements
        )
        
        # 4. Career Progression Score
        scores['career_progression'] = await self._calculate_career_progression_score(
            candidate_profile
        )
        
        # Calculate weighted overall score
        overall_score = sum(scores[key] * weights[key] for key in scores.keys())
        
        return {
            'overall_score': round(overall_score, 2),
            'component_scores': scores,
            'weights_used': weights,
            'score_breakdown': {
                key: {
                    'score': scores[key],
                    'weight': weights[key],
                    'contribution': round(scores[key] * weights[key], 2)
                } for key in scores.keys()
            }
        }
    
    async def _calculate_skills_match_score(self, candidate_profile: Dict, job_requirements: Dict) -> float:
        """Calculate skills matching percentage"""
        try:
            candidate_skills = set()
            for skill_data in candidate_profile.get('extracted_skills', []):
                if isinstance(skill_data, dict):
                    candidate_skills.add(skill_data['skill'].lower())
                else:
                    candidate_skills.add(skill_data.lower())
            
            required_skills = set(skill.lower() for skill in job_requirements.get('required_skills', []))
            preferred_skills = set(skill.lower() for skill in job_requirements.get('preferred_skills', []))
            
            if not required_skills and not preferred_skills:
                return 75.0  # Default score if no specific requirements
            
            # Calculate matches
            required_matches = len(candidate_skills.intersection(required_skills))
            preferred_matches = len(candidate_skills.intersection(preferred_skills))
            
            # Score calculation
            required_score = (required_matches / len(required_skills)) * 70 if required_skills else 70
            preferred_score = (preferred_matches / len(preferred_skills)) * 30 if preferred_skills else 30
            
            return min(required_score + preferred_score, 100.0)
        
        except Exception as e:
            logging.error(f"Skills match scoring error: {e}")
            return 50.0
    
    async def _calculate_experience_score(self, candidate_profile: Dict, job_requirements: Dict) -> float:
        """Calculate experience level alignment score"""
        try:
            candidate_experience = candidate_profile.get('experience_level', 'entry')
            required_experience = job_requirements.get('experience_level', 'mid')
            
            # Experience level hierarchy
            levels = {'entry': 1, 'mid': 2, 'senior': 3, 'executive': 4}
            
            candidate_level = levels.get(candidate_experience, 1)
            required_level = levels.get(required_experience, 2)
            
            # Perfect match gets 100, close matches get partial scores
            if candidate_level == required_level:
                return 100.0
            elif abs(candidate_level - required_level) == 1:
                return 80.0
            elif abs(candidate_level - required_level) == 2:
                return 60.0
            else:
                return 40.0
        
        except Exception as e:
            logging.error(f"Experience scoring error: {e}")
            return 50.0
    
    async def _calculate_education_score(self, candidate_profile: Dict, job_requirements: Dict) -> float:
        """Calculate education alignment score"""
        try:
            candidate_education = candidate_profile.get('education_data', [])
            required_education = job_requirements.get('education_requirements', {})
            
            if not required_education:
                return 75.0  # Default if no requirements
            
            # Check degree level requirements
            required_degree_level = required_education.get('degree_level', '')
            preferred_fields = required_education.get('preferred_fields', [])
            
            score = 50.0  # Base score
            
            # Check if candidate has required degree level
            for education in candidate_education:
                degree_level = education.get('degree_level', '')
                field_of_study = education.get('field_of_study', '').lower()
                
                if degree_level == required_degree_level:
                    score += 30.0
                
                # Check field alignment
                for preferred_field in preferred_fields:
                    if preferred_field.lower() in field_of_study:
                        score += 20.0
                        break
            
            return min(score, 100.0)
        
        except Exception as e:
            logging.error(f"Education scoring error: {e}")
            return 50.0
    
    async def _calculate_career_progression_score(self, candidate_profile: Dict) -> float:
        """Calculate career progression indicators"""
        try:
            experience_years = candidate_profile.get('years_of_experience', 0)
            experience_level = candidate_profile.get('experience_level', 'entry')
            
            # Expected years for each level
            expected_years = {
                'entry': (0, 2),
                'mid': (3, 5),
                'senior': (6, 10),
                'executive': (10, 30)
            }
            
            level_range = expected_years.get(experience_level, (0, 2))
            
            # Score based on whether experience years align with level
            if level_range[0] <= experience_years <= level_range[1]:
                return 100.0
            elif experience_years < level_range[0]:
                return 70.0  # Underqualified
            else:
                return 90.0  # Overqualified (still good)
        
        except Exception as e:
            logging.error(f"Career progression scoring error: {e}")
            return 75.0

class AutoShortlistingEngine:
    """Automated candidate shortlisting with AI recommendations"""
    
    def __init__(self, scoring_system: SmartScoringSystem):
        self.scoring_system = scoring_system
    
    async def generate_shortlist(self, 
                               candidates: List[Dict],
                               job_requirements: Dict,
                               shortlist_size: int = 10,
                               min_score_threshold: float = 70.0) -> Dict[str, Any]:
        """Generate intelligent candidate shortlist"""
        
        scored_candidates = []
        
        # Score all candidates
        for candidate in candidates:
            try:
                scoring_result = await self.scoring_system.score_candidate_against_job(
                    candidate, job_requirements
                )
                
                candidate_with_score = {
                    **candidate,
                    'ai_score': scoring_result['overall_score'],
                    'score_breakdown': scoring_result['component_scores'],
                    'score_details': scoring_result
                }
                
                scored_candidates.append(candidate_with_score)
            
            except Exception as e:
                logging.error(f"Error scoring candidate {candidate.get('id', 'unknown')}: {e}")
                continue
        
        # Filter by minimum threshold
        qualified_candidates = [
            candidate for candidate in scored_candidates 
            if candidate['ai_score'] >= min_score_threshold
        ]
        
        # Sort by score descending
        qualified_candidates.sort(key=lambda x: x['ai_score'], reverse=True)
        
        # Generate shortlist
        shortlist = qualified_candidates[:shortlist_size]
        
        # Generate auto-tags based on score ranges
        for candidate in shortlist:
            candidate['auto_tags'] = self._generate_auto_tags(candidate['ai_score'])
        
        return {
            'shortlist': shortlist,
            'total_candidates_scored': len(scored_candidates),
            'qualified_candidates': len(qualified_candidates),
            'shortlist_size': len(shortlist),
            'average_score': sum(c['ai_score'] for c in qualified_candidates) / len(qualified_candidates) if qualified_candidates else 0,
            'score_distribution': self._calculate_score_distribution(scored_candidates),
            'recommendations': self._generate_recommendations(shortlist, qualified_candidates)
        }
    
    def _generate_auto_tags(self, score: float) -> List[str]:
        """Generate automatic tags based on AI score"""
        tags = []
        
        if score >= 90:
            tags.append("Top Candidate")
        elif score >= 80:
            tags.append("Strong Match")
        elif score >= 70:
            tags.append("Good Fit")
        elif score >= 60:
            tags.append("Needs Review")
        else:
            tags.append("Below Threshold")
        
        return tags
    
    def _calculate_score_distribution(self, candidates: List[Dict]) -> Dict[str, int]:
        """Calculate score distribution for analytics"""
        distribution = {
            "90-100": 0,
            "80-89": 0,
            "70-79": 0,
            "60-69": 0,
            "Below 60": 0
        }
        
        for candidate in candidates:
            score = candidate.get('ai_score', 0)
            if score >= 90:
                distribution["90-100"] += 1
            elif score >= 80:
                distribution["80-89"] += 1
            elif score >= 70:
                distribution["70-79"] += 1
            elif score >= 60:
                distribution["60-69"] += 1
            else:
                distribution["Below 60"] += 1
        
        return distribution
    
    def _generate_recommendations(self, shortlist: List[Dict], all_qualified: List[Dict]) -> List[str]:
        """Generate hiring recommendations"""
        recommendations = []
        
        if not shortlist:
            recommendations.append("No candidates met the minimum threshold. Consider lowering requirements.")
            return recommendations
        
        top_candidate = shortlist[0]
        recommendations.append(f"Top candidate: {top_candidate.get('name', 'Unknown')} with score {top_candidate['ai_score']}")
        
        if len(shortlist) >= 3:
            recommendations.append(f"Strong candidate pool with {len(shortlist)} qualified candidates")
        elif len(shortlist) == 1:
            recommendations.append("Limited candidate pool. Consider expanding search criteria.")
        
        # Analyze score gaps
        if len(shortlist) >= 2:
            score_gap = shortlist[0]['ai_score'] - shortlist[1]['ai_score']
            if score_gap > 20:
                recommendations.append("Clear frontrunner identified with significant score advantage")
            elif score_gap < 5:
                recommendations.append("Very competitive candidate pool - additional screening recommended")
        
        return recommendations