import os

from documents.adapter.output.storage.s3_storage_adapter import S3StorageAdapter


def get_upload_document_usecase(repository_adapter_class, usecase_class):
    """
    repository_adapter_class: 저장 대상의 repository 어댑터 클래스
    usecase_class: 해당 도메인에 맞는 UploadUseCase 클래스
    """
    bucket_name = os.getenv("AWS_S3_BUCKET")
    storage_adapter = S3StorageAdapter(bucket_name)

    repository_adapter = repository_adapter_class()
    return usecase_class(storage_adapter, repository_adapter)
