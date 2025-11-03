import boto3

from typing import BinaryIO
import os

from documents.domain.port.storage_port import StoragePort


class S3StorageAdapter(StoragePort):
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "ap-northeast-2"),
        )
        self.bucket_name = bucket_name

    def upload_file(self, file: BinaryIO, filename: str) -> str:
        self.s3.upload_fileobj(file, self.bucket_name, filename)
        return f"https://{self.bucket_name}.s3.amazonaws.com/{filename}"
