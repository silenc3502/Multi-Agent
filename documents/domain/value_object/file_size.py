from pydantic import BaseModel


class FileSize(BaseModel):
    size_in_bytes: int

    @property
    def size_in_kb(self):
        return self.size_in_bytes / 1024

    def validate_size(self, max_mb: int = 5):
        if self.size_in_bytes > max_mb * 1024 * 1024:
            raise ValueError(f"파일 크기가 {max_mb}MB를 초과했습니다.")
