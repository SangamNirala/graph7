import React, { useState, useEffect } from 'react';

const InterviewAnalyticsDashboard = ({ sessionId }) => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (sessionId) {
      fetchSessionInsights();
      // Refresh insights every 30 seconds during interview
      const interval = setInterval(fetchSessionInsights, 30000);
      return () => clearInterval(interval);
    }
  }, [sessionId]);

  const fetchSessionInsights = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/analysis/session-insights/${sessionId}`);
      
      if (response.ok) {
        const data = await response.json();
        setInsights(data);
        setError(null);
      } else {
        throw new Error('Failed to fetch insights');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !insights) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error && !insights) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <strong>Error:</strong> {error}
      </div>
    );
  }

  if (!insights) {
    return (
      <div className="text-center py-8 text-gray-500">
        No analysis data available yet. Start your interview to see real-time insights.
      </div>
    );
  }

  const getScoreColor = (score) => {
    if (score >= 0.7) return 'text-green-600';
    if (score >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getPerformanceIndicator = (score) => {
    if (score >= 0.8) return { text: 'Excellent', color: 'bg-green-500' };
    if (score >= 0.6) return { text: 'Good', color: 'bg-blue-500' };
    if (score >= 0.4) return { text: 'Moderate', color: 'bg-yellow-500' };
    return { text: 'Needs Improvement', color: 'bg-red-500' };
  };

  return (
    <div className="interview-analytics-dashboard space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-lg">
        <h2 className="text-2xl font-bold mb-2">Interview Analytics Dashboard</h2>
        <p className="text-blue-100">Real-time analysis of candidate performance</p>
        <div className="mt-4 grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold">{insights.analysis_count?.video_frames || 0}</div>
            <div className="text-sm text-blue-100">Video Frames</div>
          </div>
          <div>
            <div className="text-2xl font-bold">{insights.analysis_count?.audio_clips || 0}</div>
            <div className="text-sm text-blue-100">Audio Clips</div>
          </div>
          <div>
            <div className="text-2xl font-bold">
              {insights.combined_insights?.overall_performance === 'excellent' ? '🏆' :
               insights.combined_insights?.overall_performance === 'good' ? '👍' :
               insights.combined_insights?.overall_performance === 'moderate' ? '👌' : '⚠️'}
            </div>
            <div className="text-sm text-blue-100 capitalize">
              {insights.combined_insights?.overall_performance?.replace('_', ' ') || 'Analyzing'}
            </div>
          </div>
        </div>
      </div>

      {/* Video Metrics */}
      {insights.video_metrics && Object.keys(insights.video_metrics).length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
            </svg>
            Video Analysis Metrics
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className={`text-3xl font-bold ${getScoreColor(insights.video_metrics.average_engagement)}`}>
                {Math.round(insights.video_metrics.average_engagement * 100)}%
              </div>
              <div className="text-sm text-gray-600 mt-1">Engagement Level</div>
              <div className="w-full bg-blue-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${insights.video_metrics.average_engagement * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className={`text-3xl font-bold ${getScoreColor(insights.video_metrics.average_attention)}`}>
                {Math.round(insights.video_metrics.average_attention * 100)}%
              </div>
              <div className="text-sm text-gray-600 mt-1">Attention Score</div>
              <div className="w-full bg-green-200 rounded-full h-2 mt-2">
                <div 
                  className="bg-green-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${insights.video_metrics.average_attention * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className={`text-3xl font-bold ${
                insights.video_metrics.average_stress < 0.3 ? 'text-green-600' :
                insights.video_metrics.average_stress < 0.6 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {Math.round((1 - insights.video_metrics.average_stress) * 100)}%
              </div>
              <div className="text-sm text-gray-600 mt-1">Calmness Level</div>
              <div className="w-full bg-orange-200 rounded-full h-2 mt-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-300 ${
                    insights.video_metrics.average_stress < 0.3 ? 'bg-green-500' :
                    insights.video_metrics.average_stress < 0.6 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${(1 - insights.video_metrics.average_stress) * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-lg font-bold text-purple-600">
                {insights.video_metrics.dominant_emotions && 
                 Object.keys(insights.video_metrics.dominant_emotions).length > 0
                  ? Object.entries(insights.video_metrics.dominant_emotions)
                      .sort((a, b) => b[1] - a[1])[0][0]
                  : 'Neutral'}
              </div>
              <div className="text-sm text-gray-600 mt-1">Dominant Emotion</div>
              {insights.video_metrics.dominant_emotions && (
                <div className="text-xs text-purple-600 mt-2">
                  {Math.round(Object.entries(insights.video_metrics.dominant_emotions)
                    .sort((a, b) => b[1] - a[1])[0]?.[1] * 100)}% confidence
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Audio Metrics */}
      {insights.audio_metrics && Object.keys(insights.audio_metrics).length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2 text-green-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
            </svg>
            Audio Analysis Metrics
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className={`text-2xl font-bold ${getScoreColor(insights.audio_metrics.average_confidence)}`}>
                {Math.round(insights.audio_metrics.average_confidence * 100)}%
              </div>
              <div className="text-sm text-gray-600 mt-1">Confidence</div>
            </div>

            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className={`text-2xl font-bold ${getScoreColor(insights.audio_metrics.average_fluency)}`}>
                {Math.round(insights.audio_metrics.average_fluency * 100)}%
              </div>
              <div className="text-sm text-gray-600 mt-1">Fluency</div>
            </div>

            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className={`text-2xl font-bold ${getScoreColor(insights.audio_metrics.average_clarity)}`}>
                {Math.round(insights.audio_metrics.average_clarity * 100)}%
              </div>
              <div className="text-sm text-gray-600 mt-1">Clarity</div>
            </div>

            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <div className="text-2xl font-bold text-yellow-600">
                {Math.round(insights.audio_metrics.average_speaking_rate)} WPM
              </div>
              <div className="text-sm text-gray-600 mt-1">Speaking Rate</div>
            </div>

            <div className="text-center p-4 bg-indigo-50 rounded-lg">
              <div className={`text-2xl font-bold ${getScoreColor(insights.audio_metrics.average_quality)}`}>
                {Math.round(insights.audio_metrics.average_quality * 100)}%
              </div>
              <div className="text-sm text-gray-600 mt-1">Overall Quality</div>
            </div>
          </div>
        </div>
      )}

      {/* Combined Insights */}
      {insights.combined_insights && (
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 p-6 rounded-lg">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2 text-indigo-600" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            AI-Powered Insights
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Performance Overview */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-3">Performance Assessment</h4>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm">Overall Performance</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    getPerformanceIndicator(
                      insights.combined_insights.overall_performance === 'excellent' ? 0.9 :
                      insights.combined_insights.overall_performance === 'good' ? 0.7 :
                      insights.combined_insights.overall_performance === 'moderate' ? 0.5 : 0.3
                    ).color} text-white`}>
                    {insights.combined_insights.overall_performance?.replace('_', ' ').toUpperCase()}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm">Confidence Level</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    insights.combined_insights.confidence_assessment === 'high' ? 'bg-green-500' :
                    insights.combined_insights.confidence_assessment === 'moderate' ? 'bg-yellow-500' : 'bg-red-500'
                  } text-white`}>
                    {insights.combined_insights.confidence_assessment?.toUpperCase()}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm">Stress Level</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    insights.combined_insights.stress_level === 'low' ? 'bg-green-500' :
                    insights.combined_insights.stress_level === 'normal' ? 'bg-blue-500' : 'bg-orange-500'
                  } text-white`}>
                    {insights.combined_insights.stress_level?.toUpperCase()}
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm">Engagement</span>
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    insights.combined_insights.engagement_level === 'high' ? 'bg-green-500' :
                    insights.combined_insights.engagement_level === 'moderate' ? 'bg-yellow-500' : 'bg-red-500'
                  } text-white`}>
                    {insights.combined_insights.engagement_level?.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>

            {/* Strengths and Areas for Improvement */}
            <div>
              <h4 className="font-semibold text-gray-700 mb-3">Feedback Summary</h4>
              
              {insights.combined_insights.key_strengths?.length > 0 && (
                <div className="mb-4">
                  <h5 className="text-sm font-medium text-green-700 mb-2">Key Strengths:</h5>
                  <ul className="space-y-1">
                    {insights.combined_insights.key_strengths.map((strength, index) => (
                      <li key={index} className="text-sm text-green-600 flex items-start">
                        <svg className="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        {strength}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {insights.combined_insights.areas_for_improvement?.length > 0 && (
                <div>
                  <h5 className="text-sm font-medium text-orange-700 mb-2">Areas for Improvement:</h5>
                  <ul className="space-y-1">
                    {insights.combined_insights.areas_for_improvement.map((area, index) => (
                      <li key={index} className="text-sm text-orange-600 flex items-start">
                        <svg className="w-4 h-4 mr-1 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                        {area}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Real-time Updates Indicator */}
      <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
        <svg className="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span>Updates every 30 seconds</span>
      </div>
    </div>
  );
};

export default InterviewAnalyticsDashboard;