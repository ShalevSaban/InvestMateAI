from sqlalchemy import Column, DateTime, ForeignKey, Text, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base
import uuid


class InsightLog(Base):
    __tablename__ = "insight_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    insight_result = Column(Text, nullable=False)
