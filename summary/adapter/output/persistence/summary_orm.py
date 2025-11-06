from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from documents.infrastructure.config.mysql_config import Base


class SummaryORM(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    bullet = Column(String(2048))
    abstract = Column(String(4096))
    casual = Column(String(4096))
    final_summary = Column(String(4096))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
