from pydantic import BaseModel
from typing import List

class AddDocsRequest(BaseModel):
    documents: List[str]
