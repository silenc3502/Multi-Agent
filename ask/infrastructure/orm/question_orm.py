from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Text

from config.database.session import Base


class QuestionOrm(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asker_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)