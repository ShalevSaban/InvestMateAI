from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.agent import AgentLogin, Token
from app.services.auth_service import login_agent

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=Token)
def login(agent_data: AgentLogin, db: Session = Depends(get_db)):
    token = login_agent(db, agent_data.email, agent_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
