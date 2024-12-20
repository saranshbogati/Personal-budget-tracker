from dependency import db_dependency
from db_models import User
from models.user import UserModel
from helper import sqlalchemy_to_pydantic, pydantic_to_sqlalchemy


async def get_all_users(db: db_dependency):
    users = db.query(User).all()
    user_list = []
    for user in users:
        user_list.append(sqlalchemy_to_pydantic(user, UserModel).model_dump_json())
    return {"status": True, "data": user_list}


async def create_new_user(user_model: UserModel, db: db_dependency):
    user = User(
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        username=user_model.username,
        email=user_model.email,
        password=user_model.password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_schema = sqlalchemy_to_pydantic(user, UserModel)
    return {"status": True, "data": user_schema.model_dump_json()}


async def edit_user(user_id: int, user_model: UserModel, db: db_dependency):
    print(f"user id is {user_id}")
    all_users = db.query(User).all()
    print("all users are", all_users)
    user = db.query(User).filter(User.id == user_id).first()
    print("user is ", user)
    user.first_name = user_model.first_name
    user.last_name = user_model.last_name
    user.username = user_model.username
    user.email = user_model.email
    user.password = user_model.password
    db.add(user)
    db.commit()
    db.refresh(user)
    user_schema = sqlalchemy_to_pydantic(user, UserModel)
    return {"status": True, "data": user_schema.model_dump_json()}


async def delete_user(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    return {"status": True, "data": []}


async def get_user_id(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    user_schema = sqlalchemy_to_pydantic(user, UserModel)
    return {"status": True, "data": user_schema.model_dump_json()}
