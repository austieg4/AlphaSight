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


def test_memory_cache_tracks_hits_and_misses():
    cache = MemoryCache()

    cache.set("test:key", "cached", ttl_seconds=10)

    assert cache.get("test:key") == "cached"
    assert cache.get("missing:key") is None

    stats = cache.stats()

    assert stats["items"] == 1
    assert stats["hits"] == 1
    assert stats["misses"] == 1


def test_memory_cache_clear_resets_cache_and_stats():
    cache = MemoryCache()

    cache.set("test:key", "cached", ttl_seconds=10)
    cache.get("test:key")
    cache.get("missing:key")

    cache.clear()

    stats = cache.stats()

    assert stats["items"] == 0
    assert stats["hits"] == 0
    assert stats["misses"] == 0