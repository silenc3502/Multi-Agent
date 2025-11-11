from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid
from config.mysql_config import Base

class AnonymousBoard(Base):
    __tablename__ = "anonymous_board"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
