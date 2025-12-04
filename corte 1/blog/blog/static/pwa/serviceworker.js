// Nombre del caché (cámbialo cuando actualices tu app)
const CACHE_NAME = "blog-cache-v1";

// Archivos que se guardarán para modo offline
const urlsToCache = [
  "/",
  "/static/css/bootstrap.min.css",
  "/static/css/home.css",
  "/static/js/bootstrap.bundle.min.js",
];

// Instalar Service Worker
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log("[SW] Caching app shell");
      return cache.addAll(urlsToCache);
    })
  );

  // Forzar que el SW pase a "activated" sin esperar recarga
  self.skipWaiting();
});

// Activar y eliminar cachés viejos
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            console.log("[SW] Eliminando cache viejo:", key);
            return caches.delete(key);
          }
        })
      )
    )
  );

  // Tomar control inmediato de las páginas abiertas
  self.clients.claim();
});

// Interceptar peticiones
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      // Si está en caché, devolverlo
      if (response) return response;

      // Si no, solicitarlo a la red
      return fetch(event.request).catch(() => {
        // Si la red falla, retornar la página principal
        return caches.match("/");
      });
    })
  );
});
