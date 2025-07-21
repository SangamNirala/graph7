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

// Landing Page Component
const LandingPage = ({ setCurrentPage }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-white mb-6">
            🎤 AI-Powered Voice Interview Agent
          </h1>
          <p className="text-xl text-gray-300 mb-12 max-w-3xl mx-auto">
            Experience the future of hiring with our advanced AI interviewer that conducts 
            personalized voice interviews with female AI voice and supports PDF/Word resume uploads.
          </p>
          <div className="flex justify-center space-x-6 mb-8">
            <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-3">
              <span className="text-green-200">✅ Voice Interview Mode</span>
            </div>
            <div className="bg-blue-500/20 border border-blue-500/30 rounded-lg p-3">
              <span className="text-blue-200">✅ PDF/Word/TXT Resume Support</span>
            </div>
            <div className="bg-purple-500/20 border border-purple-500/30 rounded-lg p-3">
              <span className="text-purple-200">✅ AI Female Voice Questions</span>
            </div>
          </div>
        </div>

        <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-8">
          {/* Admin Login Card */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m7 0v4m6-4v4M9 9h6m-6 4h6m-6 4h6" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-white mb-4">Admin Portal</h2>
              <p className="text-gray-300 mb-6">Upload job descriptions, manage resumes (PDF/Word/TXT), and generate secure interview tokens.</p>
              <button 
                onClick={() => setCurrentPage('admin-login')}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Admin Login
              </button>
            </div>
          </div>

          {/* Candidate Login Card */}
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 hover:bg-white/15 transition-all duration-300 transform hover:scale-105">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-white mb-4">Candidate Portal</h2>
              <p className="text-gray-300 mb-6">Enter your secure token for personalized voice interviews with AI interviewer.</p>
              <button 
                onClick={() => setCurrentPage('candidate-login')}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Candidate Login
              </button>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-20 max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-white text-center mb-12">Enhanced Features</h3>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
              </div>
              <h4 className="text-xl font-bold text-white mb-2">Voice Interviews</h4>
              <p className="text-gray-300">AI female voice asks questions, candidates respond with voice.</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h4 className="text-xl font-bold text-white mb-2">Multi-Format Resumes</h4>
              <p className="text-gray-300">Upload PDF, Word, or TXT resume files for processing.</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-yellow-500 to-orange-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h4 className="text-xl font-bold text-white mb-2">Audio Analytics</h4>
              <p className="text-gray-300">Voice recordings stored for comprehensive assessment reports.</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-red-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h4 className="text-xl font-bold text-white mb-2">Secure & Private</h4>
              <p className="text-gray-300">Token-based authentication with encrypted voice data storage.</p>
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

// Admin Dashboard Component
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

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setResumeFile(file);
    
    // Show file info
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
    formData.append('resume_file', resumeFile);

    try {
      const response = await fetch(`${API}/admin/upload-job`, {
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
        setResumeFile(null);
        document.querySelector('input[type="file"]').value = '';
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

  useEffect(() => {
    if (activeTab === 'reports') {
      fetchReports();
    }
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800">
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-white">🎤 Voice Interview Admin</h1>
          <button
            onClick={() => setCurrentPage('landing')}
            className="bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors duration-300"
          >
            Logout
          </button>
        </div>

        {/* Tabs */}
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
              📄 Upload Job & Resume
            </button>
            <button
              onClick={() => setActiveTab('reports')}
              className={`flex-1 py-3 px-4 text-sm font-medium rounded-md transition-all duration-300 ${
                activeTab === 'reports'
                  ? 'bg-blue-600 text-white shadow-lg'
                  : 'text-gray-300 hover:text-white hover:bg-white/10'
              }`}
            >
              📊 Voice Interview Reports
            </button>
          </nav>
        </div>

        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold text-white mb-6">Create New Interview Token</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
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
        return <LandingPage setCurrentPage={setCurrentPage} />;
    }
  };

  return (
    <div className="App">
      {renderPage()}
    </div>
  );
}

export default App;