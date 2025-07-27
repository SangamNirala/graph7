// Service Worker for PWA functionality
const CACHE_NAME = 'ai-interview-platform-v1.0.0';
const STATIC_CACHE_NAME = 'static-v1.0.0';
const DYNAMIC_CACHE_NAME = 'dynamic-v1.0.0';

// Files to cache for offline functionality
const STATIC_FILES = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json',
  '/favicon.ico',
  // Add other static assets
];

// API routes to cache
const CACHEABLE_APIS = [
  '/api/candidate/validate-token',
  '/api/admin/login',
  '/api/translations/'
];

// Install event - cache static files
self.addEventListener('install', (event) => {
  console.log('Service Worker installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then((cache) => {
        console.log('Caching static files');
        return cache.addAll(STATIC_FILES);
      })
      .then(() => {
        console.log('Static files cached successfully');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('Failed to cache static files:', error);
      })
  );
});

// Activate event - cleanup old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker activating...');
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE_NAME && cacheName !== DYNAMIC_CACHE_NAME) {
              console.log('Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker activated');
        return self.clients.claim();
      })
  );
});

// Fetch event - implement caching strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Handle different types of requests
  if (request.method === 'GET') {
    if (url.pathname.startsWith('/api/')) {
      // API requests - Network First strategy
      event.respondWith(networkFirstStrategy(request));
    } else if (url.pathname.startsWith('/static/')) {
      // Static files - Cache First strategy
      event.respondWith(cacheFirstStrategy(request));
    } else {
      // HTML pages - Network First with fallback
      event.respondWith(networkFirstWithFallback(request));
    }
  } else if (request.method === 'POST') {
    // Handle POST requests (form submissions, etc.)
    event.respondWith(handlePostRequest(request));
  }
});

