import React, { useState, useRef, useEffect } from 'react';
import { ReactMediaRecorder } from 'react-media-recorder';

const AdvancedAudioAnalyzer = ({ sessionId, onAnalysisUpdate, isRecording = false }) => {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const audioChunks = useRef([]);
  const mediaRecorderRef = useRef(null);

  useEffect(() => {
    if (isRecording && !isAnalyzing) {
      startAudioAnalysis();
    } else if (!isRecording && isAnalyzing) {
      stopAudioAnalysis();
    }
  }, [isRecording]);

  const startAudioAnalysis = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });

      mediaRecorderRef.current = mediaRecorder;
      audioChunks.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.current.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/webm' });
        await analyzeAudioChunk(audioBlob);
      };

      // Record in 5-second chunks for analysis
      mediaRecorder.start();
      setIsAnalyzing(true);

      // Schedule periodic analysis
      schedulePeriodicAnalysis();

    } catch (err) {
      setError('Failed to access microphone: ' + err.message);
    }
  };

  const stopAudioAnalysis = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      const tracks = mediaRecorderRef.current.stream.getTracks();
      tracks.forEach(track => track.stop());
    }
    setIsAnalyzing(false);
  };

  const schedulePeriodicAnalysis = () => {
    if (!isAnalyzing) return;

    setTimeout(() => {
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
        mediaRecorderRef.current.stop();
        
        // Restart recording for next chunk
        setTimeout(() => {
          if (isAnalyzing) {
            audioChunks.current = [];
            mediaRecorderRef.current.start();
            schedulePeriodicAnalysis();
          }
        }, 500);
      }
    }, 5000); // Analyze every 5 seconds
  };

  const analyzeAudioChunk = async (audioBlob) => {
    try {
      const formData = new FormData();
      formData.append('audio_file', audioBlob, 'audio_chunk.webm');
      formData.append('session_id', sessionId);

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/analysis/audio-stream`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        if (result.analysis) {
          setCurrentAnalysis(result.analysis);
          if (onAnalysisUpdate) {
            onAnalysisUpdate(result.analysis);
          }
        }
      }
    } catch (err) {
      console.error('Audio analysis error:', err);
    }
  };

  const getSpeakingRateColor = (rate) => {
    if (rate >= 140 && rate <= 180) return 'text-green-600';
    if (rate >= 120 && rate <= 200) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.7) return 'text-green-600';
    if (confidence >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="advanced-audio-analyzer">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Real-time Audio Metrics */}
      {currentAnalysis && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Speech Quality Metrics */}
          <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-6 rounded-lg">
            <h3 className="font-bold text-blue-800 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
              </svg>
              Speech Quality
            </h3>
            
            <div className="space-y-3">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium">Confidence Level</span>
                  <span className={`font-semibold ${getConfidenceColor(currentAnalysis.speech_metrics?.confidence_level)}`}>
                    {Math.round((currentAnalysis.speech_metrics?.confidence_level || 0) * 100)}%
                  </span>
                </div>
                <div className="w-full bg-blue-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(currentAnalysis.speech_metrics?.confidence_level || 0) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium">Voice Quality</span>
                  <span className="font-semibold">
                    {Math.round((currentAnalysis.speech_metrics?.voice_quality || 0) * 100)}%
                  </span>
                </div>
                <div className="w-full bg-blue-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(currentAnalysis.speech_metrics?.voice_quality || 0) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-600">Speaking Rate</span>
                  <div className={`font-semibold ${getSpeakingRateColor(currentAnalysis.speech_metrics?.speaking_rate || 0)}`}>
                    {Math.round(currentAnalysis.speech_metrics?.speaking_rate || 0)} WPM
                  </div>
                </div>
                <div>
                  <span className="text-gray-600">Pitch</span>
                  <div className="font-semibold">
                    {Math.round(currentAnalysis.speech_metrics?.pitch_mean || 0)} Hz
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Communication Analysis */}
          <div className="bg-gradient-to-r from-green-50 to-green-100 p-6 rounded-lg">
            <h3 className="font-bold text-green-800 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" />
                <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
              </svg>
              Communication
            </h3>

            <div className="space-y-3">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium">Fluency Score</span>
                  <span className="font-semibold text-green-600">
                    {Math.round((currentAnalysis.fluency_score || 0) * 100)}%
                  </span>
                </div>
                <div className="w-full bg-green-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(currentAnalysis.fluency_score || 0) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium">Clarity Score</span>
                  <span className="font-semibold text-green-600">
                    {Math.round((currentAnalysis.clarity_score || 0) * 100)}%
                  </span>
                </div>
                <div className="w-full bg-green-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(currentAnalysis.clarity_score || 0) * 100}%` }}
                  ></div>
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-sm font-medium">Overall Quality</span>
                  <span className="font-semibold text-green-600">
                    {Math.round((currentAnalysis.overall_quality || 0) * 100)}%
                  </span>
                </div>
                <div className="w-full bg-green-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(currentAnalysis.overall_quality || 0) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Emotional Tone Analysis */}
          <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-6 rounded-lg">
            <h3 className="font-bold text-purple-800 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9a1 1 0 100-2 1 1 0 000 2zm7-1a1 1 0 11-2 0 1 1 0 012 0zm-.464 5.535a1 1 0 10-1.415-1.414 3 3 0 01-4.242 0 1 1 0 00-1.415 1.414 5 5 0 007.072 0z" clipRule="evenodd" />
              </svg>
              Emotional Tone
            </h3>

            {currentAnalysis.emotional_tones && currentAnalysis.emotional_tones.length > 0 ? (
              <div className="space-y-2">
                {currentAnalysis.emotional_tones.slice(0, 3).map((tone, index) => (
                  <div key={index} className="flex justify-between items-center">
                    <span className="capitalize text-sm font-medium">{tone.emotion}</span>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm">{Math.round(tone.confidence * 100)}%</span>
                      <div className="w-16 bg-purple-200 rounded-full h-2">
                        <div 
                          className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${tone.confidence * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <span className="text-sm text-gray-600">Analyzing emotional tone...</span>
            )}
          </div>

          {/* Stress Indicators */}
          <div className="bg-gradient-to-r from-orange-50 to-orange-100 p-6 rounded-lg">
            <h3 className="font-bold text-orange-800 mb-4 flex items-center">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              Stress Analysis
            </h3>

            {currentAnalysis.stress_indicators && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Overall Stress</span>
                  <span className="font-semibold">
                    {Math.round(currentAnalysis.stress_indicators.overall_stress * 100)}%
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Vocal Tension</span>
                  <span>{Math.round(currentAnalysis.stress_indicators.vocal_tension * 100)}%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Speaking Anxiety</span>
                  <span>{Math.round(currentAnalysis.stress_indicators.speaking_anxiety * 100)}%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Hesitation</span>
                  <span>{Math.round(currentAnalysis.stress_indicators.hesitation * 100)}%</span>
                </div>

                {/* Overall Stress Level Indicator */}
                <div className="mt-3">
                  <div className="w-full bg-orange-200 rounded-full h-3">
                    <div 
                      className={`h-3 rounded-full transition-all duration-300 ${
                        currentAnalysis.stress_indicators.overall_stress < 0.3 
                          ? 'bg-green-500' 
                          : currentAnalysis.stress_indicators.overall_stress < 0.6 
                          ? 'bg-yellow-500' 
                          : 'bg-red-500'
                      }`}
                      style={{ width: `${currentAnalysis.stress_indicators.overall_stress * 100}%` }}
                    ></div>
                  </div>
                  <div className="text-xs text-center mt-1">
                    {currentAnalysis.stress_indicators.overall_stress < 0.3 ? 'Low Stress' :
                     currentAnalysis.stress_indicators.overall_stress < 0.6 ? 'Normal' : 'High Stress'}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Status Indicator */}
      <div className="flex items-center justify-center space-x-2 mt-4">
        {isAnalyzing && (
          <>
            <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600">Audio analysis active</span>
          </>
        )}
      </div>

      {/* Quick Insights */}
      {currentAnalysis && (
        <div className="mt-4 bg-gradient-to-r from-gray-50 to-gray-100 p-4 rounded-lg">
          <h4 className="font-semibold text-gray-800 mb-2">Quick Insights</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {Math.round((currentAnalysis.speech_metrics?.confidence_level || 0) * 100)}%
              </div>
              <div className="text-gray-600">Confidence</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {Math.round((currentAnalysis.fluency_score || 0) * 100)}%
              </div>
              <div className="text-gray-600">Fluency</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {currentAnalysis.emotional_tones && currentAnalysis.emotional_tones.length > 0 
                  ? currentAnalysis.emotional_tones[0].emotion 
                  : 'Neutral'}
              </div>
              <div className="text-gray-600">Dominant Emotion</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedAudioAnalyzer;