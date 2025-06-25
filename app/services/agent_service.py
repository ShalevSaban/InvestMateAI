from sqlalchemy.orm import Session
from app.models.agent import Agent
from app.schemas.agent import AgentCreate
from werkzeug.security import generate_password_hash
from fastapi import HTTPException


def create_agent(data: AgentCreate, db: Session) -> Agent:
    if db.query(Agent).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = generate_password_hash(data.password)
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
