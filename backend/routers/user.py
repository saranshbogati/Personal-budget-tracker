from fastapi import APIRouter
from dependency import db_dependency
from controllers.user import (
    get_all_users,
    create_new_user,
    delete_user,
    edit_user,
    get_user_id,
)
from models.user import UserModel

user_router = APIRouter()


@user_router.get("")
async def fetch_user_list(db: db_dependency):
    result = await get_all_users(db)
    return result


@user_router.post("")
async def make_new_user(user_model: UserModel, db: db_dependency):
    result = await create_new_user(user_model, db)
    return result


@user_router.put("/{user_id}")
async def update_user(user_id: str, user_model: UserModel, db: db_dependency):
    result = await edit_user(int(user_id), user_model, db)
    return result


@user_router.delete("/{user_id}")
async def remove_user(user_id: str, db: db_dependency):
    result = await delete_user(int(user_id), db)
    return result


@user_router.get("/{user_id}")
async def fetch_user_id(user_id: str, db: db_dependency):
    result = await get_user_id(int(user_id), db)
    return result
