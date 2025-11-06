from documents_analysis.domain.entity.document import Document


class DocumentFactory:
    @staticmethod
    def create(id: str, title: str, content: str, doc_type, metadata=None, author=None, created_at=None) -> Document:
        return Document(id=id, title=title, content=content, doc_type=doc_type, metadata=metadata, author=author, created_at=created_at)
