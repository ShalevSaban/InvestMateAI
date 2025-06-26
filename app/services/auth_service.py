from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.agent import Agent
from app.utils.jwt import create_access_token
from app.schemas.agent import AgentCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)


def create_agent(db: Session, agent_data: AgentCreate) -> Agent:
    agent = Agent(
        full_name=agent_data.full_name,
        phone_number=agent_data.phone_number,
        email=agent_data.email,
        password_hash=hash_password(agent_data.password)
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


def authenticate_user(db: Session, email: str, password: str) -> Agent | None:
    agent = db.query(Agent).filter(Agent.email == email).first()
    if not agent or not verify_password(password, agent.password_hash):
        return None
    return agent


def login_agent(db: Session, email: str, password: str) -> str | None:
    agent = authenticate_user(db, email, password)
    if not agent:
        return None
    token = create_access_token({"sub": agent.email})
    return token
