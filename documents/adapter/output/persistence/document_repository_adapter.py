from documents.infrastructure.config.mysql_config import SessionLocal
from documents.domain.entity.document import Document
from documents.domain.port.document_repository_port import DocumentRepositoryPort
from documents.domain.value_object.file_metadata import FileMetadata
from documents.domain.value_object.file_path import FilePath
from documents.domain.value_object.file_size import FileSize
from documents.adapter.output.persistence.document_orm import DocumentORM


class DocumentRepositoryAdapter(DocumentRepositoryPort):
    def save(self, document: Document) -> Document:
        session = SessionLocal()
        try:
            filename = f"{document.metadata.filename}.{document.metadata.extension}"
            doc_record = DocumentORM(filename=filename, s3_url=str(document.path.s3_url))

            session.add(doc_record)
            session.commit()
            session.refresh(doc_record)

            return Document(
                id=doc_record.id,
                metadata=document.metadata,
                path=document.path,
                size=document.size,
                uploaded_at=doc_record.uploaded_at
            )
        finally:
            session.close()

    def find_by_id(self, document_id: int) -> Document | None:
        session = SessionLocal()
        try:
            orm_doc = session.get(DocumentORM, document_id)
            if orm_doc is None:
                return None

            # 임시 FileMetadata는 DB에 없으므로 비워둠
            metadata = FileMetadata(filename="", extension="")

            return Document(
                id=orm_doc.id,
                metadata=metadata,
                path=FilePath(s3_url=orm_doc.s3_url),
                size=FileSize(size_in_bytes=0),  # 여기 수정됨
                uploaded_at=orm_doc.uploaded_at,
            )
        finally:
            session.close()
