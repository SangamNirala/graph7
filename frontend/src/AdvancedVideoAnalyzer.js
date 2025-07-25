import React, { useRef, useEffect, useState } from 'react';

const AdvancedVideoAnalyzer = ({ sessionId, onAnalysisUpdate, isRecording = false, isPreview = false }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentAnalysis, setCurrentAnalysis] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isRecording) {
      startVideoAnalysis();
    } else {
      stopVideoAnalysis();
    }

    return () => stopVideoAnalysis();
  }, [isRecording]);

  const startVideoAnalysis = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: { 
          width: isPreview ? 320 : 640, 
          height: isPreview ? 240 : 480,
          facingMode: 'user' // Front-facing camera
        },
        audio: false 
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsAnalyzing(true);
        if (!isPreview) {
          startFrameAnalysis();
        }
      }
    } catch (err) {
      setError('Failed to access camera: ' + err.message);
      console.error('Camera access error:', err);
    }
  };

  const stopVideoAnalysis = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setIsAnalyzing(false);
  };

  const startFrameAnalysis = () => {
    const analyzeFrame = async () => {
      if (!isAnalyzing || !videoRef.current || !canvasRef.current) return;

      try {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        
        // Set canvas size to match video
        canvas.width = videoRef.current.videoWidth || 640;
        canvas.height = videoRef.current.videoHeight || 480;
        
        // Draw current video frame to canvas
        context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
        
        // Convert canvas to base64
        const frameData = canvas.toDataURL('image/jpeg', 0.8);
        
        // Send frame for analysis
        const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/analysis/video-frame`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            frame_data: frameData,
            session_id: sessionId
          }),
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
        console.error('Frame analysis error:', err);
      }

      // Continue analysis every 2 seconds during interview
      if (isAnalyzing) {
        setTimeout(analyzeFrame, 2000);
      }
    };

    // Start analysis after video is loaded
    if (videoRef.current.readyState >= 2) {
      setTimeout(analyzeFrame, 1000);
    } else {
      videoRef.current.addEventListener('loadeddata', () => {
        setTimeout(analyzeFrame, 1000);
      });
    }
  };

  return (
    <div className="advanced-video-analyzer">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="relative">
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className="w-full max-w-md rounded-lg shadow-lg"
          style={{ display: isAnalyzing ? 'block' : 'none' }}
        />
        <canvas
          ref={canvasRef}
          className="hidden"
        />
        
        {/* Analysis Overlay */}
        {currentAnalysis && (
          <div className="absolute top-4 right-4 bg-black bg-opacity-70 text-white p-3 rounded-lg text-sm">
            <div className="space-y-1">
              <div>Engagement: {Math.round(currentAnalysis.engagement_score * 100)}%</div>
              <div>Attention: {Math.round(currentAnalysis.attention_level * 100)}%</div>
              <div>Eye Contact: {Math.round(currentAnalysis.eye_contact_score * 100)}%</div>
              {currentAnalysis.emotions && currentAnalysis.emotions.length > 0 && (
                <div>Mood: {currentAnalysis.emotions[0].emotion}</div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Real-time Metrics Dashboard */}
      {currentAnalysis && (
        <div className="mt-4 grid grid-cols-2 gap-4">
          <div className="bg-gradient-to-r from-blue-50 to-blue-100 p-4 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-2">Engagement Metrics</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">Overall Engagement</span>
                <span className="font-medium">{Math.round(currentAnalysis.engagement_score * 100)}%</span>
              </div>
              <div className="w-full bg-blue-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${currentAnalysis.engagement_score * 100}%` }}
                ></div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-green-50 to-green-100 p-4 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">Attention Level</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">Focus Score</span>
                <span className="font-medium">{Math.round(currentAnalysis.attention_level * 100)}%</span>
              </div>
              <div className="w-full bg-green-200 rounded-full h-2">
                <div 
                  className="bg-green-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${currentAnalysis.attention_level * 100}%` }}
                ></div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-r from-purple-50 to-purple-100 p-4 rounded-lg">
            <h4 className="font-semibold text-purple-800 mb-2">Emotional State</h4>
            {currentAnalysis.emotions && currentAnalysis.emotions.length > 0 ? (
              <div className="space-y-1">
                {currentAnalysis.emotions.slice(0, 3).map((emotion, index) => (
                  <div key={index} className="flex justify-between text-sm">
                    <span className="capitalize">{emotion.emotion}</span>
                    <span>{Math.round(emotion.confidence * 100)}%</span>
                  </div>
                ))}
              </div>
            ) : (
              <span className="text-sm text-gray-600">Analyzing...</span>
            )}
          </div>

          <div className="bg-gradient-to-r from-orange-50 to-orange-100 p-4 rounded-lg">
            <h4 className="font-semibold text-orange-800 mb-2">Stress Indicators</h4>
            <div className="space-y-1">
              {currentAnalysis.stress_indicators && (
                <>
                  <div className="flex justify-between text-sm">
                    <span>Overall Stress</span>
                    <span>{Math.round(currentAnalysis.stress_indicators.overall_stress * 100)}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Eye Strain</span>
                    <span>{Math.round(currentAnalysis.stress_indicators.eye_strain * 100)}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Tension</span>
                    <span>{Math.round(currentAnalysis.stress_indicators.eyebrow_tension * 100)}%</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Status Indicator */}
      <div className="mt-4 flex items-center justify-center space-x-2">
        {isAnalyzing && (
          <>
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-600">Real-time analysis active</span>
          </>
        )}
      </div>
    </div>
  );
};

export default AdvancedVideoAnalyzer;