from typing import List

from pydantic import BaseModel


class AskRAGRequest(BaseModel):
    question: str
    context_texts: List[str] = []