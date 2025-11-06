from pydantic import BaseModel

class RequestData(BaseModel):
    doc_url: str
    question: str