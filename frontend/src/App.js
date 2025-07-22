import React, { useState, useEffect, useRef } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

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
                />
              </div>

              <div>
                <label className="block text-white font-medium mb-2">
                  Candidate Resume (PDF, Word, or TXT file)
                </label>
                <div className="bg-blue-600/20 border border-blue-500/30 rounded-lg p-3 mb-2">
                  <p className="text-blue-200 text-sm">
                    ✅ <strong>Supported formats:</strong> PDF, DOC, DOCX, TXT files
                  </p>
                </div>
                <input
                  type="file"
                  accept=".pdf,.doc,.docx,.txt"
                  onChange={handleFileChange}
                  className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-600 file:text-white hover:file:bg-blue-700"
                  required
                />
                {resumeFile && (
                  <div className="mt-2 text-sm text-green-200">
                    📎 Selected: {resumeFile.name} ({(resumeFile.size / 1024).toFixed(1)} KB)
                  </div>
                )}
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50"
              >
                {loading ? 'Processing Resume & Generating Token...' : 'Generate Interview Token'}
              </button>
            </form>

            {generatedToken && (
              <div className="mt-8 space-y-4">
                <div className="p-6 bg-green-600/20 border border-green-500/30 rounded-lg">
                  <h3 className="text-xl font-bold text-green-200 mb-2">✅ Token Generated Successfully!</h3>
                  <div className="bg-black/30 rounded-lg p-4 font-mono text-lg text-green-200">
                    {generatedToken}
                  </div>
                  <p className="text-green-200 mt-2 text-sm">
                    🎤 Provide this token to the candidate to start their voice interview.
                  </p>
                </div>
                
                {resumePreview && (
                  <div className="p-6 bg-blue-600/20 border border-blue-500/30 rounded-lg">
                    <h3 className="text-xl font-bold text-blue-200 mb-2">📄 Resume Preview</h3>
                    <div className="bg-black/30 rounded-lg p-4 text-sm text-blue-200 max-h-32 overflow-y-auto">
                      {resumePreview}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Reports Tab */}
        {activeTab === 'reports' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6">🎤 Voice Interview Reports</h2>
            
            <div className="space-y-4">
              {reports.length === 0 ? (
                <p className="text-gray-300 text-center py-8">No voice interview reports available yet.</p>
              ) : (
                reports.map((report) => (
                  <div key={report.id} className="bg-white/10 rounded-lg p-6 border border-white/20">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-bold text-white flex items-center">
                          🎤 {report.candidate_name}
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
                      </div>
                    </div>
                    
                    <div className="grid md:grid-cols-2 gap-4 mb-4">
                      <div>
                        <div className="text-sm text-gray-300">Technical Score</div>
                        <div className="text-2xl font-bold text-blue-400">
                          {report.technical_score}/100
                        </div>
                      </div>
                      <div>
                        <div className="text-sm text-gray-300">Behavioral Score</div>
                        <div className="text-2xl font-bold text-green-400">
                          {report.behavioral_score}/100
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-sm text-gray-300">
                      <strong>Overall Feedback:</strong>
                      <p className="mt-1 text-white">{report.overall_feedback}</p>
                    </div>
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
        setCurrentPage('interview-session');
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

// Interview Session Component
const InterviewSession = ({ setCurrentPage }) => {
  const [messages, setMessages] = useState([]);
  const [currentAnswer, setCurrentAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [interviewData, setInterviewData] = useState(null);
  const [completed, setCompleted] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const messagesEndRef = useRef(null);

  const handleRecordingComplete = async (audioBlob) => {
    if (!audioBlob) return;

    try {
      // Send audio to backend for processing
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
        // Use the transcribed text as the answer
        handleSendMessage(data.transcript);
      } else {
        console.error('Voice processing failed');
      }
    } catch (err) {
      console.error('Failed to process voice answer:', err);
    }
  };

  const { status, startRecording, stopRecording, mediaBlobUrl } = useVoiceRecorder(handleRecordingComplete);

  useEffect(() => {
    const savedData = localStorage.getItem('interviewData');
    if (savedData) {
      const data = JSON.parse(savedData);
      setInterviewData(data);
      
      const initialMessages = [
        {
          type: 'ai',
          content: `Welcome ${data.candidateName}! I'm your AI interviewer today.`,
          timestamp: new Date().toLocaleTimeString(),
          audio: data.welcomeAudio
        },
        {
          type: 'ai',
          content: data.currentQuestion,
          timestamp: new Date().toLocaleTimeString(),
          questionNumber: data.questionNumber,
          audio: data.questionAudio
        }
      ];
      
      setMessages(initialMessages);
    }
  }, []);

  const handleSendMessage = async (messageText = currentAnswer) => {
    if (!messageText.trim() || loading) return;

    setLoading(true);

    const userMessage = {
      type: 'user',
      content: messageText,
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await fetch(`${API}/candidate/send-message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          token: interviewData.token, 
          message: messageText 
        }),
      });

      if (response.ok) {
        const data = await response.json();
        
        if (data.completed) {
          setCompleted(true);
          setMessages(prev => [...prev, {
            type: 'ai',
            content: data.message,
            timestamp: new Date().toLocaleTimeString()
          }]);
        } else {
          const aiMessage = {
            type: 'ai',
            content: data.next_question,
            timestamp: new Date().toLocaleTimeString(),
            questionNumber: data.question_number,
            audio: data.question_audio
          };
          
          setMessages(prev => [...prev, aiMessage]);
          
          setInterviewData(prev => ({
            ...prev,
            questionNumber: data.question_number,
            totalQuestions: data.total_questions
          }));
        }
      }
    } catch (err) {
      console.error('Failed to send message:', err);
    } finally {
      setCurrentAnswer('');
      setLoading(false);
    }
  };

  const handleVoiceAnswer = () => {
    if (status === 'recording') {
      stopRecording();
      setIsRecording(false);
    } else {
      startRecording();
      setIsRecording(true);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (!interviewData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 flex items-center justify-center">
        <div className="text-white text-xl">Loading interview...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center">
                🎤 {interviewData.candidateName}
              </h1>
              <p className="text-gray-300">{interviewData.jobTitle}</p>
            </div>
            <div className="text-right">
              {!completed && (
                <div className="text-sm text-gray-300">
                  Question {interviewData.questionNumber} of {interviewData.totalQuestions}
                </div>
              )}
              <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${
                completed 
                  ? 'bg-green-600/20 text-green-200 border border-green-500/30'
                  : 'bg-blue-600/20 text-blue-200 border border-blue-500/30'
              }`}>
                {completed ? '✅ Completed' : '🎤 Recording'}
              </div>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 mb-6" style={{ minHeight: '400px', maxHeight: '500px', overflowY: 'auto' }}>
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] rounded-lg p-4 ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white/20 text-white border border-white/30'
                }`}>
                  {message.questionNumber && (
                    <div className="text-xs text-gray-300 mb-2">🎤 Question {message.questionNumber}</div>
                  )}
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  {message.audio && interviewData.voiceMode && (
                    <div className="mt-3">
                      <AudioPlayer audioBase64={message.audio} autoPlay={true} />
                    </div>
                  )}
                  <div className="text-xs opacity-70 mt-2">{message.timestamp}</div>
                </div>
              </div>
            ))}
          </div>
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        {!completed && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
            {interviewData.voiceMode ? (
              /* Voice Mode UI */
              <div className="space-y-4">
                <div className="text-center">
                  <button
                    onClick={handleVoiceAnswer}
                    disabled={loading}
                    className={`w-32 h-32 rounded-full text-white font-bold text-lg transition-all duration-300 shadow-lg ${
                      isRecording 
                        ? 'bg-red-600 hover:bg-red-700 animate-pulse'
                        : 'bg-green-600 hover:bg-green-700'
                    } disabled:opacity-50`}
                  >
                    {isRecording ? '🔴 STOP' : '🎤 RECORD'}
                  </button>
                  <p className="text-white mt-4">
                    {isRecording 
                      ? 'Recording your answer...'
                      : 'Click to record your voice answer'
                    }
                  </p>
                  {status === 'stopped' && mediaBlobUrl && (
                    <div className="mt-4">
                      <p className="text-green-200 mb-2">Your recorded answer:</p>
                      <audio src={mediaBlobUrl} controls className="mx-auto" />
                    </div>
                  )}
                </div>
                
                {/* Fallback text option */}
                <details className="bg-white/10 rounded-lg p-4">
                  <summary className="text-gray-300 cursor-pointer">
                    💬 Or type your answer instead
                  </summary>
                  <div className="mt-4 space-y-4">
                    <textarea
                      value={currentAnswer}
                      onChange={(e) => setCurrentAnswer(e.target.value)}
                      rows={4}
                      className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Type your answer here..."
                    />
                    <button
                      onClick={() => handleSendMessage()}
                      disabled={loading}
                      className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-2 px-6 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 disabled:opacity-50"
                    >
                      {loading ? 'Sending...' : 'Send Text Answer'}
                    </button>
                  </div>
                </details>
              </div>
            ) : (
              /* Text Mode UI */
              <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }} className="space-y-4">
                <div>
                  <label className="block text-white font-medium mb-2">Your Answer</label>
                  <textarea
                    value={currentAnswer}
                    onChange={(e) => setCurrentAnswer(e.target.value)}
                    rows={4}
                    className="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Type your answer here..."
                    required
                  />
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50"
                >
                  {loading ? 'Sending...' : 'Send Answer'}
                </button>
              </form>
            )}
          </div>
        )}

        {/* Completion Message */}
        {completed && (
          <div className="bg-green-600/20 border border-green-500/30 rounded-2xl p-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-green-200 mb-2">🎤 Voice Interview Completed!</h3>
              <p className="text-green-200 mb-6">
                Thank you for your time. Your voice responses have been recorded, transcribed, and evaluated. 
                A comprehensive report has been generated for the hiring team.
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
          </div>
        )}
      </div>
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