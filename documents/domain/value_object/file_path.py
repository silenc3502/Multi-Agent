from pydantic import BaseModel, HttpUrl


class FilePath(BaseModel):
    s3_url: HttpUrl

    def __eq__(self, other):
        if not isinstance(other, FilePath):
            return False
        return self.s3_url == other.s3_url

    def __str__(self):
        return str(self.s3_url)
