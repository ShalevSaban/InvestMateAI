from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID


class AgentCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None


class AgentUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None


class AgentLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AgentOut(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


class AgentPublic(BaseModel):
    full_name: str
    phone_number: str

    model_config = ConfigDict(from_attributes=True)
