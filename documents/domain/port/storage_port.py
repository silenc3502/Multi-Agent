from abc import ABC, abstractmethod
from typing import BinaryIO

class StoragePort(ABC):
    """파일을 저장하기 위한 포트 인터페이스"""

    @abstractmethod
    def upload_file(self, file: BinaryIO, filename: str) -> str:
        """파일을 업로드하고 URL을 반환한다."""
        pass
