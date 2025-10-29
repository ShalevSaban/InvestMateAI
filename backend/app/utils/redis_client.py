import redis
from app.config import Config
from typing import Optional

_redis_client: Optional[redis.Redis] = None


def get_redis_client() -> Optional[redis.Redis]:
    global _redis_client

    if _redis_client is None:
        try:
            _redis_client = redis.from_url(
                Config.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            _redis_client.ping()
            print("✅ Redis connected successfully")
        except Exception as e:
            print(f"⚠️ Redis connection failed: {e}")
            print("⚠️ Running without cache (fallback mode)")
            _redis_client = None

    return _redis_client


def close_redis_client():
    """Close connection"""
    global _redis_client
    if _redis_client:
        _redis_client.close()
        _redis_client = None