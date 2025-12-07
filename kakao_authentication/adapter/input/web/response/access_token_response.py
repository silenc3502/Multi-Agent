from pydantic import BaseModel

class AccessTokenResponse(BaseModel):
    user_id: int
    email: str
