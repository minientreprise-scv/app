const addResourcesToCache = async (resources) => {
    const cache = await caches.open("v1");
    await cache.addAll(resources);
};

const cacheFirst = async (request) => {
    const responseFromCache = await caches.match(request);
    const responseFromCacheWithOtherSite = await caches.match(request.url);
    if (navigator.onLine) {
        await addResourcesToCache([request])
        return fetch(request)
    }
    else if (responseFromCache) {
        return responseFromCache;
    } else if (responseFromCacheWithOtherSite) {
        return responseFromCacheWithOtherSite;
    } else {
        return "Error no internet";
    }
};

self.addEventListener("install", (event) => {
    event.waitUntil(
        addResourcesToCache([
            "/dashboard",
            "/static/css/bulma.min.css",
            "https://site-assets.fontawesome.com/releases/v5.15.4/css/all.css",
        ])
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(cacheFirst(event.request));
})
