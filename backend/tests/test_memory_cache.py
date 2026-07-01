import time

from app.cache.memory_cache import MemoryCache


def test_memory_cache_returns_value_before_expiration():
    cache = MemoryCache()

    cache.set("test:key", {"value": 123}, ttl_seconds=10)

    assert cache.get("test:key") == {"value": 123}


def test_memory_cache_returns_none_after_expiration():
    cache = MemoryCache()

    cache.set("test:key", "expired", ttl_seconds=0)

    time.sleep(0.01)

    assert cache.get("test:key") is None