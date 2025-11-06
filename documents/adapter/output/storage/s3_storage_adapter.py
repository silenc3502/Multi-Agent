import boto3
import os
import asyncio
from urllib.parse import urlparse

class S3StorageAdapter:
    def __init__(self, bucket_name: str, download_dir: str = "downloaded_docs"):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )
        self.bucket_name = bucket_name
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    async def download_file(self, s3_url: str) -> str:
        """
        s3://bucket/key 또는 https://bucket.s3.amazonaws.com/key 형태 모두 지원
        다운로드 위치: self.download_dir
        """
        # s3:// 처리
        if s3_url.startswith("s3://"):
            parts = s3_url.replace("s3://", "").split("/", 1)
            bucket_name = parts[0]
            object_key = parts[1]
        # https://bucket.s3.amazonaws.com/key 처리
        elif s3_url.startswith("https://"):
            parsed = urlparse(s3_url)
            bucket_name = parsed.netloc.split(".s3")[0]
            object_key = parsed.path.lstrip("/")
        else:
            raise ValueError(f"Unsupported URL scheme: {s3_url}")

        local_path = os.path.join(self.download_dir, os.path.basename(object_key))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.s3.download_file(bucket_name, object_key, local_path)
        )

        return local_path
