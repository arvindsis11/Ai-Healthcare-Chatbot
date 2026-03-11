import hashlib
import json
import time
from typing import Any

try:
    import redis
except Exception:  # pragma: no cover
    redis = None


class InMemoryTTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._store: dict[str, tuple[float, Any]] = {}

    def _is_expired(self, key: str) -> bool:
        value = self._store.get(key)
        if not value:
            return True
        created_at, _ = value
        return (time.time() - created_at) > self.ttl_seconds

    def get(self, key: str) -> Any | None:
        if self._is_expired(key):
            self._store.pop(key, None)
            return None
        return self._store[key][1]

    def set(self, key: str, value: Any) -> None:
        self._store[key] = (time.time(), value)


def chat_cache_key(query: str) -> str:
    digest = hashlib.sha256(query.encode("utf-8")).hexdigest()
    return f"chat:{digest}"


class RedisCache:
    def __init__(self, redis_url: str, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self._client = None
        if redis is not None and redis_url:
            self._client = redis.Redis.from_url(redis_url, decode_responses=True)

    def get(self, key: str) -> Any | None:
        if self._client is None:
            return None
        value = self._client.get(key)
        if not value:
            return None
        return json.loads(value)

    def set(self, key: str, value: Any) -> None:
        if self._client is None:
            return
        self._client.setex(key, self.ttl_seconds, json.dumps(value))


class CompositeCache:
    def __init__(self, primary: RedisCache, fallback: InMemoryTTLCache):
        self.primary = primary
        self.fallback = fallback

    def get(self, key: str) -> Any | None:
        value = self.primary.get(key)
        if value is not None:
            return value
        return self.fallback.get(key)

    def set(self, key: str, value: Any) -> None:
        self.primary.set(key, value)
        self.fallback.set(key, value)
