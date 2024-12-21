from typing import Optional
from pydantic import BaseModel


class UserBaseModel(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    id: Optional[int] = None


class UserModel(UserBaseModel):
    password: str


class LoginRequestModel(BaseModel):
    username: Optional[str] = None
    password: str
    email: Optional[str] = None
