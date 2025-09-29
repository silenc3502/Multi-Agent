from dataclasses import dataclass
from typing import Dict, Optional

from documents_analysis.domain.entity.DocumentType import DocumentType


@dataclass
class Document:
    id: str
    title: Optional[str] = None
    doc_url: str = ""
    content: Optional[str] = None
    doc_type: Optional[DocumentType] = None
    metadata: Optional[Dict] = None
    author: Optional[str] = None
    created_at: Optional[str] = None