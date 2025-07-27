import React, { useState } from 'react';
import { useAccessibility } from './AccessibilityProvider';

// Accessibility Control Panel Component
const AccessibilityControls = ({ isOpen, onClose }) => {
  const {
    accessibility,
    toggleHighContrast,
    adjustFontSize,
    toggleReduceMotion,
    toggleScreenReader,
    toggleKeyboardNavigation,
    toggleAnnouncements,
    resetAccessibility,
    announceToScreenReader
  } = useAccessibility();

  const [isExpanded, setIsExpanded] = useState(false);

  const fontSizeOptions = [
    { value: 'small', label: 'Small', size: '14px' },
    { value: 'medium', label: 'Medium', size: '16px' },
    { value: 'large', label: 'Large', size: '18px' },
    { value: 'xlarge', label: 'Extra Large', size: '20px' }
  ];

  const handleFontSizeChange = (size) => {
    adjustFontSize(size);
  };

  const handleToggleExpanded = () => {
    setIsExpanded(!isExpanded);
    announceToScreenReader(`Accessibility panel ${!isExpanded ? 'expanded' : 'collapsed'}`);
  };

  if (!isOpen) return null;

  return (
    <div 
      className="accessibility-panel fixed top-4 right-4 bg-white/95 dark:bg-gray-900/95 backdrop-blur-lg rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50"
      role="dialog"
      aria-labelledby="accessibility-title"
      aria-describedby="accessibility-description"
    >
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <h3 id="accessibility-title" className="text-lg font-semibold text-gray-900 dark:text-white">
            <span aria-hidden="true">♿</span> Accessibility Settings
          </h3>
          <div className="flex items-center space-x-2">
            <button
              onClick={handleToggleExpanded}
              className="p-2 rounded-md bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              aria-expanded={isExpanded}
              aria-controls="accessibility-content"
              title={isExpanded ? 'Collapse panel' : 'Expand panel'}
            >
              <svg 
                className={`w-4 h-4 text-gray-600 dark:text-gray-400 transform transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <button
              onClick={onClose}
              className="p-2 rounded-md bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              aria-label="Close accessibility panel"
            >
              <svg className="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <p id="accessibility-description" className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Customize your viewing experience
        </p>
      </div>

      <div 
        id="accessibility-content"
        className={`transition-all duration-300 ${isExpanded ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0 overflow-hidden'}`}
      >
        <div className="p-4 space-y-4">
          {/* High Contrast Toggle */}
          <div className="flex items-center justify-between">
            <label htmlFor="high-contrast" className="text-sm font-medium text-gray-700 dark:text-gray-300">
              High Contrast Mode
            </label>
            <button
              id="high-contrast"
              onClick={toggleHighContrast}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                accessibility.highContrast ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
              }`}
              role="switch"
              aria-checked={accessibility.highContrast}
              aria-describedby="high-contrast-description"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  accessibility.highContrast ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          <p id="high-contrast-description" className="text-xs text-gray-500 dark:text-gray-400">
            Increases contrast for better visibility
          </p>

          {/* Font Size Adjustment */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Font Size
            </label>
            <div className="grid grid-cols-2 gap-2">
              {fontSizeOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => handleFontSizeChange(option.value)}
                  className={`px-3 py-2 text-sm rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                    accessibility.fontSize === option.value
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                  }`}
                  aria-pressed={accessibility.fontSize === option.value}
                  style={{ fontSize: option.size }}
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>

          {/* Reduce Motion Toggle */}
          <div className="flex items-center justify-between">
            <label htmlFor="reduce-motion" className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Reduce Motion
            </label>
            <button
              id="reduce-motion"
              onClick={toggleReduceMotion}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                accessibility.reduceMotion ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
              }`}
              role="switch"
              aria-checked={accessibility.reduceMotion}
              aria-describedby="reduce-motion-description"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  accessibility.reduceMotion ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          <p id="reduce-motion-description" className="text-xs text-gray-500 dark:text-gray-400">
            Minimizes animations and transitions
          </p>

          {/* Screen Reader Optimizations */}
          <div className="flex items-center justify-between">
            <label htmlFor="screen-reader" className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Screen Reader Mode
            </label>
            <button
              id="screen-reader"
              onClick={toggleScreenReader}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                accessibility.screenReader ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
              }`}
              role="switch"
              aria-checked={accessibility.screenReader}
              aria-describedby="screen-reader-description"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  accessibility.screenReader ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          <p id="screen-reader-description" className="text-xs text-gray-500 dark:text-gray-400">
            Optimizes interface for screen readers
          </p>

          {/* Keyboard Navigation */}
          <div className="flex items-center justify-between">
            <label htmlFor="keyboard-nav" className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Keyboard Navigation
            </label>
            <button
              id="keyboard-nav"
              onClick={toggleKeyboardNavigation}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                accessibility.keyboardNavigation ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
              }`}
              role="switch"
              aria-checked={accessibility.keyboardNavigation}
              aria-describedby="keyboard-nav-description"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  accessibility.keyboardNavigation ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          <p id="keyboard-nav-description" className="text-xs text-gray-500 dark:text-gray-400">
            Enhanced keyboard shortcuts and navigation
          </p>

          {/* Announcements */}
          <div className="flex items-center justify-between">
            <label htmlFor="announcements" className="text-sm font-medium text-gray-700 dark:text-gray-300">
              Screen Reader Announcements
            </label>
            <button
              id="announcements"
              onClick={toggleAnnouncements}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
                accessibility.announcements ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-700'
              }`}
              role="switch"
              aria-checked={accessibility.announcements}
              aria-describedby="announcements-description"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  accessibility.announcements ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
          <p id="announcements-description" className="text-xs text-gray-500 dark:text-gray-400">
            Announces changes and updates
          </p>

          {/* Keyboard Shortcuts Info */}
          <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Keyboard Shortcuts
            </h4>
            <div className="space-y-1 text-xs text-gray-600 dark:text-gray-400">
              <div>Alt + H: Toggle high contrast</div>
              <div>Alt + +/-: Adjust font size</div>
              <div>Alt + M: Toggle reduced motion</div>
              <div>Alt + R: Reset settings</div>
            </div>
          </div>

          {/* Reset Button */}
          <button
            onClick={resetAccessibility}
            className="w-full px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Reset to Default
          </button>
        </div>
      </div>
    </div>
  );
};

// Accessibility Button Component
export const AccessibilityButton = ({ onClick, isOpen }) => {
  const { announceToScreenReader } = useAccessibility();

  const handleClick = () => {
    onClick();
    announceToScreenReader(`Accessibility panel ${!isOpen ? 'opened' : 'closed'}`);
  };

  return (
    <button
      onClick={handleClick}
      className="fixed bottom-4 right-4 p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 z-40"
      aria-label="Open accessibility settings"
      title="Accessibility Settings (Alt + A)"
    >
      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    </button>
  );
};

export default AccessibilityControls;