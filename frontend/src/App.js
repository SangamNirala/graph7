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

const CurvedArrow = ({ direction, delay = 0, style = {} }) => {
  const getArrowPath = () => {
    switch(direction) {
      case 'arrow-right':
        return {
          path: "M5,30 Q40,10 75,30",
          marker: "M70,25 L80,30 L70,35 Z",
          viewBox: "0 0 85 60"
        };
      case 'arrow-down':
        return {
          path: "M30,5 Q10,40 30,75", 
          marker: "M25,70 L30,80 L35,70 Z",
          viewBox: "0 0 60 85"
        };
      case 'arrow-left':
        return {
          path: "M75,30 Q40,10 5,30",
          marker: "M10,25 L0,30 L10,35 Z", 
          viewBox: "0 0 85 60"
        };
      default:
        return {
          path: "M5,30 Q40,10 75,30",
          marker: "M70,25 L80,30 L70,35 Z",
          viewBox: "0 0 85 60"
        };
    }
  };

  const { path, marker, viewBox } = getArrowPath();

  return (
    <div 
      className={`curved-arrow ${direction}`}
      style={{ animationDelay: `${delay}ms`, ...style }}
    >
      <svg 
        width="100%" 
        height="100%" 
        viewBox={viewBox}
        className="arrow-svg"
      >
        <defs>
          <linearGradient id={`arrowGradient-${direction}-${delay}`} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#ef4444" />
            <stop offset="50%" stopColor="#dc2626" />
            <stop offset="100%" stopColor="#b91c1c" />
          </linearGradient>
        </defs>
        
        <path
          d={path}
          stroke={`url(#arrowGradient-${direction}-${delay})`}
          strokeWidth="4"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="arrow-path"
        />
        
        <path
          d={marker}
          fill={`url(#arrowGradient-${direction}-${delay})`}
          className="arrow-head"
        />
      </svg>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <div className="workflow-container">
        <header className="workflow-header">
          <h1 className="main-title">HR AUTOMATION</h1>
          <p className="subtitle">Professional Recruitment Process</p>
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

          <CurvedArrow direction="arrow-right" delay={400} />

          {/* Step 2: LinkedIn Integration */}
          <WorkflowStep
            title="LinkedIn Integration"
            description="Collect resumes automatically (Limit: 1000 resumes or 2 days)"
            bgColor="bg-purple-600"
            icon="💼"
            position="step-2"
            delay={600}
          />

          <CurvedArrow direction="arrow-down" delay={800} />

          {/* Step 3: ATS Scoring System */}
          <WorkflowStep
            title="ATS Scoring System"
            description="AI-powered scoring to shortlist top 50 candidates"
            bgColor="bg-black"
            icon="🎯"
            position="step-3"
            delay={1000}
          />

          <CurvedArrow direction="arrow-left" delay={1200} />

          {/* Step 4: Automated Notifications (Round 1) */}
          <WorkflowStep
            title="Automated Notifications"
            description="Mail/WhatsApp notifications for selections and rejections"
            bgColor="bg-blue-700"
            icon="📧"
            position="step-4"
            delay={1400}
          />

          <CurvedArrow direction="arrow-down" delay={1600} />

          {/* Step 5: Phone Interviews */}
          <WorkflowStep
            title="Phone Interviews"
            description="Round 2: Schedule and manage phone call interviews"
            bgColor="bg-purple-700"
            icon="📞"
            position="step-5"
            delay={1800}
          />

          <CurvedArrow direction="arrow-right" delay={2000} />

          {/* Step 6: Automated Notifications (Round 2) */}
          <WorkflowStep
            title="Automated Notifications"
            description="Mail/WhatsApp notifications for selections and rejections"
            bgColor="bg-blue-700"
            icon="📧"
            position="step-6"
            delay={2200}
          />

          <CurvedArrow direction="arrow-down" delay={2400} />

          {/* Step 7: Schedule Meetings */}
          <WorkflowStep
            title="Schedule Meetings"
            description="User adds meeting time and credentials for AI agent interview"
            bgColor="bg-black"
            icon="📅"
            position="step-7"
            delay={2600}
          />

          <CurvedArrow direction="arrow-left" delay={2800} />

          {/* Step 8: AI Agent Meeting */}
          <WorkflowStep
            title="AI Agent Meeting"
            description="AI agent will take the meet and analyze the resume for 30–45 mins"
            bgColor="bg-purple-600"
            icon="🤖"
            position="step-8"
            delay={3000}
          />

          <CurvedArrow direction="arrow-down" delay={3200} />

          {/* Step 9: Interview Scoring */}
          <WorkflowStep
            title="Interview Scoring"
            description="Generate overall interview score and shortlist the top 10"
            bgColor="bg-blue-600"
            icon="📊"
            position="step-9"
            delay={3400}
          />

          <CurvedArrow direction="arrow-right" delay={3600} />

          {/* Step 10: Shortlist Notification */}
          <WorkflowStep
            title="Shortlist Notification"
            description="Send mail to shortlisted candidates with meeting link with company head"
            bgColor="bg-black"
            icon="💌"
            position="step-10"
            delay={3800}
          />

          <CurvedArrow direction="arrow-down" delay={4000} />

          {/* Step 11: Final Shortlisting */}
          <WorkflowStep
            title="Final Shortlisting"
            description="Company heads manually shortlist top 5 candidates"
            bgColor="bg-purple-700"
            icon="✅"
            position="step-11"
            delay={4200}
          />

          <CurvedArrow direction="arrow-left" delay={4400} />

          {/* Step 12: Offer Letter Dispatch */}
          <WorkflowStep
            title="Offer Letter Dispatch"
            description="Send email to selected candidates with personalized offer letter (PDF)"
            bgColor="bg-blue-700"
            icon="📄"
            position="step-12"
            delay={4600}
          />

          <CurvedArrow direction="arrow-down" delay={4800} />

          {/* Step 13: Onboarding Steps */}
          <WorkflowStep
            title="Onboarding Steps"
            description="Send email for document collection, system provisioning, and training assignment"
            bgColor="bg-black"
            icon="📋"
            position="step-13"
            delay={5000}
          />

          <CurvedArrow direction="arrow-right" delay={5200} />

          {/* Step 14: Orientation & Training */}
          <WorkflowStep
            title="Orientation & Training"
            description="Send email about orientation and training modules"
            bgColor="bg-purple-600"
            icon="🎓"
            position="step-14"
            delay={5400}
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
            <span className="stat-label">Interview Scored</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">5</span>
            <span className="stat-label">Final Selection</span>
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
