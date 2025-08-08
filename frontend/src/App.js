import React, { useState, useEffect, useRef } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';
import AdvancedVideoAnalyzer from './AdvancedVideoAnalyzer';
import './App.css';
import './accessibility.css';

// Phase 3 imports
import { AccessibilityProvider } from './AccessibilityProvider';
import AccessibilityControls, { AccessibilityButton } from './AccessibilityControls';
import { I18nProvider, useI18n, LanguageSelector } from './I18nProvider';
import { PWAProvider, InstallBanner, UpdateBanner, OfflineBanner } from './PWAProvider';

// Phase 2 imports - AI Screening Components
import { 
  ResumeUploadSection, 
  JobRequirementsSetup, 
  ScreenCandidatesSection, 
  ResultsComponent,
  BulkScreeningInterface 
} from './ScreeningComponents';

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

// Enhanced Voice Recording Hook with Web Speech API
const useVoiceRecorder = (onRecordingComplete) => {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [voiceLevel, setVoiceLevel] = useState(0);
  const recognitionRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const microphoneRef = useRef(null);
  const animationFrameRef = useRef(null);
  const isStoppingRef = useRef(false);
  const currentTranscriptRef = useRef(''); // Store current transcript for onend handler

  // Initialize Web Speech API
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onstart = () => {
        console.log('Speech recognition started');
        setIsRecording(true);
        isStoppingRef.current = false;
        setTranscript(''); // Clear transcript when starting
        currentTranscriptRef.current = '';
      };

      recognitionRef.current.onend = () => {
        console.log('Speech recognition ended - checking if manual stop');
        
        // Only update UI if this was NOT a manual stop
        if (!isStoppingRef.current) {
          console.log('Automatic end - updating UI');
          setIsRecording(false);
          stopVoiceLevelMonitoring();
          
          // Process transcript only if this was an automatic end
          if (currentTranscriptRef.current.trim()) {
            onRecordingComplete(currentTranscriptRef.current.trim());
            setTranscript('');
            currentTranscriptRef.current = '';
          }
        } else {
          console.log('Manual stop detected - skipping automatic processing');
        }
        
        // Reset stopping flag after a delay
        setTimeout(() => {
          isStoppingRef.current = false;
        }, 100);
      };

      recognitionRef.current.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        
        // Get all results to build complete transcript
        for (let i = 0; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }
        
        // Set the complete transcript (final + interim for live preview)
        const completeTranscript = finalTranscript + interimTranscript;
        if (completeTranscript) {
          const cleanTranscript = completeTranscript.trim();
          setTranscript(cleanTranscript);
          currentTranscriptRef.current = cleanTranscript;
        }
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsRecording(false);
        stopVoiceLevelMonitoring();
        
        // Show user-friendly error message
        if (event.error === 'not-allowed' || event.error === 'permission-denied') {
          alert('Microphone access denied. Please allow microphone access to use voice recording.');
        } else if (event.error === 'no-speech') {
          console.log('No speech detected - this is normal');
        } else {
          alert('Voice recognition error. Please try again.');
        }
      };
    }
  }, [transcript, onRecordingComplete]);

  // Voice level monitoring
  const startVoiceLevelMonitoring = async () => {
    try {
      // Clean up existing AudioContext first
      await cleanupAudioContext();
      
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      microphoneRef.current = audioContextRef.current.createMediaStreamSource(stream);
      
      microphoneRef.current.connect(analyserRef.current);
      analyserRef.current.fftSize = 256;
      
      const bufferLength = analyserRef.current.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);
      
      const updateVoiceLevel = () => {
        if (!isRecording || !audioContextRef.current || audioContextRef.current.state === 'closed') return;
        
        try {
          analyserRef.current.getByteFrequencyData(dataArray);
          const average = dataArray.reduce((a, b) => a + b) / bufferLength;
          const normalizedLevel = (average / 255) * 100;
          setVoiceLevel(normalizedLevel);
          
          animationFrameRef.current = requestAnimationFrame(updateVoiceLevel);
        } catch (error) {
          console.log('Voice level monitoring stopped due to context cleanup');
        }
      };
      
      updateVoiceLevel();
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const cleanupAudioContext = async () => {
    // Cancel any pending animation frames
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
    
    // Close AudioContext only if it exists and is not already closed
    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      try {
        await audioContextRef.current.close();
        console.log('AudioContext closed successfully');
      } catch (error) {
        console.log('AudioContext was already closed or closing');
      }
    }
    
    // Clear references
    audioContextRef.current = null;
    analyserRef.current = null;
    microphoneRef.current = null;
    setVoiceLevel(0);
  };

  const stopVoiceLevelMonitoring = () => {
    cleanupAudioContext();
  };

  const startRecording = async () => {
    try {
      if (recognitionRef.current && !isRecording) {
        console.log('Starting voice recording...');
        setTranscript('');
        currentTranscriptRef.current = '';
        isStoppingRef.current = false;
        
        // Start speech recognition first
        recognitionRef.current.start();
        
        // Start voice level monitoring
        await startVoiceLevelMonitoring();
      }
    } catch (error) {
      console.error('Failed to start recording:', error);
      alert('Failed to start voice recording. Please check microphone permissions.');
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    console.log('Stop recording called - implementing safe stop');
    
    // Set stopping flag first to prevent race conditions
    isStoppingRef.current = true;
    setIsRecording(false);
    
    // Capture current transcript immediately
    const currentTranscript = transcript.trim() || currentTranscriptRef.current.trim();
    console.log('Captured transcript for processing:', currentTranscript);
    
    // Stop voice level monitoring immediately
    stopVoiceLevelMonitoring();
    
    // Process transcript if available
    if (currentTranscript) {
      onRecordingComplete(currentTranscript);
      setTranscript('');
      currentTranscriptRef.current = '';
    }
    
    // Stop speech recognition safely
    setTimeout(() => {
      try {
        if (recognitionRef.current) {
          console.log('Stopping speech recognition...');
          recognitionRef.current.stop();
        }
      } catch (error) {
        console.log('Speech recognition cleanup error (safe to ignore):', error);
      }
    }, 100);
  };

  // Cleanup function
  useEffect(() => {
    return () => {
      if (recognitionRef.current && isRecording) {
        try {
          recognitionRef.current.stop();
        } catch (error) {
          console.log('Recognition cleanup error on unmount:', error);
        }
      }
      cleanupAudioContext();
    };
  }, []);

  return { 
    status: isRecording ? 'recording' : 'idle',
    startRecording, 
    stopRecording, 
    transcript,
    voiceLevel,
    isRecording
  };
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

// Enhanced Landing Page Component with i18n support
const EnhancedLandingPage = ({ setCurrentPage }) => {
  const { t } = useI18n();
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-white mb-6">
            🎯 {t('landing.title')}
          </h1>
          <p className="text-xl text-gray-300 mb-12 max-w-4xl mx-auto">
            {t('landing.subtitle')}
          </p>
          <div className="flex flex-wrap justify-center gap-4 mb-8">
            <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-3">
              <span className="text-green-200">✅ {t('landing.features.codingChallenges')}</span>
            </div>
            <div className="bg-blue-500/20 border border-blue-500/30 rounded-lg p-3">
              <span className="text-blue-200">✅ {t('landing.features.voiceInterview')}</span>
            </div>
            <div className="bg-purple-500/20 border border-purple-500/30 rounded-lg p-3">
              <span className="text-purple-200">✅ {t('landing.features.multiVectorAssessment')}</span>
            </div>
            <div className="bg-orange-500/20 border border-orange-500/30 rounded-lg p-3">
              <span className="text-orange-200">✅ {t('landing.features.biasMitigation')}</span>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto grid md:grid-cols-3 gap-8">
          {/* Enhanced Admin Portal Card */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-white mb-4">{t('landing.adminPortal.title')}</h2>
              <p className="text-gray-300 mb-6">
                {t('landing.adminPortal.description')}
              </p>
              <div className="mb-6 space-y-2">
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                  {t('landing.adminPortal.features.candidatePipeline')}
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                  {t('landing.adminPortal.features.roleArchetypes')}
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                  {t('landing.adminPortal.features.codingChallenges')}
                </div>
              </div>
              <button 
                onClick={() => setCurrentPage('admin-login')}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                {t('landing.adminPortal.button')}
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
              <h2 className="text-2xl font-bold text-white mb-4">{t('landing.candidatePortal.title')}</h2>
              <p className="text-gray-300 mb-6">
                {t('landing.candidatePortal.description')}
              </p>
              <div className="mb-6 space-y-2">
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                  {t('landing.candidatePortal.features.setupCheck')}
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                  {t('landing.candidatePortal.features.questionCards')}
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                  {t('landing.candidatePortal.features.interactiveModules')}
                </div>
              </div>
              <button 
                onClick={() => setCurrentPage('candidate-login')}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                {t('landing.candidatePortal.button')}
              </button>
            </div>
          </div>

          {/* New Placement Preparation Card */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-white mb-4">{t('landing.placementPreparation.title')}</h2>
              <p className="text-gray-300 mb-6">
                {t('landing.placementPreparation.description')}
              </p>
              <div className="mb-6 space-y-2">
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                  {t('landing.placementPreparation.features.createInterview')}
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                  {t('landing.placementPreparation.features.practiceRounds')}
                </div>
                <div className="flex items-center justify-center text-sm text-gray-300">
                  <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                  {t('landing.placementPreparation.features.skillAssessment')}
                </div>
              </div>
              <button 
                onClick={() => setCurrentPage('placement-preparation')}
                className="w-full bg-gradient-to-r from-orange-600 to-red-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-orange-700 hover:to-red-700 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                {t('landing.placementPreparation.button')}
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
  const [detailedReportModal, setDetailedReportModal] = useState({ show: false, data: null, loading: false });
  
  // Interview question limits
  const [minQuestions, setMinQuestions] = useState(8);
  const [maxQuestions, setMaxQuestions] = useState(12);
  
  // Question Selection Controls
  const [resumeBasedCount, setResumeBasedCount] = useState(2);
  const [technicalCount, setTechnicalCount] = useState(4);
  const [behavioralCount, setBehavioralCount] = useState(4);
  
  // Question Type Selection (auto-generate vs manual)
  const [resumeQuestionType, setResumeQuestionType] = useState('auto'); // 'auto' or 'manual'
  const [technicalQuestionType, setTechnicalQuestionType] = useState('auto');
  const [behavioralQuestionType, setBehavioralQuestionType] = useState('auto');
  
  // Manual Questions Storage
  const [manualResumeQuestions, setManualResumeQuestions] = useState([]);
  const [manualTechnicalQuestions, setManualTechnicalQuestions] = useState([]);
  const [manualBehavioralQuestions, setManualBehavioralQuestions] = useState([]);

  // Phase 2: AI Screening & Shortlisting State
  const [screeningResults, setScreeningResults] = useState(null);
  const [bulkCandidates, setBulkCandidates] = useState([]);
  const [screeningProgress, setScreeningProgress] = useState(null);

  // New Screening Workflow State
  const [uploadedResumes, setUploadedResumes] = useState([]);
  const [savedJobRequirements, setSavedJobRequirements] = useState(null);
  const [screeningComplete, setScreeningComplete] = useState(false);

  // Personalized Interview State
  const [personalizedJobTitle, setPersonalizedJobTitle] = useState('');
  const [personalizedJobDescription, setPersonalizedJobDescription] = useState('');
  const [personalizedJobRequirements, setPersonalizedJobRequirements] = useState('');
  const [personalizedResumeFile, setPersonalizedResumeFile] = useState(null);
  const [personalizedResumePreview, setPersonalizedResumePreview] = useState('');
  const [personalizedGeneratedToken, setPersonalizedGeneratedToken] = useState('');
  const [personalizedLoading, setPersonalizedLoading] = useState(false);
  const [personalizedRoleArchetype, setPersonalizedRoleArchetype] = useState('General');
  const [personalizedInterviewFocus, setPersonalizedInterviewFocus] = useState('Balanced');
  const [personalizedIncludeCodingChallenge, setPersonalizedIncludeCodingChallenge] = useState(false);
  const [aiDifficultyAdjustment, setAiDifficultyAdjustment] = useState('adaptive'); // 'adaptive', 'progressive', 'static'
  const [realTimeInsights, setRealTimeInsights] = useState(true);
  const [dynamicQuestionGeneration, setDynamicQuestionGeneration] = useState(true);
  const [personalizedMinQuestions, setPersonalizedMinQuestions] = useState(8);
  const [personalizedMaxQuestions, setPersonalizedMaxQuestions] = useState(12);

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

  // Utility functions for manual questions
  const addManualQuestion = (type) => {
    const newQuestion = { question: '', expectedAnswer: '' };
    if (type === 'resume') {
      setManualResumeQuestions([...manualResumeQuestions, newQuestion]);
    } else if (type === 'technical') {
      setManualTechnicalQuestions([...manualTechnicalQuestions, newQuestion]);
    } else if (type === 'behavioral') {
      setManualBehavioralQuestions([...manualBehavioralQuestions, newQuestion]);
    }
  };

  const removeManualQuestion = (type, index) => {
    if (type === 'resume') {
      setManualResumeQuestions(manualResumeQuestions.filter((_, i) => i !== index));
    } else if (type === 'technical') {
      setManualTechnicalQuestions(manualTechnicalQuestions.filter((_, i) => i !== index));
    } else if (type === 'behavioral') {
      setManualBehavioralQuestions(manualBehavioralQuestions.filter((_, i) => i !== index));
    }
  };

  const updateManualQuestion = (type, index, field, value) => {
    if (type === 'resume') {
      const updated = [...manualResumeQuestions];
      updated[index][field] = value;
      setManualResumeQuestions(updated);
    } else if (type === 'technical') {
      const updated = [...manualTechnicalQuestions];
      updated[index][field] = value;
      setManualTechnicalQuestions(updated);
    } else if (type === 'behavioral') {
      const updated = [...manualBehavioralQuestions];
      updated[index][field] = value;
      setManualBehavioralQuestions(updated);
    }
  };

  // Auto-adjust manual questions when count changes
  const adjustManualQuestions = (type, newCount) => {
    if (type === 'resume' && resumeQuestionType === 'manual') {
      const current = manualResumeQuestions.length;
      if (newCount > current) {
        const toAdd = Array(newCount - current).fill().map(() => ({ question: '', expectedAnswer: '' }));
        setManualResumeQuestions([...manualResumeQuestions, ...toAdd]);
      } else if (newCount < current) {
        setManualResumeQuestions(manualResumeQuestions.slice(0, newCount));
      }
    } else if (type === 'technical' && technicalQuestionType === 'manual') {
      const current = manualTechnicalQuestions.length;
      if (newCount > current) {
        const toAdd = Array(newCount - current).fill().map(() => ({ question: '', expectedAnswer: '' }));
        setManualTechnicalQuestions([...manualTechnicalQuestions, ...toAdd]);
      } else if (newCount < current) {
        setManualTechnicalQuestions(manualTechnicalQuestions.slice(0, newCount));
      }
    } else if (type === 'behavioral' && behavioralQuestionType === 'manual') {
      const current = manualBehavioralQuestions.length;
      if (newCount > current) {
        const toAdd = Array(newCount - current).fill().map(() => ({ question: '', expectedAnswer: '' }));
        setManualBehavioralQuestions([...manualBehavioralQuestions, ...toAdd]);
      } else if (newCount < current) {
        setManualBehavioralQuestions(manualBehavioralQuestions.slice(0, newCount));
      }
    }
  };

  // Validate total questions within limits
  const getTotalQuestionCount = () => resumeBasedCount + technicalCount + behavioralCount;
  const isValidQuestionCount = () => {
    const total = getTotalQuestionCount();
    return total >= minQuestions && total <= maxQuestions;
  };

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
    
    // Validate total question count
    if (!isValidQuestionCount()) {
      alert(`Total questions must be between ${minQuestions} and ${maxQuestions}. Current total: ${getTotalQuestionCount()}`);
      return;
    }
    
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
    
    // Add custom question configuration
    formData.append('custom_questions_config', JSON.stringify({
      resume_based: {
        count: resumeBasedCount,
        type: resumeQuestionType,
        manual_questions: resumeQuestionType === 'manual' ? manualResumeQuestions.filter(q => q.question.trim() !== '') : []
      },
      technical: {
        count: technicalCount,
        type: technicalQuestionType,
        manual_questions: technicalQuestionType === 'manual' ? manualTechnicalQuestions.filter(q => q.question.trim() !== '') : []
      },
      behavioral: {
        count: behavioralCount,
        type: behavioralQuestionType,
        manual_questions: behavioralQuestionType === 'manual' ? manualBehavioralQuestions.filter(q => q.question.trim() !== '') : []
      }
    }));

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
        
        // Reset custom question controls
        setResumeBasedCount(2);
        setTechnicalCount(4);
        setBehavioralCount(4);
        setResumeQuestionType('auto');
        setTechnicalQuestionType('auto');
        setBehavioralQuestionType('auto');
        setManualResumeQuestions([]);
        setManualTechnicalQuestions([]);
        setManualBehavioralQuestions([]);
        
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

  // Personalized Interview Handler Functions
  const handlePersonalizedFileUpload = (e) => {
    const file = e.target.files[0];
    setPersonalizedResumeFile(file);
    
    if (file) {
      const fileType = file.name.split('.').pop().toLowerCase();
      const supportedTypes = ['pdf', 'doc', 'docx', 'txt'];
      if (!supportedTypes.includes(fileType)) {
        alert('Please upload PDF, DOC, DOCX, or TXT files only');
        e.target.value = '';
        setPersonalizedResumeFile(null);
      }
    }
  };

  const handlePersonalizedSubmit = async (e) => {
    e.preventDefault();
    setPersonalizedLoading(true);

    const formData = new FormData();
    formData.append('job_title', personalizedJobTitle);
    formData.append('job_description', personalizedJobDescription);
    formData.append('job_requirements', personalizedJobRequirements);
    formData.append('include_coding_challenge', personalizedIncludeCodingChallenge);
    formData.append('role_archetype', personalizedRoleArchetype);
    formData.append('interview_focus', personalizedInterviewFocus);
    formData.append('resume_file', personalizedResumeFile);
    
    // Add personalized interview configuration
    formData.append('interview_mode', 'personalized');
    formData.append('dynamic_question_generation', dynamicQuestionGeneration);
    formData.append('real_time_insights', realTimeInsights);
    formData.append('ai_difficulty_adjustment', aiDifficultyAdjustment);
    formData.append('min_questions', personalizedMinQuestions);
    formData.append('max_questions', personalizedMaxQuestions);

    try {
      // Use enhanced endpoint with personalized mode flag
      const response = await fetch(`${API}/admin/upload-job-enhanced`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setPersonalizedGeneratedToken(data.token);
        setPersonalizedResumePreview(data.resume_preview || '');
        
        // Reset form
        setPersonalizedJobTitle('');
        setPersonalizedJobDescription('');
        setPersonalizedJobRequirements('');
        setPersonalizedIncludeCodingChallenge(false);
        setPersonalizedRoleArchetype('General');
        setPersonalizedInterviewFocus('Balanced');
        setPersonalizedResumeFile(null);
        setDynamicQuestionGeneration(true);
        setRealTimeInsights(true);
        setAiDifficultyAdjustment('adaptive');
        setPersonalizedMinQuestions(8);
        setPersonalizedMaxQuestions(12);
        
        // Clear file input
        const fileInput = document.querySelector('input[type="file"][accept*="pdf"]');
        if (fileInput) fileInput.value = '';
        
        // Refresh pipeline if on pipeline tab
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
      setPersonalizedLoading(false);
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

  const fetchDetailedReport = async (sessionId) => {
    setDetailedReportModal({ show: true, data: null, loading: true });
    try {
      const response = await fetch(`${API}/admin/detailed-report/${sessionId}`);
      if (response.ok) {
        const data = await response.json();
        setDetailedReportModal({ show: true, data, loading: false });
      } else {
        setDetailedReportModal({ show: false, data: null, loading: false });
        alert('Failed to fetch detailed report');
      }
    } catch (err) {
      console.error('Failed to fetch detailed report:', err);
      setDetailedReportModal({ show: false, data: null, loading: false });
      alert('Error fetching detailed report');
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
              onClick={() => setActiveTab('personalized')}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-md transition-all duration-300 ${
                activeTab === 'personalized'
                  ? 'bg-purple-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              🧠 Create Personalised Interview
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
            <button
              onClick={() => setActiveTab('screening')}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-md transition-all duration-300 ${
                activeTab === 'screening'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              🤖 AI Screening
            </button>
            <button
              onClick={() => setActiveTab('results')}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-md transition-all duration-300 ${
                activeTab === 'results'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              📋 Results
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

              {/* Question Selection Controls */}
              <div className="bg-white/5 p-6 rounded-lg border border-white/10">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                  </svg>
                  Question Selection Controls
                </h3>
                <p className="text-gray-300 text-sm mb-4">
                  Customize your interview questions by specifying counts and choosing between AI-generated or manually entered questions.
                </p>
                
                {/* Total Questions Validation */}
                <div className="mb-4 p-3 rounded-lg bg-white/5">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-300">Total Questions:</span>
                    <span className={`font-medium ${isValidQuestionCount() ? 'text-green-300' : 'text-red-300'}`}>
                      {getTotalQuestionCount()} / {minQuestions}-{maxQuestions}
                    </span>
                  </div>
                  {!isValidQuestionCount() && (
                    <p className="text-red-300 text-xs mt-1">
                      ⚠️ Total questions must be between {minQuestions} and {maxQuestions}
                    </p>
                  )}
                </div>

                {/* Resume-Based Questions */}
                <div className="mb-6 p-4 bg-white/5 rounded-lg border border-white/10">
                  <h4 className="text-md font-medium text-white mb-3 flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Resume-Based Questions
                  </h4>
                  
                  <div className="grid md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <label className="block text-white font-medium mb-2">Number of Questions</label>
                      <input
                        type="number"
                        min="0"
                        max="8"
                        value={resumeBasedCount}
                        onChange={(e) => {
                          const value = parseInt(e.target.value);
                          setResumeBasedCount(value);
                          adjustManualQuestions('resume', value);
                        }}
                        className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-white font-medium mb-2">Question Type</label>
                      <div className="flex space-x-4">
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="resumeQuestionType"
                            value="auto"
                            checked={resumeQuestionType === 'auto'}
                            onChange={(e) => setResumeQuestionType(e.target.value)}
                            className="mr-2"
                          />
                          <span className="text-white text-sm">Auto-generate via AI</span>
                        </label>
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="resumeQuestionType"
                            value="manual"
                            checked={resumeQuestionType === 'manual'}
                            onChange={(e) => {
                              setResumeQuestionType(e.target.value);
                              if (e.target.value === 'manual') {
                                adjustManualQuestions('resume', resumeBasedCount);
                              }
                            }}
                            className="mr-2"
                          />
                          <span className="text-white text-sm">Manually enter questions</span>
                        </label>
                      </div>
                    </div>
                  </div>

                  {/* Manual Resume Questions */}
                  {resumeQuestionType === 'manual' && resumeBasedCount > 0 && (
                    <div className="mt-4">
                      <h5 className="text-sm font-medium text-white mb-2">Manual Resume-Based Questions</h5>
                      {Array.from({ length: resumeBasedCount }, (_, index) => (
                        <div key={index} className="mb-4 p-3 bg-white/5 rounded-lg">
                          <label className="block text-white text-sm font-medium mb-2">
                            Question {index + 1}
                          </label>
                          <textarea
                            value={manualResumeQuestions[index]?.question || ''}
                            onChange={(e) => updateManualQuestion('resume', index, 'question', e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter your resume-based question..."
                            rows={2}
                          />
                          <label className="block text-white text-sm font-medium mb-2 mt-2">
                            Expected Answer (Optional)
                          </label>
                          <textarea
                            value={manualResumeQuestions[index]?.expectedAnswer || ''}
                            onChange={(e) => updateManualQuestion('resume', index, 'expectedAnswer', e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter expected answer (optional)..."
                            rows={2}
                          />
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Technical Questions */}
                <div className="mb-6 p-4 bg-white/5 rounded-lg border border-white/10">
                  <h4 className="text-md font-medium text-white mb-3 flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                    </svg>
                    Technical Questions
                  </h4>
                  
                  <div className="grid md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <label className="block text-white font-medium mb-2">Number of Questions</label>
                      <input
                        type="number"
                        min="0"
                        max="10"
                        value={technicalCount}
                        onChange={(e) => {
                          const value = parseInt(e.target.value);
                          setTechnicalCount(value);
                          adjustManualQuestions('technical', value);
                        }}
                        className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-white font-medium mb-2">Question Type</label>
                      <div className="flex space-x-4">
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="technicalQuestionType"
                            value="auto"
                            checked={technicalQuestionType === 'auto'}
                            onChange={(e) => setTechnicalQuestionType(e.target.value)}
                            className="mr-2"
                          />
                          <span className="text-white text-sm">Auto-generate via AI</span>
                        </label>
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="technicalQuestionType"
                            value="manual"
                            checked={technicalQuestionType === 'manual'}
                            onChange={(e) => {
                              setTechnicalQuestionType(e.target.value);
                              if (e.target.value === 'manual') {
                                adjustManualQuestions('technical', technicalCount);
                              }
                            }}
                            className="mr-2"
                          />
                          <span className="text-white text-sm">Manually enter questions</span>
                        </label>
                      </div>
                    </div>
                  </div>

                  {/* Manual Technical Questions */}
                  {technicalQuestionType === 'manual' && technicalCount > 0 && (
                    <div className="mt-4">
                      <h5 className="text-sm font-medium text-white mb-2">Manual Technical Questions</h5>
                      {Array.from({ length: technicalCount }, (_, index) => (
                        <div key={index} className="mb-4 p-3 bg-white/5 rounded-lg">
                          <label className="block text-white text-sm font-medium mb-2">
                            Question {index + 1}
                          </label>
                          <textarea
                            value={manualTechnicalQuestions[index]?.question || ''}
                            onChange={(e) => updateManualQuestion('technical', index, 'question', e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter your technical question..."
                            rows={2}
                          />
                          <label className="block text-white text-sm font-medium mb-2 mt-2">
                            Expected Answer (Optional)
                          </label>
                          <textarea
                            value={manualTechnicalQuestions[index]?.expectedAnswer || ''}
                            onChange={(e) => updateManualQuestion('technical', index, 'expectedAnswer', e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter expected answer (optional)..."
                            rows={2}
                          />
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Behavioral Questions */}
                <div className="mb-4 p-4 bg-white/5 rounded-lg border border-white/10">
                  <h4 className="text-md font-medium text-white mb-3 flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    Behavioral Questions
                  </h4>
                  
                  <div className="grid md:grid-cols-2 gap-4 mb-4">
                    <div>
                      <label className="block text-white font-medium mb-2">Number of Questions</label>
                      <input
                        type="number"
                        min="0"
                        max="10"
                        value={behavioralCount}
                        onChange={(e) => {
                          const value = parseInt(e.target.value);
                          setBehavioralCount(value);
                          adjustManualQuestions('behavioral', value);
                        }}
                        className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                    
                    <div>
                      <label className="block text-white font-medium mb-2">Question Type</label>
                      <div className="flex space-x-4">
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="behavioralQuestionType"
                            value="auto"
                            checked={behavioralQuestionType === 'auto'}
                            onChange={(e) => setBehavioralQuestionType(e.target.value)}
                            className="mr-2"
                          />
                          <span className="text-white text-sm">Auto-generate via AI</span>
                        </label>
                        <label className="flex items-center">
                          <input
                            type="radio"
                            name="behavioralQuestionType"
                            value="manual"
                            checked={behavioralQuestionType === 'manual'}
                            onChange={(e) => {
                              setBehavioralQuestionType(e.target.value);
                              if (e.target.value === 'manual') {
                                adjustManualQuestions('behavioral', behavioralCount);
                              }
                            }}
                            className="mr-2"
                          />
                          <span className="text-white text-sm">Manually enter questions</span>
                        </label>
                      </div>
                    </div>
                  </div>

                  {/* Manual Behavioral Questions */}
                  {behavioralQuestionType === 'manual' && behavioralCount > 0 && (
                    <div className="mt-4">
                      <h5 className="text-sm font-medium text-white mb-2">Manual Behavioral Questions</h5>
                      {Array.from({ length: behavioralCount }, (_, index) => (
                        <div key={index} className="mb-4 p-3 bg-white/5 rounded-lg">
                          <label className="block text-white text-sm font-medium mb-2">
                            Question {index + 1}
                          </label>
                          <textarea
                            value={manualBehavioralQuestions[index]?.question || ''}
                            onChange={(e) => updateManualQuestion('behavioral', index, 'question', e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter your behavioral question..."
                            rows={2}
                          />
                          <label className="block text-white text-sm font-medium mb-2 mt-2">
                            Expected Answer (Optional)
                          </label>
                          <textarea
                            value={manualBehavioralQuestions[index]?.expectedAnswer || ''}
                            onChange={(e) => updateManualQuestion('behavioral', index, 'expectedAnswer', e.target.value)}
                            className="w-full px-3 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter expected answer (optional)..."
                            rows={2}
                          />
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Updated Question Distribution Preview */}
                <div className="mt-4 p-4 bg-white/5 rounded-lg">
                  <h4 className="text-sm font-medium text-white mb-2 flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    Question Distribution Summary
                  </h4>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div className="flex justify-between text-gray-300">
                      <span>Resume-Based:</span>
                      <span className="text-purple-300">{resumeBasedCount} ({resumeQuestionType})</span>
                    </div>
                    <div className="flex justify-between text-gray-300">
                      <span>Technical:</span>
                      <span className="text-blue-300">{technicalCount} ({technicalQuestionType})</span>
                    </div>
                    <div className="flex justify-between text-gray-300">
                      <span>Behavioral:</span>
                      <span className="text-green-300">{behavioralCount} ({behavioralQuestionType})</span>
                    </div>
                  </div>
                  <div className="mt-2 text-xs text-gray-400">
                    💡 If manual questions are incomplete, AI will auto-generate the remaining questions
                  </div>
                </div>

                {/* Interview Duration Estimation */}
                <div className="mt-4 flex items-center justify-between text-sm">
                  <span className="text-gray-300">Estimated Interview Duration:</span>
                  <span className="text-yellow-300 font-medium">
                    {Math.ceil(getTotalQuestionCount() * 2.5)} - {Math.ceil(getTotalQuestionCount() * 3)} minutes
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
                disabled={loading || !resumeFile || !isValidQuestionCount()}
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

        {/* Personalized Interview Tab */}
        {activeTab === 'personalized' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-white mb-2">🧠 Create AI-Powered Personalised Interview</h2>
              <p className="text-gray-300 text-sm">
                Leverage advanced AI to create dynamic interviews that adapt in real-time based on candidate responses, 
                performance, and experience gaps with intelligent difficulty adjustment and live performance insights.
              </p>
            </div>
            
            <form onSubmit={handlePersonalizedSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-white font-medium mb-2">Job Title</label>
                  <input
                    type="text"
                    value={personalizedJobTitle}
                    onChange={(e) => setPersonalizedJobTitle(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    placeholder="e.g., Senior AI Engineer"
                    required
                  />
                </div>

                <div>
                  <label className="block text-white font-medium mb-2">Role Archetype</label>
                  <select
                    value={personalizedRoleArchetype}
                    onChange={(e) => setPersonalizedRoleArchetype(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
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
                    value={personalizedInterviewFocus}
                    onChange={(e) => setPersonalizedInterviewFocus(e.target.value)}
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
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
                      checked={personalizedIncludeCodingChallenge}
                      onChange={(e) => setPersonalizedIncludeCodingChallenge(e.target.checked)}
                      className="mr-2 w-5 h-5 rounded border-white/30 bg-white/20 text-purple-600 focus:ring-purple-500 focus:ring-2"
                    />
                    Include Coding Challenge
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-white font-medium mb-2">Job Description</label>
                <textarea
                  value={personalizedJobDescription}
                  onChange={(e) => setPersonalizedJobDescription(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Detailed job description..."
                  required
                />
              </div>

              <div>
                <label className="block text-white font-medium mb-2">Job Requirements</label>
                <textarea
                  value={personalizedJobRequirements}
                  onChange={(e) => setPersonalizedJobRequirements(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Technical skills, experience requirements..."
                  required
                />
              </div>

              {/* Interview Questions Configuration */}
              <div className="bg-white/10 backdrop-blur-lg rounded-lg p-6 border border-white/20">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  📋 Interview Questions Configuration
                </h3>
                <p className="text-gray-300 text-sm mb-6">
                  Set the range of questions to be asked during the interview. The system will dynamically adjust based on candidate responses.
                </p>
                
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-white font-medium mb-2">
                      Minimum Questions <span className="text-purple-300">(Must be asked)</span>
                    </label>
                    <input
                      type="number"
                      min="6"
                      max="15"
                      value={personalizedMinQuestions}
                      onChange={(e) => {
                        const value = parseInt(e.target.value);
                        setPersonalizedMinQuestions(value);
                        // Ensure max is at least equal to min
                        if (personalizedMaxQuestions < value) {
                          setPersonalizedMaxQuestions(value);
                        }
                      }}
                      className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                    <p className="text-purple-300 text-xs mt-2">Recommended: 6-10 questions</p>
                  </div>
                  
                  <div>
                    <label className="block text-white font-medium mb-2">
                      Maximum Questions <span className="text-purple-300">(If needed for assessment)</span>
                    </label>
                    <input
                      type="number"
                      min={personalizedMinQuestions}
                      max="20"
                      value={personalizedMaxQuestions}
                      onChange={(e) => setPersonalizedMaxQuestions(parseInt(e.target.value))}
                      className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                    <p className="text-purple-300 text-xs mt-2">Recommended: 10-15 questions</p>
                  </div>
                </div>
                
                {/* Expected Question Distribution */}
                <div className="mt-6 bg-white/5 p-4 rounded-lg border border-white/10">
                  <h4 className="text-white font-medium mb-3 flex items-center">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v4" />
                    </svg>
                    📊 Expected Question Distribution
                  </h4>
                  <div className="grid md:grid-cols-2 gap-4 text-sm">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-300">Technical Questions:</span>
                      <span className="text-purple-300 font-medium">
                        {Math.floor(personalizedMinQuestions * 0.5)}-{Math.ceil(personalizedMaxQuestions * 0.5)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-300">Behavioral Questions:</span>
                      <span className="text-purple-300 font-medium">
                        {Math.floor(personalizedMinQuestions * 0.5)}-{Math.ceil(personalizedMaxQuestions * 0.5)}
                      </span>
                    </div>
                  </div>
                  
                  <div className="mt-4 p-3 bg-yellow-500/10 rounded-lg border border-yellow-400/20">
                    <p className="text-yellow-300 text-xs flex items-center">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      💡 The AI will adaptively adjust the number of questions based on candidate performance and responses
                    </p>
                  </div>
                </div>
                
                {/* Estimated Duration */}
                <div className="mt-4 text-right">
                  <span className="text-gray-300 text-sm">Estimated Interview Duration: </span>
                  <span className="text-purple-300 font-semibold text-lg">
                    {Math.ceil(personalizedMinQuestions * 2.5)}-{Math.ceil(personalizedMaxQuestions * 3)} minutes
                  </span>
                </div>
              </div>

              {/* AI-Powered Question Generation Configuration */}
              <div className="bg-gradient-to-r from-purple-500/10 to-pink-500/10 p-6 rounded-lg border border-purple-400/20">
                <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  🧠 AI-Powered Dynamic Question Generation
                </h3>
                <p className="text-gray-300 text-sm mb-6">
                  Instead of pre-defined questions, our AI will analyze candidate responses in real-time and generate 
                  personalized follow-up questions based on their background, experience gaps, and role requirements.
                </p>

                {/* AI Configuration Options */}
                <div className="grid md:grid-cols-3 gap-4">
                  {/* Dynamic Question Generation */}
                  <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-white font-medium flex items-center">
                        <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                        Dynamic Questions
                      </h4>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={dynamicQuestionGeneration}
                          onChange={(e) => setDynamicQuestionGeneration(e.target.checked)}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600"></div>
                      </label>
                    </div>
                    <p className="text-gray-400 text-xs">
                      AI analyzes candidate responses and generates personalized follow-up questions
                    </p>
                  </div>

                  {/* Real-time Performance Insights */}
                  <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="text-white font-medium flex items-center">
                        <span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                        Live Insights
                      </h4>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={realTimeInsights}
                          onChange={(e) => setRealTimeInsights(e.target.checked)}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600"></div>
                      </label>
                    </div>
                    <p className="text-gray-400 text-xs">
                      Real-time dashboard with confidence levels and knowledge gap analysis
                    </p>
                  </div>

                  {/* Intelligent Difficulty Adjustment */}
                  <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                    <div className="mb-3">
                      <h4 className="text-white font-medium flex items-center mb-2">
                        <span className="w-2 h-2 bg-yellow-400 rounded-full mr-2"></span>
                        Difficulty Mode
                      </h4>
                      <select
                        value={aiDifficultyAdjustment}
                        onChange={(e) => setAiDifficultyAdjustment(e.target.value)}
                        className="w-full px-3 py-2 rounded bg-white/20 border border-white/30 text-white text-xs focus:outline-none focus:ring-2 focus:ring-purple-500"
                      >
                        <option value="adaptive" className="bg-gray-800">🎯 Adaptive (Recommended)</option>
                        <option value="progressive" className="bg-gray-800">📈 Progressive</option>
                        <option value="static" className="bg-gray-800">📊 Static</option>
                      </select>
                    </div>
                    <p className="text-gray-400 text-xs">
                      AI adjusts question difficulty based on candidate performance
                    </p>
                  </div>
                </div>

                {/* AI Features Preview */}
                <div className="mt-6 grid md:grid-cols-2 gap-4">
                  <div className="bg-white/5 p-4 rounded-lg">
                    <h5 className="text-white font-medium mb-2 flex items-center">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      Dynamic Features Enabled
                    </h5>
                    <ul className="text-sm text-gray-300 space-y-1">
                      <li>• Real-time response analysis</li>
                      <li>• Experience gap detection</li>
                      <li>• Adaptive questioning flow</li>
                      <li>• Performance-based adjustments</li>
                    </ul>
                  </div>
                  <div className="bg-white/5 p-4 rounded-lg">
                    <h5 className="text-white font-medium mb-2 flex items-center">
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 00-2-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                      Live Dashboard Metrics
                    </h5>
                    <ul className="text-sm text-gray-300 space-y-1">
                      <li>• Confidence level tracking</li>
                      <li>• Knowledge gap indicators</li>
                      <li>• Behavioral pattern analysis</li>
                      <li>• Technical depth assessment</li>
                    </ul>
                  </div>
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
                    accept=".pdf,.doc,.docx,.txt"
                    onChange={handlePersonalizedFileUpload}
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-white file:bg-purple-600 hover:file:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500"
                    required={!personalizedResumeFile}
                  />
                  <div className="absolute inset-y-0 right-0 flex items-center pr-3">
                    <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                </div>
                {personalizedResumeFile && (
                  <p className="mt-2 text-sm text-green-300">
                    ✅ File uploaded: {personalizedResumeFile.name}
                  </p>
                )}
              </div>

              <button
                type="submit"
                disabled={personalizedLoading}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-600 disabled:to-gray-600 text-white font-bold py-4 px-6 rounded-lg transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg"
              >
                {personalizedLoading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Creating AI-Powered Interview...
                  </div>
                ) : (
                  <div className="flex items-center justify-center">
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    Create AI-Powered Personalized Interview
                  </div>
                )}
              </button>
            </form>

            {/* Success Display */}
            {personalizedGeneratedToken && (
              <div className="mt-8 p-6 bg-gradient-to-r from-purple-600/20 to-pink-600/20 border border-purple-500/30 rounded-2xl">
                <h3 className="text-xl font-bold text-purple-200 mb-4">✅ AI-Powered Personalized Interview Created Successfully!</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-purple-200 mb-2"><strong>Interview Token:</strong></p>
                    <code className="block bg-black/30 p-3 rounded text-purple-300 font-mono break-all">
                      {personalizedGeneratedToken}
                    </code>
                  </div>
                  <div>
                    <p className="text-purple-200 mb-2"><strong>AI Features Enabled:</strong></p>
                    <div className="space-y-1">
                      <div className="text-sm text-purple-300">🎯 Role: {personalizedRoleArchetype}</div>
                      <div className="text-sm text-purple-300">📊 Focus: {personalizedInterviewFocus}</div>
                      <div className="text-sm text-purple-300">
                        📋 Questions: {personalizedMinQuestions}-{personalizedMaxQuestions} questions
                      </div>
                      <div className="text-sm text-purple-300">
                        💻 Coding: {personalizedIncludeCodingChallenge ? 'Enabled' : 'Disabled'}
                      </div>
                      <div className="text-sm text-purple-300">
                        🧠 Dynamic Questions: {dynamicQuestionGeneration ? 'Enabled' : 'Disabled'}
                      </div>
                      <div className="text-sm text-purple-300">
                        📈 Live Insights: {realTimeInsights ? 'Enabled' : 'Disabled'}
                      </div>
                      <div className="text-sm text-purple-300">
                        🎯 Difficulty Mode: {aiDifficultyAdjustment.charAt(0).toUpperCase() + aiDifficultyAdjustment.slice(1)}
                      </div>
                    </div>
                  </div>
                </div>
                {personalizedResumePreview && (
                  <div className="mt-4">
                    <p className="text-purple-200 mb-2"><strong>Resume Preview:</strong></p>
                    <div className="bg-black/30 p-3 rounded text-purple-300 text-sm max-h-32 overflow-y-auto">
                      {personalizedResumePreview}
                    </div>
                  </div>
                )}
                
                <div className="mt-4 p-4 bg-gradient-to-r from-green-500/10 to-blue-500/10 rounded-lg border border-green-400/20">
                  <h4 className="text-green-200 font-medium mb-2">🚀 What Happens Next:</h4>
                  <ul className="text-sm text-green-300 space-y-1">
                    <li>• Candidates will experience dynamic, adaptive questioning</li>
                    <li>• AI will analyze responses and generate personalized follow-ups</li>
                    <li>• Real-time performance insights will be displayed</li>
                    <li>• Question difficulty will adjust based on candidate performance</li>
                    <li>• Comprehensive analysis will identify strengths and experience gaps</li>
                  </ul>
                </div>
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
                      <div className="text-sm text-gray-300 mb-2">
                        {new Date(candidate.created_at).toLocaleDateString()}
                      </div>
                      {candidate.status === 'Report Ready' && candidate.session_id && (
                        <button
                          onClick={() => fetchDetailedReport(candidate.session_id)}
                          className="bg-purple-600 hover:bg-purple-700 text-white text-xs font-semibold py-1 px-3 rounded transition-colors duration-300"
                        >
                          📊 View Transcript
                        </button>
                      )}
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
        
        {/* Detailed Report Modal */}
        {detailedReportModal.show && (
          <div className="fixed inset-0 bg-black/75 flex items-center justify-center z-50 p-4">
            <div className="bg-gradient-to-br from-purple-900/90 to-blue-900/90 backdrop-blur-lg rounded-2xl border border-white/20 max-w-6xl w-full max-h-[90vh] overflow-hidden">
              <div className="flex justify-between items-center p-6 border-b border-white/20">
                <h3 className="text-2xl font-bold text-white">📋 Detailed Interview Report</h3>
                <button
                  onClick={() => setDetailedReportModal({ show: false, data: null, loading: false })}
                  className="text-gray-300 hover:text-white text-2xl"
                >
                  ✕
                </button>
              </div>
              
              <div className="overflow-y-auto max-h-[calc(90vh-100px)]">
                {detailedReportModal.loading ? (
                  <div className="flex justify-center items-center h-64">
                    <div className="text-white text-lg">📊 Loading detailed report...</div>
                  </div>
                ) : detailedReportModal.data ? (
                  <div className="p-6 space-y-6">
                    {/* Header Info */}
                    <div className="grid md:grid-cols-3 gap-4">
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-sm text-gray-300">Candidate</div>
                        <div className="text-lg font-bold text-white">{detailedReportModal.data.candidate_name}</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-sm text-gray-300">Position</div>
                        <div className="text-lg font-bold text-white">{detailedReportModal.data.job_title}</div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4">
                        <div className="text-sm text-gray-300">Interview Date</div>
                        <div className="text-lg font-bold text-white">
                          {new Date(detailedReportModal.data.interview_date).toLocaleDateString()}
                        </div>
                      </div>
                    </div>

                    {/* Interview Transcript */}
                    <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                      <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                        💬 Interview Transcript
                      </h4>
                      <div className="bg-black/30 rounded-lg p-4 font-mono text-sm max-h-96 overflow-y-auto">
                        <pre className="text-gray-100 whitespace-pre-wrap leading-relaxed">
                          {detailedReportModal.data.transcript}
                        </pre>
                      </div>
                    </div>

                    {/* Enhanced Scores Summary with Individual Scoring */}
                    <div className="grid md:grid-cols-4 gap-4">
                      <div className="bg-white/10 rounded-lg p-4 text-center">
                        <div className="text-sm text-gray-300">Technical Score</div>
                        <div className="text-3xl font-bold text-blue-400">
                          {detailedReportModal.data.assessment_summary.technical_score}/100
                        </div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4 text-center">
                        <div className="text-sm text-gray-300">Behavioral Score</div>
                        <div className="text-3xl font-bold text-green-400">
                          {detailedReportModal.data.assessment_summary.behavioral_score}/100
                        </div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4 text-center">
                        <div className="text-sm text-gray-300">Overall Score</div>
                        <div className="text-3xl font-bold text-purple-400">
                          {detailedReportModal.data.assessment_summary.overall_score}/100
                        </div>
                      </div>
                      <div className="bg-white/10 rounded-lg p-4 text-center">
                        <div className="text-sm text-gray-300">Average Individual Score</div>
                        <div className="text-3xl font-bold text-orange-400">
                          {detailedReportModal.data.assessment_summary.average_individual_score}/100
                        </div>
                      </div>
                    </div>

                    {/* Individual Question Scores */}
                    {detailedReportModal.data.question_scores && (
                      <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                        <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                          📊 Individual Question Analysis
                        </h4>
                        <div className="space-y-4 max-h-96 overflow-y-auto">
                          {detailedReportModal.data.question_scores.map((questionScore, index) => (
                            <div key={index} className="bg-black/20 rounded-lg p-4 border border-white/10">
                              <div className="flex justify-between items-start mb-2">
                                <span className="text-sm font-medium text-purple-300">
                                  Question {questionScore.question_number}
                                </span>
                                <span className="text-lg font-bold text-yellow-400">
                                  {questionScore.score}/100
                                </span>
                              </div>
                              <div className="text-sm text-gray-300 mb-2 italic">
                                "{questionScore.question}"
                              </div>
                              <div className="grid grid-cols-3 gap-2 mb-2 text-xs">
                                <div className="text-center">
                                  <div className="text-gray-400">Accuracy</div>
                                  <div className="text-blue-300 font-semibold">{questionScore.accuracy}%</div>
                                </div>
                                <div className="text-center">
                                  <div className="text-gray-400">Relevance</div>
                                  <div className="text-green-300 font-semibold">{questionScore.relevance}%</div>
                                </div>
                                <div className="text-center">
                                  <div className="text-gray-400">Completeness</div>
                                  <div className="text-purple-300 font-semibold">{questionScore.completeness}%</div>
                                </div>
                              </div>
                              <div className="text-xs text-gray-300 bg-black/30 rounded p-2">
                                {questionScore.feedback}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Comprehensive AI Analysis */}
                    {detailedReportModal.data.ai_analysis && (
                      <>
                        {/* Big Five Personality Analysis */}
                        {detailedReportModal.data.ai_analysis.personality_analysis && (
                          <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                            <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                              🧠 Big Five Personality Analysis
                            </h4>
                            <div className="grid md:grid-cols-5 gap-4 mb-4">
                              {Object.entries(detailedReportModal.data.ai_analysis.personality_analysis.big_five_scores || {}).map(([trait, score]) => (
                                <div key={trait} className="bg-black/20 rounded-lg p-3 text-center">
                                  <div className="text-xs text-gray-400 capitalize mb-1">{trait}</div>
                                  <div className="text-lg font-bold text-cyan-400">{Math.round(score * 100)}%</div>
                                  <div className="w-full bg-gray-700 rounded-full h-1.5 mt-2">
                                    <div 
                                      className="bg-cyan-400 h-1.5 rounded-full" 
                                      style={{width: `${score * 100}%`}}
                                    ></div>
                                  </div>
                                </div>
                              ))}
                            </div>
                            <div className="text-sm text-gray-300">
                              <strong>Dominant Traits:</strong> {detailedReportModal.data.ai_analysis.personality_analysis.personality_summary?.dominant_traits?.map(([trait, score]) => `${trait} (${Math.round(score * 100)}%)`).join(', ')}
                            </div>
                          </div>
                        )}

                        {/* Bias Detection Analysis */}
                        {detailedReportModal.data.ai_analysis.bias_detection && (
                          <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                            <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                              ⚖️ Bias Detection & Fairness Analysis
                            </h4>
                            <div className="grid md:grid-cols-2 gap-4">
                              <div className="bg-black/20 rounded-lg p-4">
                                <div className="text-sm text-gray-400 mb-2">Overall Bias Score</div>
                                <div className={`text-2xl font-bold ${detailedReportModal.data.ai_analysis.bias_detection.overall_bias_score > 0.2 ? 'text-red-400' : 'text-green-400'}`}>
                                  {Math.round(detailedReportModal.data.ai_analysis.bias_detection.overall_bias_score * 100)}%
                                </div>
                                <div className={`text-xs ${detailedReportModal.data.ai_analysis.bias_detection.is_biased ? 'text-red-300' : 'text-green-300'}`}>
                                  {detailedReportModal.data.ai_analysis.bias_detection.is_biased ? 'Bias Detected' : 'Fair Assessment'}
                                </div>
                              </div>
                              <div className="bg-black/20 rounded-lg p-4">
                                <div className="text-sm text-gray-400 mb-2">Fairness Metrics</div>
                                <div className="space-y-1 text-xs">
                                  <div className="flex justify-between">
                                    <span className="text-gray-300">Length Fairness:</span>
                                    <span className="text-blue-300">{Math.round((detailedReportModal.data.ai_analysis.bias_detection.fairness_metrics?.response_length_fairness || 1) * 100)}%</span>
                                  </div>
                                  <div className="flex justify-between">
                                    <span className="text-gray-300">Score Consistency:</span>
                                    <span className="text-green-300">{Math.round((detailedReportModal.data.ai_analysis.bias_detection.fairness_metrics?.score_consistency || 1) * 100)}%</span>
                                  </div>
                                  <div className="flex justify-between">
                                    <span className="text-gray-300">Cultural Sensitivity:</span>
                                    <span className="text-purple-300">{Math.round((detailedReportModal.data.ai_analysis.bias_detection.fairness_metrics?.cultural_sensitivity || 1) * 100)}%</span>
                                  </div>
                                </div>
                              </div>
                            </div>
                            {detailedReportModal.data.ai_analysis.bias_detection.bias_indicators?.length > 0 && (
                              <div className="mt-4 bg-yellow-900/20 border border-yellow-500/30 rounded-lg p-4">
                                <div className="text-sm font-semibold text-yellow-300 mb-2">⚠️ Bias Indicators Detected:</div>
                                <ul className="text-xs text-yellow-200 space-y-1">
                                  {detailedReportModal.data.ai_analysis.bias_detection.bias_indicators.map((indicator, index) => (
                                    <li key={index}>• {indicator}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                          </div>
                        )}

                        {/* Predictive Hiring Analysis */}
                        {detailedReportModal.data.ai_analysis.predictive_hiring && (
                          <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                            <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                              🎯 Predictive Hiring Analytics
                            </h4>
                            <div className="grid md:grid-cols-3 gap-4 mb-4">
                              <div className="bg-black/20 rounded-lg p-4 text-center">
                                <div className="text-sm text-gray-400 mb-1">Success Probability</div>
                                <div className="text-2xl font-bold text-green-400">
                                  {Math.round((detailedReportModal.data.ai_analysis.predictive_hiring.success_probability || 0) * 100)}%
                                </div>
                              </div>
                              <div className="bg-black/20 rounded-lg p-4 text-center">
                                <div className="text-sm text-gray-400 mb-1">Hiring Probability</div>
                                <div className="text-2xl font-bold text-blue-400">
                                  {Math.round((detailedReportModal.data.ai_analysis.predictive_hiring.hiring_probability || 0) * 100)}%
                                </div>
                              </div>
                              <div className="bg-black/20 rounded-lg p-4 text-center">
                                <div className="text-sm text-gray-400 mb-1">Growth Potential</div>
                                <div className="text-2xl font-bold text-purple-400">
                                  {Math.round(detailedReportModal.data.ai_analysis.predictive_hiring.growth_potential || 0)}%
                                </div>
                              </div>
                            </div>
                            <div className="bg-black/20 rounded-lg p-4">
                              <div className="text-sm text-gray-400 mb-2">Risk Assessment</div>
                              <div className="flex flex-wrap gap-2">
                                {Object.entries(detailedReportModal.data.ai_analysis.predictive_hiring.risk_factors || {}).map(([risk, hasRisk]) => (
                                  <span key={risk} className={`px-2 py-1 rounded text-xs ${hasRisk ? 'bg-red-900/30 text-red-300 border border-red-500/30' : 'bg-green-900/30 text-green-300 border border-green-500/30'}`}>
                                    {risk.replace(/_/g, ' ')}: {hasRisk ? 'High' : 'Low'}
                                  </span>
                                ))}
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Communication Analysis */}
                        {detailedReportModal.data.ai_analysis.communication_analysis && (
                          <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                            <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                              💬 Communication Analysis
                            </h4>
                            <div className="grid md:grid-cols-5 gap-3">
                              {Object.entries(detailedReportModal.data.ai_analysis.communication_analysis).map(([metric, score]) => (
                                <div key={metric} className="bg-black/20 rounded-lg p-3 text-center">
                                  <div className="text-xs text-gray-400 capitalize mb-1">{metric.replace(/_/g, ' ')}</div>
                                  <div className="text-lg font-bold text-cyan-400">{Math.round(score)}</div>
                                  <div className="w-full bg-gray-700 rounded-full h-1 mt-2">
                                    <div 
                                      className="bg-cyan-400 h-1 rounded-full" 
                                      style={{width: `${Math.min(100, score)}%`}}
                                    ></div>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Technical & Behavioral Analysis */}
                        <div className="grid md:grid-cols-2 gap-4">
                          {detailedReportModal.data.ai_analysis.technical_analysis && (
                            <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                              <h4 className="text-lg font-bold text-white mb-4 flex items-center">
                                ⚙️ Technical Analysis
                              </h4>
                              <div className="space-y-3 text-sm">
                                {Object.entries(detailedReportModal.data.ai_analysis.technical_analysis).filter(([key]) => key !== 'accuracy_breakdown').map(([key, value]) => (
                                  <div key={key} className="bg-black/20 rounded p-3">
                                    <div className="text-gray-400 capitalize text-xs mb-1">{key.replace(/_/g, ' ')}</div>
                                    <div className="text-gray-200">{value}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {detailedReportModal.data.ai_analysis.behavioral_analysis && (
                            <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                              <h4 className="text-lg font-bold text-white mb-4 flex items-center">
                                👥 Behavioral Analysis
                              </h4>
                              <div className="space-y-3 text-sm">
                                {Object.entries(detailedReportModal.data.ai_analysis.behavioral_analysis).filter(([key]) => key !== 'emotional_intelligence').map(([key, value]) => (
                                  <div key={key} className="bg-black/20 rounded p-3">
                                    <div className="text-gray-400 capitalize text-xs mb-1">{key.replace(/_/g, ' ')}</div>
                                    <div className="text-gray-200">{value}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>

                        {/* AI Recommendations */}
                        {detailedReportModal.data.ai_analysis.improvement_recommendations && (
                          <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                            <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                              💡 AI-Generated Recommendations
                            </h4>
                            <div className="grid md:grid-cols-2 gap-4">
                              <div className="bg-black/20 rounded-lg p-4">
                                <div className="text-sm font-semibold text-green-300 mb-2">✅ Strengths to Leverage</div>
                                <ul className="text-xs text-gray-300 space-y-1">
                                  {(detailedReportModal.data.ai_analysis.improvement_recommendations.strengths_to_leverage || []).map((strength, index) => (
                                    <li key={index}>• {strength}</li>
                                  ))}
                                </ul>
                              </div>
                              <div className="bg-black/20 rounded-lg p-4">
                                <div className="text-sm font-semibold text-orange-300 mb-2">🎯 Development Areas</div>
                                <ul className="text-xs text-gray-300 space-y-1">
                                  {(detailedReportModal.data.ai_analysis.improvement_recommendations.development_areas || []).map((area, index) => (
                                    <li key={index}>• {area}</li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                            <div className="mt-4 bg-blue-900/20 border border-blue-500/30 rounded-lg p-4">
                              <div className="text-sm font-semibold text-blue-300 mb-2">🚀 Immediate Actions</div>
                              <ul className="text-xs text-blue-200 space-y-1">
                                {(detailedReportModal.data.ai_analysis.improvement_recommendations.immediate_actions || []).map((action, index) => (
                                  <li key={index}>• {action}</li>
                                ))}
                              </ul>
                            </div>
                          </div>
                        )}

                        {/* Overall AI Assessment */}
                        {detailedReportModal.data.ai_analysis.overall_assessment && (
                          <div className="bg-gradient-to-r from-purple-900/30 to-blue-900/30 rounded-lg p-6 border border-purple-500/30">
                            <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                              🎯 Final AI Assessment
                            </h4>
                            <div className="grid md:grid-cols-3 gap-4 mb-4">
                              <div className="text-center">
                                <div className="text-sm text-gray-400">Hiring Recommendation</div>
                                <div className="text-lg font-bold text-purple-300">
                                  {detailedReportModal.data.ai_analysis.overall_assessment.hiring_recommendation}
                                </div>
                              </div>
                              <div className="text-center">
                                <div className="text-sm text-gray-400">Analysis Confidence</div>
                                <div className="text-lg font-bold text-blue-300">
                                  {Math.round((detailedReportModal.data.ai_analysis.overall_assessment.confidence_level || 0) * 100)}%
                                </div>
                              </div>
                              <div className="text-center">
                                <div className="text-sm text-gray-400">Analysis Date</div>
                                <div className="text-sm text-gray-300">
                                  {new Date(detailedReportModal.data.ai_analysis.analysis_timestamp).toLocaleString()}
                                </div>
                              </div>
                            </div>
                            <div className="grid md:grid-cols-2 gap-4">
                              <div className="bg-black/20 rounded-lg p-4">
                                <div className="text-sm font-semibold text-green-300 mb-2">💪 Key Strengths</div>
                                <ul className="text-xs text-gray-300 space-y-1">
                                  {(detailedReportModal.data.ai_analysis.overall_assessment.strengths || []).map((strength, index) => (
                                    <li key={index}>• {strength}</li>
                                  ))}
                                </ul>
                              </div>
                              <div className="bg-black/20 rounded-lg p-4">
                                <div className="text-sm font-semibold text-yellow-300 mb-2">📈 Development Areas</div>
                                <ul className="text-xs text-gray-300 space-y-1">
                                  {(detailedReportModal.data.ai_analysis.overall_assessment.areas_for_development || []).map((area, index) => (
                                    <li key={index}>• {area}</li>
                                  ))}
                                </ul>
                              </div>
                            </div>
                          </div>
                        )}
                      </>
                    )}

                    {/* Detailed Justification */}
                    <div className="bg-white/5 rounded-lg p-6 border border-white/10">
                      <h4 className="text-xl font-bold text-white mb-4 flex items-center">
                        ⚖️ Hiring Assessment & Justification
                      </h4>
                      <div className="bg-black/30 rounded-lg p-4">
                        <pre className="text-gray-100 whitespace-pre-wrap leading-relaxed text-sm">
                          {detailedReportModal.data.detailed_justification}
                        </pre>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="p-6 text-center">
                    <div className="text-red-400">❌ Failed to load detailed report</div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Phase 2: AI Screening & Shortlisting Tab */}
        {activeTab === 'screening' && (
          <div className="space-y-8">
            {/* Resume Upload Section */}
            <ResumeUploadSection 
              onUploadComplete={(resumes) => {
                setUploadedResumes(resumes);
                setSavedJobRequirements(null); // Reset job requirements when new resumes uploaded
                setScreeningComplete(false);
              }}
              disabled={false}
            />
            
            {/* Job Requirements Setup - Enabled after resume upload */}
            <JobRequirementsSetup 
              disabled={uploadedResumes.length === 0}
              uploadedResumes={uploadedResumes}
              onJobRequirementsSaved={(jobReq) => {
                setSavedJobRequirements(jobReq);
                setScreeningComplete(false);
              }}
            />
            
            {/* Screen Candidates Section - Enabled after job requirements saved */}
            <ScreenCandidatesSection 
              uploadedResumes={uploadedResumes}
              savedJobRequirements={savedJobRequirements}
              onScreeningComplete={(results) => {
                setScreeningResults(results);
                setScreeningComplete(true);
              }}
            />

            {/* Optional: Keep the existing bulk screening interface for advanced users */}
            {savedJobRequirements && uploadedResumes.length > 0 && (
              <div className="mt-8 p-4 bg-white/5 backdrop-blur-lg rounded-xl border border-white/10">
                <h3 className="text-lg font-bold text-white mb-4">🔧 Advanced Bulk Operations</h3>
                <BulkScreeningInterface 
                  candidatePipeline={candidatePipeline} 
                  refreshPipeline={fetchCandidatePipeline}
                />
              </div>
            )}
          </div>
        )}

        {/* Results Tab */}
        {activeTab === 'results' && (
          <ResultsComponent />
        )}
      </div>
    </div>
  );
};

// Placement Preparation Dashboard Component
const PlacementPreparationDashboard = ({ setCurrentPage }) => {
  const [activeTab, setActiveTab] = useState('create-interview');
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [jobRequirements, setJobRequirements] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [generatedToken, setGeneratedToken] = useState('');
  const [resumePreview, setResumePreview] = useState('');
  const [loading, setLoading] = useState(false);
  
  // Enhanced features state
  const [includeCodingChallenge, setIncludeCodingChallenge] = useState(false);
  const [roleArchetype, setRoleArchetype] = useState('General');
  const [interviewFocus, setInterviewFocus] = useState('Balanced');
  
  // Interview question limits
  const [minQuestions, setMinQuestions] = useState(8);
  const [maxQuestions, setMaxQuestions] = useState(12);
  
  // Question Selection Controls
  const [resumeBasedCount, setResumeBasedCount] = useState(2);
  const [technicalCount, setTechnicalCount] = useState(4);
  const [behavioralCount, setBehavioralCount] = useState(4);
  
  // Question Type Selection (auto-generate vs manual)
  const [resumeQuestionType, setResumeQuestionType] = useState('auto');
  const [technicalQuestionType, setTechnicalQuestionType] = useState('auto');
  const [behavioralQuestionType, setBehavioralQuestionType] = useState('auto');
  
  // Manual Questions Storage
  const [manualResumeQuestions, setManualResumeQuestions] = useState([]);
  const [manualTechnicalQuestions, setManualTechnicalQuestions] = useState([]);
  const [manualBehavioralQuestions, setManualBehavioralQuestions] = useState([]);

  const roleArchetypes = [
    'General',
    'Technical Lead',
    'Senior Developer',
    'Junior Developer',
    'Product Manager',
    'Data Scientist',
    'UI/UX Designer',
    'DevOps Engineer',
    'Marketing Manager',
    'Sales Representative'
  ];

  const interviewFocusOptions = [
    'Balanced',
    'Technical Heavy',
    'Behavioral Heavy',
    'Leadership Focused',
    'Problem Solving',
    'Communication Skills',
    'Industry Specific'
  ];

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setResumeFile(file);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('resume', file);

      const response = await fetch(`${API}/admin/upload`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResumePreview(data.preview);
      } else {
        const errorData = await response.json().catch(() => ({}));
        alert(`Failed to upload resume: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (err) {
      console.error('Upload error:', err);
      alert('Upload error: Please check your internet connection');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateInterview = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const payload = {
        job_title: jobTitle,
        job_description: jobDescription,
        job_requirements: jobRequirements,
        resume_text: resumePreview,
        include_coding_challenge: includeCodingChallenge,
        role_archetype: roleArchetype,
        interview_focus: interviewFocus,
        min_questions: minQuestions,
        max_questions: maxQuestions,
        question_distribution: {
          resume_based: resumeBasedCount,
          technical: technicalCount,
          behavioral: behavioralCount
        },
        question_types: {
          resume: resumeQuestionType,
          technical: technicalQuestionType,
          behavioral: behavioralQuestionType
        },
        manual_questions: {
          resume: manualResumeQuestions.filter(q => q.question.trim()),
          technical: manualTechnicalQuestions.filter(q => q.question.trim()),
          behavioral: manualBehavioralQuestions.filter(q => q.question.trim())
        }
      };

      const response = await fetch(`${API}/admin/create-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        const data = await response.json();
        setGeneratedToken(data.token);
      } else {
        const errorData = await response.json().catch(() => ({}));
        alert(`Failed to create interview token: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (err) {
      console.error('Error creating interview:', err);
      alert('Error creating interview: Please check your internet connection');
    } finally {
      setLoading(false);
    }
  };

  const addManualQuestion = (type) => {
    const newQuestion = { question: '', expected_answer: '' };
    
    switch(type) {
      case 'resume':
        setManualResumeQuestions([...manualResumeQuestions, newQuestion]);
        break;
      case 'technical':
        setManualTechnicalQuestions([...manualTechnicalQuestions, newQuestion]);
        break;
      case 'behavioral':
        setManualBehavioralQuestions([...manualBehavioralQuestions, newQuestion]);
        break;
    }
  };

  const updateManualQuestion = (type, index, field, value) => {
    switch(type) {
      case 'resume':
        const updatedResumeQuestions = [...manualResumeQuestions];
        updatedResumeQuestions[index][field] = value;
        setManualResumeQuestions(updatedResumeQuestions);
        break;
      case 'technical':
        const updatedTechnicalQuestions = [...manualTechnicalQuestions];
        updatedTechnicalQuestions[index][field] = value;
        setManualTechnicalQuestions(updatedTechnicalQuestions);
        break;
      case 'behavioral':
        const updatedBehavioralQuestions = [...manualBehavioralQuestions];
        updatedBehavioralQuestions[index][field] = value;
        setManualBehavioralQuestions(updatedBehavioralQuestions);
        break;
    }
  };

  const removeManualQuestion = (type, index) => {
    switch(type) {
      case 'resume':
        setManualResumeQuestions(manualResumeQuestions.filter((_, i) => i !== index));
        break;
      case 'technical':
        setManualTechnicalQuestions(manualTechnicalQuestions.filter((_, i) => i !== index));
        break;
      case 'behavioral':
        setManualBehavioralQuestions(manualBehavioralQuestions.filter((_, i) => i !== index));
        break;
    }
  };

  // Check if all required fields are filled
  const isFormValid = () => {
    return (
      jobTitle.trim() !== '' &&
      jobDescription.trim() !== '' &&
      jobRequirements.trim() !== '' &&
      resumeFile !== null &&
      resumePreview !== ''
    );
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Token copied to clipboard!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-white">📚 Placement Preparation</h1>
          <button
            onClick={() => setCurrentPage('landing')}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300"
          >
            Back to Home
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="mb-8">
          <nav className="flex space-x-1 bg-white/10 backdrop-blur-lg rounded-lg p-1">
            <button
              onClick={() => setActiveTab('create-interview')}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-md transition-all duration-300 ${
                activeTab === 'create-interview'
                  ? 'bg-orange-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              🚀 Create Interview
            </button>
          </nav>
        </div>

        {/* Create Interview Tab */}
        {activeTab === 'create-interview' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            {!generatedToken ? (
              <form onSubmit={handleCreateInterview} className="space-y-8">
                <div className="grid md:grid-cols-2 gap-8">
                  {/* Job Details */}
                  <div className="space-y-6">
                    <h2 className="text-2xl font-bold text-white mb-4">Job Details</h2>
                    
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Job Title
                      </label>
                      <input
                        type="text"
                        value={jobTitle}
                        onChange={(e) => setJobTitle(e.target.value)}
                        className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                        placeholder="e.g., Senior Frontend Developer"
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Job Description
                      </label>
                      <textarea
                        value={jobDescription}
                        onChange={(e) => setJobDescription(e.target.value)}
                        rows={4}
                        className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                        placeholder="Describe the role and responsibilities..."
                        required
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Job Requirements
                      </label>
                      <textarea
                        value={jobRequirements}
                        onChange={(e) => setJobRequirements(e.target.value)}
                        rows={4}
                        className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                        placeholder="List required skills, experience, qualifications..."
                        required
                      />
                    </div>
                  </div>

                  {/* Resume Upload */}
                  <div className="space-y-6">
                    <h2 className="text-2xl font-bold text-white mb-4">Resume Upload</h2>
                    
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Upload Resume (PDF, DOC, DOCX, TXT)
                      </label>
                      <input
                        type="file"
                        onChange={handleFileUpload}
                        accept=".pdf,.doc,.docx,.txt"
                        className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-orange-600 file:text-white hover:file:bg-orange-700"
                        required
                      />
                    </div>

                    {resumePreview && (
                      <div className="bg-white/5 rounded-lg p-4 shadow-lg border border-white/10">
                        <h3 className="text-lg font-semibold text-white mb-3">Resume Preview</h3>
                        <div className="bg-white/10 rounded-lg p-3 h-48 overflow-y-auto shadow-inner border border-white/20 scrollbar-thin scrollbar-track-transparent scrollbar-thumb-orange-500/50 hover:scrollbar-thumb-orange-500/70">
                          <p className="text-gray-200 text-sm whitespace-pre-wrap leading-relaxed">{resumePreview}</p>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Enhanced Configuration */}
                <div className="border-t border-white/20 pt-8">
                  <h2 className="text-2xl font-bold text-white mb-6">Interview Configuration</h2>
                  
                  <div className="grid md:grid-cols-3 gap-6 mb-6">
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Role Archetype
                      </label>
                      <select
                        value={roleArchetype}
                        onChange={(e) => setRoleArchetype(e.target.value)}
                        className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                      >
                        {roleArchetypes.map(role => (
                          <option key={role} value={role} className="bg-gray-800">{role}</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Interview Focus
                      </label>
                      <select
                        value={interviewFocus}
                        onChange={(e) => setInterviewFocus(e.target.value)}
                        className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                      >
                        {interviewFocusOptions.map(focus => (
                          <option key={focus} value={focus} className="bg-gray-800">{focus}</option>
                        ))}
                      </select>
                    </div>

                    <div className="flex items-center">
                      <label className="flex items-center text-white">
                        <input
                          type="checkbox"
                          checked={includeCodingChallenge}
                          onChange={(e) => setIncludeCodingChallenge(e.target.checked)}
                          className="mr-2 w-5 h-5 text-orange-600 bg-white/20 border-white/30 rounded focus:ring-orange-500"
                        />
                        Include Coding Challenge
                      </label>
                    </div>
                  </div>

                  {/* Question Configuration */}
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Total Questions Range
                      </label>
                      <div className="flex space-x-4">
                        <div className="flex-1">
                          <input
                            type="number"
                            value={minQuestions}
                            onChange={(e) => setMinQuestions(parseInt(e.target.value))}
                            min="6"
                            max="20"
                            className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                          />
                          <label className="block text-xs text-gray-300 mt-1">Min</label>
                        </div>
                        <div className="flex-1">
                          <input
                            type="number"
                            value={maxQuestions}
                            onChange={(e) => setMaxQuestions(parseInt(e.target.value))}
                            min="6"
                            max="20"
                            className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                          />
                          <label className="block text-xs text-gray-300 mt-1">Max</label>
                        </div>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-white mb-2">
                        Question Distribution
                      </label>
                      <div className="grid grid-cols-3 gap-2">
                        <div>
                          <input
                            type="number"
                            value={resumeBasedCount}
                            onChange={(e) => setResumeBasedCount(parseInt(e.target.value))}
                            min="0"
                            max="8"
                            className="w-full px-2 py-2 text-sm rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                          />
                          <label className="block text-xs text-gray-300 mt-1">Resume</label>
                        </div>
                        <div>
                          <input
                            type="number"
                            value={technicalCount}
                            onChange={(e) => setTechnicalCount(parseInt(e.target.value))}
                            min="0"
                            max="10"
                            className="w-full px-2 py-2 text-sm rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                          />
                          <label className="block text-xs text-gray-300 mt-1">Technical</label>
                        </div>
                        <div>
                          <input
                            type="number"
                            value={behavioralCount}
                            onChange={(e) => setBehavioralCount(parseInt(e.target.value))}
                            min="0"
                            max="8"
                            className="w-full px-2 py-2 text-sm rounded-lg bg-white/20 border border-white/30 text-white focus:outline-none focus:ring-2 focus:ring-orange-500"
                          />
                          <label className="block text-xs text-gray-300 mt-1">Behavioral</label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading || !isFormValid()}
                  className="w-full bg-gradient-to-r from-orange-600 to-red-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-orange-700 hover:to-red-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Creating...' : 'Create Interview Token'}
                </button>
              </form>
            ) : (
              <div className="text-center">
                <div className="mb-8">
                  <div className="w-24 h-24 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <h2 className="text-3xl font-bold text-white mb-4">Interview Token Created Successfully!</h2>
                  <div className="bg-white/10 rounded-xl p-6 mb-6">
                    <p className="text-xl text-white mb-4">Interview Token:</p>
                    <div className="bg-white/20 rounded-lg p-4 mb-4">
                      <code className="text-2xl font-mono text-green-400 break-all">{generatedToken}</code>
                    </div>
                    <button
                      onClick={() => copyToClipboard(generatedToken)}
                      className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300"
                    >
                      Copy Token
                    </button>
                  </div>
                  <p className="text-gray-300 mb-8">
                    Share this token with the candidate to begin their interview preparation session.
                  </p>
                  <button
                    onClick={() => {
                      setGeneratedToken('');
                      setJobTitle('');
                      setJobDescription('');
                      setJobRequirements('');
                      setResumeFile(null);
                      setResumePreview('');
                    }}
                    className="bg-gradient-to-r from-orange-600 to-red-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-orange-700 hover:to-red-700 transition-all duration-300"
                  >
                    Create Another Interview
                  </button>
                </div>
              </div>
            )}
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

  // Confirm and proceed to interview
  const confirmInterview = async () => {
    setLoading(true);
    try {
      // Store captured image data
      const interviewData = JSON.parse(localStorage.getItem('interviewData') || '{}');
      interviewData.capturedImage = capturedImage;
      localStorage.setItem('interviewData', JSON.stringify(interviewData));
      
      setCurrentPage('interview-session');
    } catch (error) {
      console.error('Error proceeding to interview:', error);
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

  // Voice recording - now handles transcribed text by populating the answer field
  const handleVoiceRecording = async (transcribedText) => {
    if (!transcribedText || transcribedText.trim() === '') {
      alert('No speech detected. Please try recording again.');
      return;
    }
    
    console.log('Voice recording completed with transcript:', transcribedText);
    
    // Populate the answer field with the transcribed text
    setUserAnswer(transcribedText.trim());
    
    // Show success message
    console.log('Transcript populated into answer field');
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

  // Add a processing state for when recording stops and is being processed
  const [isProcessingVoice, setIsProcessingVoice] = useState(false);
  const [isStoppingRecording, setIsStoppingRecording] = useState(false);

  // Enhance the voice recording handler to show processing state
  const enhancedHandleVoiceRecording = async (transcribedText) => {
    setIsProcessingVoice(true);
    try {
      await handleVoiceRecording(transcribedText);
    } finally {
      setIsProcessingVoice(false);
    }
  };

  // Voice recording hook with enhanced handler
  const { status: recordingStatus, startRecording, stopRecording: originalStopRecording, transcript, voiceLevel, isRecording } = useVoiceRecorder(enhancedHandleVoiceRecording);
  
  // Wrap stopRecording for instant UI feedback
  const stopRecording = () => {
    console.log('Button clicked - initiating instant stop');
    setIsStoppingRecording(true);
    
    // Call the optimized stop function immediately
    originalStopRecording();
    
    // Reset stopping state quickly
    setTimeout(() => {
      setIsStoppingRecording(false);
    }, 300);
  };

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
                  {/* Recording Button with Voice Level Indicator */}
                  <div className="relative">
                    <button
                      onClick={() => {
                        console.log('RED BUTTON CLICKED - Timestamp:', Date.now());
                        if (recordingStatus === 'recording') {
                          stopRecording();
                        } else {
                          startRecording();
                        }
                      }}
                      disabled={isAnswering || isProcessingVoice}
                      className={`w-20 h-20 rounded-full flex items-center justify-center text-white font-semibold transition-all duration-100 transform relative ${
                        recordingStatus === 'recording'
                          ? 'bg-red-600 hover:bg-red-700 animate-pulse scale-110'
                          : isStoppingRecording
                            ? 'bg-gray-600 scale-95' 
                            : 'bg-blue-600 hover:bg-blue-700 hover:scale-105'
                      } ${(isAnswering || isProcessingVoice) ? 'opacity-50 cursor-not-allowed' : ''}`}
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
                    
                    {/* Voice Level Ring Animation */}
                    {recordingStatus === 'recording' && (
                      <div 
                        className="absolute inset-0 rounded-full border-4 border-white/50 animate-ping"
                        style={{
                          transform: `scale(${1 + (voiceLevel / 100)})`,
                          opacity: Math.max(0.3, voiceLevel / 100)
                        }}
                      ></div>
                    )}
                  </div>

                  {/* Voice Level Meter */}
                  {recordingStatus === 'recording' && (
                    <div className="w-full max-w-xs bg-gray-700/50 rounded-full h-2 overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-green-400 via-yellow-400 to-red-400 transition-all duration-150"
                        style={{ width: `${Math.min(voiceLevel, 100)}%` }}
                      ></div>
                    </div>
                  )}

                  <p className="text-center text-gray-300 text-sm">
                    {isProcessingVoice 
                      ? '⚙️ Processing your voice answer...'
                      : !isRecording && !recordingStatus === 'recording'
                        ? '✅ Recording stopped'
                        : recordingStatus === 'recording' 
                          ? '🔴 Recording... Click the red button to stop' 
                          : '🎤 Click to record your answer'
                    }
                  </p>

                  {/* Live Transcript Preview */}
                  {recordingStatus === 'recording' && transcript && (
                    <div className="w-full bg-black/30 rounded-lg p-3 border border-white/20">
                      <p className="text-xs text-gray-400 mb-1">Live Transcript:</p>
                      <p className="text-sm text-white">{transcript}</p>
                    </div>
                  )}
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

// Main App Component with Phase 3 features
function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [isAdmin, setIsAdmin] = useState(false);
  const [token, setToken] = useState('');
  const [validatedJob, setValidatedJob] = useState(null);
  const [accessibilityOpen, setAccessibilityOpen] = useState(false);

  // Clear global spoken texts when starting new sessions
  useEffect(() => {
    if (currentPage === 'landing') {
      globalSpokenTexts.clear();
    }
  }, [currentPage]);

  const renderPage = () => {
    switch (currentPage) {
      case 'admin-login':
        return <AdminLogin setCurrentPage={setCurrentPage} setIsAdmin={setIsAdmin} />;
      case 'admin-dashboard':
        return <AdminDashboard setCurrentPage={setCurrentPage} />;
      case 'placement-preparation':
        return <PlacementPreparationDashboard setCurrentPage={setCurrentPage} />;
      case 'candidate-login':
        return <CandidateLogin setCurrentPage={setCurrentPage} setToken={setToken} setValidatedJob={setValidatedJob} />;
      case 'interview-start':
        return <InterviewStart setCurrentPage={setCurrentPage} token={token} validatedJob={validatedJob} />;
      case 'capture-image':
        return <CaptureImage setCurrentPage={setCurrentPage} token={token} validatedJob={validatedJob} />;
      case 'interview-session':
        return <InterviewSession setCurrentPage={setCurrentPage} />;
      default:
        return <EnhancedLandingPage setCurrentPage={setCurrentPage} />;
    }
  };

  return (
    <PWAProvider>
      <I18nProvider>
        <AccessibilityProvider>
          <div className="App">
            {/* Top Navigation with Language and Accessibility */}
            <nav className="fixed top-4 right-4 z-40 flex items-center gap-4">
              <LanguageSelector />
            </nav>

            {/* PWA Banners */}
            <InstallBanner />
            <UpdateBanner />
            <OfflineBanner />

            {/* Main Content */}
            <main id="main-content" role="main" className="min-h-screen">
              {renderPage()}
            </main>

            {/* Accessibility Controls */}
            <AccessibilityControls 
              isOpen={accessibilityOpen} 
              onClose={() => setAccessibilityOpen(false)} 
            />
            <AccessibilityButton 
              onClick={() => setAccessibilityOpen(!accessibilityOpen)}
              isOpen={accessibilityOpen}
            />
          </div>
        </AccessibilityProvider>
      </I18nProvider>
    </PWAProvider>
  );
}

export default App;