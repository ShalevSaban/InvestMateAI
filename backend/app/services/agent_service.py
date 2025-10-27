from sqlalchemy.orm import Session
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate
from werkzeug.security import generate_password_hash
from fastapi import HTTPException
from app.services.auth_service import hash_password
import uuid


def create_agent(data: AgentCreate, db: Session) -> Agent:
    if db.query(Agent).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(data.password)
    agent = Agent(
        full_name=data.full_name,
        phone_number=data.phone_number,
        email=data.email,
        password_hash=hashed_password
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


def get_all_agents(db: Session):
    return db.query(Agent).all()


def get_agent(agent_id: str, db: Session):
    agent = db.query(Agent).get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


def update_agent(agent_id: str, updates: AgentUpdate, db: Session):
    agent = get_agent(agent_id, db)

    if updates.email:
        existing = db.query(Agent).filter(Agent.email == updates.email, Agent.id != agent_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        agent.email = updates.email

    if updates.full_name:
        agent.full_name = updates.full_name
    if updates.phone_number:
        agent.phone_number = updates.phone_number
    if updates.password:
        agent.password_hash = generate_password_hash(updates.password)

    db.commit()
    db.refresh(agent)
    return agent


def delete_agent(agent_id: str, db: Session):
    agent = get_agent(agent_id, db)
    db.delete(agent)
    db.commit()
