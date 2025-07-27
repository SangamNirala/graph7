import React, { createContext, useContext, useState, useEffect } from 'react';

// Create PWA Context
const PWAContext = createContext();

// PWA Provider Component
export const PWAProvider = ({ children }) => {
  const [isInstallable, setIsInstallable] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [updateAvailable, setUpdateAvailable] = useState(false);
  const [swRegistration, setSwRegistration] = useState(null);
  const [installPromptShown, setInstallPromptShown] = useState(false);

  // Check if app is installed
  useEffect(() => {
    const checkInstalled = () => {
      if (window.matchMedia('(display-mode: standalone)').matches) {
        setIsInstalled(true);
      }
    };
    
    checkInstalled();
    
    // Listen for display mode changes
    const mediaQuery = window.matchMedia('(display-mode: standalone)');
    mediaQuery.addEventListener('change', checkInstalled);
    
    return () => mediaQuery.removeEventListener('change', checkInstalled);
  }, []);

  // Register service worker
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      registerServiceWorker();
    }
  }, []);

  const registerServiceWorker = async () => {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js');
      setSwRegistration(registration);
      console.log('Service Worker registered:', registration);
      
      // Check for updates
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            setUpdateAvailable(true);
          }
        });
      });
      
      // Listen for messages from service worker
      navigator.serviceWorker.addEventListener('message', (event) => {
        handleServiceWorkerMessage(event);
      });
      
    } catch (error) {
      console.error('Service Worker registration failed:', error);
    }
  };

  const handleServiceWorkerMessage = (event) => {
    const { type, data } = event.data;
    
    switch (type) {
      case 'NETWORK_STATUS':
        setIsOnline(data.online);
        break;
      case 'RETRY_SUCCESS':
        console.log('Request retry successful:', data.url);
        break;
      default:
        console.log('Unknown message from service worker:', event.data);
    }
  };

  // Handle install prompt
  useEffect(() => {
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setIsInstallable(true);
      
      // Show install prompt after a delay if not shown before
      if (!installPromptShown) {
        setTimeout(() => {
          showInstallPrompt();
        }, 30000); // Show after 30 seconds
      }
    };
    
    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    
    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, [installPromptShown]);

  // Handle app installed
  useEffect(() => {
    const handleAppInstalled = () => {
      setIsInstalled(true);
      setIsInstallable(false);
      setDeferredPrompt(null);
      console.log('PWA installed successfully');
    };
    
    window.addEventListener('appinstalled', handleAppInstalled);
    
    return () => {
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  // Handle online/offline events
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Show install prompt
  const showInstallPrompt = async () => {
    if (!deferredPrompt) return false;
    
    try {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      
      if (outcome === 'accepted') {
        console.log('User accepted install prompt');
        setInstallPromptShown(true);
      } else {
        console.log('User dismissed install prompt');
      }
      
      setDeferredPrompt(null);
      setIsInstallable(false);
      
      return outcome === 'accepted';
    } catch (error) {
      console.error('Install prompt failed:', error);
      return false;
    }
  };

  // Update service worker
  const updateServiceWorker = async () => {
    if (!swRegistration) return;
    
    try {
      const newWorker = swRegistration.waiting;
      if (newWorker) {
        newWorker.postMessage({ type: 'SKIP_WAITING' });
        setUpdateAvailable(false);
        window.location.reload();
      }
    } catch (error) {
      console.error('Service worker update failed:', error);
    }
  };

  // Clear cache
  const clearCache = async () => {
    if (!swRegistration) return;
    
    try {
      const messageChannel = new MessageChannel();
      messageChannel.port1.onmessage = (event) => {
        if (event.data.success) {
          console.log('Cache cleared successfully');
        }
      };
      
      swRegistration.active.postMessage(
        { type: 'CLEAR_CACHE' },
        [messageChannel.port2]
      );
    } catch (error) {
      console.error('Clear cache failed:', error);
    }
  };

  // Request notification permission
  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      const permission = await Notification.requestPermission();
      return permission === 'granted';
    }
    return false;
  };

  // Show notification
  const showNotification = (title, options = {}) => {
    if ('Notification' in window && Notification.permission === 'granted') {
      return new Notification(title, {
        icon: '/favicon.ico',
        badge: '/favicon.ico',
        ...options
      });
    }
    return null;
  };

  // Add to home screen prompt
  const addToHomeScreen = () => {
    if (deferredPrompt) {
      return showInstallPrompt();
    } else if (isInstallable) {
      // Manual instructions for iOS
      return showIOSInstallInstructions();
    }
    return false;
  };

  // Show iOS install instructions
  const showIOSInstallInstructions = () => {
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    const isSafari = /Safari/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent);
    
    if (isIOS && isSafari) {
      alert('To install this app on your iOS device, tap the share button and select "Add to Home Screen"');
      return true;
    }
    
    return false;
  };

  // Get PWA capabilities
  const getPWACapabilities = () => {
    return {
      serviceWorker: 'serviceWorker' in navigator,
      notifications: 'Notification' in window,
      pushManager: 'PushManager' in window,
      backgroundSync: 'serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype,
      periodicBackgroundSync: 'serviceWorker' in navigator && 'periodicSync' in window.ServiceWorkerRegistration.prototype,
      webShare: 'share' in navigator,
      storage: 'storage' in navigator,
      badging: 'setAppBadge' in navigator,
      shortcuts: 'getInstalledRelatedApps' in navigator
    };
  };

  // Share content
  const shareContent = async (data) => {
    if ('share' in navigator) {
      try {
        await navigator.share(data);
        return true;
      } catch (error) {
        console.error('Share failed:', error);
        return false;
      }
    }
    
    // Fallback to clipboard
    if (navigator.clipboard && data.url) {
      try {
        await navigator.clipboard.writeText(data.url);
        return true;
      } catch (error) {
        console.error('Clipboard write failed:', error);
      }
    }
    
    return false;
  };

  // Set app badge
  const setAppBadge = (count = 0) => {
    if ('setAppBadge' in navigator) {
      navigator.setAppBadge(count);
    }
  };

  // Clear app badge
  const clearAppBadge = () => {
    if ('clearAppBadge' in navigator) {
      navigator.clearAppBadge();
    }
  };

  // Get network information
  const getNetworkInfo = () => {
    if ('connection' in navigator) {
      const connection = navigator.connection;
      return {
        effectiveType: connection.effectiveType,
        downlink: connection.downlink,
        rtt: connection.rtt,
        saveData: connection.saveData
      };
    }
    return null;
  };

  const contextValue = {
    isInstallable,
    isInstalled,
    isOnline,
    updateAvailable,
    swRegistration,
    showInstallPrompt,
    addToHomeScreen,
    updateServiceWorker,
    clearCache,
    requestNotificationPermission,
    showNotification,
    shareContent,
    setAppBadge,
    clearAppBadge,
    getNetworkInfo,
    getPWACapabilities
  };

  return (
    <PWAContext.Provider value={contextValue}>
      {children}
    </PWAContext.Provider>
  );
};

