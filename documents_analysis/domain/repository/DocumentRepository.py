from abc import ABC, abstractmethod
from typing import List, Optional

from documents_analysis.domain.entity.document import DocumentAnalysisResult


class DocumentRepository(ABC):
    @abstractmethod
    def save(self, document: DocumentAnalysisResult) -> None:
        pass

    @abstractmethod
    def find_by_id(self, document_id: str) -> Optional[DocumentAnalysisResult]:
        pass

    @abstractmethod
    def list_all(self) -> List[DocumentAnalysisResult]:
        pass
