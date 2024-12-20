from fastapi import HTTPException
from dependency import db_dependency
from db_models import User
from models.user import LoginRequestModel, UserModel, UserBaseModel
from helper import sqlalchemy_to_pydantic, pydantic_to_sqlalchemy
import bcrypt


async def get_all_users(db: db_dependency):
    users = db.query(User).all()
    user_list = []
    for user in users:
        user_list.append(sqlalchemy_to_pydantic(user, UserBaseModel).model_dump_json())
    return {"status": True, "data": user_list}


async def create_new_user(user_model: UserBaseModel, db: db_dependency):
    user = User(
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        username=user_model.username,
        email=user_model.email,
        password=get_hashed_password(user_model.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_schema = sqlalchemy_to_pydantic(user, UserBaseModel)
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
    user.password = get_hashed_password(user_model.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    user_schema = sqlalchemy_to_pydantic(user, UserBaseModel)
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


def get_username(username: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()
    return user


def get_email(email: str, db: db_dependency):
    user = db.query(User).filter(User.email == email).first()
    return user


async def get_user_id(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    user_schema = sqlalchemy_to_pydantic(user, UserModel)
    return {"status": True, "data": user_schema.model_dump_json()}


def get_hashed_password(password: str):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pw.decode()


def check_password(password_to_check: str, hash_from_db: str):
    return bcrypt.checkpw(
        password_to_check.encode("utf-8"), hash_from_db.encode("utf-8")
    )


async def login(login_request: LoginRequestModel, db: db_dependency):
    user = None
    if login_request.username:
        user: User = get_username(login_request.username, db)
    elif login_request.email:
        user: User = get_email(login_request.email, db)

    if user:
        return check_user_password(login_request, user)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No user with username {login_request.username}",
        )


def check_user_password(login_request: LoginRequestModel, user: User):
    if check_password(login_request.password, user.password):
        return {"status": True, "data": "Return jwt token here"}
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password. Please try again!"
        )
