from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.agent import AgentCreate, AgentOut, AgentUpdate
from app.services.agent_service import (
    create_agent, get_all_agents, get_agent,
    update_agent, delete_agent
)
from app.database import get_db
from app.services.cleanup_service import keep_last_10_conversations_per_agent, delete_old_conversations_for_agent
from app.models.conversation import Conversation, Message

from app.models import Agent  # כדי לעבוד ישירות מול הטבלה

router = APIRouter()


@router.post("/", response_model=AgentOut, status_code=201)
def create_agent_route(agent: AgentCreate, db: Session = Depends(get_db)):
    return create_agent(agent, db)


@router.get("/", response_model=list[AgentOut])
def get_agents_route(db: Session = Depends(get_db)):
    return get_all_agents(db)


@router.get("/{agent_id}", response_model=AgentOut)
def get_agent_route(agent_id: str, db: Session = Depends(get_db)):
    return get_agent(agent_id, db)


@router.put("/{agent_id}", response_model=AgentOut)
def update_agent_route(agent_id: str, updates: AgentUpdate, db: Session = Depends(get_db)):
    return update_agent(agent_id, updates, db)


@router.delete("/{agent_id}", status_code=204)
def delete_agent_route(agent_id: str, db: Session = Depends(get_db)):
    delete_agent(agent_id, db)
    return


@router.delete("/chats/keep_last_10_per_agent", summary="Keep only the last 10 conversations per agent")
def cleanup_old_chats(db: Session = Depends(get_db)):
    return keep_last_10_conversations_per_agent(db)


@router.get("/{agent_id}/telegram-link")
def get_agent_telegram_link(agent_id: UUID, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == str(agent_id)).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    link = f"https://t.me/InvestMateAI_bot?start={agent_id}"
    return {"agent_id": str(agent_id), "telegram_link": link}


# ===== לינק לפי שם =====
@router.get("/by-name/{agent_name}/telegram-link")
def get_agents_by_name_telegram_links(agent_name: str, db: Session = Depends(get_db)):
    """
    מחזיר לינקים לכל הסוכנים ששמם מתאים ל-agent_name (חיפוש case-insensitive)
    """
    agents = db.query(Agent).filter(Agent.full_name.ilike(f"%{agent_name}%")).all()

    if not agents:
        raise HTTPException(status_code=404, detail="No agents found with that name")

    results = []
    for agent in agents:
        link = f"https://t.me/InvestMateAI_bot?start={agent.id}"
        results.append({
            "agent_id": str(agent.id),
            "full_name": agent.full_name,
            "telegram_link": link
        })

    return {"count": len(results), "agents": results}


@router.delete("/{agent_id}/conversations/cleanup", summary="Delete agent's old conversations")
def cleanup_agent_conversations_route(
        agent_id: str,
        days: int = 2,
        db: Session = Depends(get_db)
):
    # וידוא שהסוכן קיים
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if days < 1:
        raise HTTPException(status_code=400, detail="Days must be at least 1")

    try:
        result = delete_old_conversations_for_agent(db, agent_id, days)

        return {
            "message": f"Successfully cleaned up conversations for {agent.full_name}",
            "agent_name": agent.full_name,
            "agent_id": agent_id,
            "days_kept": days,
            **result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")
