from typing import BinaryIO

from documents.domain.port.storage_port import StoragePort


class UploadDocumentUseCase:
    def __init__(self, storage_port: StoragePort):
        self.storage_port = storage_port

    def execute(self, file: BinaryIO, filename: str) -> str:
        """문서를 S3에 업로드"""
        return self.storage_port.upload_file(file, filename)
