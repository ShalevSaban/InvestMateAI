from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.agent import AgentCreate, AgentOut
from app.services.agent_service import create_agent
from app.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=AgentOut, status_code=201)
def create_agent_route(agent: AgentCreate, db: Session = Depends(get_db)):
    return create_agent(agent, db)
