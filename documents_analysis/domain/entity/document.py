from typing import Optional
from pydantic import BaseModel
from documents_analysis.domain.entity.DocumentType import DocumentType

class DocumentAnalysisResult(BaseModel):
    id: str  # UUID
    doc_url: str
    file_type: Optional[DocumentType] = None

    bullet_summary: Optional[str] = None
    abstract_summary: Optional[str] = None
    casual_summary: Optional[str] = None
    final_summary: Optional[str] = None

    question: Optional[str] = None
    answer: Optional[str] = None
