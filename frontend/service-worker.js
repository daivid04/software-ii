// Service Worker para caché offline
const CACHE_NAME = 'taller-diego-v5';
const STATIC_CACHE = 'static-v5';
const API_CACHE = 'api-v5';

// Assets estáticos para cachear
const STATIC_ASSETS = [
  './views/inventory.html',
  './views/service.html',
  './views/index.html',
  './styles/css/inventory.css',
  './styles/css/side_bar.css',
  './styles/css/header.css',
  './styles/css/main.css',
  './assets/icons/home.png',
  './assets/icons/package.png',
  './assets/icons/toolbox.png',
  './assets/icons/search.png',
  'https://fonts.googleapis.com/css2?family=Istok+Web:wght@400;700&display=swap'
];

// Instalar Service Worker
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        return cache.addAll(STATIC_ASSETS);
      })
      .catch(err => console.error('Error cacheando assets:', err))
  );
  self.skipWaiting();
});

// Activar Service Worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== STATIC_CACHE && cache !== API_CACHE) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
  return self.clients.claim();
});

// Interceptar peticiones
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);


  if (request.method !== 'GET') {
    // Simplemente pasar al navegador sin interceptar
    return;
  }

  // Si la petición es a otro origen (ej. backend en otro puerto), no interceptar
  if (url.origin !== self.location.origin) {
    event.respondWith(fetch(request));
    return;
  }

  // Peticiones a la API (mismo origen) -> solo red, sin cachear
  if (url.pathname.startsWith('/api/v1/')) {
    event.respondWith(
      fetch(request).catch(() => new Response(
        JSON.stringify({ error: 'offline' }),
        {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        }
      ))
    );
    return;
  }

  // Estrategia diferenciada según tipo de recurso
  // HTML: Network First (siempre datos frescos)
  // CSS/JS/Imágenes: Cache First (rendimiento)

  const isHTMLRequest = request.headers.get('accept')?.includes('text/html') ||
    url.pathname.endsWith('.html');

  if (isHTMLRequest) {
    // Network First para HTML - siempre intenta obtener contenido fresco
    event.respondWith(
      fetch(request)
        .then(response => {
          // Cachear la nueva respuesta
          if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(STATIC_CACHE).then(cache => {
              cache.put(request, responseClone);
            });
          }
          return response;
        })
        .catch(err => {
          // Solo si falla la red, usar caché
          console.log('Service Worker: Red no disponible, usando caché para:', request.url);
          return caches.match(request)
            .then(cached => cached || new Response(null, { status: 504 }));
        })
    );
  } else {
    // Cache First para assets estáticos (CSS, JS, imágenes)
    event.respondWith(
      caches.match(request)
        .then(cached => {
          if (cached) {
            console.log('Service Worker: Sirviendo desde caché:', request.url);
            return cached;
          }

          return fetch(request)
            .then(response => {
              // Cachear la nueva respuesta
              if (response && response.status === 200) {
                const responseClone = response.clone();
                caches.open(STATIC_CACHE).then(cache => {
                  cache.put(request, responseClone);
                });
              }
              return response;
            });
        })
        .catch(err => {
          console.error('Service Worker: Error en fetch:', err);
          return new Response(null, { status: 504 });
        })
    );
  }
});
