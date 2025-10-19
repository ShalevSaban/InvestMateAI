import json
from datetime import datetime
from typing import Optional
from app.utils.redis_client import get_redis_client
from app.config import Config


class InsightCache:
    """Manages GPT insights in Redis with automatic TTL."""

    @staticmethod
    def _get_key(agent_id: str, date: str = None) -> str:
        """Generate Redis key for insight."""
        date = date or datetime.utcnow().date().isoformat()
        return f"insight:{agent_id}:{date}"

    @staticmethod
    def get_cached_insight(agent_id: str) -> Optional[dict]:
        """Get today's cached insight."""
        client = get_redis_client()
        if not client:
            return None

        try:
            data = client.get(InsightCache._get_key(agent_id))
            return json.loads(data) if data else None
        except Exception as e:
            print(f"⚠️ Insight read error: {e}")
            return None

    @staticmethod
    def save_insight(agent_id: str, result: dict) -> bool:
        """Save insight with TTL."""
        client = get_redis_client()
        if not client:
            return False

        try:
            ttl = Config.INSIGHT_TTL_DAYS * 86400
            key = InsightCache._get_key(agent_id)

            client.setex(
                key,
                ttl,
                json.dumps(result, ensure_ascii=False)
            )
            return True
        except Exception as e:
            print(f"⚠️ Insight save error: {e}")
            return False
