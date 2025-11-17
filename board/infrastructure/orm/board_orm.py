from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config.database.session import Base

class BoardORM(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(2000), nullable=False)
    author_id = Column(String(255), nullable=False)  # 인증된 사용자 ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
