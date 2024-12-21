from pydantic import BaseModel


class TokenResponseModel(BaseModel):
    token_type: str
    access_token: str
