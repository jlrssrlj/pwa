const CACHE_NAME = "blog-cache-v1";
const urlsToCache = [
  "/",
  "/static/css/bootstrap.min.css",
  "/static/css/home.css",
  "/static/js/bootstrap.bundle.min.js",
];

//  service worker
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log("Caching app shell");
      return cache.addAll(urlsToCache);
    })
  );
});

// Activar y limpiar viejos caches
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keyList => {
      return Promise.all(
        keyList.map(key => {
          if (key !== CACHE_NAME) {
            console.log("Eliminando cache viejo:", key);
            return caches.delete(key);
          }
        })
      );
    })
  );
});

// Interceptar peticiones
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      // Retornar desde cache
      if (response) return response;

      // Sino, pedir a la red
      return fetch(event.request).catch(() =>
        caches.match("/")
      );
    })
  );
});
