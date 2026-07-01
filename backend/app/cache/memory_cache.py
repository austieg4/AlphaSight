import time


class MemoryCache:
    def __init__(self):
        self._cache = {}
        self._hits = 0
        self._misses = 0

    def get(self, key):
        cached_item = self._cache.get(key)

        if cached_item is None:
            self._misses += 1
            return None

        expires_at = cached_item["expires_at"]

        if time.time() > expires_at:
            del self._cache[key]
            self._misses += 1
            return None

        self._hits += 1
        return cached_item["value"]

    def set(self, key, value, ttl_seconds):
        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl_seconds,
        }

    def stats(self):
        return {
            "items": len(self._cache),
            "hits": self._hits,
            "misses": self._misses,
        }

    def clear(self):
        self._cache = {}
        self._hits = 0
        self._misses = 0


memory_cache = MemoryCache()