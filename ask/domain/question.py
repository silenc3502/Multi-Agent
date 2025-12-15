from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Question:
    id: Optional[int]
    asker_id: int
    content: str
    created_at: datetime
