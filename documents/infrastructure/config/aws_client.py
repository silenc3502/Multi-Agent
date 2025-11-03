import os

from documents.adapter.output.storage.s3_storage_adapter import S3StorageAdapter
from documents.application.usecase.upload_document_usecase import UploadDocumentUseCase


def get_upload_document_usecase():
    bucket_name = os.getenv("AWS_S3_BUCKET", "my-documents")
    storage_adapter = S3StorageAdapter(bucket_name)
    return UploadDocumentUseCase(storage_adapter)
