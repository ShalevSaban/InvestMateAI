from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CachedCriteria
from app.services.chat_service import process_chat_question
from app.services.cache_service import CacheService
from app.services.conversation_cache import ConversationCache

router = APIRouter(prefix="/gpt", tags=["GPT"])

from typing import Optional
from uuid import UUID


@router.post("/chat")
@router.post("/chat/")
def chat_with_gpt(
        question: str = Body(..., embed=True),
        agent_id: Optional[UUID] = Body(None, embed=True),
        db: Session = Depends(get_db),
):
    return process_chat_question(question, db, agent_id)


@router.get("/cache/stats")
def get_cache_stats():
    """Returns cache statistics"""
    return CacheService.get_cache_stats()


@router.delete("/cache/clear")
def clear_cache():
    """Clears all cache (development only)"""
    CacheService.clear_all_criteria()
    return {"message": "Cache cleared successfully"}


@router.delete("/cache/clearOldCache")
def clear_criteria_cache(db: Session = Depends(get_db)):
    deleted = db.query(CachedCriteria).delete()
    db.commit()
    return {"message": f"Deleted {deleted} cached criteria"}


@router.get("/conversations/{agent_id}")
def get_agent_conversations(
        agent_id: str,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """Get conversation history for agent"""
    conversations = ConversationCache.get_agent_conversations(agent_id, limit)
    return {
        "agent_id": agent_id,
        "count": len(conversations),
        "conversations": conversations
    }


@router.delete("/conversations/{agent_id}")
def delete_agent_conversations(agent_id: str):
    """Delete all conversations for agent"""
    deleted = ConversationCache.delete_agent_conversations(agent_id)
    return {"message": f"Deleted {deleted} conversations"}
