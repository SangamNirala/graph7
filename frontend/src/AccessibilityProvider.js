import React, { createContext, useContext, useState, useEffect } from 'react';

// Create Accessibility Context
const AccessibilityContext = createContext();

// WCAG 2.1 AA Compliance Provider
export const AccessibilityProvider = ({ children }) => {
  const [accessibility, setAccessibility] = useState(() => {
    // Load saved preferences from localStorage
    const saved = localStorage.getItem('accessibility-preferences');
    return saved ? JSON.parse(saved) : {
      highContrast: false,
      fontSize: 'medium',
      reduceMotion: false,
      screenReader: false,
      keyboardNavigation: true,
      focusVisible: true,
      announcements: true
    };
  });

  // Save preferences to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('accessibility-preferences', JSON.stringify(accessibility));
    
    // Apply accessibility preferences to document
    applyAccessibilityPreferences();
  }, [accessibility]);

  const applyAccessibilityPreferences = () => {
    const root = document.documentElement;
    
    // High contrast mode
    if (accessibility.highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }
    
    // Font size adjustments
    root.classList.remove('font-small', 'font-medium', 'font-large', 'font-xlarge');
    root.classList.add(`font-${accessibility.fontSize}`);
    
    // Reduced motion
    if (accessibility.reduceMotion) {
      root.classList.add('reduce-motion');
    } else {
      root.classList.remove('reduce-motion');
    }
    
    // Screen reader optimizations
    if (accessibility.screenReader) {
      root.classList.add('screen-reader-mode');
    } else {
      root.classList.remove('screen-reader-mode');
    }
    
    // Keyboard navigation
    if (accessibility.keyboardNavigation) {
      root.classList.add('keyboard-navigation');
    } else {
      root.classList.remove('keyboard-navigation');
    }
    
    // Focus visibility
    if (accessibility.focusVisible) {
      root.classList.add('focus-visible');
    } else {
      root.classList.remove('focus-visible');
    }
  };

  const toggleHighContrast = () => {
    setAccessibility(prev => ({
      ...prev,
      highContrast: !prev.highContrast
    }));
    announceToScreenReader('High contrast mode ' + (!accessibility.highContrast ? 'enabled' : 'disabled'));
  };

  const adjustFontSize = (size) => {
    setAccessibility(prev => ({
      ...prev,
      fontSize: size
    }));
    announceToScreenReader(`Font size changed to ${size}`);
  };

  const toggleReduceMotion = () => {
    setAccessibility(prev => ({
      ...prev,
      reduceMotion: !prev.reduceMotion
    }));
    announceToScreenReader('Reduce motion ' + (!accessibility.reduceMotion ? 'enabled' : 'disabled'));
  };

  const toggleScreenReader = () => {
    setAccessibility(prev => ({
      ...prev,
      screenReader: !prev.screenReader
    }));
    announceToScreenReader('Screen reader optimizations ' + (!accessibility.screenReader ? 'enabled' : 'disabled'));
  };

  const toggleKeyboardNavigation = () => {
    setAccessibility(prev => ({
      ...prev,
      keyboardNavigation: !prev.keyboardNavigation
    }));
    announceToScreenReader('Keyboard navigation ' + (!accessibility.keyboardNavigation ? 'enabled' : 'disabled'));
  };

  const toggleAnnouncements = () => {
    setAccessibility(prev => ({
      ...prev,
      announcements: !prev.announcements
    }));
  };

  // Screen reader announcements
  const announceToScreenReader = (message) => {
    if (!accessibility.announcements) return;
    
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  };

  // Reset all accessibility settings
  const resetAccessibility = () => {
    const defaults = {
      highContrast: false,
      fontSize: 'medium',
      reduceMotion: false,
      screenReader: false,
      keyboardNavigation: true,
      focusVisible: true,
      announcements: true
    };
    setAccessibility(defaults);
    announceToScreenReader('Accessibility settings reset to default');
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (!accessibility.keyboardNavigation) return;
      
      // Alt + H: Toggle high contrast
      if (event.altKey && event.key === 'h') {
        event.preventDefault();
        toggleHighContrast();
      }
      
      // Alt + +: Increase font size
      if (event.altKey && event.key === '+') {
        event.preventDefault();
        const sizes = ['small', 'medium', 'large', 'xlarge'];
        const currentIndex = sizes.indexOf(accessibility.fontSize);
        if (currentIndex < sizes.length - 1) {
          adjustFontSize(sizes[currentIndex + 1]);
        }
      }
      
      // Alt + -: Decrease font size
      if (event.altKey && event.key === '-') {
        event.preventDefault();
        const sizes = ['small', 'medium', 'large', 'xlarge'];
        const currentIndex = sizes.indexOf(accessibility.fontSize);
        if (currentIndex > 0) {
          adjustFontSize(sizes[currentIndex - 1]);
        }
      }
      
      // Alt + M: Toggle reduced motion
      if (event.altKey && event.key === 'm') {
        event.preventDefault();
        toggleReduceMotion();
      }
      
      // Alt + R: Reset accessibility settings
      if (event.altKey && event.key === 'r') {
        event.preventDefault();
        resetAccessibility();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [accessibility]);

  // Focus management
  const skipToMain = () => {
    const main = document.querySelector('main, [role="main"], #main-content');
    if (main) {
      main.focus();
      main.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const skipToNavigation = () => {
    const nav = document.querySelector('nav, [role="navigation"], #navigation');
    if (nav) {
      nav.focus();
      nav.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const contextValue = {
    accessibility,
    toggleHighContrast,
    adjustFontSize,
    toggleReduceMotion,
    toggleScreenReader,
    toggleKeyboardNavigation,
    toggleAnnouncements,
    resetAccessibility,
    announceToScreenReader,
    skipToMain,
    skipToNavigation
  };

  return (
    <AccessibilityContext.Provider value={contextValue}>
      {/* Skip navigation links */}
      <div className="skip-links">
        <button 
          onClick={skipToMain}
          className="skip-link"
          onFocus={(e) => e.target.classList.add('visible')}
          onBlur={(e) => e.target.classList.remove('visible')}
        >
          Skip to main content
        </button>
        <button 
          onClick={skipToNavigation}
          className="skip-link"
          onFocus={(e) => e.target.classList.add('visible')}
          onBlur={(e) => e.target.classList.remove('visible')}
        >
          Skip to navigation
        </button>
      </div>
      
      {/* Main content wrapper with accessibility classes */}
      <div className={`app-wrapper ${
        accessibility.highContrast ? 'high-contrast' : ''
      } ${
        accessibility.fontSize === 'small' ? 'text-sm' : 
        accessibility.fontSize === 'large' ? 'text-lg' : 
        accessibility.fontSize === 'xlarge' ? 'text-xl' : 'text-base'
      } ${
        accessibility.reduceMotion ? 'reduce-motion' : ''
      } ${
        accessibility.screenReader ? 'screen-reader-mode' : ''
      } ${
        accessibility.keyboardNavigation ? 'keyboard-navigation' : ''
      } ${
        accessibility.focusVisible ? 'focus-visible' : ''
      }`}>
        {children}
      </div>
    </AccessibilityContext.Provider>
  );
};

// Hook to use accessibility context
export const useAccessibility = () => {
  const context = useContext(AccessibilityContext);
  if (!context) {
    throw new Error('useAccessibility must be used within an AccessibilityProvider');
  }
  return context;
};

// HOC for accessibility features
export const withAccessibility = (Component) => {
  return function AccessibilityWrappedComponent(props) {
    const accessibility = useAccessibility();
    return <Component {...props} accessibility={accessibility} />;
  };
};