// Hook to use PWA context
export const usePWA = () => {
  const context = useContext(PWAContext);
  if (!context) {
    throw new Error('usePWA must be used within a PWAProvider');
  }
  return context;
};

// Install Banner Component
export const InstallBanner = ({ onInstall, onDismiss }) => {
  const { isInstallable, addToHomeScreen } = usePWA();
  const [dismissed, setDismissed] = useState(false);

  const handleInstall = async () => {
    const success = await addToHomeScreen();
    if (success) {
      onInstall && onInstall();
    }
    setDismissed(true);
  };

  const handleDismiss = () => {
    setDismissed(true);
    onDismiss && onDismiss();
  };

  if (!isInstallable || dismissed) {
    return null;
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 bg-blue-600 text-white p-4 rounded-lg shadow-lg z-50 flex items-center justify-between">
      <div>
        <h3 className="font-semibold">Install AI Interview Platform</h3>
        <p className="text-sm opacity-90">Install this app on your device for a better experience</p>
      </div>
      <div className="flex items-center space-x-2">
        <button
          onClick={handleInstall}
          className="bg-white text-blue-600 px-4 py-2 rounded-md font-medium hover:bg-gray-100 transition-colors"
        >
          Install
        </button>
        <button
          onClick={handleDismiss}
          className="text-white hover:text-gray-200 transition-colors"
        >
          ×
        </button>
      </div>
    </div>
  );
};

// Update Banner Component
export const UpdateBanner = () => {
  const { updateAvailable, updateServiceWorker } = usePWA();
  const [dismissed, setDismissed] = useState(false);

  const handleUpdate = () => {
    updateServiceWorker();
    setDismissed(true);
  };

  const handleDismiss = () => {
    setDismissed(true);
  };

  if (!updateAvailable || dismissed) {
    return null;
  }

  return (
    <div className="fixed top-4 left-4 right-4 bg-green-600 text-white p-4 rounded-lg shadow-lg z-50 flex items-center justify-between">
      <div>
        <h3 className="font-semibold">Update Available</h3>
        <p className="text-sm opacity-90">A new version is available. Update now?</p>
      </div>
      <div className="flex items-center space-x-2">
        <button
          onClick={handleUpdate}
          className="bg-white text-green-600 px-4 py-2 rounded-md font-medium hover:bg-gray-100 transition-colors"
        >
          Update
        </button>
        <button
          onClick={handleDismiss}
          className="text-white hover:text-gray-200 transition-colors"
        >
          Later
        </button>
      </div>
    </div>
  );
};

// Offline Banner Component
export const OfflineBanner = () => {
  const { isOnline } = usePWA();
  const [dismissed, setDismissed] = useState(false);

  const handleDismiss = () => {
    setDismissed(true);
  };

  if (isOnline || dismissed) {
    return null;
  }

  return (
    <div className="fixed top-4 left-4 right-4 bg-orange-600 text-white p-4 rounded-lg shadow-lg z-50 flex items-center justify-between">
      <div>
        <h3 className="font-semibold">You are offline</h3>
        <p className="text-sm opacity-90">Some features may be limited while offline</p>
      </div>
      <button
        onClick={handleDismiss}
        className="text-white hover:text-gray-200 transition-colors"
      >
        ×
      </button>
    </div>
  );
};

export default PWAProvider;