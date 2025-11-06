from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from documents.infrastructure.config.mysql_config import Base


class AnswerORM(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    question = Column(String(1024), nullable=False)
    answer = Column(String(4096), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
