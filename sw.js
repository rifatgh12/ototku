/* OtotKu - Service Worker for Offline & PWA Support (v3 - Creatine & Mobile Ready) */
const CACHE_NAME = 'ototku-cache-v3';
const CORE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './qrcode.min.js',
  './icon.svg',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable.png',
  './apple-touch-icon.png',
  './favicon.png'
];

// Hosts that serve dynamic Cloud Database / Sync API responses (NEVER cache these)
const BYPASS_HOSTS = [
  'api.restful-api.dev',
  'ntfy.sh',
  'supabase.co',
  'firebaseio.com',
  'firebasedatabase.app',
  'googleapis.com',
  'api.github.com',
  'raw.githubusercontent.com'
];

// Install: Cache core assets immediately
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(CORE_ASSETS).catch(err => {
        console.warn('Gagal caching beberapa aset saat install:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate: Clean up previous version caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Bypass Cloud DB APIs, Network-first for HTML/JSON, Stale-while-revalidate for static assets
self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  // Skip non-GET and non-http requests
  if (req.method !== 'GET' || !url.protocol.startsWith('http')) {
    return;
  }

  // Never cache dynamic database / sync requests or SSE streams
  if (
    BYPASS_HOSTS.some(h => url.hostname === h || url.hostname.endsWith('.' + h)) ||
    url.pathname.endsWith('/db.json') ||
    req.headers.get('accept') === 'text/event-stream'
  ) {
    return;
  }

  // Network-first for HTML navigation so GitHub Pages updates appear immediately
  if (req.mode === 'navigate' || url.pathname.endsWith('/') || url.pathname.endsWith('/index.html')) {
    event.respondWith(
      fetch(req).then(networkResponse => {
        if (networkResponse && networkResponse.status === 200) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(req, clone));
        }
        return networkResponse;
      }).catch(() => {
        return caches.match(req).then(r => r || caches.match('./index.html'));
      })
    );
    return;
  }

  // Stale-while-revalidate for static assets (icons, scripts, fonts)
  event.respondWith(
    caches.match(req).then(cachedResponse => {
      const fetchPromise = fetch(req).then(networkResponse => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(req, responseToCache);
          });
        }
        return networkResponse;
      }).catch(() => null);

      return cachedResponse || fetchPromise;
    })
  );
});
