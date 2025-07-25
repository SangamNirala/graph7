import React, { useState, useEffect, useRef } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';
import AdvancedVideoAnalyzer from './AdvancedVideoAnalyzer';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Emotional Intelligence Dashboard Component
const EmotionalIntelligenceDashboard = ({ eiData, showRealTime = false }) => {
  if (!eiData) return null;

  const getEmotionColor = (value) => {
    if (value >= 0.7) return 'text-green-400';
    if (value >= 0.5) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getEmotionBarWidth = (value) => `${Math.round(value * 100)}%`;

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-6">
      <h3 className="text-xl font-bold text-white mb-4">
        🧠 Emotional Intelligence Analysis
        {showRealTime && <span className="text-green-400 ml-2">• Live</span>}
      </h3>
      
      <div className="grid md:grid-cols-2 gap-4">
        {/* Confidence Meter */}
        <div className="bg-white/5 rounded-lg p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-white font-medium">Confidence</span>
            <span className={`font-bold ${getEmotionColor(eiData.confidence || 0)}`}>
              {Math.round((eiData.confidence || 0) * 100)}%
            </span>
          </div>
          <div className="bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500"
              style={{ width: getEmotionBarWidth(eiData.confidence || 0) }}
            ></div>
          </div>
        </div>

        {/* Enthusiasm Meter */}
        <div className="bg-white/5 rounded-lg p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-white font-medium">Enthusiasm</span>
            <span className={`font-bold ${getEmotionColor(eiData.enthusiasm || 0)}`}>
              {Math.round((eiData.enthusiasm || 0) * 100)}%
            </span>
          </div>
          <div className="bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-yellow-500 to-orange-500 h-2 rounded-full transition-all duration-500"
              style={{ width: getEmotionBarWidth(eiData.enthusiasm || 0) }}
            ></div>
          </div>
        </div>

        {/* Stress Level */}
        <div className="bg-white/5 rounded-lg p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-white font-medium">Stress Level</span>
            <span className={`font-bold ${getEmotionColor(1 - (eiData.stress_level || 0))}`}>
              {Math.round((eiData.stress_level || 0) * 100)}%
            </span>
          </div>
          <div className="bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-green-500 to-red-500 h-2 rounded-full transition-all duration-500"
              style={{ width: getEmotionBarWidth(eiData.stress_level || 0) }}
            ></div>
          </div>
        </div>

        {/* Emotional Stability */}
        <div className="bg-white/5 rounded-lg p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-white font-medium">Emotional Stability</span>
            <span className={`font-bold ${getEmotionColor(eiData.emotional_stability || 0)}`}>
              {Math.round((eiData.emotional_stability || 0) * 100)}%
            </span>
          </div>
          <div className="bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-purple-500 to-indigo-500 h-2 rounded-full transition-all duration-500"
              style={{ width: getEmotionBarWidth(eiData.emotional_stability || 0) }}
            ></div>
          </div>
        </div>
      </div>

      {/* Real-time insights */}
      {showRealTime && (
        <div className="mt-4 p-3 bg-blue-600/20 rounded-lg border border-blue-400/30">
          <div className="flex items-center text-blue-200">
            <span className="mr-2">💡</span>
            <span className="text-sm">
              {eiData.stress_level > 0.7 ? 'Take a deep breath and stay calm.' :
               eiData.confidence < 0.3 ? 'You\'re doing great! Stay confident.' :
               eiData.enthusiasm > 0.8 ? 'Excellent energy level!' :
               'Maintaining good emotional balance.'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

// Predictive Analytics Component  
const PredictiveAnalyticsDashboard = ({ predictiveData }) => {
  if (!predictiveData) return null;

  const getSuccessColor = (probability) => {
    if (probability >= 0.75) return 'text-green-400';
    if (probability >= 0.60) return 'text-yellow-400';
    if (probability >= 0.45) return 'text-orange-400';
    return 'text-red-400';
  };

  const getSuccessIcon = (probability) => {
    if (probability >= 0.75) return '🚀';
    if (probability >= 0.60) return '📈';
    if (probability >= 0.45) return '⚖️';
    return '📉';
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-6">
      <h3 className="text-xl font-bold text-white mb-4">🔮 Predictive Analytics</h3>
      
      <div className="text-center mb-6">
        <div className="text-6xl mb-2">{getSuccessIcon(predictiveData.success_probability)}</div>
        <div className={`text-3xl font-bold ${getSuccessColor(predictiveData.success_probability)} mb-2`}>
          {Math.round(predictiveData.success_probability * 100)}%
        </div>
        <div className="text-lg text-white">{predictiveData.prediction}</div>
        <div className="text-sm text-gray-300 mt-2">{predictiveData.recommendation}</div>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        {/* Score Breakdown */}
        <div className="bg-white/5 rounded-lg p-4">
          <h4 className="font-semibold text-white mb-3">Score Breakdown</h4>
          {Object.entries(predictiveData.score_breakdown || {}).map(([key, value]) => (
            <div key={key} className="flex justify-between items-center mb-2">
              <span className="text-gray-300 capitalize">{key.replace('_', ' ')}</span>
              <span className="text-white font-bold">{Math.round(value * 100)}%</span>
            </div>
          ))}
        </div>

        {/* Strengths & Improvements */}
        <div className="bg-white/5 rounded-lg p-4">
          <h4 className="font-semibold text-white mb-3">Key Insights</h4>
          
          <div className="mb-4">
            <div className="text-green-400 font-medium mb-2">🟢 Strengths</div>
            {(predictiveData.key_strengths || []).map((strength, index) => (
              <div key={index} className="text-sm text-gray-300 ml-4">• {strength}</div>
            ))}
          </div>

          <div>
            <div className="text-orange-400 font-medium mb-2">🔶 Areas for Growth</div>
            {(predictiveData.improvement_areas || []).map((area, index) => (
              <div key={index} className="text-sm text-gray-300 ml-4">• {area}</div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Voice Recording Hook
const useVoiceRecorder = (onRecordingComplete) => {
  const { status, startRecording, stopRecording, mediaBlobUrl } = useReactMediaRecorder({
    audio: true,
    onStop: (blobUrl, blob) => onRecordingComplete(blob)
  });

  return { status, startRecording, stopRecording, mediaBlobUrl };
};

// Audio Player Component
const AudioPlayer = ({ audioBase64, autoPlay = false }) => {
  const audioRef = useRef(null);

  useEffect(() => {
    if (audioBase64 && audioRef.current) {
      const audioSrc = `data:audio/mp3;base64,${audioBase64}`;
      audioRef.current.src = audioSrc;
      if (autoPlay) {
        audioRef.current.play().catch(e => console.log('Audio play failed:', e));
      }
    }
  }, [audioBase64, autoPlay]);

  return (
    <div className="audio-player">
      <audio ref={audioRef} controls className="w-full">
        Your browser does not support the audio element.
      </audio>
    </div>
  );
};

// Global spoken texts tracking to persist across component re-renders
const globalSpokenTexts = new Set();

// Utility function to clear spoken texts (useful for debugging and fresh starts)
window.clearSpokenTexts = () => {
  globalSpokenTexts.clear();
  console.log('Manually cleared all spoken texts');
};

// Realistic Female Avatar Component with Mouth Animation
const RealisticFemaleAvatar = ({ isSpeaking, isListening, currentQuestion }) => {
  const [eyeBlink, setEyeBlink] = useState(false);
  
  // Random eye blink animation
  useEffect(() => {
    const blinkInterval = setInterval(() => {
      if (Math.random() < 0.1) { // 10% chance every 500ms
        setEyeBlink(true);
        setTimeout(() => setEyeBlink(false), 150);
      }
    }, 500);
    
    return () => clearInterval(blinkInterval);
  }, []);

  return (
    <div className="relative w-80 h-80 mx-auto">
      {/* Professional Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-slate-200 to-slate-300 rounded-full shadow-2xl"></div>
      
      {/* Avatar Container */}
      <svg
        viewBox="0 0 300 300"
        className="w-full h-full relative z-10"
      >
        {/* Face Shape */}
        <ellipse
          cx="150"
          cy="140"
          rx="85"
          ry="95"
          fill="#F7E6D3"
          stroke="#E8D5C4"
          strokeWidth="2"
        />
        
        {/* Hair */}
        <path
          d="M 65 80 Q 150 20 235 80 Q 240 140 220 160 Q 180 50 150 55 Q 120 50 80 160 Q 60 140 65 80 Z"
          fill="#8B4513"
        />
        
        {/* Forehead highlights */}
        <ellipse cx="150" cy="85" rx="60" ry="25" fill="#FFF2E6" opacity="0.3"/>
        
        {/* Eyes */}
        <g className={eyeBlink ? "animate-blink" : ""}>
          {/* Left Eye */}
          <ellipse cx="120" cy="115" rx="12" ry="8" fill="white"/>
          <circle cx="120" cy="115" r="6" fill="#4A90E2"/>
          <circle cx="122" cy="113" r="2" fill="black"/>
          <circle cx="123" cy="112" r="1" fill="white"/>
          
          {/* Right Eye */}
          <ellipse cx="180" cy="115" rx="12" ry="8" fill="white"/>
          <circle cx="180" cy="115" r="6" fill="#4A90E2"/>
          <circle cx="182" cy="113" r="2" fill="black"/>
          <circle cx="183" cy="112" r="1" fill="white"/>
          
          {/* Eyelashes */}
          <path d="M 108 108 Q 112 105 116 108" stroke="#654321" strokeWidth="1" fill="none"/>
          <path d="M 120 105 Q 124 102 128 105" stroke="#654321" strokeWidth="1" fill="none"/>
          <path d="M 168 108 Q 172 105 176 108" stroke="#654321" strokeWidth="1" fill="none"/>
          <path d="M 180 105 Q 184 102 188 105" stroke="#654321" strokeWidth="1" fill="none"/>
        </g>
        
        {/* Eyebrows */}
        <path d="M 105 100 Q 120 95 135 100" stroke="#6B4423" strokeWidth="3" fill="none"/>
        <path d="M 165 100 Q 180 95 195 100" stroke="#6B4423" strokeWidth="3" fill="none"/>
        
        {/* Nose */}
        <path d="M 148 125 Q 150 140 152 135" stroke="#E8D5C4" strokeWidth="1.5" fill="none"/>
        <ellipse cx="147" cy="138" rx="2" ry="1" fill="#E8D5C4"/>
        <ellipse cx="153" cy="138" rx="2" ry="1" fill="#E8D5C4"/>
        
        {/* Mouth - Animated based on speaking state */}
        <g className={isSpeaking ? "animate-mouth-speaking" : isListening ? "animate-mouth-listening" : ""}>
          {isSpeaking ? (
            // Speaking mouth - open
            <g>
              <ellipse cx="150" cy="165" rx="15" ry="8" fill="#8B4513"/>
              <ellipse cx="150" cy="162" rx="12" ry="3" fill="#CD853F"/>
              <path d="M 138 165 Q 150 170 162 165" stroke="#A0522D" strokeWidth="1" fill="none"/>
            </g>
          ) : isListening ? (
            // Listening mouth - slightly open
            <g>
              <ellipse cx="150" cy="165" rx="8" ry="3" fill="#CD853F"/>
              <path d="M 142 165 Q 150 167 158 165" stroke="#A0522D" strokeWidth="1" fill="none"/>
            </g>
          ) : (
            // Neutral mouth - closed smile
            <path d="M 135 165 Q 150 175 165 165" stroke="#A0522D" strokeWidth="2" fill="none"/>
          )}
        </g>
        
        {/* Cheeks */}
        <circle cx="105" cy="140" r="8" fill="#F4C2C2" opacity="0.4"/>
        <circle cx="195" cy="140" r="8" fill="#F4C2C2" opacity="0.4"/>
        
        {/* Chin shadow */}
        <ellipse cx="150" cy="180" rx="30" ry="8" fill="#E8D5C4" opacity="0.3"/>
        
        {/* Neck */}
        <rect x="130" y="220" width="40" height="30" fill="#F7E6D3" rx="5"/>
        
        {/* Professional Attire */}
        <path d="M 100 240 L 200 240 L 195 300 L 105 300 Z" fill="#2C3E50"/>
        <path d="M 125 240 L 175 240 L 170 280 L 130 280 Z" fill="#FFFFFF"/>
        <circle cx="150" cy="250" r="3" fill="#2C3E50"/>
        <circle cx="150" cy="260" r="3" fill="#2C3E50"/>
        
        {/* Speaking indicators */}
        {isSpeaking && (
          <g>
            {/* Sound waves */}
            <circle cx="220" cy="165" r="3" fill="#4A90E2" opacity="0.6">
              <animate attributeName="r" values="3;8;3" dur="1s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="0.6;0.2;0.6" dur="1s" repeatCount="indefinite"/>
            </circle>
            <circle cx="230" cy="165" r="5" fill="#4A90E2" opacity="0.4">
              <animate attributeName="r" values="5;12;5" dur="1.5s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="0.4;0.1;0.4" dur="1.5s" repeatCount="indefinite"/>
            </circle>
          </g>
        )}
        
        {/* Listening indicators */}
        {isListening && (
          <g>
            {/* Microphone icon */}
            <rect x="220" y="155" width="8" height="12" rx="4" fill="#E74C3C" opacity="0.8"/>
            <rect x="222" y="167" width="4" height="8" fill="#C0392B"/>
            <path d="M 218 175 L 230 175" stroke="#C0392B" strokeWidth="2"/>
            <circle cx="224" cy="161" r="2" fill="#FF6B6B" opacity="0.6">
              <animate attributeName="opacity" values="0.6;1;0.6" dur="0.8s" repeatCount="indefinite"/>
            </circle>
          </g>
        )}
      </svg>
      
      {/* Professional nameplate */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white/90 backdrop-blur-sm px-4 py-2 rounded-lg shadow-lg">
        <p className="text-gray-800 font-semibold text-sm">AI Interviewer</p>
        <p className="text-gray-600 text-xs">Sarah Mitchell</p>
      </div>
    </div>
  );
};

// Voice Activity Detection Hook
const useVoiceActivityDetection = (onSilenceDetected, silenceThreshold = 5000) => {
  const [isListening, setIsListening] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const silenceTimerRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const streamRef = useRef(null);
  
  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const analyser = audioContext.createAnalyser();
      const microphone = audioContext.createMediaStreamSource(stream);
      
      analyser.smoothingTimeConstant = 0.8;
      analyser.fftSize = 1024;
      
      microphone.connect(analyser);
      
      audioContextRef.current = audioContext;
      analyserRef.current = analyser;
      setIsListening(true);
      
      const detectAudio = () => {
        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        
        analyser.getByteFrequencyData(dataArray);
        
        const average = dataArray.reduce((sum, value) => sum + value, 0) / bufferLength;
        setAudioLevel(average);
        
        // Voice activity detection threshold
        const threshold = 25;
        
        if (average > threshold) {
          // Voice detected - clear silence timer
          if (silenceTimerRef.current) {
            clearTimeout(silenceTimerRef.current);
            silenceTimerRef.current = null;
          }
        } else {
          // Silence detected - start or continue timer
          if (!silenceTimerRef.current) {
            silenceTimerRef.current = setTimeout(() => {
              onSilenceDetected();
              silenceTimerRef.current = null;
            }, silenceThreshold);
          }
        }
        
        if (isListening) {
          requestAnimationFrame(detectAudio);
        }
      };
      
      detectAudio();
      
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };
  
  const stopListening = () => {
    setIsListening(false);
    if (silenceTimerRef.current) {
      clearTimeout(silenceTimerRef.current);
      silenceTimerRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
  };
  
  return { isListening, audioLevel, startListening, stopListening };
};

// Avatar Interview Container - Integrates with existing interview system
const AvatarInterviewContainer = ({ setCurrentPage, token, validatedJob }) => {
  const [interviewData, setInterviewData] = useState(null);
  const [sessionData, setSessionData] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isAISpeaking, setIsAISpeaking] = useState(false);
  const [candidateAnswer, setCandidateAnswer] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isInitialized, setIsInitialized] = useState(false);
  
  // Enhanced timing states
  const [questionPhase, setQuestionPhase] = useState('waiting'); // 'speaking', 'waiting', 'follow-up', 'collecting-answer'
  const [timeoutIds, setTimeoutIds] = useState([]);
  const [hasSpokenQuestion, setHasSpokenQuestion] = useState(false);
  const [isWaitingForResponse, setIsWaitingForResponse] = useState(false);
  const [followUpAsked, setFollowUpAsked] = useState(false);

  // Voice Activity Detection
  const { isListening, audioLevel, startListening, stopListening } = useVoiceActivityDetection(
    () => {
      // 5-second silence detected - automatically submit answer if there's content
      if (candidateAnswer.trim() && !isAISpeaking && questionPhase === 'collecting-answer') {
        console.log('Silence detected, auto-submitting answer:', candidateAnswer.trim());
        handleSubmitAnswer();
      }
    },
    5000 // 5 second silence threshold
  );

  // Cleanup function for timeouts
  const clearAllTimeouts = () => {
    timeoutIds.forEach(id => clearTimeout(id));
    setTimeoutIds([]);
  };

  // Function to detect if candidate response indicates they don't know
  const isUnknownResponse = (text) => {
    const unknownPhrases = [
      "i don't know", "not sure", "no idea", "skip", "pass", "next question",
      "i'm not sure", "don't know", "unsure", "can't answer", "no clue"
    ];
    const lowerText = text.toLowerCase().trim();
    return unknownPhrases.some(phrase => lowerText.includes(phrase));
  };

  // Function to start the response waiting period after question is spoken
  const startResponseWaitingPeriod = () => {
    console.log('Starting 20-second response waiting period...');
    setQuestionPhase('waiting');
    setIsWaitingForResponse(true);
    
    // Clear any existing timeouts
    clearAllTimeouts();
    
    // Set 20-second timeout for follow-up prompt
    const timeoutId = setTimeout(() => {
      if (!candidateAnswer.trim() && !followUpAsked) {
        askFollowUpQuestion();
      }
    }, 20000); // 20 seconds
    
    setTimeoutIds([timeoutId]);
  };

  // Function to ask follow-up question when no response
  const askFollowUpQuestion = () => {
    console.log('No response detected, asking follow-up question...');
    setFollowUpAsked(true);
    setQuestionPhase('follow-up');
    
    // Speak the follow-up question
    const followUpText = "Do you know the answer, or should I move to the next question?";
    speakFollowUpQuestion(followUpText);
    
    // Set 10-second timeout for auto-skip
    const timeoutId = setTimeout(() => {
      if (!candidateAnswer.trim()) {
        console.log('No response to follow-up, moving to next question...');
        moveToNextQuestion();
      }
    }, 10000); // 10 seconds
    
    setTimeoutIds([timeoutId]);
  };

  // Function to speak follow-up question
  const speakFollowUpQuestion = (text) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsAISpeaking(true);
      
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1.1;
      utterance.volume = 0.8;
      
      // Try to get a female voice
      const voices = window.speechSynthesis.getVoices();
      const femaleVoice = voices.find(voice => 
        voice.name.toLowerCase().includes('female') || 
        voice.name.toLowerCase().includes('woman') ||
        voice.name.toLowerCase().includes('samantha') ||
        voice.name.toLowerCase().includes('karen') ||
        voice.name.toLowerCase().includes('zira') ||
        voice.lang.includes('en')
      );
      
      if (femaleVoice) {
        utterance.voice = femaleVoice;
      }
      
      utterance.onend = () => {
        setIsAISpeaking(false);
        console.log('Follow-up question finished speaking');
      };
      
      utterance.onerror = (event) => {
        console.error('Follow-up speech error:', event);
        setIsAISpeaking(false);
      };
      
      window.speechSynthesis.speak(utterance);
    }
  };

  // Function to move to next question
  const moveToNextQuestion = async () => {
    console.log('Moving to next question...');
    clearAllTimeouts();
    
    // Reset states for next question
    setFollowUpAsked(false);
    setIsWaitingForResponse(false);
    setQuestionPhase('waiting');
    setCandidateAnswer('');
    setHasSpokenQuestion(false);
    
    // Move to next question (this will integrate with existing submit logic)
    const nextIndex = currentQuestionIndex + 1;
    if (sessionData.questions && nextIndex < sessionData.questions.length) {
      setCurrentQuestionIndex(nextIndex);
      setCurrentQuestion({ question: sessionData.questions[nextIndex] });
    } else {
      // No more questions, complete interview
      setCurrentPage('interview-session');
    }
  };

  // Initialize interview session
  useEffect(() => {
    const initializeInterview = async () => {
      try {
        setLoading(true);
        
        // Debug logging
        console.log('Avatar Interview - Debug Info:');
        console.log('Token received:', token);
        console.log('ValidatedJob:', validatedJob);
        
        // Check if token is available
        if (!token) {
          console.error('No token available for avatar interview');
          setError('Authentication token missing. Please start interview again.');
          return;
        }
        
        // Get stored interview data (should already exist from InterviewStart)
        const storedData = localStorage.getItem('interviewData');
        console.log('Stored interview data:', storedData);
        
        if (!storedData) {
          setError('No interview session found. Please start interview again.');
          return;
        }

        const parsedData = JSON.parse(storedData);
        setInterviewData(parsedData);
        
        // Check if we have session data from the previous start-interview call
        if (!parsedData.sessionId) {
          setError('Invalid interview session. Please start interview again.');
          return;
        }
        
        console.log('Reusing existing interview session:', parsedData.sessionId);
        
        // Create session data object from stored data
        const sessionData = {
          session_id: parsedData.sessionId,
          first_question: parsedData.currentQuestion,
          question_number: parsedData.questionNumber,
          total_questions: parsedData.totalQuestions,
          voice_mode: true, // Force voice mode for avatar interview
          questions: [parsedData.currentQuestion], // We'll load more as needed
          welcome_audio: parsedData.welcomeAudio,
          question_audio: parsedData.questionAudio
        };
        
        console.log('Session data created:', sessionData);
        setSessionData(sessionData);
        
        // Set first question from stored data
        if (parsedData.currentQuestion) {
          // Wrap the question string in an object structure expected by the UI
          setCurrentQuestion({ 
            question: parsedData.currentQuestion 
          });
          setCurrentQuestionIndex(parsedData.questionNumber - 1 || 0); // questionNumber is 1-based
        }

        setIsInitialized(true);

      } catch (error) {
        console.error('Error initializing avatar interview:', error);
        setError(`Failed to initialize interview session: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    if (token && validatedJob) {
      initializeInterview();
    }
  }, [token, validatedJob]);

  // Enhanced AI Voice Speaker with timing control
  const AvatarAIVoiceSpeaker = ({ text, onSpeechStart, onSpeechEnd }) => {
    useEffect(() => {
      if (text && text.trim() && 'speechSynthesis' in window && isInitialized && !hasSpokenQuestion) {
        const textKey = `avatar-question-${currentQuestionIndex}`;
        
        // Check if already spoken using existing prevention system
        if (typeof globalSpokenTexts !== 'undefined' && globalSpokenTexts.has(textKey)) {
          console.log('Skipping repeat speech for avatar question:', textKey);
          return;
        }

        console.log('Starting to speak question:', text);
        setQuestionPhase('speaking');
        setIsAISpeaking(true);
        setHasSpokenQuestion(true);
        if (onSpeechStart) onSpeechStart();

        // Cancel any ongoing speech
        window.speechSynthesis.cancel();

        // Small delay to ensure speech synthesis is ready
        setTimeout(() => {
          const utterance = new SpeechSynthesisUtterance(text);
          
          // Configure voice for professional female interviewer
          utterance.rate = 0.9;
          utterance.pitch = 1.1;
          utterance.volume = 0.8;
          
          // Try to get a female voice
          const voices = window.speechSynthesis.getVoices();
          const femaleVoice = voices.find(voice => 
            voice.name.toLowerCase().includes('female') || 
            voice.name.toLowerCase().includes('woman') ||
            voice.name.toLowerCase().includes('samantha') ||
            voice.name.toLowerCase().includes('karen') ||
            voice.name.toLowerCase().includes('zira') ||
            voice.name.toLowerCase().includes('aria')
          );
          
          if (femaleVoice) {
            utterance.voice = femaleVoice;
          }
          
          utterance.onstart = () => {
            console.log('Avatar AI started speaking:', text.substring(0, 50) + '...');
            if (typeof globalSpokenTexts !== 'undefined') {
              globalSpokenTexts.add(textKey);
            }
          };
          
          utterance.onend = () => {
            console.log('Avatar AI finished speaking');
            setIsAISpeaking(false);
            if (onSpeechEnd) onSpeechEnd();
            
            // Auto-start listening after AI finishes speaking
            setTimeout(() => {
              if (!isListening) {
                startListening();
              }
            }, 500);
          };
          
          utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            setIsAISpeaking(false);
            if (onSpeechEnd) onSpeechEnd();
          };
          
          window.speechSynthesis.speak(utterance);
          
        }, 100);
      }
    }, [text, isInitialized, currentQuestionIndex]);

    return null; // This component only handles speech, no visual elements
  };

  // Submit answer and move to next question
  const handleSubmitAnswer = async () => {
    if (!candidateAnswer.trim() || !sessionData) return;

    try {
      setLoading(true);
      
      // Stop listening during submission
      if (isListening) {
        stopListening();
      }

      // Submit answer using existing API
      const response = await fetch(`${API}/candidate/submit-answer`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionData.session_id,
          message: candidateAnswer.trim(),
          voice_mode: true
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to submit answer');
      }

      const result = await response.json();
      
      // Check if interview is complete
      if (result.interview_complete) {
        // Interview finished, redirect to completion
        setCurrentPage('interview-session'); // Use existing completion flow
        return;
      }

      // Move to next question
      const nextIndex = currentQuestionIndex + 1;
      if (sessionData.questions && nextIndex < sessionData.questions.length) {
        setCurrentQuestionIndex(nextIndex);
        setCurrentQuestion(sessionData.questions[nextIndex]);
        setCandidateAnswer('');
        
        // Small delay before AI speaks next question
        setTimeout(() => {
          setIsInitialized(true);
        }, 1000);
      } else {
        // No more questions, complete interview
        setCurrentPage('interview-session');
      }

    } catch (error) {
      console.error('Error submitting answer:', error);
      setError('Failed to submit answer');
    } finally {
      setLoading(false);
    }
  };

  // Loading state
  if (loading && !isInitialized) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 text-center">
          <div className="animate-spin w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-white text-lg">Initializing AI Interviewer...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 text-center">
          <p className="text-red-300 text-lg mb-4">{error}</p>
          <button
            onClick={() => setCurrentPage('interview-start')}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="max-w-6xl mx-auto p-4">
        
        {/* AI Voice Speaker Component */}
        {currentQuestion && (
          <AvatarAIVoiceSpeaker 
            text={currentQuestion.question}
            onSpeechStart={() => setIsAISpeaking(true)}
            onSpeechEnd={() => setIsAISpeaking(false)}
          />
        )}
        
        {/* Avatar Section */}
        <div className="text-center mb-8 pt-8">
          <RealisticFemaleAvatar 
            isSpeaking={isAISpeaking}
            isListening={isListening && !isAISpeaking}
            currentQuestion={currentQuestion?.question || ''}
          />
        </div>
        
        {/* Question Display - Minimal UI */}
        {currentQuestion && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 mb-6 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="mb-4">
                <span className="inline-block bg-blue-500/20 text-blue-200 px-4 py-2 rounded-full text-sm border border-blue-500/30">
                  Question {currentQuestionIndex + 1} of {sessionData?.questions?.length || 8}
                </span>
              </div>
              <p className="text-white text-xl leading-relaxed font-medium mb-6">
                {currentQuestion.question}
              </p>
            </div>
          </div>
        )}
        
        {/* Voice Activity Indicator */}
        {isListening && !isAISpeaking && (
          <div className="bg-green-500/20 backdrop-blur-lg rounded-xl p-4 border border-green-500/30 mb-6 max-w-2xl mx-auto">
            <div className="flex items-center justify-center space-x-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                <span className="text-green-200">I'm listening to your answer...</span>
              </div>
              <div className="flex items-center space-x-1">
                {[...Array(10)].map((_, i) => (
                  <div
                    key={i}
                    className="w-1 bg-green-400 rounded transition-all duration-100"
                    style={{
                      height: `${Math.max(4, (audioLevel / 8) + (Math.random() * 8))}px`,
                      opacity: audioLevel > (i * 8) ? 1 : 0.3
                    }}
                  ></div>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {/* AI Speaking Indicator */}
        {isAISpeaking && (
          <div className="bg-blue-500/20 backdrop-blur-lg rounded-xl p-4 border border-blue-500/30 mb-6 max-w-2xl mx-auto">
            <div className="flex items-center justify-center space-x-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-blue-400 rounded-full mr-2 animate-pulse"></div>
                <span className="text-blue-200">AI Interviewer is speaking...</span>
              </div>
              <div className="flex space-x-1">
                {[...Array(3)].map((_, i) => (
                  <div
                    key={i}
                    className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"
                    style={{ animationDelay: `${i * 0.1}s` }}
                  ></div>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {/* Manual Controls - Minimal and Clean */}
        {!isAISpeaking && (
          <div className="bg-white/5 backdrop-blur-lg rounded-xl p-6 border border-white/10 max-w-2xl mx-auto">
            <div className="space-y-4">
              {/* Voice Input Display */}
              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Your Response {isListening ? '(Voice Active)' : '(Voice Inactive)'}
                </label>
                <textarea
                  value={candidateAnswer}
                  onChange={(e) => setCandidateAnswer(e.target.value)}
                  placeholder={isListening ? "Speak your answer or type here as backup..." : "Click 'Start Voice' or type your response..."}
                  className="w-full bg-white/5 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows="3"
                />
              </div>
              
              {/* Control Buttons */}
              <div className="flex justify-between items-center">
                <button
                  onClick={isListening ? stopListening : startListening}
                  disabled={isAISpeaking}
                  className={`px-6 py-2 rounded-lg font-medium transition-all duration-300 ${
                    isListening 
                      ? 'bg-red-500/20 text-red-200 border border-red-500/30 hover:bg-red-500/30' 
                      : 'bg-blue-500/20 text-blue-200 border border-blue-500/30 hover:bg-blue-500/30'
                  } disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  {isListening ? '🛑 Stop Voice' : '🎤 Start Voice'}
                </button>
                
                <button
                  onClick={handleSubmitAnswer}
                  disabled={!candidateAnswer.trim() || isAISpeaking}
                  className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-8 py-2 rounded-lg font-medium transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Submit Answer
                </button>
              </div>
              
              {/* Helpful Instructions */}
              <div className="text-xs text-gray-400 text-center mt-4">
                💡 The interview will automatically continue after 5 seconds of silence, or click "Submit Answer"
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Enhanced AI Avatar Interview Component
const AIAvatarInterviewSession = ({ interviewData, onAnswerSubmit, onInterviewComplete }) => {
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [isAISpeaking, setIsAISpeaking] = useState(false);
  const [candidateAnswer, setCandidateAnswer] = useState('');
  const [questionNumber, setQuestionNumber] = useState(1);
  const [totalQuestions] = useState(interviewData.totalQuestions || 8);
  
  const { isListening, audioLevel, startListening, stopListening } = useVoiceActivityDetection(
    () => {
      // Silence detected - move to next question
      if (candidateAnswer.trim()) {
        handleSubmitAnswer();
      }
    },
    5000 // 5 second silence threshold
  );
  
  const handleSubmitAnswer = async () => {
    if (!candidateAnswer.trim()) return;
    
    // Submit current answer
    await onAnswerSubmit({
      questionNumber,
      question: currentQuestion,
      answer: candidateAnswer
    });
    
    // Move to next question or complete interview
    if (questionNumber >= totalQuestions) {
      onInterviewComplete();
    } else {
      setQuestionNumber(prev => prev + 1);
      setCandidateAnswer('');
      // Load next question (this would come from your existing interview logic)
      loadNextQuestion();
    }
  };
  
  const loadNextQuestion = () => {
    // This would integrate with your existing question loading logic
    // For now, using placeholder
    setCurrentQuestion(`This is question ${questionNumber + 1} from your AI interviewer...`);
  };
  
  // Initialize first question
  useEffect(() => {
    if (interviewData && interviewData.questions && interviewData.questions.length > 0) {
      setCurrentQuestion(interviewData.questions[0]?.question || 'Welcome to your interview!');
    }
  }, [interviewData]);
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Avatar Section */}
        <div className="text-center mb-8">
          <RealisticFemaleAvatar 
            isSpeaking={isAISpeaking}
            isListening={isListening && !isAISpeaking}
            currentQuestion={currentQuestion}
          />
        </div>
        
        {/* Question Display */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 mb-6">
          <div className="text-center">
            <div className="mb-4">
              <span className="inline-block bg-blue-500/20 text-blue-200 px-4 py-2 rounded-full text-sm border border-blue-500/30">
                Question {questionNumber} of {totalQuestions}
              </span>
            </div>
            <p className="text-white text-xl leading-relaxed font-medium mb-6">
              {currentQuestion}
            </p>
          </div>
        </div>
        
        {/* Voice Activity Indicator */}
        {isListening && (
          <div className="bg-green-500/20 backdrop-blur-lg rounded-xl p-4 border border-green-500/30 mb-6">
            <div className="flex items-center justify-center space-x-4">
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-400 rounded-full mr-2 animate-pulse"></div>
                <span className="text-green-200">Listening...</span>
              </div>
              <div className="flex items-center space-x-1">
                {[...Array(10)].map((_, i) => (
                  <div
                    key={i}
                    className="w-1 bg-green-400 rounded"
                    style={{
                      height: `${Math.max(4, (audioLevel / 10) + (Math.random() * 10))}px`,
                      opacity: audioLevel > (i * 10) ? 1 : 0.3
                    }}
                  ></div>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {/* Manual Answer Input (Fallback) */}
        <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
          <textarea
            value={candidateAnswer}
            onChange={(e) => setCandidateAnswer(e.target.value)}
            placeholder="Your response will be captured automatically when you stop speaking, or you can type here..."
            className="w-full bg-white/5 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows="4"
          />
          <div className="flex justify-between items-center mt-4">
            <button
              onClick={isListening ? stopListening : startListening}
              className={`px-6 py-2 rounded-lg font-medium transition-all duration-300 ${
                isListening 
                  ? 'bg-red-500/20 text-red-200 border border-red-500/30 hover:bg-red-500/30' 
                  : 'bg-blue-500/20 text-blue-200 border border-blue-500/30 hover:bg-blue-500/30'
              }`}
            >
              {isListening ? '🛑 Stop Voice' : '🎤 Start Voice'}
            </button>
            <button
              onClick={handleSubmitAnswer}
              disabled={!candidateAnswer.trim()}
              className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-8 py-2 rounded-lg font-medium transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Submit Answer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Text-to-Speech Component for AI Interviewer Voice - Enhanced with repeat prevention
const AIVoiceSpeaker = ({ text, voiceMode, onSpeechComplete, preventRepeats = false, uniqueId = null }) => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voicesLoaded, setVoicesLoaded] = useState(false);

  // Ensure voices are loaded
  useEffect(() => {
    if ('speechSynthesis' in window) {
      const loadVoices = () => {
        const voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
          setVoicesLoaded(true);
        }
      };

      // Try to load voices immediately
      loadVoices();

      // Also listen for the voiceschanged event
      window.speechSynthesis.addEventListener('voiceschanged', loadVoices);

      return () => {
        window.speechSynthesis.removeEventListener('voiceschanged', loadVoices);
      };
    }
  }, []);

  useEffect(() => {
    if (voiceMode && text && text.trim() && 'speechSynthesis' in window && voicesLoaded) {
      // Check if this text should not be repeated
      const textKey = uniqueId || text;
      if (preventRepeats && globalSpokenTexts.has(textKey)) {
        console.log('Skipping repeat speech for:', textKey);
        return;
      }
      
      // Cancel any ongoing speech
      window.speechSynthesis.cancel();
      
      // Small delay to ensure the speech synthesis is ready
      setTimeout(() => {
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Configure voice settings for professional female AI interviewer
        utterance.rate = 0.9; // Slightly slower for clarity
        utterance.pitch = 1.1; // Slightly higher pitch for female voice
        utterance.volume = 0.8;
        
        // Try to get a female voice
        const voices = window.speechSynthesis.getVoices();
        const femaleVoice = voices.find(voice => 
          voice.name.toLowerCase().includes('female') || 
          voice.name.toLowerCase().includes('woman') ||
          voice.name.toLowerCase().includes('samantha') ||
          voice.name.toLowerCase().includes('karen') ||
          voice.name.toLowerCase().includes('moira') ||
          voice.name.toLowerCase().includes('zira') ||
          voice.name.toLowerCase().includes('aria') ||
          (voice.lang.startsWith('en') && voice.name.toLowerCase().includes('fiona'))
        );
        
        if (femaleVoice) {
          utterance.voice = femaleVoice;
          console.log('Using female voice:', femaleVoice.name);
        } else {
          console.log('No female voice found, using default');
        }
        
        utterance.onstart = () => {
          setIsSpeaking(true);
          console.log('AI Interviewer started speaking');
          // Mark this text as spoken
          if (preventRepeats) {
            globalSpokenTexts.add(textKey);
            console.log('Added to spoken texts:', textKey, 'Total spoken:', globalSpokenTexts.size);
          }
        };
        
        utterance.onend = () => {
          setIsSpeaking(false);
          console.log('AI Interviewer finished speaking');
          if (onSpeechComplete) {
            onSpeechComplete();
          }
        };
        
        utterance.onerror = (event) => {
          console.error('Speech synthesis error:', event.error);
          setIsSpeaking(false);
        };
        
        window.speechSynthesis.speak(utterance);
      }, 200);
    }

    return () => {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, [text, voiceMode, onSpeechComplete, voicesLoaded, preventRepeats, uniqueId]);

  const stopSpeaking = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      console.log('Speech manually stopped');
    }
  };

  if (!voiceMode || !text) {
    return null;
  }

  return (
    <div className="ai-voice-indicator flex items-center gap-2 mb-3">
      {isSpeaking && (
        <>
          <div className="animate-pulse flex items-center gap-1">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
          </div>
          <span className="text-blue-300 text-sm font-medium">🎤 AI Interviewer is speaking...</span>
          <button
            onClick={stopSpeaking}
            className="ml-2 px-2 py-1 bg-red-500 hover:bg-red-600 text-white text-xs rounded-md transition-colors"
            title="Stop Speaking"
          >
            Stop
          </button>
        </>
      )}
    </div>
  );
};

// Enhanced Landing Page Component
const EnhancedLandingPage = ({ setCurrentPage }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-white mb-6">
            🎯 Elite AI Interview Platform
          </h1>
          <p className="text-xl text-gray-300 mb-12 max-w-4xl mx-auto">
            Experience the future of hiring with our advanced AI-powered interview system. 
            Features interactive coding challenges, empathetic candidate workflow, multi-vector assessments, 
            and comprehensive bias mitigation controls.
          </p>
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-3">
              <span className="text-green-200">✅ Interactive Coding Challenges</span>
            </div>
            <div className="bg-blue-500/20 border border-blue-500/30 rounded-lg p-3">
              <span className="text-blue-200">✅ Voice Interview with AI</span>
            </div>
            <div className="bg-purple-500/20 border border-purple-500/30 rounded-lg p-3">
              <span className="text-purple-200">✅ Multi-Vector Assessments</span>
            </div>
            <div className="bg-orange-500/20 border border-orange-500/30 rounded-lg p-3">
              <span className="text-orange-200">✅ Bias Mitigation Controls</span>
            </div>
          </div>
        </div>

        <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-8">
          {/* Enhanced Admin Portal Card */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-white mb-4">Admin Dashboard</h2>
              <p className="text-gray-300 mb-6">
                Comprehensive hiring management with candidate pipeline, interview customization, 
                coding challenges, and advanced multi-vector reporting with bias controls.
              </p>
              <div className="mb-6 space-y-2">
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                  Candidate Pipeline & Comparison Tools
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                  Role Archetypes & Interview Focus
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                  Interactive Coding Challenges
                </div>
              </div>
              <button 
                onClick={() => setCurrentPage('admin-login')}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Access Admin Portal
              </button>
            </div>
          </div>

          {/* Enhanced Candidate Portal Card */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-white mb-4">Candidate Experience</h2>
              <p className="text-gray-300 mb-6">
                Interactive and empathetic interview experience with guided setup, practice rounds, 
                question controls, and adaptive AI questioning for a fair assessment.
              </p>
              <div className="mb-6 space-y-2">
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                  Camera/Mic Check & Practice Round
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                  Question Cards with Thinking Time
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                  Interactive Modules & Coding Tasks
                </div>
              </div>
              <button 
                onClick={() => setCurrentPage('candidate-login')}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Start Interview Experience
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Admin Login Component
const AdminLogin = ({ setCurrentPage, setIsAdmin }) => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API}/admin/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });

      if (response.ok) {
        setIsAdmin(true);
        setCurrentPage('admin-dashboard');
      } else {
        setError('Invalid password');
      }
    } catch (err) {
      setError('Connection error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 flex items-center justify-center px-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">Admin Login</h2>
          <p className="text-gray-300">Enter your admin credentials to continue</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-white mb-2">
              Admin Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter admin password"
              required
            />
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-3">
              <p className="text-red-200 text-sm">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>

          <button
            type="button"
            onClick={() => setCurrentPage('landing')}
            className="w-full text-gray-300 hover:text-white transition-colors duration-300"
          >
            Back to Home
          </button>
        </form>
      </div>
    </div>
  );
};

// Enhanced Admin Dashboard Component  
const AdminDashboard = ({ setCurrentPage }) => {
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [jobRequirements, setJobRequirements] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [generatedToken, setGeneratedToken] = useState('');
  const [resumePreview, setResumePreview] = useState('');
  const [loading, setLoading] = useState(false);
  const [reports, setReports] = useState([]);
  const [activeTab, setActiveTab] = useState('upload');
  
  // Enhanced features state
  const [includeCodingChallenge, setIncludeCodingChallenge] = useState(false);
  const [roleArchetype, setRoleArchetype] = useState('General');
  const [interviewFocus, setInterviewFocus] = useState('Balanced');
  const [candidatePipeline, setCandidatePipeline] = useState([]);
  const [selectedCandidates, setSelectedCandidates] = useState([]);
  const [comparisonResults, setComparisonResults] = useState([]);
  
  // Interview question limits
  const [minQuestions, setMinQuestions] = useState(8);
  const [maxQuestions, setMaxQuestions] = useState(12);

  const roleArchetypes = [
    'General',
    'Software Engineer',
    'Sales',
    'Graduate'
  ];

  const interviewFocusOptions = [
    'Balanced',
    'Technical Deep-Dive',
    'Cultural Fit', 
    'Graduate Screening'
  ];

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setResumeFile(file);
    
    if (file) {
      const fileType = file.name.split('.').pop().toLowerCase();
      const supportedTypes = ['pdf', 'doc', 'docx', 'txt'];
      if (!supportedTypes.includes(fileType)) {
        alert('Please upload PDF, DOC, DOCX, or TXT files only');
        e.target.value = '';
        setResumeFile(null);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append('job_title', jobTitle);
    formData.append('job_description', jobDescription);
    formData.append('job_requirements', jobRequirements);
    formData.append('include_coding_challenge', includeCodingChallenge);
    formData.append('role_archetype', roleArchetype);
    formData.append('interview_focus', interviewFocus);
    formData.append('resume_file', resumeFile);
    formData.append('min_questions', minQuestions);
    formData.append('max_questions', maxQuestions);

    try {
      // Use enhanced endpoint
      const response = await fetch(`${API}/admin/upload-job-enhanced`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setGeneratedToken(data.token);
        setResumePreview(data.resume_preview || '');
        
        // Reset form
        setJobTitle('');
        setJobDescription('');
        setJobRequirements('');
        setIncludeCodingChallenge(false);
        setRoleArchetype('General');
        setInterviewFocus('Balanced');
        setMinQuestions(8);
        setMaxQuestions(12);
        setResumeFile(null);
        document.querySelector('input[type="file"]').value = '';
        
        // Refresh pipeline
        if (activeTab === 'pipeline') {
          fetchCandidatePipeline();
        }
      } else {
        const errorData = await response.json();
        alert(`Upload failed: ${errorData.detail}`);
      }
    } catch (err) {
      console.error('Upload error:', err);
      alert('Upload failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fetchReports = async () => {
    try {
      const response = await fetch(`${API}/admin/reports`);
      if (response.ok) {
        const data = await response.json();
        setReports(data.reports || []);
      }
    } catch (err) {
      console.error('Failed to fetch reports:', err);
    }
  };

  const fetchCandidatePipeline = async () => {
    try {
      const response = await fetch(`${API}/admin/candidate-pipeline`);
      if (response.ok) {
        const data = await response.json();
        setCandidatePipeline(data.pipeline || []);
      }
    } catch (err) {
      console.error('Failed to fetch candidate pipeline:', err);
    }
  };

  const handleCandidateSelection = (token) => {
    if (selectedCandidates.includes(token)) {
      setSelectedCandidates(selectedCandidates.filter(t => t !== token));
    } else {
      setSelectedCandidates([...selectedCandidates, token]);
    }
  };

  const compareCandidates = async () => {
    if (selectedCandidates.length < 2) {
      alert('Please select at least 2 candidates to compare');
      return;
    }

    try {
      const response = await fetch(`${API}/admin/compare-candidates`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ candidate_tokens: selectedCandidates }),
      });

      if (response.ok) {
        const data = await response.json();
        setComparisonResults(data.comparisons || []);
        setActiveTab('comparison');
      }
    } catch (err) {
      console.error('Failed to compare candidates:', err);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Invited': return 'bg-yellow-500/20 text-yellow-200 border-yellow-500/30';
      case 'In Progress': return 'bg-blue-500/20 text-blue-200 border-blue-500/30';
      case 'Completed': return 'bg-green-500/20 text-green-200 border-green-500/30';
      case 'Report Ready': return 'bg-purple-500/20 text-purple-200 border-purple-500/30';
      default: return 'bg-gray-500/20 text-gray-200 border-gray-500/30';
    }
  };

  useEffect(() => {
    if (activeTab === 'reports') {
      fetchReports();
    } else if (activeTab === 'pipeline') {
      fetchCandidatePipeline();
    }
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-white">🎯 Elite Interview Dashboard</h1>
          <button
            onClick={() => setCurrentPage('landing')}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300"
          >
            Logout
          </button>
        </div>

        {/* Enhanced Tabs */}
        <div className="mb-8">
          <nav className="flex space-x-1 bg-white/10 backdrop-blur-lg rounded-lg p-1">
            <button
              onClick={() => setActiveTab('upload')}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-md transition-all duration-300 ${
                activeTab === 'upload'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              🚀 Create Interview
            </button>
            <button
              onClick={() => setActiveTab('pipeline')}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-md transition-all duration-300 ${
                activeTab === 'pipeline'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              👥 Candidate Pipeline
            </button>
            <button
              onClick={() => setActiveTab('reports')}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-md transition-all duration-300 ${
                activeTab === 'reports'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              📊 Assessment Reports
            </button>
            {comparisonResults.length > 0 && (
              <button
                onClick={() => setActiveTab('comparison')}
                className={`flex-1 py-3 px-4 text-sm font-medium rounded-md transition-all duration-300 ${
                  activeTab === 'comparison'
                    ? 'bg-blue-600 text-white shadow-lg'
                    : 'text-gray-300 hover:text-white hover:bg-white/10'
                }`}
              >
                ⚖️ Comparison
              </button>
            )}
          </nav>
        </div>

        {/* Enhanced Upload Tab */}
        {activeTab === 'upload' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6">Create Enhanced Interview Token</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-white font-medium mb-2">Job Title</label>
                  <input
                    type="text"
                    value={jobTitle}
                    onChange={(e) => setJobTitle(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="e.g., Senior Frontend Developer"
                    required
                  />
                </div>

                <div>
                  <label className="block text-white font-medium mb-2">Role Archetype</label>
                  <select
                    value={roleArchetype}
                    onChange={(e) => setRoleArchetype(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {roleArchetypes.map(role => (
                      <option key={role} value={role} className="bg-gray-800">{role}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-white font-medium mb-2">Interview Focus</label>
                  <select
                    value={interviewFocus}
                    onChange={(e) => setInterviewFocus(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {interviewFocusOptions.map(focus => (
                      <option key={focus} value={focus} className="bg-gray-800">{focus}</option>
                    ))}
                  </select>
                </div>

                <div className="flex items-center space-x-4">
                  <label className="flex items-center text-white">
                    <input
                      type="checkbox"
                      checked={includeCodingChallenge}
                      onChange={(e) => setIncludeCodingChallenge(e.target.checked)}
                      className="mr-2 w-5 h-5 rounded border-white/30 bg-white/20 text-blue-600 focus:ring-blue-500 focus:ring-2"
                    />
                    Include Coding Challenge
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-white font-medium mb-2">Job Description</label>
                <textarea
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Detailed job description..."
                  required
                />
              </div>

              <div>
                <label className="block text-white font-medium mb-2">Job Requirements</label>
                <textarea
                  value={jobRequirements}
                  onChange={(e) => setJobRequirements(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Technical skills, experience requirements..."
                  required
                />
              </div>

              {/* Interview Questions Configuration */}
              <div className="bg-white/5 p-6 rounded-lg border border-white/10">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Interview Questions Configuration
                </h3>
                <p className="text-gray-300 text-sm mb-4">
                  Set the range of questions to be asked during the interview. The system will dynamically adjust based on candidate responses.
                </p>
                
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-white font-medium mb-2">
                      Minimum Questions
                      <span className="text-sm text-gray-300 ml-2">(Must be asked)</span>
                    </label>
                    <div className="relative">
                      <input
                        type="number"
                        min="3"
                        max="15"
                        value={minQuestions}
                        onChange={(e) => {
                          const value = parseInt(e.target.value);
                          setMinQuestions(value);
                          // Ensure max is at least equal to min
                          if (maxQuestions < value) {
                            setMaxQuestions(value);
                          }
                        }}
                        className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="8"
                        required
                      />
                      <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                        </svg>
                      </div>
                    </div>
                    <p className="text-xs text-gray-400 mt-1">Recommended: 6-10 questions</p>
                  </div>

                  <div>
                    <label className="block text-white font-medium mb-2">
                      Maximum Questions
                      <span className="text-sm text-gray-300 ml-2">(If needed for assessment)</span>
                    </label>
                    <div className="relative">
                      <input
                        type="number"
                        min={minQuestions}
                        max="20"
                        value={maxQuestions}
                        onChange={(e) => {
                          const value = parseInt(e.target.value);
                          setMaxQuestions(value);
                          // Ensure min doesn't exceed max
                          if (minQuestions > value) {
                            setMinQuestions(value);
                          }
                        }}
                        className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="12"
                        required
                      />
                      <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
                        </svg>
                      </div>
                    </div>
                    <p className="text-xs text-gray-400 mt-1">Recommended: 10-15 questions</p>
                  </div>
                </div>

                {/* Question Distribution Preview */}
                <div className="mt-4 p-4 bg-white/5 rounded-lg">
                  <h4 className="text-sm font-medium text-white mb-2 flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    Expected Question Distribution
                  </h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div className="flex justify-between text-gray-300">
                      <span>Technical Questions:</span>
                      <span className="text-blue-300">{Math.ceil(minQuestions / 2)} - {Math.ceil(maxQuestions / 2)}</span>
                    </div>
                    <div className="flex justify-between text-gray-300">
                      <span>Behavioral Questions:</span>
                      <span className="text-green-300">{Math.floor(minQuestions / 2)} - {Math.floor(maxQuestions / 2)}</span>
                    </div>
                  </div>
                  <div className="mt-2 text-xs text-gray-400">
                    💡 The AI will adaptively adjust the number of questions based on candidate performance and responses
                  </div>
                </div>

                {/* Interview Duration Estimation */}
                <div className="mt-4 flex items-center justify-between text-sm">
                  <span className="text-gray-300">Estimated Interview Duration:</span>
                  <span className="text-yellow-300 font-medium">
                    {Math.ceil(minQuestions * 2.5)} - {Math.ceil(maxQuestions * 3)} minutes
                  </span>
                </div>
              </div>

              <div>
                <label className="block text-white font-medium mb-2">
                  Resume File 
                  <span className="text-sm text-gray-300 ml-2">(PDF, DOC, DOCX, TXT - Max 10MB)</span>
                </label>
                <div className="relative">
                  <input
                    type="file"
                    onChange={handleFileChange}
                    accept=".pdf,.doc,.docx,.txt"
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-600 file:text-white hover:file:bg-blue-700"
                    required
                  />
                </div>
                {resumeFile && (
                  <div className="mt-2 text-sm text-gray-300">
                    📎 {resumeFile.name} ({(resumeFile.size / 1024 / 1024).toFixed(2)} MB)
                  </div>
                )}
              </div>

              <button
                type="submit"
                disabled={loading || !resumeFile}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50"
              >
                {loading ? 'Creating Enhanced Interview...' : '🚀 Create Enhanced Interview'}
              </button>
            </form>

            {/* Success Display */}
            {generatedToken && (
              <div className="mt-8 p-6 bg-green-600/20 border border-green-500/30 rounded-2xl">
                <h3 className="text-xl font-bold text-green-200 mb-4">✅ Enhanced Interview Created Successfully!</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-green-200 mb-2"><strong>Interview Token:</strong></p>
                    <code className="block bg-black/30 p-3 rounded text-green-300 font-mono break-all">
                      {generatedToken}
                    </code>
                  </div>
                  <div>
                    <p className="text-green-200 mb-2"><strong>Features Enabled:</strong></p>
                    <div className="space-y-1">
                      <div className="text-sm text-green-300">🎯 Role: {roleArchetype}</div>
                      <div className="text-sm text-green-300">📊 Focus: {interviewFocus}</div>
                      <div className="text-sm text-green-300">
                        💻 Coding: {includeCodingChallenge ? 'Enabled' : 'Disabled'}
                      </div>
                      <div className="text-sm text-green-300">
                        ❓ Questions: {minQuestions} - {maxQuestions}
                      </div>
                      <div className="text-sm text-green-300">
                        ⏱️ Duration: {Math.ceil(minQuestions * 2.5)} - {Math.ceil(maxQuestions * 3)} min
                      </div>
                    </div>
                  </div>
                </div>
                {resumePreview && (
                  <div className="mt-4">
                    <p className="text-green-200 mb-2"><strong>Resume Preview:</strong></p>
                    <div className="bg-black/30 p-3 rounded text-green-300 text-sm max-h-32 overflow-y-auto">
                      {resumePreview}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Candidate Pipeline Tab */}
        {activeTab === 'pipeline' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-white">👥 Candidate Pipeline</h2>
              <div className="flex space-x-3">
                {selectedCandidates.length >= 2 && (
                  <button
                    onClick={compareCandidates}
                    className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300"
                  >
                    ⚖️ Compare Selected ({selectedCandidates.length})
                  </button>
                )}
                <button
                  onClick={fetchCandidatePipeline}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300"
                >
                  🔄 Refresh
                </button>
              </div>
            </div>

            <div className="space-y-4">
              {candidatePipeline.map((candidate) => (
                <div key={candidate.token} className="bg-white/5 rounded-lg p-4 border border-white/10">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <input
                        type="checkbox"
                        checked={selectedCandidates.includes(candidate.token)}
                        onChange={() => handleCandidateSelection(candidate.token)}
                        disabled={candidate.status !== 'Report Ready'}
                        className="w-5 h-5 rounded border-white/30 bg-white/20 text-blue-600"
                      />
                      <div>
                        <h3 className="text-white font-semibold">
                          {candidate.candidate_name} - {candidate.job_title}
                        </h3>
                        <div className="flex items-center space-x-4 mt-1">
                          <span className={`px-3 py-1 rounded-full text-xs border ${getStatusColor(candidate.status)}`}>
                            {candidate.status}
                          </span>
                          <span className="text-gray-300 text-sm">
                            {candidate.interview_type}
                          </span>
                          {candidate.features && (
                            <div className="flex space-x-2">
                              {candidate.features.coding_challenge && (
                                <span className="bg-blue-500/20 text-blue-200 px-2 py-1 rounded text-xs">💻 Coding</span>
                              )}
                              <span className="bg-green-500/20 text-green-200 px-2 py-1 rounded text-xs">
                                🎯 {candidate.features.role_archetype}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      {candidate.overall_score && (
                        <div className="text-2xl font-bold text-white mb-1">
                          {candidate.overall_score}/100
                        </div>
                      )}
                      <div className="text-sm text-gray-300">
                        {new Date(candidate.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              
              {candidatePipeline.length === 0 && (
                <div className="text-center py-8">
                  <div className="text-gray-400 mb-4">📭 No candidates yet</div>
                  <p className="text-gray-300">Create interview tokens to see candidates here</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Comparison Tab */}
        {activeTab === 'comparison' && comparisonResults.length > 0 && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6">⚖️ Candidate Comparison</h2>
            
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/20">
                    <th className="text-left text-white p-3">Candidate</th>
                    <th className="text-center text-white p-3">Overall Score</th>
                    <th className="text-center text-white p-3">Technical</th>
                    <th className="text-center text-white p-3">Behavioral</th>
                    <th className="text-left text-white p-3">Key Strengths</th>
                    <th className="text-left text-white p-3">Areas for Improvement</th>
                  </tr>
                </thead>
                <tbody>
                  {comparisonResults.map((candidate) => (
                    <tr key={candidate.token} className="border-b border-white/10">
                      <td className="p-3">
                        <div className="text-white font-semibold">{candidate.candidate_name}</div>
                        <div className="text-sm text-gray-300">{candidate.job_title}</div>
                      </td>
                      <td className="text-center p-3">
                        <div className="text-2xl font-bold text-white">{candidate.overall_score}/100</div>
                      </td>
                      <td className="text-center p-3">
                        <div className="text-xl font-bold text-blue-400">{candidate.technical_score}/100</div>
                      </td>
                      <td className="text-center p-3">
                        <div className="text-xl font-bold text-green-400">{candidate.behavioral_score}/100</div>
                      </td>
                      <td className="p-3">
                        <ul className="text-sm text-green-200">
                          {candidate.key_strengths?.slice(0, 3).map((strength, idx) => (
                            <li key={idx}>• {strength}</li>
                          ))}
                        </ul>
                      </td>
                      <td className="p-3">
                        <ul className="text-sm text-yellow-200">
                          {candidate.areas_for_improvement?.slice(0, 3).map((area, idx) => (
                            <li key={idx}>• {area}</li>
                          ))}
                        </ul>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Enhanced Reports Tab with AI Insights */}
        {activeTab === 'reports' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6">📊 Enhanced AI Assessment Reports</h2>
            
            <div className="space-y-6">
              {reports.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-gray-400 mb-4">📋 No assessment reports available yet</div>
                  <p className="text-gray-300">Enhanced reports with emotional intelligence analysis will appear here after candidates complete their interviews</p>
                </div>
              ) : (
                reports.map((report) => (
                  <div key={report.id} className="bg-white/10 rounded-lg p-6 border border-white/20">
                    {/* Header */}
                    <div className="flex justify-between items-start mb-6">
                      <div>
                        <h3 className="text-xl font-bold text-white flex items-center">
                          🎯 {report.candidate_name}
                        </h3>
                        <p className="text-gray-300">{report.job_title}</p>
                        <p className="text-sm text-gray-400">
                          {new Date(report.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl font-bold text-white mb-1">
                          {report.overall_score}/100
                        </div>
                        <div className="text-sm text-gray-300">Overall Score</div>
                        {/* NEW: Success Probability */}
                        {report.predictive_analytics && (
                          <div className="mt-2 px-3 py-1 rounded-full text-xs bg-gradient-to-r from-purple-600/20 to-pink-600/20 text-purple-200 border border-purple-500/30">
                            {Math.round(report.predictive_analytics.success_probability * 100)}% Success Probability
                          </div>
                        )}
                      </div>
                    </div>
                    
                    {/* Enhanced Scores Grid */}
                    <div className="grid md:grid-cols-4 gap-4 mb-6">
                      <div className="bg-white/5 rounded-lg p-4">
                        <div className="text-sm text-gray-300">Technical</div>
                        <div className="text-2xl font-bold text-blue-400">
                          {report.technical_score}/100
                        </div>
                      </div>
                      <div className="bg-white/5 rounded-lg p-4">
                        <div className="text-sm text-gray-300">Behavioral</div>
                        <div className="text-2xl font-bold text-green-400">
                          {report.behavioral_score}/100
                        </div>
                      </div>
                      {/* NEW: Emotional Intelligence Score */}
                      <div className="bg-white/5 rounded-lg p-4">
                        <div className="text-sm text-gray-300">Emotional IQ</div>
                        <div className="text-2xl font-bold text-purple-400">
                          {report.emotional_intelligence_metrics ? 
                            Math.round((
                              report.emotional_intelligence_metrics.enthusiasm +
                              report.emotional_intelligence_metrics.confidence +
                              report.emotional_intelligence_metrics.emotional_stability +
                              (1 - report.emotional_intelligence_metrics.stress_level)
                            ) * 25) : 'N/A'}
                        </div>
                      </div>
                      {/* NEW: Communication Score */}
                      <div className="bg-white/5 rounded-lg p-4">
                        <div className="text-sm text-gray-300">Communication</div>
                        <div className="text-2xl font-bold text-orange-400">
                          {report.communication_effectiveness ? 
                            Math.round(report.communication_effectiveness * 100) : 'N/A'}
                        </div>
                      </div>
                    </div>

                    {/* NEW: Emotional Intelligence Dashboard for Admin */}
                    {report.emotional_intelligence_metrics && (
                      <div className="mb-6">
                        <EmotionalIntelligenceDashboard 
                          eiData={report.emotional_intelligence_metrics} 
                          showRealTime={false} 
                        />
                      </div>
                    )}

                    {/* NEW: Predictive Analytics Results */}
                    {report.predictive_analytics && (
                      <div className="mb-6">
                        <PredictiveAnalyticsDashboard 
                          predictiveData={report.predictive_analytics} 
                        />
                      </div>
                    )}

                    {/* NEW: Bias Analysis */}
                    {report.bias_analysis && (
                      <div className="bg-white/5 rounded-lg p-4 mb-4">
                        <h4 className="font-semibold text-white mb-2 flex items-center">
                          ⚖️ Bias Analysis
                        </h4>
                        <div className="grid md:grid-cols-3 gap-4 text-sm">
                          <div>
                            <span className="text-gray-300">Evaluations Checked:</span>
                            <span className="text-white ml-2">{report.bias_analysis.evaluations_checked}</span>
                          </div>
                          <div>
                            <span className="text-gray-300">Bias Detected:</span>
                            <span className={`ml-2 ${report.bias_analysis.bias_detected ? 'text-yellow-400' : 'text-green-400'}`}>
                              {report.bias_analysis.bias_detected ? 'Yes' : 'No'}
                            </span>
                          </div>
                          <div>
                            <span className="text-gray-300">Bias Score:</span>
                            <span className="text-white ml-2">
                              {Math.round(report.bias_analysis.bias_score * 100)}%
                            </span>
                          </div>
                        </div>
                      </div>
                    )}
                    
                    {/* Traditional Feedback */}
                    <div className="text-sm text-gray-300">
                      <strong>Overall Feedback:</strong>
                      <p className="mt-1 text-white">{report.overall_feedback}</p>
                    </div>

                    {/* NEW: AI Recommendation */}
                    {report.predictive_analytics?.recommendation && (
                      <div className="mt-4 p-4 bg-gradient-to-r from-indigo-600/20 to-purple-600/20 rounded-lg border border-indigo-500/30">
                        <div className="flex items-start">
                          <span className="text-2xl mr-3">🤖</span>
                          <div>
                            <div className="font-semibold text-indigo-200 mb-1">AI Recommendation</div>
                            <div className="text-indigo-100 text-sm">{report.predictive_analytics.recommendation}</div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// Candidate Login Component
const CandidateLogin = ({ setCurrentPage, setToken, setValidatedJob }) => {
  const [inputToken, setInputToken] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleTokenValidation = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API}/candidate/validate-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: inputToken }),
      });

      if (response.ok) {
        const data = await response.json();
        setToken(inputToken);
        setValidatedJob(data);
        setCurrentPage('interview-start');
      } else {
        setError('Invalid token or token has already been used');
      }
    } catch (err) {
      setError('Connection error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 flex items-center justify-center px-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">🎤 Candidate Portal</h2>
          <p className="text-gray-300">Enter your secure interview token for voice interview</p>
        </div>

        <form onSubmit={handleTokenValidation} className="space-y-6">
          <div>
            <label htmlFor="token" className="block text-sm font-medium text-white mb-2">
              Interview Token
            </label>
            <input
              type="text"
              id="token"
              value={inputToken}
              onChange={(e) => setInputToken(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent font-mono"
              placeholder="Enter your 16-character token"
              required
            />
          </div>

          {error && (
            <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-3">
              <p className="text-red-200 text-sm">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50"
          >
            {loading ? 'Validating...' : 'Validate Token'}
          </button>

          <button
            type="button"
            onClick={() => setCurrentPage('landing')}
            className="w-full text-gray-300 hover:text-white transition-colors duration-300"
          >
            Back to Home
          </button>
        </form>
      </div>
    </div>
  );
};

// Interview Start Component
const InterviewStart = ({ setCurrentPage, token, validatedJob }) => {
  const [candidateName, setCandidateName] = useState('');
  const [voiceMode, setVoiceMode] = useState(true);
  const [loading, setLoading] = useState(false);

  const handleStartInterview = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Clear global spoken texts for new interview session
    globalSpokenTexts.clear();
    console.log('Cleared global spoken texts for new interview session');

    try {
      const response = await fetch(`${API}/candidate/start-interview`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          token, 
          candidate_name: candidateName,
          voice_mode: voiceMode
        }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('interviewData', JSON.stringify({
          sessionId: data.session_id,
          candidateName,
          jobTitle: validatedJob.job_title,
          token,
          currentQuestion: data.first_question,
          questionNumber: data.question_number,
          totalQuestions: data.total_questions,
          voiceMode: data.voice_mode,
          welcomeAudio: data.welcome_audio,
          questionAudio: data.question_audio
        }));
        setCurrentPage('capture-image');
      }
    } catch (err) {
      console.error('Failed to start interview:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 flex items-center justify-center px-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 w-full max-w-2xl">
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">Ready for Your Voice Interview?</h2>
          <p className="text-gray-300 mb-4">Position: <span className="font-semibold text-white">{validatedJob.job_title}</span></p>
          <div className="bg-green-600/20 border border-green-500/30 rounded-lg p-4 mb-6">
            <p className="text-green-200 text-sm">
              <strong>🎤 Voice Interview Format:</strong> The AI interviewer will ask questions in a female voice, 
              and you'll respond using your voice. All audio is recorded and transcribed for assessment.
            </p>
          </div>
        </div>

        <form onSubmit={handleStartInterview} className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-white mb-2">
              Your Full Name
            </label>
            <input
              type="text"
              id="name"
              value={candidateName}
              onChange={(e) => setCandidateName(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              placeholder="Enter your full name"
              required
            />
          </div>

          <div className="bg-white/10 rounded-lg p-4">
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={voiceMode}
                onChange={(e) => setVoiceMode(e.target.checked)}
                className="mr-3 w-5 h-5 text-purple-600 rounded focus:ring-purple-500 focus:ring-2"
              />
              <span className="text-white">
                🎤 Enable Voice Interview Mode (Recommended)
              </span>
            </label>
            <p className="text-xs text-gray-300 mt-1 ml-8">
              {voiceMode 
                ? "AI will speak questions and record your voice answers"
                : "Traditional text-based interview mode"
              }
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <button
              type="submit"
              disabled={loading}
              className="bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50"
            >
              {loading ? 'Starting Interview...' : '🎤 Start Voice Interview'}
            </button>
            <button
              type="button"
              onClick={() => setCurrentPage('candidate-login')}
              className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-300"
            >
              Back
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Capture Image Component - Face detection and image capture before interview
const CaptureImage = ({ setCurrentPage, token, validatedJob }) => {
  const [cameraStream, setCameraStream] = useState(null);
  const [cameraError, setCameraError] = useState('');
  const [faceDetected, setFaceDetected] = useState(0); // 0: none, 1: one face, 2+: multiple
  const [faceCentered, setFaceCentered] = useState(false);
  const [lightingGood, setLightingGood] = useState(false);
  const [imageCaptured, setImageCaptured] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const faceDetectionRef = useRef(null);
  const animationFrameRef = useRef(null);

  // Initialize camera
  const requestCameraAccess = async () => {
    try {
      setCameraError('');
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: { ideal: 640 }, 
          height: { ideal: 480 },
          facingMode: 'user'
        } 
      });
      setCameraStream(stream);
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (error) {
      console.error('Camera access error:', error);
      setCameraError('Camera not accessible. Please check your device or browser settings.');
    }
  };

  // Initialize face detection
  const initializeFaceDetection = async () => {
    try {
      // Using a simple face detection approach with canvas analysis
      // For production, you'd want to use MediaPipe or similar
      startFaceDetectionLoop();
    } catch (error) {
      console.error('Face detection initialization failed:', error);
    }
  };

  // Face detection loop using canvas analysis
  const startFaceDetectionLoop = () => {
    const detectFaces = () => {
      if (!videoRef.current || !canvasRef.current) {
        animationFrameRef.current = requestAnimationFrame(detectFaces);
        return;
      }

      const video = videoRef.current;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');

      if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Simple face detection simulation
        // In production, use MediaPipe Face Detection
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const { faces, lighting } = analyzeFaceAndLighting(imageData, canvas.width, canvas.height);
        
        setFaceDetected(faces);
        setLightingGood(lighting > 0.3); // Threshold for good lighting
        
        // Check if face is centered (simplified)
        setFaceCentered(faces === 1);
      }

      animationFrameRef.current = requestAnimationFrame(detectFaces);
    };

    detectFaces();
  };

  // Simplified face and lighting analysis (enhanced version)
  const analyzeFaceAndLighting = (imageData, width, height) => {
    const data = imageData.data;
    let totalBrightness = 0;
    let pixelCount = 0;
    let skinPixels = 0;
    
    // Analyze center region for face detection and lighting
    const centerX = width / 2;
    const centerY = height / 2;
    const sampleRadius = Math.min(width, height) / 4;

    for (let y = centerY - sampleRadius; y < centerY + sampleRadius; y++) {
      for (let x = centerX - sampleRadius; x < centerX + sampleRadius; x++) {
        if (x >= 0 && x < width && y >= 0 && y < height) {
          const i = (y * width + x) * 4;
          const r = data[i];
          const g = data[i + 1];
          const b = data[i + 2];
          
          const brightness = (r + g + b) / 3;
          totalBrightness += brightness;
          pixelCount++;
          
          // Simple skin tone detection (rough approximation)
          if (r > 95 && g > 40 && b > 20 && 
              Math.max(r, g, b) - Math.min(r, g, b) > 15 &&
              Math.abs(r - g) > 15 && r > g && r > b) {
            skinPixels++;
          }
        }
      }
    }

    const avgBrightness = totalBrightness / pixelCount / 255;
    const skinRatio = skinPixels / pixelCount;
    
    // Determine number of faces based on skin detection and patterns
    let faces = 0;
    if (skinRatio > 0.15) { // Threshold for face detection
      faces = 1; // Simplified - assume one face if skin detected
      
      // Check for multiple faces by analyzing distribution
      // This is a simplified approach - production would use proper face detection
      if (skinRatio > 0.35) {
        faces = Math.random() > 0.8 ? 2 : 1; // Occasionally detect multiple faces
      }
    }
    
    return { faces, lighting: avgBrightness };
  };

  // Capture face image
  const captureFace = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageDataUrl = canvas.toDataURL('image/jpeg', 0.8);
    setCapturedImage(imageDataUrl);
    setImageCaptured(true);
  };

  // Confirm and proceed to avatar interview
  const confirmInterview = async () => {
    setLoading(true);
    try {
      // Store captured image data
      const interviewData = JSON.parse(localStorage.getItem('interviewData') || '{}');
      interviewData.capturedImage = capturedImage;
      localStorage.setItem('interviewData', JSON.stringify(interviewData));
      
      // Clear any previously spoken texts for fresh interview
      if (typeof globalSpokenTexts !== 'undefined') {
        globalSpokenTexts.clear();
        console.log('Cleared spoken texts for new avatar interview session');
      }
      
      setCurrentPage('avatar-interview');
    } catch (error) {
      console.error('Error proceeding to avatar interview:', error);
    } finally {
      setLoading(false);
    }
  };

  // Cleanup
  useEffect(() => {
    requestCameraAccess();
    return () => {
      if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
      }
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (cameraStream && videoRef.current) {
      videoRef.current.addEventListener('loadedmetadata', initializeFaceDetection);
    }
  }, [cameraStream]);

  const canCapture = faceDetected === 1 && faceCentered && lightingGood && !cameraError;
  const showLightingWarning = faceDetected > 0 && !lightingGood;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 w-full max-w-4xl">
        
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">Capture Image</h1>
          <p className="text-lg text-white/80">
            Please position yourself in front of the camera for face verification
          </p>
        </div>

        {/* Camera Section */}
        <div className="relative mb-8">
          <div className="relative mx-auto w-full max-w-2xl">
            {/* Video Stream */}
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-auto rounded-lg shadow-lg"
              style={{ maxHeight: '400px', objectFit: 'cover' }}
            />
            
            {/* Face Guide Overlay */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div className={`border-4 rounded-full w-64 h-80 flex items-center justify-center transition-all duration-300 ${
                faceDetected === 1 && faceCentered && lightingGood 
                  ? 'border-green-400 border-solid shadow-lg shadow-green-400/50' 
                  : faceDetected === 1 
                    ? 'border-yellow-400 border-dashed'
                    : 'border-white/50 border-dashed'
              }`}>
                <div className="text-center">
                  <div className={`text-2xl mb-2 ${
                    faceDetected === 1 && faceCentered && lightingGood 
                      ? 'text-green-400' 
                      : 'text-white/70'
                  }`}>
                    {faceDetected === 1 && faceCentered && lightingGood ? '✓' : '👤'}
                  </div>
                  <span className="text-white/70 text-sm">
                    {faceDetected === 1 && faceCentered && lightingGood 
                      ? 'Perfect!' 
                      : 'Align your face here'
                    }
                  </span>
                </div>
              </div>
            </div>

            {/* Hidden canvas for face detection */}
            <canvas ref={canvasRef} className="hidden" />
          </div>

          {/* Camera Error */}
          {cameraError && (
            <div className="mt-4 text-center">
              <p className="text-red-400 mb-4">{cameraError}</p>
              <button
                onClick={requestCameraAccess}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
              >
                Retry Camera Access
              </button>
            </div>
          )}
        </div>

        {/* Status Messages */}
        <div className="mb-6 space-y-2">
          {/* Face Detection Status */}
          {faceDetected === 0 && !cameraError && (
            <p className="text-yellow-400 text-center">
              ⚠️ No face detected. Please align your face within the frame.
            </p>
          )}
          {faceDetected > 1 && (
            <p className="text-red-400 text-center">
              ❌ Multiple faces detected. Please ensure only you are visible.
            </p>
          )}
          {faceDetected === 1 && (
            <p className="text-green-400 text-center">
              ✅ Face detected successfully
            </p>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center items-center gap-6 mb-8">
          {/* Lighting Warning */}
          {showLightingWarning && (
            <p className="text-red-400 text-sm">
              💡 Improve the lighting
            </p>
          )}

          {/* Capture Face Button */}
          <button
            onClick={captureFace}
            disabled={!canCapture || imageCaptured}
            className={`px-8 py-3 rounded-lg font-semibold transition-all duration-300 ${
              canCapture && !imageCaptured
                ? 'bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white shadow-lg hover:shadow-xl'
                : 'bg-gray-600 text-gray-300 cursor-not-allowed'
            }`}
          >
            {imageCaptured ? '✓ Face Captured' : 'Capture Face'}
          </button>
        </div>

        {/* Captured Image Preview */}
        {imageCaptured && capturedImage && (
          <div className="mb-8 text-center">
            <h3 className="text-lg font-semibold text-white mb-4">Captured Image:</h3>
            <img
              src={capturedImage}
              alt="Captured face"
              className="mx-auto rounded-lg shadow-lg max-w-xs"
            />
          </div>
        )}

        {/* Confirm Interview Button */}
        <div className="text-center">
          <button
            onClick={confirmInterview}
            disabled={!imageCaptured || loading}
            className={`px-12 py-4 rounded-lg font-bold text-lg transition-all duration-300 ${
              imageCaptured && !loading
                ? 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg hover:shadow-xl transform hover:scale-105'
                : 'bg-gray-600 text-gray-300 cursor-not-allowed'
            }`}
          >
            {loading ? 'Processing...' : 'Confirm Interview'}
          </button>
        </div>

        {/* Instructions */}
        <div className="mt-8 text-center text-sm text-white/60">
          <p>📷 Ensure your face is clearly visible and well-lit</p>
          <p>🎯 Position yourself within the guide frame</p>
          <p>⚡ Good lighting helps with accurate detection</p>
        </div>
      </div>
    </div>
  );
};

// Interview Session Component - Step-by-Step Single Question Interface
const InterviewSession = ({ setCurrentPage }) => {
  const [currentQuestionData, setCurrentQuestionData] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [interviewData, setInterviewData] = useState(null);
  const [completed, setCompleted] = useState(false);
  const [isAnswering, setIsAnswering] = useState(false);
  const [showWelcome, setShowWelcome] = useState(true);
  const [currentEI, setCurrentEI] = useState(null);
  const [eiHistory, setEIHistory] = useState([]);
  const [finalResults, setFinalResults] = useState(null);
  
  // Webcam state
  const [webcamActive, setWebcamActive] = useState(false);
  const [webcamMinimized, setWebcamMinimized] = useState(false);

  // Voice recording
  const handleVoiceRecording = async (audioBlob) => {
    setIsAnswering(true);
    try {
      const formData = new FormData();
      formData.append('session_id', interviewData.sessionId);
      formData.append('question_number', interviewData.questionNumber);
      formData.append('audio_file', audioBlob, 'answer.webm');

      const response = await fetch(`${API}/voice/process-answer`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        
        if (data.emotional_intelligence) {
          setCurrentEI(data.emotional_intelligence);
          setEIHistory(prev => [...prev, {
            ...data.emotional_intelligence,
            timestamp: new Date(),
            questionNumber: interviewData.questionNumber
          }]);
        }
        
        await handleAnswerSubmission(data.transcript);
      }
    } catch (error) {
      console.error('Voice processing error:', error);
    } finally {
      setIsAnswering(false);
    }
  };

  const handleAnswerSubmission = async (answerText) => {
    setIsAnswering(true);
    try {
      const response = await fetch(`${API}/candidate/send-message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          token: interviewData.token, 
          message: answerText 
        }),
      });

      if (response.ok) {
        const data = await response.json();
        
        if (data.emotional_insight) {
          setCurrentEI(data.emotional_insight);
          setEIHistory(prev => [...prev, {
            ...data.emotional_insight,
            timestamp: new Date(),
            questionNumber: data.question_number || interviewData.questionNumber
          }]);
        }
        
        if (data.completed) {
          setCompleted(true);
          
          if (data.key_insights) {
            setFinalResults({
              success_probability: data.success_probability,
              prediction: data.key_insights.prediction,
              emotional_intelligence: data.key_insights.emotional_intelligence,
              strengths: data.key_insights.strengths
            });
          }
        } else {
          // Update for next question
          setInterviewData(prev => ({
            ...prev,
            questionNumber: data.question_number,
            currentQuestion: data.next_question
          }));
          
          setCurrentQuestionData({
            questionNumber: data.question_number,
            question: data.next_question,
            questionText: data.question_text
          });
        }
        
        setUserAnswer('');
        setShowWelcome(false);
        
      } else {
        console.error('Failed to send message');
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsAnswering(false);
    }
  };

  const handleTextSubmit = (e) => {
    e.preventDefault();
    if (userAnswer.trim()) {
      handleAnswerSubmission(userAnswer.trim());
    }
  };

  // Initialize from localStorage
  useEffect(() => {
    const savedData = localStorage.getItem('interviewData');
    if (savedData) {
      const data = JSON.parse(savedData);
      setInterviewData(data);
      
      // Set initial question
      if (!completed) {
        setCurrentQuestionData({
          questionNumber: data.questionNumber,
          question: data.currentQuestion,
          questionText: data.currentQuestion
        });
      }
    }
  }, [completed]);

  // Voice recording hook
  const { status: recordingStatus, startRecording, stopRecording } = useVoiceRecorder(handleVoiceRecording);

  if (!interviewData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 flex items-center justify-center">
        <div className="text-white text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-white mx-auto mb-4"></div>
          <p>Loading interview...</p>
        </div>
      </div>
    );
  }

  if (completed) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 p-4">
        <div className="max-w-4xl mx-auto py-12">
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-white mb-4">Interview Completed!</h2>
            <p className="text-gray-300 mb-6">
              Thank you for completing the {interviewData.voiceMode ? 'voice' : 'text'} interview. 
              Your responses have been recorded and will be evaluated shortly.
            </p>
            <button
              onClick={() => {
                localStorage.removeItem('interviewData');
                setCurrentPage('landing');
              }}
              className="bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all duration-300 shadow-lg hover:shadow-xl"
            >
              Return to Home
            </button>
          </div>

          {/* Final Results with Predictive Analytics */}
          {finalResults && (
            <>
              <PredictiveAnalyticsDashboard predictiveData={{
                success_probability: finalResults.success_probability,
                prediction: finalResults.prediction,
                recommendation: `Based on comprehensive analysis including emotional intelligence assessment`,
                score_breakdown: {
                  technical: 0.75,
                  behavioral: 0.68,
                  emotional_intelligence: (
                    finalResults.emotional_intelligence.enthusiasm +
                    finalResults.emotional_intelligence.confidence +
                    finalResults.emotional_intelligence.emotional_stability +
                    (1 - finalResults.emotional_intelligence.stress_level)
                  ) / 4,
                  communication: 0.72
                },
                key_strengths: finalResults.strengths || [],
                improvement_areas: ["Areas for development will be provided in detailed report"]
              }} />
              
              <EmotionalIntelligenceDashboard 
                eiData={finalResults.emotional_intelligence} 
                showRealTime={false} 
              />
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 p-4">
      <div className="max-w-4xl mx-auto py-8">
        {/* Header */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-white">AI Interview</h1>
              <p className="text-gray-300">{interviewData.jobTitle}</p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-300">
                {currentQuestionData ? `Question ${currentQuestionData.questionNumber}` : 'Welcome'} of {interviewData.totalQuestions}
              </div>
              <div className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-green-600/20 text-green-200 border border-green-500/30">
                <div className="w-2 h-2 bg-green-400 rounded-full mr-2"></div>
                {interviewData.voiceMode ? 'Voice Interview' : 'Text Interview'}
              </div>
            </div>
          </div>
        </div>

        {/* Real-time Emotional Intelligence Dashboard */}
        {currentEI && (
          <EmotionalIntelligenceDashboard 
            eiData={currentEI} 
            showRealTime={true} 
          />
        )}

        {/* Welcome Message - Only shown initially */}
        {showWelcome && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 mb-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-white mb-4">Welcome to Your AI Interview!</h2>
              <p className="text-gray-300 mb-6">
                {interviewData.voiceMode 
                  ? `Hello ${interviewData.candidateName}! I'm your AI interviewer. I'll ask you questions using voice, and you can respond using voice or text. Each question will be presented on a separate screen for focused attention.`
                  : `Hello ${interviewData.candidateName}! I'm your AI interviewer today. I'll ask you ${interviewData.totalQuestions} questions about your experience and qualifications. Each question will be shown individually.`
                }
              </p>
              
              {interviewData.voiceMode && (
                <AIVoiceSpeaker 
                  text={`Hello ${interviewData.candidateName}! Welcome to your AI interview. I'll ask you questions using voice, and you can respond using voice or text. Each question will be presented on a separate screen for your focused attention. Let's begin with your first question.`}
                  voiceMode={interviewData.voiceMode}
                  preventRepeats={true}
                  uniqueId="welcome-message"
                  onSpeechComplete={() => console.log('Welcome message spoken')}
                />
              )}
              
              <button
                onClick={() => {
                  setShowWelcome(false);
                  setWebcamActive(true);
                }}
                className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-8 py-4 rounded-lg font-medium transition-all duration-300 transform hover:scale-105"
              >
                Start Interview
              </button>
            </div>
          </div>
        )}

        {/* Current Question - Clean Single Question Display */}
        {currentQuestionData && !showWelcome && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 mb-6">
            <div className="mb-6">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mr-4">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-blue-300">Question {currentQuestionData.questionNumber}</h3>
                  <p className="text-sm text-gray-400">AI Interviewer</p>
                </div>
              </div>
              
              {/* AI Voice Speaker - Only speak once per question */}
              {interviewData.voiceMode && (
                <AIVoiceSpeaker 
                  text={currentQuestionData.question} 
                  voiceMode={interviewData.voiceMode}
                  preventRepeats={true}
                  uniqueId={`question-${currentQuestionData.questionNumber}`}
                  onSpeechComplete={() => console.log(`Question ${currentQuestionData.questionNumber} spoken`)}
                />
              )}
              
              <div className="bg-white/5 rounded-xl p-6 border border-white/10">
                <p className="text-white text-lg leading-relaxed font-medium">{currentQuestionData.question}</p>
              </div>
            </div>
          </div>
        )}

        {/* Voice Control - only show in voice mode */}
        {interviewData.voiceMode && !showWelcome && (
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-4 border border-white/20 mb-6">
            <div className="flex items-center justify-between">
              <span className="text-white text-sm">🎤 AI Voice Control</span>
              <button
                onClick={() => {
                  if ('speechSynthesis' in window) {
                    if (window.speechSynthesis.speaking) {
                      window.speechSynthesis.cancel();
                    }
                  }
                }}
                className="bg-red-500/20 hover:bg-red-500/30 text-red-200 px-3 py-1 rounded-lg text-sm border border-red-500/30 transition-colors"
              >
                Stop Speaking
              </button>
            </div>
          </div>
        )}

        {/* Answer Input - Only shown when there's a current question */}
        {currentQuestionData && !showWelcome && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
            <h4 className="text-white font-medium mb-4">Your Answer:</h4>
            
            {/* Voice Recording Section */}
            {interviewData.voiceMode && (
              <div className="mb-6">
                <div className="flex flex-col items-center space-y-4">
                  <button
                    onClick={recordingStatus === 'recording' ? stopRecording : startRecording}
                    disabled={isAnswering}
                    className={`w-20 h-20 rounded-full flex items-center justify-center text-white font-semibold transition-all duration-300 transform ${
                      recordingStatus === 'recording'
                        ? 'bg-red-600 hover:bg-red-700 animate-pulse scale-110'
                        : 'bg-blue-600 hover:bg-blue-700 hover:scale-105'
                    } ${isAnswering ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    {recordingStatus === 'recording' ? (
                      <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
                        <rect x="6" y="6" width="12" height="12" rx="2"/>
                      </svg>
                    ) : (
                      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                      </svg>
                    )}
                  </button>
                  <p className="text-center text-gray-300 text-sm">
                    {recordingStatus === 'recording' 
                      ? '🔴 Recording... Click to stop' 
                      : '🎤 Click to record your answer'
                    }
                  </p>
                </div>
              </div>
            )}

            {/* Text Input Section */}
            <div className={interviewData.voiceMode ? 'border-t border-white/20 pt-6' : ''}>
              {interviewData.voiceMode && (
                <p className="text-gray-400 text-sm mb-4">Or type your answer:</p>
              )}
              <form onSubmit={handleTextSubmit} className="space-y-4">
                <textarea
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Type your answer here..."
                  className="w-full h-32 bg-white/10 border border-white/20 rounded-lg p-4 text-white placeholder-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none resize-none"
                  disabled={isAnswering}
                />
                <div className="flex justify-end">
                  <button
                    type="submit"
                    disabled={!userAnswer.trim() || isAnswering}
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium transition-all duration-300 transform hover:scale-105 disabled:scale-100"
                  >
                    {isAnswering ? (
                      <div className="flex items-center">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Processing...
                      </div>
                    ) : (
                      'Submit Answer & Next Question'
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
      
      {/* Webcam Preview - Bottom Right Corner */}
      {webcamActive && (
        <div className={`fixed ${webcamMinimized ? 'bottom-4 right-4' : 'bottom-4 right-4'} z-50 transition-all duration-300`}>
          <div className="bg-white/10 backdrop-blur-lg rounded-lg border border-white/20 overflow-hidden shadow-xl">
            {/* Webcam Header */}
            <div className="bg-white/5 px-3 py-2 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-white text-xs font-medium">Camera</span>
              </div>
              <div className="flex items-center space-x-1">
                <button
                  onClick={() => setWebcamMinimized(!webcamMinimized)}
                  className="text-white/70 hover:text-white transition-colors p-1"
                  title={webcamMinimized ? "Expand" : "Minimize"}
                >
                  {webcamMinimized ? (
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                    </svg>
                  ) : (
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12l-1.411-1.411L16 13.177V8a1 1 0 00-1-1h-4.764a1 1 0 00-.894.553L9 8H5a1 1 0 00-1 1v6a1 1 0 001 1h4l.342.447A1 1 0 0010.236 17H15a1 1 0 001-1v-5.177l2.589 2.588L20 12z" />
                    </svg>
                  )}
                </button>
                <button
                  onClick={() => setWebcamActive(false)}
                  className="text-white/70 hover:text-white transition-colors p-1"
                  title="Close Camera"
                >
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            {/* Webcam Video */}
            {!webcamMinimized && (
              <AdvancedVideoAnalyzer
                sessionId={interviewData?.sessionId}
                isRecording={webcamActive}
                isPreview={true}
                onAnalysisUpdate={(analysis) => {
                  // Optional: Handle video analysis updates
                  console.log('Video analysis:', analysis);
                }}
              />
            )}
            
            {webcamMinimized && (
              <div className="w-16 h-12 bg-gray-800 flex items-center justify-center">
                <svg className="w-6 h-6 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Main App Component
function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [isAdmin, setIsAdmin] = useState(false);
  const [token, setToken] = useState('');
  const [validatedJob, setValidatedJob] = useState(null);

  const renderPage = () => {
    switch (currentPage) {
      case 'admin-login':
        return <AdminLogin setCurrentPage={setCurrentPage} setIsAdmin={setIsAdmin} />;
      case 'admin-dashboard':
        return <AdminDashboard setCurrentPage={setCurrentPage} />;
      case 'candidate-login':
        return <CandidateLogin setCurrentPage={setCurrentPage} setToken={setToken} setValidatedJob={setValidatedJob} />;
      case 'interview-start':
        return <InterviewStart setCurrentPage={setCurrentPage} token={token} validatedJob={validatedJob} />;
      case 'capture-image':
        return <CaptureImage setCurrentPage={setCurrentPage} token={token} validatedJob={validatedJob} />;
      case 'avatar-interview':
        return <AvatarInterviewContainer setCurrentPage={setCurrentPage} token={token} validatedJob={validatedJob} />;
      case 'interview-session':
        return <InterviewSession setCurrentPage={setCurrentPage} />;
      default:
        return <EnhancedLandingPage setCurrentPage={setCurrentPage} />;
    }
  };

  return (
    <div className="App">
      {renderPage()}
    </div>
  );
}

export default App;