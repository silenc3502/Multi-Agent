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

            # DB에서 반환받은 id와 uploaded_at을 도메인 모델에 반영
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
            doc_record = session.query(DocumentORM).filter(DocumentORM.id == document_id).first()
            if not doc_record:
                return None

            filename, ext = doc_record.filename.rsplit('.', 1)
            metadata = FileMetadata(filename=filename, extension=ext)
            path = FilePath(s3_url=doc_record.s3_url)
            size = FileSize(size_in_bytes=0)  # 실제 파일 크기 조회는 필요 시 구현

            return Document(
                id=doc_record.id,
                metadata=metadata,
                path=path,
                size=size,
                uploaded_at=doc_record.uploaded_at
            )
        finally:
            session.close()
