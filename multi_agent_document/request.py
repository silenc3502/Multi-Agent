from pydantic import BaseModel


class MultiAgentRequest(BaseModel):
    doc_url: str
    question: str