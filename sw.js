/* OtotKu - Service Worker for Offline & PWA Support */
const CACHE_NAME = 'ototku-cache-v1';
const CORE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './qrcode.min.js',
  './icon.svg',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  './favicon.png'
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

// Fetch: Network-first for dynamic, Cache-first / stale-while-revalidate for static assets
self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  // Skip non-GET and chrome-extension / non-http requests
  if (req.method !== 'GET' || !url.protocol.startsWith('http')) {
    return;
  }

  // Handle local files & CDN scripts
  event.respondWith(
    caches.match(req).then(cachedResponse => {
      // Fetch from network in background or foreground
      const fetchPromise = fetch(req).then(networkResponse => {
        // Cache valid responses for static assets and CDNs
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(req, responseToCache);
          });
        }
        return networkResponse;
      }).catch(err => {
        // If offline and request is HTML navigation, fallback to index.html
        if (req.mode === 'navigate') {
          return caches.match('./index.html');
        }
        return null;
      });

      // If we have cached version, return it right away; otherwise wait for network
      return cachedResponse || fetchPromise;
    })
  );
});
