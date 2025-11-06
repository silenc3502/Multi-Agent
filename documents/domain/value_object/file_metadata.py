from pydantic import BaseModel


class FileMetadata(BaseModel):
    filename: str
    extension: str

    @classmethod
    def from_filename(cls, filename: str):
        if "." not in filename:
            raise ValueError("파일 확장자가 필요합니다.")

        name, ext = filename.rsplit(".", 1)
        return cls(filename=name, extension=ext)
