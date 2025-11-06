from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from documents.infrastructure.config.mysql_config import Base


class DocumentORM(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    s3_url = Column(String(1024), nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
