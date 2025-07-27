import React, { createContext, useContext, useState, useEffect } from 'react';
import { translations } from './translations';

// Create I18n Context
const I18nContext = createContext();

// I18n Provider Component
export const I18nProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState(() => {
    // Try to get saved language from localStorage
    const saved = localStorage.getItem('user-language');
    if (saved) return saved;
    
    // Try to detect browser language
    const browserLang = navigator.language.split('-')[0];
    return supportedLanguages.includes(browserLang) ? browserLang : 'en';
  });

  const [direction, setDirection] = useState('ltr');

  const supportedLanguages = [
    'en', 'es', 'fr', 'de', 'it', 'pt', 'ja', 'zh'
  ];

  const languageNames = {
    en: 'English',
    es: 'Español',
    fr: 'Français',
    de: 'Deutsch',
    it: 'Italiano',
    pt: 'Português',
    ja: '日本語',
    zh: '中文'
  };

  const rtlLanguages = ['ar', 'he', 'fa', 'ur'];

  // Update document language and direction
  useEffect(() => {
    document.documentElement.lang = currentLanguage;
    const newDirection = rtlLanguages.includes(currentLanguage) ? 'rtl' : 'ltr';
    setDirection(newDirection);
    document.documentElement.dir = newDirection;
    
    // Save to localStorage
    localStorage.setItem('user-language', currentLanguage);
  }, [currentLanguage]);

  // Translation function
  const t = (key, params = {}) => {
    try {
      const keys = key.split('.');
      let value = translations[currentLanguage];
      
      for (const k of keys) {
        value = value[k];
        if (value === undefined) {
          // Fallback to English if key doesn't exist
          value = translations.en;
          for (const k of keys) {
            value = value[k];
            if (value === undefined) {
              console.warn(`Translation key "${key}" not found in ${currentLanguage} or English`);
              return key;
            }
          }
          break;
        }
      }
      
      // Replace parameters in translation
      if (typeof value === 'string') {
        return value.replace(/\{\{(\w+)\}\}/g, (match, param) => params[param] || match);
      }
      
      return value;
    } catch (error) {
      console.error(`Translation error for key "${key}":`, error);
      return key;
    }
  };

  // Pluralization function
  const tn = (key, count, params = {}) => {
    const pluralKey = count === 1 ? `${key}.singular` : `${key}.plural`;
    return t(pluralKey, { ...params, count });
  };

  // Format date according to locale
  const formatDate = (date, options = {}) => {
    return new Intl.DateTimeFormat(currentLanguage, options).format(date);
  };

  // Format number according to locale
  const formatNumber = (number, options = {}) => {
    return new Intl.NumberFormat(currentLanguage, options).format(number);
  };

  // Format currency according to locale
  const formatCurrency = (amount, currency = 'USD', options = {}) => {
    return new Intl.NumberFormat(currentLanguage, {
      style: 'currency',
      currency,
      ...options
    }).format(amount);
  };

  // Format relative time
  const formatRelativeTime = (date) => {
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
      return t('time.justNow');
    } else if (diffInSeconds < 3600) {
      const minutes = Math.floor(diffInSeconds / 60);
      return t('time.minutesAgo', { minutes });
    } else if (diffInSeconds < 86400) {
      const hours = Math.floor(diffInSeconds / 3600);
      return t('time.hoursAgo', { hours });
    } else {
      const days = Math.floor(diffInSeconds / 86400);
      return t('time.daysAgo', { days });
    }
  };

  // Change language
  const changeLanguage = (langCode) => {
    if (supportedLanguages.includes(langCode)) {
      setCurrentLanguage(langCode);
      
      // Announce language change for screen readers
      if (window.announceToScreenReader) {
        window.announceToScreenReader(t('accessibility.languageChanged', { language: languageNames[langCode] }));
      }
    }
  };

  // Get current language info
  const getCurrentLanguageInfo = () => ({
    code: currentLanguage,
    name: languageNames[currentLanguage],
    direction,
    isRTL: direction === 'rtl'
  });

  // Get all supported languages
  const getSupportedLanguages = () => {
    return supportedLanguages.map(code => ({
      code,
      name: languageNames[code],
      isRTL: rtlLanguages.includes(code)
    }));
  };

  // Load dynamic translations (for server-side content)
  const loadDynamicTranslations = async (module) => {
    try {
      const response = await fetch(`/api/translations/${currentLanguage}/${module}`);
      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Error loading dynamic translations:', error);
    }
    return {};
  };

  const contextValue = {
    currentLanguage,
    direction,
    supportedLanguages,
    languageNames,
    t,
    tn,
    formatDate,
    formatNumber,
    formatCurrency,
    formatRelativeTime,
    changeLanguage,
    getCurrentLanguageInfo,
    getSupportedLanguages,
    loadDynamicTranslations
  };

  return (
    <I18nContext.Provider value={contextValue}>
      <div className={`app-i18n ${direction}`} dir={direction}>
        {children}
      </div>
    </I18nContext.Provider>
  );
};

// Hook to use I18n context
export const useI18n = () => {
  const context = useContext(I18nContext);
  if (!context) {
    throw new Error('useI18n must be used within an I18nProvider');
  }
  return context;
};

// HOC for i18n
export const withI18n = (Component) => {
  return function I18nWrappedComponent(props) {
    const i18n = useI18n();
    return <Component {...props} i18n={i18n} />;
  };
};

// Language Selector Component
export const LanguageSelector = ({ className = '', showFlags = true }) => {
  const { currentLanguage, changeLanguage, getSupportedLanguages } = useI18n();
  const [isOpen, setIsOpen] = useState(false);
  
  const languages = getSupportedLanguages();
  const currentLang = languages.find(lang => lang.code === currentLanguage);
  
  const flagEmojis = {
    en: '🇺🇸',
    es: '🇪🇸',
    fr: '🇫🇷',
    de: '🇩🇪',
    it: '🇮🇹',
    pt: '🇵🇹',
    ja: '🇯🇵',
    zh: '🇨🇳'
  };

  const handleLanguageChange = (langCode) => {
    changeLanguage(langCode);
    setIsOpen(false);
  };

  return (
    <div className={`language-selector relative ${className}`}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 bg-white/10 backdrop-blur-lg rounded-lg border border-white/20 text-white hover:bg-white/20 transition-colors"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-label={`Current language: ${currentLang?.name}. Click to change language.`}
      >
        {showFlags && (
          <span className="text-lg" aria-hidden="true">
            {flagEmojis[currentLanguage]}
          </span>
        )}
        <span className="font-medium">{currentLang?.name}</span>
        <svg 
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      
      {isOpen && (
        <div className="absolute top-full left-0 mt-1 w-48 bg-white/95 dark:bg-gray-900/95 backdrop-blur-lg rounded-lg shadow-xl border border-white/20 dark:border-gray-700 z-50">
          <div className="py-2" role="listbox">
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => handleLanguageChange(lang.code)}
                className={`w-full flex items-center gap-3 px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors ${
                  lang.code === currentLanguage ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-300'
                }`}
                role="option"
                aria-selected={lang.code === currentLanguage}
              >
                {showFlags && (
                  <span className="text-lg" aria-hidden="true">
                    {flagEmojis[lang.code]}
                  </span>
                )}
                <span className="font-medium">{lang.name}</span>
                {lang.code === currentLanguage && (
                  <svg className="w-4 h-4 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default I18nProvider;