import React, { useState, useEffect } from 'react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Resume Upload Component
export const ResumeUploadSection = ({ onUploadComplete, disabled = false }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [uploadMessage, setUploadMessage] = useState('');

  const handleFiles = async (files) => {
    if (disabled) return;
    
    setUploading(true);
    setUploadMessage('');

    const formData = new FormData();
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch(`${API}/admin/screening/upload-resumes`, {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      
      if (result.success) {
        setUploadedFiles(result.uploaded_resumes);
        setUploadMessage(`Successfully uploaded ${result.total_files} resume(s)`);
        onUploadComplete(result.uploaded_resumes);
      } else {
        setUploadMessage('Upload failed. Please try again.');
      }
    } catch (error) {
      console.error('Upload error:', error);
      setUploadMessage('Upload failed. Please try again.');
    }

    setUploading(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFiles(files);
    }
  };

  const handleChange = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      handleFiles(files);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 mb-8">
      <h2 className="text-2xl font-bold text-white mb-6">📁 Resume Upload</h2>
      <p className="text-gray-300 mb-4">
        Upload candidate resumes (PDF/DOCX format) to enable AI-powered screening and ATS scoring.
      </p>
      
      {/* Upload Area */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-300 ${
          disabled 
            ? 'border-gray-600 bg-gray-800/20 cursor-not-allowed opacity-50' 
            : dragActive
              ? 'border-blue-400 bg-blue-600/20'
              : 'border-gray-400 bg-white/5 hover:border-blue-400 hover:bg-blue-600/10'
        }`}
        onDragEnter={!disabled ? handleDrag : undefined}
        onDragLeave={!disabled ? handleDrag : undefined}
        onDragOver={!disabled ? handleDrag : undefined}
        onDrop={!disabled ? handleDrop : undefined}
      >
        <input
          type="file"
          multiple
          accept=".pdf,.docx"
          onChange={handleChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={disabled || uploading}
        />
        
        <div className="pointer-events-none">
          <div className="text-4xl mb-4">
            {uploading ? '⏳' : '📤'}
          </div>
          <h3 className="text-lg font-semibold text-white mb-2">
            {uploading ? 'Uploading Resumes...' : 'Drop resume files here or click to browse'}
          </h3>
          <p className="text-gray-400 text-sm">
            {disabled 
              ? 'Complete job requirements setup first' 
              : 'Supports PDF and DOCX files (max 10MB each)'
            }
          </p>
        </div>
      </div>

      {/* Upload Message */}
      {uploadMessage && (
        <div className={`mt-4 p-4 rounded-lg ${
          uploadMessage.includes('Successfully') 
            ? 'bg-green-500/20 text-green-400' 
            : 'bg-red-500/20 text-red-400'
        }`}>
          {uploadMessage}
        </div>
      )}

      {/* Uploaded Files */}
      {uploadedFiles.length > 0 && (
        <div className="mt-6">
          <h4 className="text-white font-medium mb-3">Uploaded Resumes ({uploadedFiles.length})</h4>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {uploadedFiles.map((file, index) => (
              <div key={index} className="bg-white/5 rounded-lg p-3 flex justify-between items-center">
                <div>
                  <div className="text-white font-medium">{file.candidate_name || 'Unknown Candidate'}</div>
                  <div className="text-gray-300 text-sm">{file.filename}</div>
                  {file.extracted_skills.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-1">
                      {file.extracted_skills.slice(0, 3).map((skill, skillIndex) => (
                        <span key={skillIndex} className="px-2 py-1 bg-blue-600/20 text-blue-400 rounded text-xs">
                          {skill}
                        </span>
                      ))}
                      {file.extracted_skills.length > 3 && (
                        <span className="px-2 py-1 bg-gray-600/20 text-gray-400 rounded text-xs">
                          +{file.extracted_skills.length - 3} more
                        </span>
                      )}
                    </div>
                  )}
                </div>
                <div className="text-right">
                  <div className="text-gray-400 text-xs">{(file.file_size / 1024).toFixed(1)} KB</div>
                  <div className="text-green-400 text-sm">✓ Processed</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Enhanced Job Requirements Setup Component
export const JobRequirementsSetup = ({ disabled = false, onJobRequirementsSaved, uploadedResumes = [] }) => {
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [requiredSkills, setRequiredSkills] = useState([]);
  const [preferredSkills, setPreferredSkills] = useState([]);
  const [experienceLevel, setExperienceLevel] = useState('mid');
  const [educationRequirements, setEducationRequirements] = useState({});
  const [industryPreferences, setIndustryPreferences] = useState([]);
  const [scoringWeights, setScoringWeights] = useState({
    skills_match: 40,
    experience_level: 30,
    education_fit: 20,
    career_progression: 10
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [jobRequirements, setJobRequirements] = useState([]);
  const [newSkill, setNewSkill] = useState('');

  // Fetch existing job requirements
  const fetchJobRequirements = async () => {
    try {
      const response = await fetch(`${API}/admin/screening/job-requirements`);
      const data = await response.json();
      if (data.success) {
        setJobRequirements(data.job_requirements);
      }
    } catch (error) {
      console.error('Error fetching job requirements:', error);
    }
  };

  useEffect(() => {
    fetchJobRequirements();
  }, []);

  // Add skill to required or preferred skills
  const addSkill = (type) => {
    if (newSkill.trim()) {
      if (type === 'required') {
        setRequiredSkills([...requiredSkills, newSkill.trim()]);
      } else {
        setPreferredSkills([...preferredSkills, newSkill.trim()]);
      }
      setNewSkill('');
    }
  };

  // Remove skill
  const removeSkill = (skill, type) => {
    if (type === 'required') {
      setRequiredSkills(requiredSkills.filter(s => s !== skill));
    } else {
      setPreferredSkills(preferredSkills.filter(s => s !== skill));
    }
  };

  // Handle weight changes
  const handleWeightChange = (key, value) => {
    const newWeights = { ...scoringWeights, [key]: parseInt(value) };
    
    // Ensure weights add up to 100
    const total = Object.values(newWeights).reduce((sum, w) => sum + w, 0);
    if (total === 100) {
      setScoringWeights(newWeights);
    }
  };

  // Save job requirements
  const handleSaveJobRequirements = async () => {
    if (!jobTitle.trim() || !jobDescription.trim()) {
      setMessage('Please fill in job title and description');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API}/admin/screening/job-requirements`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_title: jobTitle,
          job_description: jobDescription,
          required_skills: requiredSkills,
          preferred_skills: preferredSkills,
          experience_level: experienceLevel,
          education_requirements: educationRequirements,
          industry_preferences: industryPreferences,
          scoring_weights: {
            skills_match: scoringWeights.skills_match / 100,
            experience_level: scoringWeights.experience_level / 100,
            education_fit: scoringWeights.education_fit / 100,
            career_progression: scoringWeights.career_progression / 100
          }
        })
      });

      const data = await response.json();
      if (data.success) {
        setMessage('Job requirements saved successfully!');
        fetchJobRequirements();
        onJobRequirementsSaved && onJobRequirementsSaved(data);
        // Reset form
        setJobTitle('');
        setJobDescription('');
        setRequiredSkills([]);
        setPreferredSkills([]);
      } else {
        setMessage('Error saving job requirements');
      }
    } catch (error) {
      setMessage('Error saving job requirements');
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className={`bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 ${disabled ? 'opacity-50' : ''}`}>
      <h2 className="text-2xl font-bold text-white mb-6">🎯 Job Requirements & Screening Setup</h2>
      {disabled && (
        <div className="mb-4 p-4 bg-yellow-500/20 text-yellow-400 rounded-lg border border-yellow-500/30">
          ⚠️ Please upload resumes first to enable job requirements setup
        </div>
      )}
      
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Job Definition Section */}
        <div className="space-y-6">
          <div>
            <label className="block text-white font-medium mb-2">Job Title *</label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              disabled={disabled}
              className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
              placeholder="e.g., Senior Frontend Developer"
            />
          </div>

          <div>
            <label className="block text-white font-medium mb-2">Job Description *</label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              disabled={disabled}
              rows="4"
              className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
              placeholder="Describe the role, responsibilities, and company culture..."
            />
          </div>

          <div>
            <label className="block text-white font-medium mb-2">Experience Level</label>
            <select
              value={experienceLevel}
              onChange={(e) => setExperienceLevel(e.target.value)}
              disabled={disabled}
              className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <option value="entry">Entry Level (0-2 years)</option>
              <option value="mid">Mid Level (3-5 years)</option>
              <option value="senior">Senior Level (6-10 years)</option>
              <option value="executive">Executive Level (10+ years)</option>
            </select>
          </div>

          {/* Skills Section */}
          <div>
            <label className="block text-white font-medium mb-2">Add Skills</label>
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                disabled={disabled}
                className="flex-1 p-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
                placeholder="e.g., React, Python, AWS..."
                onKeyPress={(e) => e.key === 'Enter' && !disabled && addSkill('required')}
              />
              <button
                onClick={() => addSkill('required')}
                disabled={disabled}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Add Required
              </button>
              <button
                onClick={() => addSkill('preferred')}
                disabled={disabled}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Add Preferred
              </button>
            </div>

            {/* Required Skills */}
            <div className="mb-4">
              <h4 className="text-white font-medium mb-2">Required Skills:</h4>
              <div className="flex flex-wrap gap-2">
                {requiredSkills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-red-600 text-white rounded-full text-sm flex items-center gap-2"
                  >
                    {skill}
                    <button
                      onClick={() => removeSkill(skill, 'required')}
                      className="text-white hover:text-gray-300"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Preferred Skills */}
            <div>
              <h4 className="text-white font-medium mb-2">Preferred Skills:</h4>
              <div className="flex flex-wrap gap-2">
                {preferredSkills.map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-green-600 text-white rounded-full text-sm flex items-center gap-2"
                  >
                    {skill}
                    <button
                      onClick={() => removeSkill(skill, 'preferred')}
                      className="text-white hover:text-gray-300"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Scoring Weights Section */}
        <div className="space-y-6">
          <div>
            <h3 className="text-xl font-bold text-white mb-4">⚖️ Scoring Weights (Total: 100%)</h3>
            <div className="space-y-4">
              {Object.entries({
                skills_match: 'Skills Match',
                experience_level: 'Experience Level',
                education_fit: 'Education Fit',
                career_progression: 'Career Progression'
              }).map(([key, label]) => (
                <div key={key}>
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-white font-medium">{label}</label>
                    <span className="text-white">{scoringWeights[key]}%</span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={scoringWeights[key]}
                    onChange={(e) => handleWeightChange(key, e.target.value)}
                    className="w-full"
                  />
                </div>
              ))}
            </div>
            <div className="mt-4 p-3 bg-white/5 rounded-lg">
              <div className="text-white text-sm">
                Total: {Object.values(scoringWeights).reduce((sum, w) => sum + w, 0)}%
                {Object.values(scoringWeights).reduce((sum, w) => sum + w, 0) !== 100 && (
                  <span className="text-red-400 ml-2">⚠️ Must equal 100%</span>
                )}
              </div>
            </div>
          </div>

          {/* Threshold Settings */}
          <div>
            <h3 className="text-xl font-bold text-white mb-4">📊 Auto-Tagging Thresholds</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                <span className="text-white">Top Candidate</span>
                <span className="text-green-400 font-bold">90%+</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                <span className="text-white">Strong Match</span>
                <span className="text-blue-400 font-bold">80-89%</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                <span className="text-white">Good Fit</span>
                <span className="text-yellow-400 font-bold">70-79%</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                <span className="text-white">Needs Review</span>
                <span className="text-orange-400 font-bold">60-69%</span>
              </div>
            </div>
          </div>

          <button
            onClick={handleSaveJobRequirements}
            disabled={disabled || loading || Object.values(scoringWeights).reduce((sum, w) => sum + w, 0) !== 100}
            className="w-full py-3 px-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Saving...' : 'Save Job Requirements'}
          </button>

          {message && (
            <div className={`p-4 rounded-lg ${
              message.includes('success') ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
            }`}>
              {message}
            </div>
          )}
        </div>
      </div>

      {/* Existing Job Requirements */}
      {jobRequirements.length > 0 && (
        <div className="mt-8">
          <h3 className="text-xl font-bold text-white mb-4">📋 Existing Job Requirements</h3>
          <div className="grid gap-4">
            {jobRequirements.map((job) => (
              <div key={job.id} className="bg-white/5 rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="text-white font-bold">{job.job_title}</h4>
                    <p className="text-gray-300 text-sm mb-2">{job.job_description.substring(0, 100)}...</p>
                    <div className="flex gap-2">
                      <span className="px-2 py-1 bg-blue-600/20 text-blue-400 rounded text-xs">
                        {job.required_skills?.length || 0} Required Skills
                      </span>
                      <span className="px-2 py-1 bg-green-600/20 text-green-400 rounded text-xs">
                        {job.preferred_skills?.length || 0} Preferred Skills
                      </span>
                      <span className="px-2 py-1 bg-purple-600/20 text-purple-400 rounded text-xs">
                        {job.experience_level} Level
                      </span>
                    </div>
                  </div>
                  <span className="text-gray-400 text-xs">
                    {new Date(job.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Bulk Screening Interface Component
export const BulkScreeningInterface = ({ candidatePipeline, refreshPipeline }) => {
  const [selectedCandidates, setSelectedCandidates] = useState([]);
  const [selectedJobRequirements, setSelectedJobRequirements] = useState('');
  const [jobRequirements, setJobRequirements] = useState([]);
  const [screeningProgress, setScreeningProgress] = useState(null);
  const [screeningResults, setScreeningResults] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchJobRequirements();
  }, []);

  const fetchJobRequirements = async () => {
    try {
      const response = await fetch(`${API}/admin/screening/job-requirements`);
      const data = await response.json();
      if (data.success) {
        setJobRequirements(data.job_requirements);
      }
    } catch (error) {
      console.error('Error fetching job requirements:', error);
    }
  };

  const handleCandidateSelection = (candidateId) => {
    setSelectedCandidates(prev => 
      prev.includes(candidateId) 
        ? prev.filter(id => id !== candidateId)
        : [...prev, candidateId]
    );
  };

  const selectAllCandidates = () => {
    if (selectedCandidates.length === candidatePipeline.length) {
      setSelectedCandidates([]);
    } else {
      setSelectedCandidates(candidatePipeline.map(c => c.id || c.token));
    }
  };

  const startBulkScreening = async () => {
    if (!selectedJobRequirements) {
      alert('Please select job requirements first');
      return;
    }

    if (selectedCandidates.length === 0) {
      alert('Please select candidates to screen');
      return;
    }

    setLoading(true);
    setScreeningProgress({ status: 'starting', processed: 0, total: selectedCandidates.length });

    try {
      // First, score the selected candidates
      const response = await fetch(`${API}/admin/screening/score-candidates`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          job_requirements_id: selectedJobRequirements,
          candidate_ids: selectedCandidates
        })
      });

      const data = await response.json();
      if (data.success) {
        setScreeningResults(data);
        setScreeningProgress({ 
          status: 'completed', 
          processed: data.candidates_scored,
          total: selectedCandidates.length 
        });
        refreshPipeline(); // Refresh the pipeline to show updated scores
      } else {
        throw new Error('Screening failed');
      }
    } catch (error) {
      console.error('Error in bulk screening:', error);
      setScreeningProgress({ status: 'error', error: error.message });
    }
    setLoading(false);
  };

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-400';
    if (score >= 80) return 'text-blue-400';
    if (score >= 70) return 'text-yellow-400';
    if (score >= 60) return 'text-orange-400';
    return 'text-red-400';
  };

  const getScoreTag = (score) => {
    if (score >= 90) return { text: 'Top Candidate', color: 'bg-green-600' };
    if (score >= 80) return { text: 'Strong Match', color: 'bg-blue-600' };
    if (score >= 70) return { text: 'Good Fit', color: 'bg-yellow-600' };
    if (score >= 60) return { text: 'Needs Review', color: 'bg-orange-600' };
    return { text: 'Below Threshold', color: 'bg-red-600' };
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-6">🤖 AI-Powered Bulk Screening</h2>
      
      {/* Job Requirements Selection */}
      <div className="mb-6 p-4 bg-white/5 rounded-lg">
        <label className="block text-white font-medium mb-2">Select Job Requirements</label>
        <select
          value={selectedJobRequirements}
          onChange={(e) => setSelectedJobRequirements(e.target.value)}
          className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white"
        >
          <option value="">-- Select Job Requirements --</option>
          {jobRequirements.map((job) => (
            <option key={job.id} value={job.id}>
              {job.job_title} ({job.required_skills?.length || 0} required skills)
            </option>
          ))}
        </select>
      </div>

      {/* Candidate Selection */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-white">Select Candidates to Screen</h3>
          <button
            onClick={selectAllCandidates}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            {selectedCandidates.length === candidatePipeline.length ? 'Deselect All' : 'Select All'} 
            ({candidatePipeline.length} candidates)
          </button>
        </div>

        <div className="max-h-96 overflow-y-auto space-y-2">
          {candidatePipeline.map((candidate) => (
            <div
              key={candidate.id || candidate.token}
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                selectedCandidates.includes(candidate.id || candidate.token)
                  ? 'bg-blue-600/20 border-blue-400'
                  : 'bg-white/5 border-white/20 hover:border-white/40'
              }`}
              onClick={() => handleCandidateSelection(candidate.id || candidate.token)}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="text-white font-medium">
                    {candidate.name || candidate.candidateName || 'Unknown Candidate'}
                  </h4>
                  <p className="text-gray-300 text-sm">
                    {candidate.jobTitle || candidate.position || 'No position specified'}
                  </p>
                  {candidate.extractedSkills && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {candidate.extractedSkills.slice(0, 5).map((skill, index) => (
                        <span key={index} className="px-2 py-1 bg-gray-700 text-gray-300 rounded text-xs">
                          {skill}
                        </span>
                      ))}
                      {candidate.extractedSkills.length > 5 && (
                        <span className="px-2 py-1 bg-gray-600 text-gray-400 rounded text-xs">
                          +{candidate.extractedSkills.length - 5} more
                        </span>
                      )}
                    </div>
                  )}
                </div>
                <div className="text-right">
                  {candidate.score && (
                    <div>
                      <div className={`text-lg font-bold ${getScoreColor(candidate.score)}`}>
                        {candidate.score}%
                      </div>
                      <div className={`px-2 py-1 rounded text-xs text-white ${getScoreTag(candidate.score).color}`}>
                        {getScoreTag(candidate.score).text}
                      </div>
                    </div>
                  )}
                  <div className="mt-1">
                    <input
                      type="checkbox"
                      checked={selectedCandidates.includes(candidate.id || candidate.token)}
                      onChange={() => handleCandidateSelection(candidate.id || candidate.token)}
                      className="w-4 h-4"
                    />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Screening Controls */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={startBulkScreening}
          disabled={loading || !selectedJobRequirements || selectedCandidates.length === 0}
          className="flex-1 py-3 px-6 bg-gradient-to-r from-green-600 to-blue-600 text-white font-bold rounded-lg hover:from-green-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Screening in Progress...' : `Screen ${selectedCandidates.length} Candidates`}
        </button>
      </div>

      {/* Screening Progress */}
      {screeningProgress && (
        <div className="mb-6 p-4 bg-white/5 rounded-lg">
          <h4 className="text-white font-medium mb-2">Screening Progress</h4>
          {screeningProgress.status === 'starting' && (
            <div className="text-blue-400">Starting screening process...</div>
          )}
          {screeningProgress.status === 'completed' && (
            <div className="text-green-400">
              ✅ Screening completed! Processed {screeningProgress.processed} out of {screeningProgress.total} candidates.
            </div>
          )}
          {screeningProgress.status === 'error' && (
            <div className="text-red-400">
              ❌ Screening failed: {screeningProgress.error}
            </div>
          )}
        </div>
      )}

      {/* Screening Results */}
      {screeningResults && (
        <div className="p-4 bg-white/5 rounded-lg">
          <h4 className="text-white font-medium mb-4">📊 Screening Results Summary</h4>
          <div className="grid md:grid-cols-3 gap-4 mb-4">
            <div className="text-center p-3 bg-blue-600/20 rounded-lg">
              <div className="text-2xl font-bold text-blue-400">{screeningResults.candidates_scored}</div>
              <div className="text-sm text-gray-300">Candidates Scored</div>
            </div>
            <div className="text-center p-3 bg-green-600/20 rounded-lg">
              <div className="text-2xl font-bold text-green-400">{screeningResults.average_score.toFixed(1)}%</div>
              <div className="text-sm text-gray-300">Average Score</div>
            </div>
            <div className="text-center p-3 bg-purple-600/20 rounded-lg">
              <div className="text-2xl font-bold text-purple-400">
                {screeningResults.scored_candidates.filter(c => c.overall_score >= 80).length}
              </div>
              <div className="text-sm text-gray-300">High-Quality Matches</div>
            </div>
          </div>

          {/* Top Candidates */}
          <div>
            <h5 className="text-white font-medium mb-2">🏆 Top Scored Candidates</h5>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {screeningResults.scored_candidates.slice(0, 10).map((candidate, index) => (
                <div key={candidate.candidate_id} className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                  <div>
                    <div className="text-white font-medium">#{index + 1} {candidate.name}</div>
                    <div className="text-sm text-gray-300">
                      Skills: {candidate.component_scores?.skills_match?.toFixed(1)}% | 
                      Experience: {candidate.component_scores?.experience_level?.toFixed(1)}%
                    </div>
                  </div>
                  <div className="text-right">
                    <div className={`text-lg font-bold ${getScoreColor(candidate.overall_score)}`}>
                      {candidate.overall_score.toFixed(1)}%
                    </div>
                    <div className={`px-2 py-1 rounded text-xs text-white ${getScoreTag(candidate.overall_score).color}`}>
                      {getScoreTag(candidate.overall_score).text}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Screen Candidates Component
export const ScreenCandidatesSection = ({ 
  uploadedResumes = [], 
  savedJobRequirements = null, 
  onScreeningComplete 
}) => {
  const [selectedResumes, setSelectedResumes] = useState([]);
  const [screening, setScreening] = useState(false);
  const [screeningResults, setScreeningResults] = useState(null);
  const [message, setMessage] = useState('');

  const canScreen = uploadedResumes.length > 0 && savedJobRequirements;

  const handleResumeSelection = (resumeId) => {
    setSelectedResumes(prev => 
      prev.includes(resumeId) 
        ? prev.filter(id => id !== resumeId)
        : [...prev, resumeId]
    );
  };

  const selectAllResumes = () => {
    if (selectedResumes.length === uploadedResumes.length) {
      setSelectedResumes([]);
    } else {
      setSelectedResumes(uploadedResumes.map(r => r.id));
    }
  };

  const handleScreenCandidates = async () => {
    if (!savedJobRequirements || selectedResumes.length === 0) {
      setMessage('Please select candidates and ensure job requirements are saved');
      return;
    }

    setScreening(true);
    setMessage('');

    try {
      const response = await fetch(`${API}/admin/screening/screen-candidates`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_ids: selectedResumes,
          job_requirements_id: savedJobRequirements.job_requirements_id
        })
      });

      const result = await response.json();
      
      if (result.success) {
        setScreeningResults(result);
        setMessage(`Successfully screened ${result.analysis_results.length} candidate(s)`);
        onScreeningComplete && onScreeningComplete(result);
      } else {
        setMessage('Screening failed. Please try again.');
      }
    } catch (error) {
      console.error('Screening error:', error);
      setMessage('Screening failed. Please try again.');
    }

    setScreening(false);
  };

  if (!canScreen) {
    return (
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 opacity-50">
        <h2 className="text-2xl font-bold text-white mb-6">🤖 Screen Candidates</h2>
        <div className="text-center p-8">
          <div className="text-4xl mb-4">⏳</div>
          <p className="text-gray-400">
            {uploadedResumes.length === 0 
              ? 'Upload resumes and save job requirements to enable candidate screening'
              : 'Save job requirements to enable candidate screening'
            }
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-6">🤖 Screen Candidates</h2>
      
      {/* Resume Selection */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-white">Select Resumes to Screen</h3>
          <button
            onClick={selectAllResumes}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            {selectedResumes.length === uploadedResumes.length ? 'Deselect All' : 'Select All'} 
            ({uploadedResumes.length} resumes)
          </button>
        </div>

        <div className="max-h-80 overflow-y-auto space-y-2">
          {uploadedResumes.map((resume) => (
            <div
              key={resume.id}
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                selectedResumes.includes(resume.id)
                  ? 'bg-blue-600/20 border-blue-400'
                  : 'bg-white/5 border-white/20 hover:border-white/40'
              }`}
              onClick={() => handleResumeSelection(resume.id)}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h4 className="text-white font-medium">
                    {resume.candidate_name || 'Unknown Candidate'}
                  </h4>
                  <p className="text-gray-300 text-sm">{resume.filename}</p>
                  {resume.extracted_skills.length > 0 && (
                    <div className="flex flex-wrap gap-1 mt-2">
                      {resume.extracted_skills.slice(0, 5).map((skill, index) => (
                        <span key={index} className="px-2 py-1 bg-gray-700 text-gray-300 rounded text-xs">
                          {skill}
                        </span>
                      ))}
                      {resume.extracted_skills.length > 5 && (
                        <span className="px-2 py-1 bg-gray-600 text-gray-400 rounded text-xs">
                          +{resume.extracted_skills.length - 5} more
                        </span>
                      )}
                    </div>
                  )}
                </div>
                <div className="text-right">
                  <input
                    type="checkbox"
                    checked={selectedResumes.includes(resume.id)}
                    onChange={() => handleResumeSelection(resume.id)}
                    className="w-4 h-4"
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Screen Button */}
      <button
        onClick={handleScreenCandidates}
        disabled={screening || selectedResumes.length === 0}
        className="w-full py-4 px-6 bg-gradient-to-r from-green-600 to-blue-600 text-white font-bold rounded-lg hover:from-green-700 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-lg"
      >
        {screening 
          ? `Screening ${selectedResumes.length} Candidate(s)...` 
          : `Screen ${selectedResumes.length} Selected Candidate(s)`
        }
      </button>

      {/* Message */}
      {message && (
        <div className={`mt-4 p-4 rounded-lg ${
          message.includes('Successfully') 
            ? 'bg-green-500/20 text-green-400' 
            : 'bg-red-500/20 text-red-400'
        }`}>
          {message}
        </div>
      )}

      {/* Quick Results Preview */}
      {screeningResults && (
        <div className="mt-6 p-4 bg-white/5 rounded-lg">
          <h4 className="text-white font-medium mb-4">📊 Screening Summary</h4>
          <div className="grid md:grid-cols-3 gap-4">
            <div className="text-center p-3 bg-blue-600/20 rounded-lg">
              <div className="text-2xl font-bold text-blue-400">{screeningResults.analysis_results.length}</div>
              <div className="text-sm text-gray-300">Candidates Screened</div>
            </div>
            <div className="text-center p-3 bg-green-600/20 rounded-lg">
              <div className="text-2xl font-bold text-green-400">{screeningResults.average_score.toFixed(1)}%</div>
              <div className="text-sm text-gray-300">Average ATS Score</div>
            </div>
            <div className="text-center p-3 bg-purple-600/20 rounded-lg">
              <div className="text-2xl font-bold text-purple-400">{screeningResults.top_candidates.length}</div>
              <div className="text-sm text-gray-300">Top Candidates (80%+)</div>
            </div>
          </div>
          <div className="mt-4 text-center">
            <p className="text-gray-300 text-sm">Check the Results tab for detailed analysis</p>
          </div>
        </div>
      )}
    </div>
  );
};

// Results Component for displaying ATS scores
export const ResultsComponent = () => {
  const [results, setResults] = useState([]);
  const [statistics, setStatistics] = useState({});
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all'); // all, high, medium, low

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API}/admin/screening/results`);
      const data = await response.json();
      
      if (data.success) {
        setResults(data.results);
        setStatistics(data.statistics);
      }
    } catch (error) {
      console.error('Error fetching results:', error);
    }
    setLoading(false);
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 70) return 'text-blue-400';
    if (score >= 60) return 'text-yellow-400';
    if (score >= 50) return 'text-orange-400';
    return 'text-red-400';
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return { text: 'Excellent Match', color: 'bg-green-600' };
    if (score >= 70) return { text: 'Good Match', color: 'bg-blue-600' };
    if (score >= 60) return { text: 'Fair Match', color: 'bg-yellow-600' };
    if (score >= 50) return { text: 'Poor Match', color: 'bg-orange-600' };
    return { text: 'No Match', color: 'bg-red-600' };
  };

  const filteredResults = results.filter(result => {
    if (filter === 'high') return result.overall_score >= 80;
    if (filter === 'medium') return result.overall_score >= 60 && result.overall_score < 80;
    if (filter === 'low') return result.overall_score < 60;
    return true;
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 p-8">
        <div className="container mx-auto">
          <h1 className="text-4xl font-bold text-white mb-8">📊 ATS Screening Results</h1>
          <div className="text-center p-8">
            <div className="text-4xl mb-4">⏳</div>
            <p className="text-gray-400">Loading screening results...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 p-8">
      <div className="container mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">📊 ATS Screening Results</h1>

        {/* Statistics Cards */}
        {statistics.total_candidates > 0 && (
          <div className="grid lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold text-white mb-2">Total Candidates</h3>
              <div className="text-3xl font-bold text-blue-400">{statistics.total_candidates}</div>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold text-white mb-2">Average Score</h3>
              <div className="text-3xl font-bold text-green-400">{statistics.average_score.toFixed(1)}%</div>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold text-white mb-2">Top Performers</h3>
              <div className="text-3xl font-bold text-purple-400">{statistics.candidates_above_80}</div>
              <div className="text-sm text-gray-300">80%+ Score</div>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <h3 className="text-xl font-bold text-white mb-2">Score Range</h3>
              <div className="text-lg font-bold text-yellow-400">
                {statistics.lowest_score.toFixed(1)}% - {statistics.highest_score.toFixed(1)}%
              </div>
            </div>
          </div>
        )}

        {/* Filter Buttons */}
        <div className="mb-6 flex gap-4">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              filter === 'all' 
                ? 'bg-blue-600 text-white' 
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            All Candidates ({results.length})
          </button>
          <button
            onClick={() => setFilter('high')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              filter === 'high' 
                ? 'bg-green-600 text-white' 
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            High Scores ({results.filter(r => r.overall_score >= 80).length})
          </button>
          <button
            onClick={() => setFilter('medium')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              filter === 'medium' 
                ? 'bg-yellow-600 text-white' 
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            Medium Scores ({results.filter(r => r.overall_score >= 60 && r.overall_score < 80).length})
          </button>
          <button
            onClick={() => setFilter('low')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              filter === 'low' 
                ? 'bg-red-600 text-white' 
                : 'bg-white/10 text-gray-300 hover:bg-white/20'
            }`}
          >
            Low Scores ({results.filter(r => r.overall_score < 60).length})
          </button>
        </div>

        {/* Results List */}
        {filteredResults.length === 0 ? (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 text-center">
            <div className="text-4xl mb-4">📝</div>
            <p className="text-gray-400">No screening results available. Screen candidates first.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredResults.map((result, index) => (
              <div key={result.candidate_id} className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <div className="grid lg:grid-cols-4 gap-6">
                  {/* Candidate Info */}
                  <div>
                    <h3 className="text-xl font-bold text-white mb-2">
                      #{index + 1} {result.candidate_name}
                    </h3>
                    <p className="text-gray-300 text-sm mb-2">{result.resume_filename}</p>
                    <div className={`inline-flex px-3 py-1 rounded-full text-xs text-white ${getScoreLabel(result.overall_score).color}`}>
                      {getScoreLabel(result.overall_score).text}
                    </div>
                  </div>

                  {/* Overall Score */}
                  <div className="text-center">
                    <div className="text-sm text-gray-300 mb-1">Overall ATS Score</div>
                    <div className={`text-3xl font-bold ${getScoreColor(result.overall_score)}`}>
                      {result.overall_score.toFixed(1)}%
                    </div>
                  </div>

                  {/* Component Scores */}
                  <div>
                    <div className="text-sm text-gray-300 mb-2">Component Scores</div>
                    {Object.entries(result.component_scores || {}).map(([key, value]) => (
                      <div key={key} className="flex justify-between text-sm mb-1">
                        <span className="text-gray-300 capitalize">{key.replace('_', ' ')}</span>
                        <span className={`font-semibold ${getScoreColor(value)}`}>{value.toFixed(1)}%</span>
                      </div>
                    ))}
                  </div>

                  {/* Skills & Recommendations */}
                  <div>
                    <div className="text-sm text-gray-300 mb-2">Analysis</div>
                    {result.missing_skills.length > 0 && (
                      <div className="mb-2">
                        <div className="text-xs text-red-400 mb-1">Missing Skills:</div>
                        <div className="flex flex-wrap gap-1">
                          {result.missing_skills.slice(0, 3).map((skill, i) => (
                            <span key={i} className="px-2 py-1 bg-red-600/20 text-red-400 rounded text-xs">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                    {result.recommendations.length > 0 && (
                      <div>
                        <div className="text-xs text-blue-400 mb-1">Key Recommendations:</div>
                        <div className="text-xs text-gray-300">
                          {result.recommendations[0]}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Refresh Button */}
        <div className="mt-8 text-center">
          <button
            onClick={fetchResults}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-lg hover:from-blue-700 hover:to-purple-700"
          >
            🔄 Refresh Results
          </button>
        </div>
      </div>
    </div>
  );
};