from fastapi import APIRouter, Depends
from dependency import get_db, Session
from controllers.transaction import (
    create_transaction,
    find_transaction,
    delete_transaction,
    delete_category,
    update_transaction,
    update_category,
)
from schemas.transaction_schema import TransactionCreateSchema

t_router = APIRouter()


@t_router.get("{transaction_id}")
def get_transaction_router(transaction_id: str, db: Session = Depends(get_db)):
    return find_transaction(transaction_id, db)


@t_router.post("")
def get_transaction_router(
    transaction_create_schema: TransactionCreateSchema, db: Session = Depends(get_db)
):
    return create_transaction(transaction_create_schema, db)


@t_router.put("/{transaction_id}")
def udpate_transaction_router(
    transaction_id: str,
    transaction_create_schema: TransactionCreateSchema,
    db: Session = Depends(get_db),
):
    return update_transaction(transaction_id, transaction_create_schema, db)


@t_router.delete("{transaction_id}")
def delete_transaction_router(transaction_id: str, db: Session = Depends(get_db)):
    return delete_transaction(transaction_id, db)
