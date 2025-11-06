from datetime import datetime
from pydantic import BaseModel


class Answer(BaseModel):
    id: int | None = None
    document_id: int
    question: str
    answer: str
    created_at: datetime | None = None
