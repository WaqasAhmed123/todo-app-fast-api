
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database import Base


class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)