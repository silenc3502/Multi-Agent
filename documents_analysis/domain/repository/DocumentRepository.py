from abc import ABC, abstractmethod
from typing import List, Optional

from documents_analysis.domain.entity.document import Document


class DocumentRepository(ABC):
    @abstractmethod
    def save(self, document: Document) -> None:
        pass

    @abstractmethod
    def find_by_id(self, document_id: str) -> Optional[Document]:
        pass

    @abstractmethod
    def list_all(self) -> List[Document]:
        pass
