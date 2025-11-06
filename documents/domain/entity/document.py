from datetime import datetime
from pydantic import BaseModel

from documents.domain.value_object.file_metadata import FileMetadata
from documents.domain.value_object.file_path import FilePath
from documents.domain.value_object.file_size import FileSize

class Document(BaseModel):
    id: int | None = None
    metadata: FileMetadata
    path: FilePath
    size: FileSize
    uploaded_at: datetime | None = None
