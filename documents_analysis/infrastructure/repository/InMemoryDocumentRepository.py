from typing import List, Optional

from documents_analysis.domain.entity.document import Document
from documents_analysis.domain.repository.DocumentRepository import DocumentRepository


class InMemoryDocumentRepository(DocumentRepository):
    def __init__(self):
        self._store = {}

    async def save(self, document: Document) -> None:
        self._store[document.id] = document

    async def find_by_id(self, document_id: str) -> Optional[Document]:
        return self._store.get(document_id)

    async def list_all(self) -> List[Document]:
        return list(self._store.values())
