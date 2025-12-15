from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

from config.database.session import Base


class AnswerOrm(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    responder_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)