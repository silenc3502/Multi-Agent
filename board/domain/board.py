from typing import Optional
from datetime import datetime

class Board:
    def __init__(self, title: str, content: str, author_id: str):
        self.id: Optional[int] = None
        self.title = title
        self.content = content
        self.author_id = author_id  # 인증된 사용자 필드
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    def update(self, title: str, content: str):
        self.title = title
        self.content = content
        self.updated_at = datetime.utcnow()
