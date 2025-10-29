import json
from typing import Optional
from app.utils.redis_client import get_redis_client
from app.config import Config


class CacheService:
    """
    Service for managing search criteria cache.
    Separates business logic from Redis client.
    """

    @staticmethod
    def _get_client():
        """Helper: returns client or None"""
        return get_redis_client()

    @staticmethod
    def get_search_criteria(question: str) -> Optional[dict]:
        """
        Returns cached criteria for a question.

        Args:
            question: User's search question

        Returns:
            dict with criteria or None if not in cache
        """
        client = CacheService._get_client()
        if not client:
            return None

        try:
            key = f"criteria:{question}"
            data = client.get(key)

            if data:
                print(f"✅ Cache HIT: {question[:50]}...")
                return json.loads(data)

            print(f"❌ Cache MISS: {question[:50]}...")
            return None

        except Exception as e:
            print(f"⚠️ Cache read error: {e}")
            return None

    @staticmethod
    def save_search_criteria(question: str, criteria: dict) -> bool:
        """
        Saves criteria to cache.

        Args:
            question: User's search question
            criteria: Extracted search criteria

        Returns:
            True if saved successfully, False otherwise
        """
        client = CacheService._get_client()
        if not client:
            return False

        try:
            key = f"criteria:{question}"
            ttl = Config.CRITERIA_TTL_DAYS * 86400  # days to seconds

            # Save with TTL
            client.setex(
                key,
                ttl,
                json.dumps(criteria, ensure_ascii=False)
            )

            # Track by timestamp (for LRU cleanup)
            timestamp = client.time()[0]
            client.zadd("criteria_keys", {question: timestamp})

            # Cleanup if exceeded maximum
            CacheService._cleanup_old_entries(client)

            print(f"✅ Cached: {question[:50]}...")
            return True

        except Exception as e:
            print(f"⚠️ Cache write error: {e}")
            return False

    @staticmethod
    def _cleanup_old_entries(client):
        """Removes old entries if maximum exceeded"""
        try:
            count = client.zcard("criteria_keys")
            max_items = Config.MAX_CACHED_CRITERIA

            if count > max_items:
                # Delete oldest entries
                overflow = count - max_items
                old_keys = client.zrange("criteria_keys", 0, overflow - 1)

                for key in old_keys:
                    client.delete(f"criteria:{key}")

                client.zremrangebyrank("criteria_keys", 0, overflow - 1)

                print(f"🧹 Cleaned {len(old_keys)} old cache entries")

        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")

    @staticmethod
    def clear_all_criteria():
        """Clears all cache (for testing)"""
        client = CacheService._get_client()
        if not client:
            return

        try:
            keys = client.keys("criteria:*")
            if keys:
                client.delete(*keys)
            client.delete("criteria_keys")
            print(f"🧹 Cleared {len(keys)} cache entries")
        except Exception as e:
            print(f"⚠️ Clear error: {e}")

    @staticmethod
    def get_cache_stats() -> dict:
        """Returns cache statistics"""
        client = CacheService._get_client()
        if not client:
            return {"status": "unavailable"}

        try:
            count = client.zcard("criteria_keys")
            memory = client.info("memory").get("used_memory_human", "N/A")

            return {
                "status": "connected",
                "cached_items": count,
                "max_items": Config.MAX_CACHED_CRITERIA,
                "memory_used": memory
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}