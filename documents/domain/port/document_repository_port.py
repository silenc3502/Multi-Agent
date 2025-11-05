from abc import ABC, abstractmethod

from documents.domain.entity.document import Document


class DocumentRepositoryPort(ABC):
    @abstractmethod
    def save(self, document: Document) -> Document:
        """Document 엔티티를 DB에 저장"""
        pass

    @abstractmethod
    def find_by_id(self, document_id: int) -> Document | None:
        """Document 조회"""
        pass
