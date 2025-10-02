from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_service import process_chat_question
from app.services.cache_service import CacheService

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