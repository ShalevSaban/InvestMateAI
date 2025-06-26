from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.agent import AgentCreate, AgentOut, AgentUpdate
from app.services.agent_service import (
    create_agent, get_all_agents, get_agent,
    update_agent, delete_agent
)
from app.database import get_db

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
