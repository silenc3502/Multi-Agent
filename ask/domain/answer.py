from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Answer:
    id: Optional[int]
    question_id: int
    responder_id: int
    content: str
    created_at: datetime
