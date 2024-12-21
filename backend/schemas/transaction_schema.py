from typing import Optional
from pydantic import BaseModel


class TransactionCreateSchema(BaseModel):
    id: Optional[int]
    name: str
    category: str
    amount: int
    is_expense: bool


class CategorySchema(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    user_id: int


class TransactionSchema(BaseModel):
    id: Optional[int]
    name: str
    date: Optional[str]
    is_expense: bool
    amount: float
    category_id: int
    category: Optional[CategorySchema]
