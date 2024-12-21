from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from db_models import Category, Transaction
from helper import commit_and_return, sqlalchemy_to_pydantic
from schemas.transaction_schema import (
    CategorySchema,
    TransactionSchema,
    TransactionCreateSchema,
)


def find_transaction(t_id: int, db: Session):
    t = db.query(Transaction).filter(Transaction.id == t_id).first()
    return sqlalchemy_to_pydantic(t, TransactionSchema).model_dump()


def update_transaction(t_id: int, transaction: TransactionCreateSchema, db: Session):
    t = db.query(Transaction).filter(Transaction.id == t_id).first()
    if not t:
        raise HTTPException(status_code=400, detail="Transaction not found")
    t.amount = transaction.amount
    t.is_expense = transaction.is_expense
    category: Category = find_or_create_category(transaction.category)
    t.category_id = category.id
    t.name = transaction.name
    result = commit_and_return(t, db)
    return sqlalchemy_to_pydantic(result, TransactionSchema).model_dump()


def delete_transaction(t_id: int, db: Session):
    t = db.query(Transaction).filter(Transaction.id == t_id).first()
    db.delete(t)
    db.commit()
    return True


def create_transaction(transaction_request: TransactionCreateSchema, db: Session):
    # handle the category first
    category: Category = find_or_create_category(transaction_request.category)

    transaction = Transaction(
        date=datetime.now(timezone.utc),
        is_expense=transaction_request.is_expense,
        category_id=category.id,
        amount=transaction_request.amount,
    )
    transaction = commit_and_return(transaction)
    return sqlalchemy_to_pydantic(transaction, TransactionSchema).model_dump()


def find_or_create_category(name: str, db: Session):
    category: Category = db.query(Category).filter(Category.name == name).first()
    if category:
        return category
    category = Category(name=name)
    return commit_and_return(category)


def delete_category(c_id: int, db: Session):
    cat: Category = db.query(Category).filter(Category.id == c_id).first()
    db.delete(cat)
    db.commit()
    return True


def update_category(c_id: int, cat: CategorySchema, db: Session):
    c: Category = db.query(Category).filter(Category.id == c_id).first()
    c.name = cat.name
    c.description = cat.description
    res = commit_and_return(c, db)
    return sqlalchemy_to_pydantic(res, CategorySchema).model_dump()
