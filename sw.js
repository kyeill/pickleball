/* Rating Journal service worker — installable + offline.
   Network-first for everything (so a new deploy always reaches you), with a
   cache fallback that keeps the app usable offline. Bump CACHE on shell changes. */
const CACHE = 'rj-v7';
const SHELL = ['./', './index.html', './manifest.webmanifest', './favicon.svg',
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
  // Never touch cross-origin requests (e.g. the GitHub API save calls).
  if (u.origin !== self.location.origin) return;
  // Data files carry a cache-busting query; key the cache on the bare path.
  const key = (u.pathname.endsWith('/data.json') || u.pathname.endsWith('/overrides.json'))
    ? u.origin + u.pathname : e.request;
  e.respondWith(
    fetch(e.request).then(r => {
      const cp = r.clone();
      caches.open(CACHE).then(c => c.put(key, cp));
      return r;
    }).catch(() => caches.match(key)));
});
