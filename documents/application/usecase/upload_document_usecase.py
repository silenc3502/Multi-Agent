from io import BytesIO

from fastapi import UploadFile

from documents.domain.port.storage_port import StoragePort
from documents.domain.port.document_repository_port import DocumentRepositoryPort
from documents.domain.entity.document import Document
from documents.domain.value_object.file_path import FilePath
from documents.domain.value_object.file_metadata import FileMetadata
from documents.domain.value_object.file_size import FileSize


class UploadDocumentUseCase:
    def __init__(
        self,
        storage_port: StoragePort,
        document_repo: DocumentRepositoryPort
    ):
        self.storage_port = storage_port
        self.document_repo = document_repo

    def execute(self, file: UploadFile, filename: str) -> Document:
        # UploadFile을 읽어서 메모리 파일로 변환
        content = file.read()  # 여기서 바로 읽기
        memory_file = BytesIO(content)

        # S3 업로드
        s3_url = self.storage_port.upload_file(memory_file, filename)

        # 메타데이터, VO 생성
        metadata = FileMetadata.from_filename(filename)
        path = FilePath(s3_url=s3_url)
        size = FileSize(size_in_bytes=len(content))

        # Document 엔티티 생성 및 DB 저장
        document = Document(metadata=metadata, path=path, size=size)
        saved_doc = self.document_repo.save(document)

        return saved_doc
