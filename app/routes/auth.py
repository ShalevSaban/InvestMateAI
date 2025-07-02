from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.agent import AgentLogin, Token
from app.services.auth_service import login_agent
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    token = login_agent(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    return JSONResponse(content={"detail": "Logged out (token deleted on client)"})



