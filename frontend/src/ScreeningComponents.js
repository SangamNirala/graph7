import React, { useState, useEffect } from 'react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Job Requirements Configuration Component
export const JobRequirementsSetup = () => {
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
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-6">🎯 Job Requirements & Screening Setup</h2>
      
      <div className="grid lg:grid-cols-2 gap-8">
        {/* Job Definition Section */}
        <div className="space-y-6">
          <div>
            <label className="block text-white font-medium mb-2">Job Title *</label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
              placeholder="e.g., Senior Frontend Developer"
            />
          </div>

          <div>
            <label className="block text-white font-medium mb-2">Job Description *</label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows="4"
              className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
              placeholder="Describe the role, responsibilities, and company culture..."
            />
          </div>

          <div>
            <label className="block text-white font-medium mb-2">Experience Level</label>
            <select
              value={experienceLevel}
              onChange={(e) => setExperienceLevel(e.target.value)}
              className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white"
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
                className="flex-1 p-2 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
                placeholder="e.g., React, Python, AWS..."
                onKeyPress={(e) => e.key === 'Enter' && addSkill('required')}
              />
              <button
                onClick={() => addSkill('required')}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                Add Required
              </button>
              <button
                onClick={() => addSkill('preferred')}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
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
            disabled={loading || Object.values(scoringWeights).reduce((sum, w) => sum + w, 0) !== 100}
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

// Direct Resume Upload and Screening Component
export const DirectResumeScreening = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [selectedJobRequirements, setSelectedJobRequirements] = useState('');
  const [jobRequirements, setJobRequirements] = useState([]);
  const [batchName, setBatchName] = useState('');
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(null);
  const [screeningResults, setScreeningResults] = useState(null);
  const [dragOver, setDragOver] = useState(false);

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

  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files);
    handleFiles(files);
  };

  const handleFiles = (files) => {
    const validFiles = files.filter(file => {
      const validTypes = ['.pdf', '.doc', '.docx', '.txt'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      return validTypes.includes(fileExtension) && file.size <= 10 * 1024 * 1024; // 10MB limit
    });

    if (validFiles.length !== files.length) {
      alert(`${files.length - validFiles.length} files were rejected. Only PDF, DOC, DOCX, and TXT files under 10MB are allowed.`);
    }

    if (validFiles.length + selectedFiles.length > 50) {
      alert('Maximum 50 files allowed for direct screening');
      return;
    }

    setSelectedFiles([...selectedFiles, ...validFiles]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  };

  const removeFile = (index) => {
    const newFiles = selectedFiles.filter((_, i) => i !== index);
    setSelectedFiles(newFiles);
  };

  const startDirectScreening = async () => {
    if (!selectedJobRequirements) {
      alert('Please select job requirements first');
      return;
    }

    if (selectedFiles.length === 0) {
      alert('Please upload at least one resume file');
      return;
    }

    setLoading(true);
    setUploadProgress({ status: 'uploading', processed: 0, total: selectedFiles.length });
    
    try {
      const formData = new FormData();
      selectedFiles.forEach(file => {
        formData.append('files', file);
      });
      formData.append('job_requirements_id', selectedJobRequirements);
      formData.append('batch_name', batchName || `Direct Screening ${new Date().toLocaleString()}`);

      const response = await fetch(`${API}/admin/screening/upload-and-analyze`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      if (data.success) {
        setScreeningResults(data);
        setUploadProgress({ 
          status: 'completed', 
          processed: data.processing_summary.successfully_processed,
          total: data.processing_summary.total_files 
        });
        
        // Clear form for next batch
        setSelectedFiles([]);
        setBatchName('');
      } else {
        throw new Error('Screening failed');
      }
    } catch (error) {
      console.error('Error in direct screening:', error);
      setUploadProgress({ status: 'error', error: error.message });
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

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
      <h2 className="text-2xl font-bold text-white mb-6">📎 Upload & Screen Resumes Instantly</h2>
      
      {/* Job Requirements Selection */}
      <div className="mb-6 p-4 bg-white/5 rounded-lg">
        <label className="block text-white font-medium mb-2">Select Job Requirements for Screening</label>
        <div className="grid lg:grid-cols-3 gap-4">
          <div className="lg:col-span-2">
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
          <div>
            <input
              type="text"
              placeholder="Batch Name (Optional)"
              value={batchName}
              onChange={(e) => setBatchName(e.target.value)}
              className="w-full p-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400"
            />
          </div>
        </div>
      </div>

      {/* File Upload Area */}
      <div className="mb-6">
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${
            dragOver
              ? 'border-blue-400 bg-blue-400/10'
              : 'border-white/30 hover:border-white/50'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center space-y-4">
            <div className="text-4xl text-white/70">📁</div>
            <div>
              <p className="text-white text-lg mb-2">
                Drop resume files here or click to browse
              </p>
              <p className="text-gray-400 text-sm">
                Supports PDF, DOC, DOCX, TXT files (max 10MB each, up to 50 files)
              </p>
            </div>
            <input
              type="file"
              multiple
              accept=".pdf,.doc,.docx,.txt"
              onChange={handleFileSelect}
              className="hidden"
              id="resume-upload"
            />
            <label
              htmlFor="resume-upload"
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer transition-colors"
            >
              Browse Files
            </label>
          </div>
        </div>
      </div>

      {/* Selected Files Display */}
      {selectedFiles.length > 0 && (
        <div className="mb-6 p-4 bg-white/5 rounded-lg">
          <div className="flex justify-between items-center mb-4">
            <h4 className="text-white font-medium">Selected Files ({selectedFiles.length})</h4>
            <button
              onClick={() => setSelectedFiles([])}
              className="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              Clear All
            </button>
          </div>
          <div className="max-h-40 overflow-y-auto space-y-2">
            {selectedFiles.map((file, index) => (
              <div key={index} className="flex justify-between items-center p-3 bg-white/5 rounded-lg">
                <div className="flex-1">
                  <div className="text-white font-medium truncate">{file.name}</div>
                  <div className="text-sm text-gray-300">
                    {formatFileSize(file.size)} • {file.name.split('.').pop().toUpperCase()}
                  </div>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="ml-2 px-2 py-1 bg-red-600/50 text-white rounded hover:bg-red-600 text-sm"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Button */}
      <div className="mb-6">
        <button
          onClick={startDirectScreening}
          disabled={loading || !selectedJobRequirements || selectedFiles.length === 0}
          className="w-full py-4 px-6 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {loading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Analyzing & Scoring Resumes...</span>
            </div>
          ) : (
            `🚀 Upload & Screen ${selectedFiles.length} Resume${selectedFiles.length !== 1 ? 's' : ''} Instantly`
          )}
        </button>
      </div>

      {/* Upload Progress */}
      {uploadProgress && (
        <div className="mb-6 p-4 bg-white/5 rounded-lg">
          <h4 className="text-white font-medium mb-2">Processing Status</h4>
          {uploadProgress.status === 'uploading' && (
            <div className="text-blue-400 flex items-center space-x-2">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-400"></div>
              <span>Uploading and analyzing resumes...</span>
            </div>
          )}
          {uploadProgress.status === 'completed' && (
            <div className="text-green-400">
              ✅ Screening completed! Processed {uploadProgress.processed} out of {uploadProgress.total} resumes successfully.
            </div>
          )}
          {uploadProgress.status === 'error' && (
            <div className="text-red-400">
              ❌ Screening failed: {uploadProgress.error}
            </div>
          )}
        </div>
      )}

      {/* Screening Results */}
      {screeningResults && (
        <div className="space-y-6">
          {/* Summary Statistics */}
          <div className="p-6 bg-white/5 rounded-lg">
            <h4 className="text-white font-bold text-xl mb-4">📊 Screening Results Summary</h4>
            
            {/* Key Metrics */}
            <div className="grid md:grid-cols-4 gap-4 mb-6">
              <div className="text-center p-4 bg-blue-600/20 rounded-lg">
                <div className="text-3xl font-bold text-blue-400">{screeningResults.screening_results.candidates_screened}</div>
                <div className="text-sm text-gray-300">Candidates Screened</div>
              </div>
              <div className="text-center p-4 bg-green-600/20 rounded-lg">
                <div className="text-3xl font-bold text-green-400">{screeningResults.screening_results.average_score}%</div>
                <div className="text-sm text-gray-300">Average Score</div>
              </div>
              <div className="text-center p-4 bg-purple-600/20 rounded-lg">
                <div className="text-3xl font-bold text-purple-400">{screeningResults.screening_results.high_quality_matches}</div>
                <div className="text-sm text-gray-300">High-Quality Matches</div>
              </div>
              <div className="text-center p-4 bg-orange-600/20 rounded-lg">
                <div className="text-3xl font-bold text-orange-400">{screeningResults.processing_summary.processing_rate}</div>
                <div className="text-sm text-gray-300">Success Rate</div>
              </div>
            </div>

            {/* Score Distribution */}
            <div className="mb-6">
              <h5 className="text-white font-medium mb-3">Score Distribution</h5>
              <div className="grid grid-cols-4 gap-2">
                <div className="text-center p-3 bg-green-600/20 rounded">
                  <div className="text-lg font-bold text-green-400">{screeningResults.screening_results.score_distribution.excellent}</div>
                  <div className="text-xs text-gray-300">Excellent (90%+)</div>
                </div>
                <div className="text-center p-3 bg-blue-600/20 rounded">
                  <div className="text-lg font-bold text-blue-400">{screeningResults.screening_results.score_distribution.good}</div>
                  <div className="text-xs text-gray-300">Good (80-89%)</div>
                </div>
                <div className="text-center p-3 bg-yellow-600/20 rounded">
                  <div className="text-lg font-bold text-yellow-400">{screeningResults.screening_results.score_distribution.fair}</div>
                  <div className="text-xs text-gray-300">Fair (70-79%)</div>
                </div>
                <div className="text-center p-3 bg-red-600/20 rounded">
                  <div className="text-lg font-bold text-red-400">{screeningResults.screening_results.score_distribution.poor}</div>
                  <div className="text-xs text-gray-300">Poor (<70%)</div>
                </div>
              </div>
            </div>
          </div>

          {/* Top Candidates */}
          {screeningResults.top_candidates.length > 0 && (
            <div className="p-6 bg-white/5 rounded-lg">
              <h5 className="text-white font-bold text-lg mb-4">🏆 Top Candidates</h5>
              <div className="space-y-3 max-h-80 overflow-y-auto">
                {screeningResults.top_candidates.map((candidate, index) => (
                  <div key={candidate.candidate_id} className="p-4 bg-white/5 rounded-lg border border-white/10">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="text-white font-medium">#{index + 1}</span>
                          <span className="text-white font-bold">{candidate.name}</span>
                          <span className="text-xs text-gray-400">({candidate.filename})</span>
                        </div>
                        <div className="text-sm text-gray-300 mb-2">
                          {candidate.experience_level} Level • {candidate.years_experience} years experience
                        </div>
                      </div>
                      <div className="text-right">
                        <div className={`text-2xl font-bold ${getScoreColor(candidate.overall_score)}`}>
                          {candidate.overall_score.toFixed(1)}%
                        </div>
                        <div className={`px-3 py-1 rounded-lg text-sm font-medium text-white ${getScoreTag(candidate.overall_score).color}`}>
                          {getScoreTag(candidate.overall_score).text}
                        </div>
                      </div>
                    </div>
                    
                    {/* Score Breakdown */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                      {Object.entries(candidate.component_scores || {}).map(([key, value]) => (
                        <div key={key} className="text-center p-2 bg-white/5 rounded">
                          <div className="font-medium text-white">{value.toFixed(1)}%</div>
                          <div className="text-gray-400 capitalize">{key.replace('_', ' ')}</div>
                        </div>
                      ))}
                    </div>

                    {/* Skills */}
                    {candidate.extracted_skills && candidate.extracted_skills.length > 0 && (
                      <div className="mt-3">
                        <div className="text-xs text-gray-400 mb-1">Key Skills:</div>
                        <div className="flex flex-wrap gap-1">
                          {candidate.extracted_skills.slice(0, 8).map((skill, skillIndex) => (
                            <span key={skillIndex} className="px-2 py-1 bg-gray-700 text-gray-300 rounded text-xs">
                              {skill}
                            </span>
                          ))}
                          {candidate.extracted_skills.length > 8 && (
                            <span className="px-2 py-1 bg-gray-600 text-gray-400 rounded text-xs">
                              +{candidate.extracted_skills.length - 8} more
                            </span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Failed Files */}
          {screeningResults.failed_files && screeningResults.failed_files.length > 0 && (
            <div className="p-6 bg-red-600/10 border border-red-600/20 rounded-lg">
              <h5 className="text-red-400 font-bold text-lg mb-4">⚠️ Failed Files ({screeningResults.failed_files.length})</h5>
              <div className="space-y-2 max-h-40 overflow-y-auto">
                {screeningResults.failed_files.map((failed, index) => (
                  <div key={index} className="flex justify-between items-center p-3 bg-red-600/5 rounded">
                    <div className="text-white font-medium">{failed.filename}</div>
                    <div className="text-red-400 text-sm">{failed.error}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};