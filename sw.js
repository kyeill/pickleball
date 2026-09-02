/* Rating Journal service worker — installable + offline.
   Shell is cache-first; data is network-first (fresh ratings) with an
   offline cache fallback. Bump CACHE to force clients onto new code. */
const CACHE = 'rj-v2';
const SHELL = ['./', './index.html', './manifest.webmanifest',
               './icons/icon-192.png', './icons/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const u = new URL(e.request.url);
  // Data files carry a cache-busting query; key the cache on the bare path so
  // the offline fallback still resolves.
  if (u.pathname.endsWith('/data.json') || u.pathname.endsWith('/overrides.json')) {
    const key = u.origin + u.pathname;
    e.respondWith(
      fetch(e.request).then(r => {
        const cp = r.clone();
        caches.open(CACHE).then(c => c.put(key, cp));
        return r;
      }).catch(() => caches.match(key)));
    return;
  }
  e.respondWith(caches.match(e.request).then(c => c || fetch(e.request)));
});
