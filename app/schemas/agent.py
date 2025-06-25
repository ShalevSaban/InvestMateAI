from pydantic import BaseModel, EmailStr
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


class AgentOut(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True
