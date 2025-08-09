#!/usr/bin/env python3
"""
Enhanced AI Interview Analysis Report Testing
Tests the comprehensive AI analysis report functionality including:
- Individual question scoring for each Q&A pair
- Big Five personality analysis integration  
- Bias detection and fairness metrics
- Predictive hiring analytics with ML insights
- Speech analysis capabilities
- Enhanced communication, technical, and behavioral analysis
- Average individual score calculation
"""

import requests
import json
import time
import io
import base64
import tempfile
from typing import Dict, Any, Optional

# Backend URL - using the production URL from frontend .env
BASE_URL = "https://5d65efb8-ad0f-4fc8-b912-067b82ffbbaa.preview.emergentagent.com/api"

class EnhancedAIAnalysisTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.generated_token = None
        self.session_id = None
        self.assessment_id = None
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def test_admin_login(self) -> bool:
        """Test admin authentication"""
        try:
            payload = {"password": "Game@1234"}
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json=payload,
                timeout=10
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = data.get("success", False)
            
            details = f"Status: {response.status_code}, Response: {response.text[:200]}"
            self.log_test("Admin Login", success, details)
            return success
        except Exception as e:
            self.log_test("Admin Login", False, f"Exception: {str(e)}")
            return False
    
    def create_comprehensive_interview_session(self) -> bool:
        """Create a comprehensive interview session with multiple Q&A pairs for AI analysis"""
        try:
            # Create enhanced resume content for comprehensive analysis
            resume_content = """Dr. Sarah Chen
Senior AI Research Engineer & Team Lead
Email: sarah.chen@techcorp.com
Phone: (555) 987-6543
LinkedIn: linkedin.com/in/sarahchen-ai

PROFESSIONAL SUMMARY:
Innovative AI Research Engineer with 8+ years of experience in machine learning, natural language processing, and computer vision. Led cross-functional teams of 12+ engineers in developing production-scale AI systems. Published 15+ peer-reviewed papers and holds 3 patents in deep learning architectures.

TECHNICAL EXPERTISE:
• Machine Learning: TensorFlow, PyTorch, Scikit-learn, XGBoost, Neural Networks
• Programming: Python, R, Java, C++, SQL, JavaScript, Go
• Cloud Platforms: AWS (SageMaker, EC2, S3), Google Cloud (AI Platform, BigQuery), Azure ML
• Big Data: Spark, Hadoop, Kafka, Elasticsearch, MongoDB, PostgreSQL
• MLOps: Docker, Kubernetes, Jenkins, MLflow, Kubeflow, Git, CI/CD
• Specializations: NLP, Computer Vision, Reinforcement Learning, Time Series Analysis

PROFESSIONAL EXPERIENCE:

Senior AI Research Engineer & Team Lead | TechCorp Inc. | 2020 - Present
• Led development of multi-modal AI system processing 10M+ daily transactions with 99.7% accuracy
• Architected and deployed real-time recommendation engine increasing user engagement by 45%
• Managed team of 12 engineers across 3 time zones, implementing agile methodologies
• Reduced model training time by 60% through distributed computing and optimization techniques
• Established MLOps pipeline reducing deployment time from weeks to hours

AI Research Scientist | DataVision Labs | 2018 - 2020
• Developed novel deep learning architecture for medical image analysis (published in Nature AI)
• Built end-to-end computer vision pipeline for autonomous vehicle perception system
• Collaborated with Stanford Medical School on FDA-approved diagnostic AI tool
• Mentored 5 junior researchers and interns in machine learning best practices

Machine Learning Engineer | StartupAI | 2016 - 2018
• Implemented production ML models serving 1M+ users with sub-100ms latency
• Designed A/B testing framework for ML model evaluation and continuous improvement
• Built real-time fraud detection system reducing false positives by 40%
• Optimized recommendation algorithms increasing conversion rates by 25%

EDUCATION:
Ph.D. in Computer Science (Machine Learning) | MIT | 2016
• Dissertation: "Attention Mechanisms in Multi-Modal Deep Learning"
• GPA: 3.9/4.0, Summa Cum Laude

M.S. in Computer Science | Stanford University | 2014
B.S. in Computer Science & Mathematics | UC Berkeley | 2012

PUBLICATIONS & PATENTS:
• "Transformer-Based Multi-Modal Learning for Healthcare" - Nature AI (2023)
• "Efficient Neural Architecture Search for Edge Devices" - ICML (2022)
• "Federated Learning in Production Systems" - NeurIPS (2021)
• Patent: "Method for Real-Time Anomaly Detection in Streaming Data" (US Patent 11,234,567)

LEADERSHIP & ACHIEVEMENTS:
• Led $2M AI research initiative resulting in 3 production systems
• Keynote speaker at AI Summit 2023 (1000+ attendees)
• Winner of "Best AI Innovation" award at TechCorp (2022)
• Mentor in Women in AI program, guided 20+ early-career professionals
• Open source contributor: 5000+ GitHub stars across ML projects

CERTIFICATIONS:
• AWS Certified Machine Learning - Specialty
• Google Cloud Professional ML Engineer
• Certified Kubernetes Administrator (CKA)"""
            
            files = {
                'resume_file': ('comprehensive_resume.txt', io.StringIO(resume_content), 'text/plain')
            }
            
            data = {
                'job_title': 'Principal AI Architect - Advanced Analytics Platform',
                'job_description': '''We are seeking an exceptional Principal AI Architect to lead our advanced analytics platform development. This role involves architecting next-generation AI systems, leading cross-functional teams, and driving innovation in machine learning applications. The ideal candidate will have deep expertise in ML/AI, proven leadership experience, and a track record of delivering production-scale AI solutions.

Key Responsibilities:
- Design and architect scalable AI/ML systems handling petabyte-scale data
- Lead technical strategy for AI platform serving 100M+ users globally  
- Mentor and guide team of 15+ senior engineers and data scientists
- Drive research initiatives and translate cutting-edge research into products
- Collaborate with C-suite executives on AI strategy and roadmap
- Establish best practices for MLOps, model governance, and AI ethics
- Partner with product teams to identify AI opportunities and solutions''',
                'job_requirements': '''Required Qualifications:
- Ph.D. in Computer Science, Machine Learning, or related field
- 8+ years of hands-on experience in machine learning and AI
- 5+ years of technical leadership experience managing large engineering teams
- Expert-level proficiency in Python, TensorFlow/PyTorch, and cloud platforms
- Proven track record of deploying production ML systems at scale
- Strong background in deep learning, NLP, computer vision, or reinforcement learning
- Experience with distributed systems, microservices, and cloud architecture
- Published research in top-tier conferences (ICML, NeurIPS, ICLR, etc.)

Preferred Qualifications:
- Previous experience as Principal Engineer or Staff Engineer at tech companies
- Track record of leading AI initiatives with measurable business impact
- Experience with MLOps tools and practices (MLflow, Kubeflow, etc.)
- Knowledge of AI ethics, fairness, and responsible AI practices
- Strong communication skills and ability to present to executive leadership
- Experience mentoring and developing high-performing engineering teams'''
            }
            
            response = self.session.post(
                f"{self.base_url}/admin/upload-job",
                files=files,
                data=data,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                result = response.json()
                success = (result.get("success", False) and 
                          "token" in result and 
                          "resume_preview" in result)
                if success:
                    self.generated_token = result["token"]
            
            details = f"Status: {response.status_code}, Token: {self.generated_token[:8] if self.generated_token else 'None'}..."
            self.log_test("Create Comprehensive Interview Session", success, details)
            return success
        except Exception as e:
            self.log_test("Create Comprehensive Interview Session", False, f"Exception: {str(e)}")
            return False
    
    def start_interview_session(self) -> bool:
        """Start the interview session"""
        if not self.generated_token:
            self.log_test("Start Interview Session", False, "No token available")
            return False
        
        try:
            payload = {
                "token": self.generated_token,
                "candidate_name": "Dr. Sarah Chen",
                "voice_mode": False
            }
            response = self.session.post(
                f"{self.base_url}/candidate/start-interview",
                json=payload,
                timeout=15
            )
            
            success = response.status_code == 200
            if success:
                data = response.json()
                success = ("session_id" in data and 
                          "first_question" in data and 
                          "question_number" in data)
                if success:
                    self.session_id = data["session_id"]
            
            details = f"Status: {response.status_code}, Session ID: {self.session_id[:8] if self.session_id else 'None'}..."
            self.log_test("Start Interview Session", success, details)
            return success
        except Exception as e:
            self.log_test("Start Interview Session", False, f"Exception: {str(e)}")
            return False
    
    def conduct_comprehensive_interview(self) -> bool:
        """Conduct a comprehensive interview with detailed answers for AI analysis"""
        if not self.generated_token:
            self.log_test("Conduct Comprehensive Interview", False, "No token available")
            return False
        
        # Comprehensive answers that will provide rich data for AI analysis
        comprehensive_answers = [
            # Technical Question 1 - Architecture & System Design
            """I approach large-scale AI system architecture with a focus on scalability, reliability, and maintainability. For our recent multi-modal AI platform at TechCorp, I designed a microservices architecture using Kubernetes orchestration. The system processes 10 million daily transactions with 99.7% accuracy.

Key architectural principles I follow:
1. Separation of concerns - distinct services for data ingestion, preprocessing, model inference, and result aggregation
2. Horizontal scalability - using auto-scaling groups and load balancers to handle traffic spikes
3. Fault tolerance - implementing circuit breakers, retry mechanisms, and graceful degradation
4. Model versioning - A/B testing framework for safe model deployments

For the data pipeline, I implemented a streaming architecture using Apache Kafka for real-time data ingestion, with Apache Spark for distributed processing. We use feature stores for consistent feature engineering across training and inference. The inference layer uses TensorFlow Serving with GPU acceleration, achieving sub-100ms latency even for complex deep learning models.

Monitoring is crucial - we use Prometheus and Grafana for system metrics, MLflow for model performance tracking, and custom dashboards for business KPIs. This comprehensive approach reduced our deployment time from weeks to hours while maintaining high reliability.""",

            # Technical Question 2 - Machine Learning Innovation
            """My most impactful ML innovation was developing a novel attention mechanism for multi-modal learning, which became the foundation for our healthcare diagnostic AI tool. The challenge was combining medical images, patient history text, and structured lab data into a unified prediction model.

Traditional approaches treated each modality separately, losing crucial cross-modal relationships. I designed a cross-attention transformer architecture that learns dynamic relationships between different data types. The key innovation was a learnable attention weighting mechanism that adapts based on the specific case - for some diagnoses, images are most important, while for others, lab values dominate.

Technical implementation details:
- Custom transformer blocks with cross-modal attention layers
- Positional encoding adapted for medical time series data
- Regularization techniques to prevent overfitting on small medical datasets
- Uncertainty quantification using Monte Carlo dropout for clinical safety

Results were remarkable: 15% improvement in diagnostic accuracy over previous state-of-the-art, published in Nature AI with 200+ citations. More importantly, the FDA approved our tool for clinical use, and it's now deployed in 50+ hospitals. This work demonstrates how theoretical ML advances can create real-world impact in critical applications like healthcare.""",

            # Technical Question 3 - Team Leadership & Technical Strategy
            """Leading a team of 12 engineers across three time zones requires both technical expertise and strong leadership skills. My approach combines clear technical vision with empowering individual growth.

Technical Leadership Strategy:
1. Establish clear architectural principles and coding standards
2. Implement robust code review processes with automated testing
3. Create technical roadmaps aligned with business objectives
4. Foster knowledge sharing through tech talks and documentation

For the distributed team challenge, I implemented several solutions:
- Asynchronous communication using Slack and Notion for documentation
- Overlapping hours for critical collaboration (9 AM PST / 12 PM EST / 9 PM IST)
- Rotating meeting times to share timezone burden fairly
- Clear handoff procedures between regions

One specific example: When we needed to reduce model training time by 60%, I led the technical strategy to implement distributed training. I worked with the team to:
- Analyze bottlenecks in our existing pipeline
- Research and prototype distributed training frameworks (Horovod, PyTorch DDP)
- Design data parallelism strategy for our specific models
- Implement gradient compression and mixed precision training

The key was balancing technical depth with delegation - I provided architectural guidance while empowering team members to own specific components. This approach not only achieved our performance goals but also developed the team's expertise in distributed systems.""",

            # Technical Question 4 - Problem Solving & Innovation
            """The most challenging technical problem I solved was building a real-time fraud detection system that needed to process 100,000 transactions per second with sub-50ms latency while maintaining high accuracy and low false positive rates.

The complexity came from multiple constraints:
- Real-time processing requirements (< 50ms response time)
- High throughput (100K TPS)
- Complex feature engineering from streaming data
- Model accuracy requirements (> 99% precision, > 95% recall)
- Regulatory compliance for financial data

My solution involved several innovative approaches:

1. Hybrid Architecture: Combined rule-based filters for obvious cases with ML models for complex patterns
2. Feature Engineering Pipeline: Real-time feature computation using Apache Flink with sliding window aggregations
3. Model Ensemble: Gradient boosting for structured features + neural networks for sequence patterns
4. Caching Strategy: Redis cluster for hot features and model predictions
5. A/B Testing Framework: Safe deployment of model updates with automatic rollback

The breakthrough came from realizing that most fraud patterns have temporal dependencies. I designed a sequence-to-sequence model that captures transaction patterns over time windows. This increased detection accuracy by 25% while reducing false positives by 40%.

Implementation challenges included:
- Memory optimization for real-time feature stores
- Model quantization for faster inference
- Distributed model serving with consistent hashing
- Monitoring and alerting for model drift

The system now processes over 1 billion transactions monthly, saving the company $50M annually in fraud losses. This project taught me the importance of understanding business constraints alongside technical requirements.""",

            # Behavioral Question 1 - Leadership & Conflict Resolution
            """I faced a significant leadership challenge when two senior engineers on my team had fundamentally different approaches to implementing our new recommendation system. One advocated for a deep learning approach using transformers, while the other pushed for a more traditional collaborative filtering method with gradient boosting.

The conflict was affecting team morale and delaying our project timeline. Both engineers were highly skilled and had valid technical arguments, but they were becoming entrenched in their positions.

My approach to resolution:
1. Individual conversations: I met with each engineer separately to understand their perspectives and concerns
2. Technical deep-dive: I organized a structured technical review where both approaches were evaluated against our specific requirements
3. Prototype comparison: I suggested we implement small-scale prototypes of both approaches to gather empirical data
4. Collaborative decision-making: I facilitated a team meeting where we evaluated results together

The key insight was that both engineers were optimizing for different metrics - one for accuracy, the other for interpretability and computational efficiency. I helped the team realize we could combine both approaches: use the transformer model for complex user patterns and the collaborative filtering for simpler cases.

This hybrid solution actually outperformed either individual approach and gave both engineers ownership of critical components. The experience taught me that technical conflicts often stem from different priorities rather than right vs. wrong solutions. As a leader, my role is to help the team find solutions that leverage everyone's strengths while meeting business objectives.""",

            # Behavioral Question 2 - Innovation & Risk Taking
            """I took a significant calculated risk when I proposed implementing federated learning for our client's healthcare AI system. This was 2019, and federated learning was still largely academic with limited production deployments.

The challenge: Our healthcare client needed to train models on sensitive patient data across multiple hospitals, but data privacy regulations prevented centralized data collection. Traditional approaches would require each hospital to train separate models, leading to poor performance due to limited data.

The risk factors:
- Unproven technology in production healthcare environments
- Significant engineering effort with uncertain outcomes
- Regulatory compliance concerns
- Client skepticism about new approaches

My risk mitigation strategy:
1. Proof of concept: I led a small team to build a prototype using synthetic medical data
2. Literature review: Comprehensive analysis of federated learning research and potential pitfalls
3. Regulatory consultation: Worked with legal team to understand compliance implications
4. Phased implementation: Proposed gradual rollout starting with non-critical use cases

The breakthrough came when our prototype showed 30% better model performance compared to individual hospital models, while maintaining strict data privacy. I presented these results to the client with a detailed implementation plan and risk assessment.

Results exceeded expectations:
- Successfully deployed federated learning across 8 hospitals
- Achieved state-of-the-art diagnostic accuracy while maintaining data privacy
- Published our approach at NeurIPS 2021, establishing our company as a thought leader
- Led to $5M in additional contracts from other healthcare clients

This experience taught me that calculated risks in emerging technologies can create significant competitive advantages. The key is thorough preparation, clear success metrics, and having contingency plans.""",

            # Behavioral Question 3 - Continuous Learning & Adaptation
            """Staying current in AI/ML requires a systematic approach given the field's rapid evolution. I've developed a multi-faceted learning strategy that balances depth and breadth.

My continuous learning framework:

1. Research Engagement:
- Subscribe to key venues (ICML, NeurIPS, ICLR proceedings)
- Weekly paper reviews with my team - we discuss 2-3 papers each Friday
- Maintain relationships with academic collaborators at MIT and Stanford
- Attend major conferences annually (NeurIPS, ICML, ICLR)

2. Hands-on Experimentation:
- Personal research projects exploring emerging techniques
- Kaggle competitions to test new methods on real problems
- Open source contributions to major ML frameworks
- Internal hackathons to explore new technologies

3. Community Involvement:
- Mentor in Women in AI program - teaching others reinforces my own learning
- Regular tech talks at meetups and conferences
- Active on ML Twitter and research communities
- Peer discussions with other industry leaders

Recent example: When GPT-3 was released, I immediately saw potential applications for our NLP systems. I spent weekends experimenting with the API, built several prototypes, and presented findings to leadership. This led to a successful project integrating large language models into our customer service platform, improving response quality by 40%.

Another example: I noticed growing interest in MLOps and model governance. I took Google's ML Engineering course, implemented MLflow in our production systems, and established model monitoring practices. This proactive learning prevented several potential model drift issues.

The key is balancing theoretical understanding with practical application. I don't just read papers - I implement key ideas and test them on real problems. This approach has kept me at the forefront of AI developments and enabled me to guide my team's technical direction effectively.""",

            # Behavioral Question 4 - Mentorship & Team Development
            """Developing junior team members is one of my most rewarding responsibilities. I've mentored over 20 engineers and data scientists, with 15 receiving promotions during our collaboration.

My mentorship philosophy centers on three principles:

1. Individualized Development Plans:
I work with each mentee to understand their career goals, strengths, and growth areas. For example, I mentored a junior ML engineer who wanted to transition into research. I helped her:
- Identify research problems aligned with business needs
- Develop paper-writing skills through internal technical reports
- Present at conferences and build her research network
- Balance research interests with product delivery responsibilities

She's now a senior research scientist and has published 3 papers.

2. Progressive Challenge and Support:
I believe in stretching people just beyond their comfort zone while providing necessary support. With a new graduate hire, I:
- Started with well-defined tasks with clear success criteria
- Gradually increased complexity and ambiguity
- Provided regular feedback and course correction
- Celebrated successes and treated failures as learning opportunities

This approach helped him grow from implementing basic ML models to leading the architecture of our recommendation system.

3. Knowledge Transfer and Documentation:
I ensure mentees don't just learn to do tasks, but understand the reasoning behind decisions. I encourage:
- Technical documentation of their work
- Presenting their solutions to the broader team
- Teaching others what they've learned
- Contributing to our internal knowledge base

Specific example: When mentoring a data scientist struggling with production ML systems, I paired her with our MLOps engineer for a month. She learned deployment practices hands-on while contributing to our model serving infrastructure. This cross-functional mentoring approach gave her both technical skills and broader perspective.

The most rewarding aspect is seeing mentees become mentors themselves. Several of my former mentees now lead their own teams and have adopted similar development approaches. This creates a multiplier effect that strengthens our entire engineering organization."""
        ]
        
        try:
            for i, answer in enumerate(comprehensive_answers):
                payload = {
                    "token": self.generated_token,
                    "message": answer
                }
                
                response = self.session.post(
                    f"{self.base_url}/candidate/send-message",
                    json=payload,
                    timeout=30  # Longer timeout for AI processing
                )
                
                if response.status_code != 200:
                    details = f"Failed at question {i+1}, Status: {response.status_code}, Response: {response.text[:200]}"
                    self.log_test("Conduct Comprehensive Interview", False, details)
                    return False
                
                data = response.json()
                
                # Check if interview is completed
                if data.get("completed", False):
                    if "assessment_id" in data:
                        self.assessment_id = data["assessment_id"]
                    success = i >= 6  # Should complete after sufficient questions
                    details = f"Interview completed after {i+1} questions, Assessment ID: {self.assessment_id[:8] if self.assessment_id else 'None'}..."
                    self.log_test("Conduct Comprehensive Interview", success, details)
                    return success
                
                # Small delay between questions
                time.sleep(2)
            
            # If we reach here, interview didn't complete as expected
            self.log_test("Conduct Comprehensive Interview", False, "Interview didn't complete after all questions")
            return False
            
        except Exception as e:
            self.log_test("Conduct Comprehensive Interview", False, f"Exception: {str(e)}")
            return False
    
    def test_enhanced_detailed_report(self) -> bool:
        """Test the enhanced detailed report endpoint with comprehensive AI analysis"""
        if not self.session_id:
            self.log_test("Enhanced Detailed Report", False, "No session ID available")
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/admin/detailed-report/{self.session_id}",
                timeout=30  # Longer timeout for comprehensive analysis
            )
            
            success = response.status_code == 200
            if not success:
                details = f"Status: {response.status_code}, Response: {response.text[:300]}"
                self.log_test("Enhanced Detailed Report", success, details)
                return False
            
            data = response.json()
            
            # Verify basic report structure
            required_fields = ["report", "session_info", "candidate_info"]
            for field in required_fields:
                if field not in data:
                    details = f"Missing required field: {field}"
                    self.log_test("Enhanced Detailed Report", False, details)
                    return False
            
            report = data["report"]
            
            # Test 1: Individual Question Scoring
            individual_scores_present = "individual_question_scores" in report
            if individual_scores_present:
                individual_scores = report["individual_question_scores"]
                if isinstance(individual_scores, list) and len(individual_scores) > 0:
                    # Check structure of individual scores
                    first_score = individual_scores[0]
                    required_score_fields = ["question_number", "question_text", "answer_text", "accuracy_score", "relevance_score", "completeness_score", "individual_score"]
                    individual_scores_valid = all(field in first_score for field in required_score_fields)
                else:
                    individual_scores_valid = False
            else:
                individual_scores_valid = False
            
            # Test 2: Average Individual Score Calculation
            avg_individual_score_present = "average_individual_score" in report
            if avg_individual_score_present and individual_scores_present:
                avg_score = report["average_individual_score"]
                # Verify calculation
                calculated_avg = sum(score["individual_score"] for score in individual_scores) / len(individual_scores)
                avg_calculation_correct = abs(avg_score - calculated_avg) < 0.01
            else:
                avg_calculation_correct = False
            
            # Test 3: Big Five Personality Analysis
            personality_analysis_present = "personality_analysis" in report
            if personality_analysis_present:
                personality = report["personality_analysis"]
                big_five_traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
                personality_valid = all(trait in personality for trait in big_five_traits)
            else:
                personality_valid = False
            
            # Test 4: Bias Detection and Fairness Metrics
            bias_analysis_present = "bias_analysis" in report
            if bias_analysis_present:
                bias_analysis = report["bias_analysis"]
                required_bias_fields = ["overall_bias_score", "fairness_metrics", "bias_indicators"]
                bias_analysis_valid = all(field in bias_analysis for field in required_bias_fields)
                
                if bias_analysis_valid and "fairness_metrics" in bias_analysis:
                    fairness_metrics = bias_analysis["fairness_metrics"]
                    fairness_fields = ["demographic_parity", "equalized_odds", "calibration"]
                    fairness_metrics_valid = all(field in fairness_metrics for field in fairness_fields)
                else:
                    fairness_metrics_valid = False
            else:
                bias_analysis_valid = False
                fairness_metrics_valid = False
            
            # Test 5: Predictive Hiring Analytics with ML Insights
            predictive_analytics_present = "predictive_analytics" in report
            if predictive_analytics_present:
                predictive = report["predictive_analytics"]
                required_predictive_fields = ["success_probability", "performance_prediction", "retention_likelihood", "ml_insights"]
                predictive_valid = all(field in predictive for field in required_predictive_fields)
            else:
                predictive_valid = False
            
            # Test 6: Speech Analysis Capabilities (if voice mode was used)
            speech_analysis_present = "speech_analysis" in report
            if speech_analysis_present:
                speech_analysis = report["speech_analysis"]
                speech_fields = ["voice_confidence", "speech_pace", "emotional_indicators"]
                speech_analysis_valid = any(field in speech_analysis for field in speech_fields)
            else:
                # Speech analysis might not be present for text-only interviews
                speech_analysis_valid = True  # Don't fail if not present
            
            # Test 7: Enhanced Communication, Technical, and Behavioral Analysis
            enhanced_analysis_present = all(field in report for field in [
                "communication_analysis", "technical_analysis", "behavioral_analysis"
            ])
            
            if enhanced_analysis_present:
                comm_analysis = report["communication_analysis"]
                tech_analysis = report["technical_analysis"]
                behav_analysis = report["behavioral_analysis"]
                
                # Check for enhanced fields
                enhanced_comm_valid = "clarity_score" in comm_analysis and "articulation_score" in comm_analysis
                enhanced_tech_valid = "depth_score" in tech_analysis and "innovation_score" in tech_analysis
                enhanced_behav_valid = "leadership_score" in behav_analysis and "adaptability_score" in behav_analysis
                
                enhanced_analysis_valid = enhanced_comm_valid and enhanced_tech_valid and enhanced_behav_valid
            else:
                enhanced_analysis_valid = False
            
            # Compile results
            test_results = {
                "Individual Question Scoring": individual_scores_valid,
                "Average Individual Score Calculation": avg_calculation_correct,
                "Big Five Personality Analysis": personality_valid,
                "Bias Detection & Fairness Metrics": bias_analysis_valid and fairness_metrics_valid,
                "Predictive Hiring Analytics": predictive_valid,
                "Speech Analysis Capabilities": speech_analysis_valid,
                "Enhanced Analysis Components": enhanced_analysis_valid
            }
            
            # Overall success
            overall_success = all(test_results.values())
            
            # Detailed results
            passed_tests = sum(test_results.values())
            total_tests = len(test_results)
            
            details = f"Comprehensive AI Analysis Tests: {passed_tests}/{total_tests} passed\n"
            for test_name, result in test_results.items():
                status = "✅" if result else "❌"
                details += f"   {status} {test_name}\n"
            
            if individual_scores_present:
                details += f"   📊 Individual Questions Analyzed: {len(individual_scores)}\n"
            if avg_individual_score_present:
                details += f"   📈 Average Individual Score: {report['average_individual_score']:.2f}\n"
            if personality_analysis_present:
                details += f"   🧠 Personality Traits Analyzed: {len(personality.keys())}\n"
            if predictive_analytics_present:
                details += f"   🔮 Success Probability: {predictive['success_probability']:.2f}\n"
            
            self.log_test("Enhanced Detailed Report", overall_success, details.strip())
            return overall_success
            
        except Exception as e:
            self.log_test("Enhanced Detailed Report", False, f"Exception: {str(e)}")
            return False
    
    def test_individual_question_scoring_accuracy(self) -> bool:
        """Test the accuracy of individual question scoring"""
        if not self.session_id:
            self.log_test("Individual Question Scoring Accuracy", False, "No session ID available")
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/admin/detailed-report/{self.session_id}",
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test("Individual Question Scoring Accuracy", False, f"Failed to get report: {response.status_code}")
                return False
            
            data = response.json()
            report = data.get("report", {})
            
            if "individual_question_scores" not in report:
                self.log_test("Individual Question Scoring Accuracy", False, "No individual question scores found")
                return False
            
            individual_scores = report["individual_question_scores"]
            
            # Validate scoring accuracy
            scoring_issues = []
            
            for i, score_data in enumerate(individual_scores):
                question_num = score_data.get("question_number", i+1)
                
                # Check score ranges (should be 0-100)
                accuracy = score_data.get("accuracy_score", 0)
                relevance = score_data.get("relevance_score", 0)
                completeness = score_data.get("completeness_score", 0)
                individual_score = score_data.get("individual_score", 0)
                
                if not (0 <= accuracy <= 100):
                    scoring_issues.append(f"Q{question_num}: Accuracy score out of range: {accuracy}")
                if not (0 <= relevance <= 100):
                    scoring_issues.append(f"Q{question_num}: Relevance score out of range: {relevance}")
                if not (0 <= completeness <= 100):
                    scoring_issues.append(f"Q{question_num}: Completeness score out of range: {completeness}")
                if not (0 <= individual_score <= 100):
                    scoring_issues.append(f"Q{question_num}: Individual score out of range: {individual_score}")
                
                # Check if individual score is reasonable composite of component scores
                expected_individual = (accuracy + relevance + completeness) / 3
                if abs(individual_score - expected_individual) > 5:  # Allow 5-point variance
                    scoring_issues.append(f"Q{question_num}: Individual score ({individual_score}) doesn't match components average ({expected_individual:.1f})")
            
            success = len(scoring_issues) == 0
            
            if success:
                details = f"All {len(individual_scores)} questions scored correctly with valid ranges and calculations"
            else:
                details = f"Found {len(scoring_issues)} scoring issues:\n" + "\n".join(f"   • {issue}" for issue in scoring_issues[:5])
                if len(scoring_issues) > 5:
                    details += f"\n   • ... and {len(scoring_issues) - 5} more issues"
            
            self.log_test("Individual Question Scoring Accuracy", success, details)
            return success
            
        except Exception as e:
            self.log_test("Individual Question Scoring Accuracy", False, f"Exception: {str(e)}")
            return False
    
    def test_ai_analysis_data_structure(self) -> bool:
        """Validate the comprehensive analysis data structure"""
        if not self.session_id:
            self.log_test("AI Analysis Data Structure", False, "No session ID available")
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/admin/detailed-report/{self.session_id}",
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test("AI Analysis Data Structure", False, f"Failed to get report: {response.status_code}")
                return False
            
            data = response.json()
            
            # Validate top-level structure
            required_top_level = ["report", "session_info", "candidate_info"]
            structure_issues = []
            
            for field in required_top_level:
                if field not in data:
                    structure_issues.append(f"Missing top-level field: {field}")
            
            if "report" not in data:
                self.log_test("AI Analysis Data Structure", False, "Missing report field")
                return False
            
            report = data["report"]
            
            # Validate report structure
            expected_report_sections = [
                "individual_question_scores",
                "average_individual_score", 
                "personality_analysis",
                "bias_analysis",
                "predictive_analytics",
                "communication_analysis",
                "technical_analysis",
                "behavioral_analysis"
            ]
            
            for section in expected_report_sections:
                if section not in report:
                    structure_issues.append(f"Missing report section: {section}")
            
            # Validate individual question scores structure
            if "individual_question_scores" in report:
                scores = report["individual_question_scores"]
                if isinstance(scores, list) and len(scores) > 0:
                    required_score_fields = [
                        "question_number", "question_text", "answer_text",
                        "accuracy_score", "relevance_score", "completeness_score", "individual_score"
                    ]
                    for field in required_score_fields:
                        if field not in scores[0]:
                            structure_issues.append(f"Missing individual score field: {field}")
            
            # Validate personality analysis structure
            if "personality_analysis" in report:
                personality = report["personality_analysis"]
                big_five = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
                for trait in big_five:
                    if trait not in personality:
                        structure_issues.append(f"Missing personality trait: {trait}")
            
            # Validate bias analysis structure
            if "bias_analysis" in report:
                bias = report["bias_analysis"]
                required_bias_fields = ["overall_bias_score", "fairness_metrics", "bias_indicators"]
                for field in required_bias_fields:
                    if field not in bias:
                        structure_issues.append(f"Missing bias analysis field: {field}")
            
            # Validate predictive analytics structure
            if "predictive_analytics" in report:
                predictive = report["predictive_analytics"]
                required_predictive_fields = ["success_probability", "performance_prediction", "retention_likelihood"]
                for field in required_predictive_fields:
                    if field not in predictive:
                        structure_issues.append(f"Missing predictive analytics field: {field}")
            
            success = len(structure_issues) == 0
            
            if success:
                details = "All required data structure components present and correctly formatted"
            else:
                details = f"Found {len(structure_issues)} structure issues:\n" + "\n".join(f"   • {issue}" for issue in structure_issues[:10])
                if len(structure_issues) > 10:
                    details += f"\n   • ... and {len(structure_issues) - 10} more issues"
            
            self.log_test("AI Analysis Data Structure", success, details)
            return success
            
        except Exception as e:
            self.log_test("AI Analysis Data Structure", False, f"Exception: {str(e)}")
            return False
    
    def run_comprehensive_ai_analysis_tests(self) -> Dict[str, bool]:
        """Run all enhanced AI analysis tests"""
        print("=" * 80)
        print("ENHANCED AI INTERVIEW ANALYSIS REPORT TESTING")
        print("Testing Comprehensive AI Analysis Features")
        print("=" * 80)
        print()
        
        results = {}
        
        # Setup phase
        results["admin_login"] = self.test_admin_login()
        results["create_interview_session"] = self.create_comprehensive_interview_session()
        results["start_interview"] = self.start_interview_session()
        results["conduct_interview"] = self.conduct_comprehensive_interview()
        
        # Core AI analysis testing
        results["enhanced_detailed_report"] = self.test_enhanced_detailed_report()
        results["individual_scoring_accuracy"] = self.test_individual_question_scoring_accuracy()
        results["ai_analysis_data_structure"] = self.test_ai_analysis_data_structure()
        
        # Summary
        print("=" * 80)
        print("ENHANCED AI ANALYSIS TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        # Group results by category
        categories = {
            "Setup Phase": ["admin_login", "create_interview_session", "start_interview", "conduct_interview"],
            "AI Analysis Features": ["enhanced_detailed_report", "individual_scoring_accuracy", "ai_analysis_data_structure"]
        }
        
        for category, test_names in categories.items():
            print(f"\n{category}:")
            for test_name in test_names:
                if test_name in results:
                    status = "✅ PASS" if results[test_name] else "❌ FAIL"
                    print(f"  {status} {test_name}")
        
        print()
        print(f"OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Enhanced AI analysis features are working correctly.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Most AI analysis features are functional.")
        else:
            print("⚠️  Multiple tests failed. Enhanced AI analysis needs attention.")
        
        return results

def main():
    """Main test execution"""
    tester = EnhancedAIAnalysisTester()
    results = tester.run_comprehensive_ai_analysis_tests()
    
    # Return exit code based on results
    all_passed = all(results.values())
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())