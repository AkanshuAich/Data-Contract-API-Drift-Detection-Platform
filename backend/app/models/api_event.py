import uuid
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.db.base import Base

class APIEvent(Base):
    __tablename__ = "api_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service = Column(String, nullable=False)
    environment = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    request_body = Column(JSONB)
    response_body = Column(JSONB)
    status_code = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
