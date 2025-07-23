import React from "react";
import "./App.css";

const WorkflowStep = ({ 
  title, 
  description, 
  bgColor, 
  textColor = "white", 
  icon,
  position,
  delay = 0 
}) => (
  <div 
    className={`workflow-step ${bgColor} ${textColor === "dark" ? "text-gray-800" : "text-white"} ${position}`}
    style={{ animationDelay: `${delay}ms` }}
  >
    <div className="step-icon">
      {icon}
    </div>
    <div className="step-content">
      <h3 className="step-title">{title}</h3>
      <p className="step-description">{description}</p>
    </div>
  </div>
);

const Arrow = ({ direction, delay = 0 }) => (
  <div 
    className={`arrow ${direction}`}
    style={{ animationDelay: `${delay}ms` }}
  >
    <svg viewBox="0 0 24 24" fill="currentColor" className="arrow-icon">
      <path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"/>
    </svg>
  </div>
);

function App() {
  return (
    <div className="App">
      <div className="workflow-container">
        <header className="workflow-header">
          <h1 className="main-title">HR AUTOMATION WORKFLOW</h1>
          <p className="subtitle">Streamlined Recruitment Process</p>
        </header>

        <div className="workflow-grid">
          {/* Step 1: Job Posting Form */}
          <WorkflowStep
            title="Job Posting Form"
            description="User submits job requirements, description, and criteria"
            bgColor="bg-blue-600"
            icon="📝"
            position="step-1"
            delay={200}
          />

          <Arrow direction="arrow-right" delay={400} />

          {/* Step 2: LinkedIn Integration */}
          <WorkflowStep
            title="LinkedIn Integration"
            description="Collect resumes automatically (Limit: 1000 resumes or 2 days)"
            bgColor="bg-indigo-600"
            icon="💼"
            position="step-2"
            delay={600}
          />

          <Arrow direction="arrow-down" delay={800} />

          {/* Step 3: ATS Scoring System */}
          <WorkflowStep
            title="ATS Scoring System"
            description="AI-powered scoring to shortlist top 50 candidates"
            bgColor="bg-purple-600"
            icon="🎯"
            position="step-3"
            delay={1000}
          />

          <Arrow direction="arrow-left" delay={1200} />

          {/* Step 4: Automated Notifications (Round 1) */}
          <WorkflowStep
            title="Automated Notifications"
            description="Mail/WhatsApp notifications for selections and rejections"
            bgColor="bg-orange-600"
            icon="📧"
            position="step-4"
            delay={1400}
          />

          <Arrow direction="arrow-down" delay={1600} />

          {/* Step 5: Phone Interviews */}
          <WorkflowStep
            title="Phone Interviews"
            description="Round 2: Schedule and manage phone call interviews"
            bgColor="bg-red-600"
            icon="📞"
            position="step-5"
            delay={1800}
          />

          <Arrow direction="arrow-right" delay={2000} />

          {/* Step 6: Automated Notifications (Round 2) */}
          <WorkflowStep
            title="Automated Notifications"
            description="Mail/WhatsApp notifications for selections and rejections"
            bgColor="bg-orange-600"
            icon="📧"
            position="step-6"
            delay={2200}
          />

          <Arrow direction="arrow-down" delay={2400} />

          {/* Step 7: Schedule Meetings */}
          <WorkflowStep
            title="Schedule Meetings"
            description="User adds meeting time and credential for AI agent interview"
            bgColor="bg-green-600"
            icon="📅"
            position="step-7"
            delay={2600}
          />

          <Arrow direction="arrow-left" delay={2800} />

          {/* Step 8: AI Agent Meeting */}
          <WorkflowStep
            title="AI Agent Meeting"
            description="AI agent will take the meet and analyze the resume for 30-45 min"
            bgColor="bg-teal-600"
            icon="🤖"
            position="step-8"
            delay={3000}
          />

          <Arrow direction="arrow-down" delay={3200} />

          {/* Step 9: Interview Scoring */}
          <WorkflowStep
            title="Interview Scoring"
            description="Generate overall interview score and shortlist the top 10 ranking people"
            bgColor="bg-cyan-600"
            icon="📊"
            position="step-9"
            delay={3400}
          />

          <Arrow direction="arrow-right" delay={3600} />

          {/* Step 10: Send Mails to Shortlisted */}
          <WorkflowStep
            title="Company Head Meeting"
            description="Send mails to shortlisted people which include meeting link with the company head"
            bgColor="bg-emerald-600"
            icon="💌"
            position="step-10"
            delay={3800}
          />

          <Arrow direction="arrow-down" delay={4000} />

          {/* Step 11: Final Shortlisting */}
          <WorkflowStep
            title="Final Shortlisting"
            description="Shortlisting of further 5 people (manually by company heads)"
            bgColor="bg-rose-600"
            icon="✅"
            position="step-11"
            delay={4200}
          />
        </div>

        <div className="workflow-stats">
          <div className="stat-item">
            <span className="stat-number">1000+</span>
            <span className="stat-label">Resumes Processed</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">50</span>
            <span className="stat-label">Initial Shortlist</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">10</span>
            <span className="stat-label">Final Selection</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">2 Days</span>
            <span className="stat-label">Collection Time</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">30-45 Min</span>
            <span className="stat-label">AI Interview</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">100%</span>
            <span className="stat-label">Automated</span>
          </div>
        </div>

        <footer className="workflow-footer">
          <p>🚀 Powered by AI-driven recruitment technology</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
