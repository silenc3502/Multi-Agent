from datetime import datetime
from pydantic import BaseModel


class Summary(BaseModel):
    id: int | None = None
    document_id: int
    bullet: str | None = None
    abstract: str | None = None
    casual: str | None = None
    final_summary: str | None = None
    created_at: datetime | None = None
