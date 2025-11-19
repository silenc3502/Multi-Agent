from typing import List
from documents.application.port.document_repository_port import DocumentRepositoryPort
from documents.domain.document import Document

class DocumentRepositoryImpl(DocumentRepositoryPort):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.repository = DocumentRepositoryImpl.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

            cls.__instance._documents = []
            cls.__instance._id_counter = 1

        return cls.__instance

    def save(self, document: Document) -> Document:
        if document.id is None:
            document.id = self._id_counter
            self._id_counter += 1

        self._documents.append(document)
        return document

    def find_all(self) -> List[Document]:
        return self._documents