// Network First Strategy - for API calls
async function networkFirstStrategy(request) {
  try {
    const networkResponse = await fetch(request);
    
    // Cache successful responses
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('Network failed, trying cache:', error);
    
    // Try cache if network fails
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline response for API calls
    return new Response(JSON.stringify({
      error: 'Network unavailable',
      message: 'Please check your internet connection',
      offline: true
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Cache First Strategy - for static files
async function cacheFirstStrategy(request) {
  try {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(STATIC_CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.error('Cache first strategy failed:', error);
    return new Response('Resource not available offline', { status: 503 });
  }
}

// Network First with Fallback - for HTML pages
async function networkFirstWithFallback(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('Network failed for HTML, trying cache:', error);
    
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline page
    return caches.match('/offline.html').then((offlineResponse) => {
      return offlineResponse || new Response('Offline - Please check your connection', {
        status: 503,
        headers: { 'Content-Type': 'text/html' }
      });
    });
  }
}

// Handle POST requests
async function handlePostRequest(request) {
  try {
    const networkResponse = await fetch(request);
    return networkResponse;
  } catch (error) {
    console.log('POST request failed:', error);
    
    // Store failed POST requests for retry when online
    const requestData = {
      url: request.url,
      method: request.method,
      headers: Object.fromEntries(request.headers.entries()),
      body: await request.text(),
      timestamp: Date.now()
    };
    
    // Store in IndexedDB for background sync
    await storeFailedRequest(requestData);
    
    return new Response(JSON.stringify({
      error: 'Request failed',
      message: 'Your request has been queued and will be sent when connection is restored',
      queued: true
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Store failed requests for background sync
async function storeFailedRequest(requestData) {
  try {
    const db = await openDB();
    const transaction = db.transaction(['failedRequests'], 'readwrite');
    const store = transaction.objectStore('failedRequests');
    await store.add(requestData);
  } catch (error) {
    console.error('Failed to store request:', error);
  }
}

// Open IndexedDB
function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('AIInterviewPlatform', 1);
    
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains('failedRequests')) {
        const store = db.createObjectStore('failedRequests', { keyPath: 'id', autoIncrement: true });
        store.createIndex('timestamp', 'timestamp');
      }
    };
  });
}

// Background sync for failed requests
self.addEventListener('sync', (event) => {
  if (event.tag === 'retry-failed-requests') {
    event.waitUntil(retryFailedRequests());
  }
});

// Retry failed requests when online
async function retryFailedRequests() {
  try {
    const db = await openDB();
    const transaction = db.transaction(['failedRequests'], 'readwrite');
    const store = transaction.objectStore('failedRequests');
    const requests = await store.getAll();
    
    for (const requestData of requests) {
      try {
        const response = await fetch(requestData.url, {
          method: requestData.method,
          headers: requestData.headers,
          body: requestData.body
        });
        
        if (response.ok) {
          // Remove successful request from storage
          await store.delete(requestData.id);
          
          // Notify client of successful retry
          self.clients.matchAll().then((clients) => {
            clients.forEach((client) => {
              client.postMessage({
                type: 'RETRY_SUCCESS',
                url: requestData.url
              });
            });
          });
        }
      } catch (error) {
        console.error('Retry failed for request:', requestData.url, error);
      }
    }
  } catch (error) {
    console.error('Background sync failed:', error);
  }
}

// Push notification handling
self.addEventListener('push', (event) => {
  console.log('Push event received');
  
  const options = {
    body: event.data ? event.data.text() : 'You have a new notification',
    icon: '/favicon.ico',
    badge: '/favicon.ico',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'open',
        title: 'Open App',
        icon: '/favicon.ico'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/favicon.ico'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('AI Interview Platform', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', (event) => {
  console.log('Notification click received');
  
  event.notification.close();
  
  if (event.action === 'open') {
    event.waitUntil(
      self.clients.openWindow('/')
    );
  }
});

// Message handling from client
self.addEventListener('message', (event) => {
  console.log('Message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});

// Network status monitoring
self.addEventListener('online', () => {
  console.log('Network is online');
  
  // Trigger background sync
  self.registration.sync.register('retry-failed-requests');
  
  // Notify clients
  self.clients.matchAll().then((clients) => {
    clients.forEach((client) => {
      client.postMessage({
        type: 'NETWORK_STATUS',
        online: true
      });
    });
  });
});

self.addEventListener('offline', () => {
  console.log('Network is offline');
  
  // Notify clients
  self.clients.matchAll().then((clients) => {
    clients.forEach((client) => {
      client.postMessage({
        type: 'NETWORK_STATUS',
        online: false
      });
    });
  });
});

// Cache management utilities
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            return caches.delete(cacheName);
          })
        );
      }).then(() => {
        event.ports[0].postMessage({ success: true });
      })
    );
  }
});

// Service Worker lifecycle logging
console.log('Service Worker script loaded');

// Error handling
self.addEventListener('error', (event) => {
  console.error('Service Worker error:', event.error);
});

self.addEventListener('unhandledrejection', (event) => {
  console.error('Service Worker unhandled promise rejection:', event.reason);
});

// Performance monitoring
self.addEventListener('fetch', (event) => {
  const startTime = performance.now();
  
  event.respondWith(
    handleFetch(event.request).then((response) => {
      const endTime = performance.now();
      console.log(`Fetch completed in ${endTime - startTime}ms for ${event.request.url}`);
      return response;
    })
  );
});

// Main fetch handler
async function handleFetch(request) {
  const url = new URL(request.url);
  
  // Handle different request types
  if (request.method === 'GET') {
    if (url.pathname.startsWith('/api/')) {
      return networkFirstStrategy(request);
    } else if (url.pathname.startsWith('/static/')) {
      return cacheFirstStrategy(request);
    } else {
      return networkFirstWithFallback(request);
    }
  } else if (request.method === 'POST') {
    return handlePostRequest(request);
  }
  
  // Default fetch for other methods
  return fetch(request);
}