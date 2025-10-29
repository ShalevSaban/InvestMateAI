import json
from datetime import datetime
from typing import Optional, List, Dict
from uuid import uuid4
from app.utils.redis_client import get_redis_client
from app.config import Config


class ConversationCache:

    @staticmethod
    def save_message(agent_id: str, conversation_id: str, role: str, content: str):
        """
        Save single message and update analytics in one operation.
        Much more efficient than saving entire conversation.
        """
        client = get_redis_client()
        if not client:
            return False

        try:
            timestamp = datetime.utcnow()
            hour = (timestamp.hour + 3) % 24  # UTC+3

            message = {
                "role": role,
                "content": content,
                "timestamp": timestamp.isoformat()
            }

            # Use pipeline for atomic operations
            pipe = client.pipeline()

            # 1. Save message to list
            pipe.rpush(f"conv:{conversation_id}:messages", json.dumps(message, ensure_ascii=False))

            # 2. Set conversation metadata (first time only)
            conv_meta_key = f"conv:{conversation_id}:meta"
            pipe.hsetnx(conv_meta_key, "agent_id", agent_id)
            pipe.hsetnx(conv_meta_key, "created_at", timestamp.isoformat())

            # 3. Track conversation in agent's sorted set
            pipe.zadd(f"agent:{agent_id}:convs", {conversation_id: timestamp.timestamp()})

            # 4. Set TTL on conversation data
            ttl = Config.CONVERSATION_TTL_DAYS * 86400
            pipe.expire(f"conv:{conversation_id}:messages", ttl)
            pipe.expire(conv_meta_key, ttl)

            # 5. If user message - update analytics
            if role == "user":
                # Increment question counter
                pipe.zincrby(f"agent:{agent_id}:questions", 1, content)

                # Increment hour counter
                pipe.hincrby(f"agent:{agent_id}:hours", str(hour), 1)

            # Execute all at once
            pipe.execute()

            # 6. Cleanup old conversations (separate operation)
            ConversationCache._cleanup_old_conversations(client, agent_id)

            return True

        except Exception as e:
            print(f"⚠️ Message save error: {e}")
            return False

    @staticmethod
    def get_conversation(conversation_id: str) -> Optional[Dict]:
        """Get single conversation with messages"""
        client = get_redis_client()
        if not client:
            return None

        try:
            # Get metadata
            meta = client.hgetall(f"conv:{conversation_id}:meta")
            if not meta:
                return None

            # Get messages
            messages_json = client.lrange(f"conv:{conversation_id}:messages", 0, -1)
            messages = [json.loads(m) for m in messages_json]

            return {
                "id": conversation_id,
                "agent_id": meta.get("agent_id"),
                "created_at": meta.get("created_at"),
                "messages": messages
            }

        except Exception as e:
            print(f"⚠️ Get conversation error: {e}")
            return None

    @staticmethod
    def get_agent_conversations(agent_id: str, limit: int = None) -> List[Dict]:
        """Get last N conversations for agent"""
        client = get_redis_client()
        if not client:
            return []

        try:
            if limit is None:
                limit = Config.MAX_CONVERSATIONS_PER_AGENT

            # Get conversation IDs (newest first)
            conv_ids = client.zrevrange(f"agent:{agent_id}:convs", 0, limit - 1)

            conversations = []
            for conv_id in conv_ids:
                conv = ConversationCache.get_conversation(conv_id)
                if conv:
                    conversations.append(conv)

            return conversations

        except Exception as e:
            print(f"⚠️ Get conversations error: {e}")
            return []

    @staticmethod
    def get_faqs(agent_id: str, limit: int = 5) -> List[Dict]:
        """Get top questions - O(log N) instead of O(N)"""
        client = get_redis_client()
        if not client:
            return []

        try:
            # Get top questions with scores (already sorted!)
            questions = client.zrevrange(
                f"agent:{agent_id}:questions",
                0, limit - 1,
                withscores=True
            )

            return [
                {"question": q, "count": int(score)}
                for q, score in questions
            ]

        except Exception as e:
            print(f"⚠️ FAQs error: {e}")
            return []

    @staticmethod
    def get_peak_hours(agent_id: str) -> List[Dict]:
        """Get peak hours - O(1) instead of O(N)"""
        client = get_redis_client()
        if not client:
            return []

        try:
            # Get all hours with counts
            hour_counts = client.hgetall(f"agent:{agent_id}:hours")

            # Convert to list and sort
            result = [
                {"hour": int(hour), "count": int(count)}
                for hour, count in hour_counts.items()
            ]

            return sorted(result, key=lambda x: x["hour"])

        except Exception as e:
            print(f"⚠️ Peak hours error: {e}")
            return []

    @staticmethod
    def track_property_mention(agent_id: str, address: str):
        """Track property mention - called from search results"""
        client = get_redis_client()
        if not client:
            return

        try:
            client.zincrby(f"agent:{agent_id}:mentions", 1, address)
        except Exception as e:
            print(f"⚠️ Mention tracking error: {e}")

    @staticmethod
    def get_popular_properties(agent_id: str, db, limit: int = 5) -> List[Dict]:
        """Get properties mentioned most in conversations"""
        from app.models import Property

        client = get_redis_client()
        if not client:
            return []

        try:
            # Option 1: Use Redis mentions (NEW - faster)
            properties = client.zrevrange(
                f"agent:{agent_id}:mentions",
                0, limit - 1,
                withscores=True
            )

            return [
                {"address": addr, "mentions": int(score)}
                for addr, score in properties
            ]

        except Exception as e:
            print(f"⚠️ Popular properties error: {e}")
            return []

    @staticmethod
    def get_conversation_stats(agent_id: str) -> Dict:
        """Get stats - O(1) operations"""
        client = get_redis_client()
        if not client:
            return {}

        try:
            # Count conversations
            total_convs = client.zcard(f"agent:{agent_id}:convs")

            # Count total questions
            total_questions = int(client.get(f"agent:{agent_id}:total_questions") or 0)

            return {
                "total_conversations": total_convs,
                "total_questions": total_questions,
                "unique_questions": client.zcard(f"agent:{agent_id}:questions"),
                "hours_tracked": client.hlen(f"agent:{agent_id}:hours")
            }

        except Exception as e:
            print(f"⚠️ Stats error: {e}")
            return {}

    @staticmethod
    def _cleanup_old_conversations(client, agent_id: str):
        """Remove old conversations efficiently"""
        try:
            max_convs = Config.MAX_CONVERSATIONS_PER_AGENT
            total = client.zcard(f"agent:{agent_id}:convs")

            if total <= max_convs:
                return

            # Get oldest conversation IDs to delete
            to_delete = total - max_convs
            old_conv_ids = client.zrange(f"agent:{agent_id}:convs", 0, to_delete - 1)

            # Delete in pipeline
            pipe = client.pipeline()
            for conv_id in old_conv_ids:
                pipe.delete(f"conv:{conv_id}:messages")
                pipe.delete(f"conv:{conv_id}:meta")

            # Remove from sorted set
            pipe.zremrangebyrank(f"agent:{agent_id}:convs", 0, to_delete - 1)

            pipe.execute()

            print(f"🧹 Cleaned {len(old_conv_ids)} old conversations")

        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")

    @staticmethod
    def delete_agent_data(agent_id: str) -> int:
        """Delete all data for an agent"""
        client = get_redis_client()
        if not client:
            return 0

        try:
            # Get all conversation IDs
            conv_ids = client.zrange(f"agent:{agent_id}:convs", 0, -1)

            # Delete all keys in pipeline
            pipe = client.pipeline()

            # Conversation data
            for conv_id in conv_ids:
                pipe.delete(f"conv:{conv_id}:messages")
                pipe.delete(f"conv:{conv_id}:meta")

            # Analytics data
            pipe.delete(f"agent:{agent_id}:convs")
            pipe.delete(f"agent:{agent_id}:questions")
            pipe.delete(f"agent:{agent_id}:hours")
            pipe.delete(f"agent:{agent_id}:mentions")
            pipe.delete(f"agent:{agent_id}:total_questions")

            results = pipe.execute()
            deleted = sum(1 for r in results if r)

            print(f"🗑️ Deleted {deleted} keys for agent {agent_id}")
            return deleted

        except Exception as e:
            print(f"⚠️ Delete error: {e}")
            return 0