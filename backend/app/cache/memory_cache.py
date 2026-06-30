import time


class MemoryCache:
    def __init__(self):
        self._cache = {}

    def get(self, key):
        cached_item = self._cache.get(key)

        if cached_item is None:
            return None

        expires_at = cached_item["expires_at"]

        if time.time() > expires_at:
            del self._cache[key]
            return None

        return cached_item["value"]

    def set(self, key, value, ttl_seconds):
        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl_seconds,
        }


memory_cache = MemoryCache()