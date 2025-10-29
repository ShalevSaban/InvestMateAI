
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.agent import Agent
from app.utils.jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_agent(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> Agent:
    payload = verify_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    agent = db.query(Agent).filter_by(email=payload["sub"]).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent
