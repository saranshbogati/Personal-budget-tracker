from typing import Optional
from pydantic import BaseModel


class UserModel(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
