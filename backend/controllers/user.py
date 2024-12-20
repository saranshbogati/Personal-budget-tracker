from datetime import timedelta
from fastapi import HTTPException
from models.util import TokenResponseModel
from auth_token import create_access_token
from dependency import Session
from db_models import User
from models.user import LoginRequestModel, UserModel, UserBaseModel
from helper import sqlalchemy_to_pydantic, pydantic_to_sqlalchemy
import bcrypt
from env import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session


def get_all_users(db: Session):
    users = db.query(User).all()
    user_list = []
    for user in users:
        user_list.append(sqlalchemy_to_pydantic(user, UserBaseModel).model_dump())
    return {"status": True, "data": user_list}


def create_new_user(user_model: UserBaseModel, db: Session):
    user = None
    user = get_username(user_model.username, db)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = get_email(user_model.email, db)
    if user:
        raise HTTPException(status_code=400, detail="Email already exists")
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
    access_token = get_access_token(user_schema.username)
    return access_token.model_dump()


def edit_user(user_id: int, user_model: UserModel, db: Session):
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
    return {"status": True, "data": user_schema.model_dump()}


def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    return {"status": True, "data": []}


def get_user_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    user_schema = sqlalchemy_to_pydantic(user, UserModel)
    return {"status": True, "data": user_schema.model_dump()}


def get_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    return user


def get_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def get_user_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    user_schema = sqlalchemy_to_pydantic(user, UserModel)
    return {"status": True, "data": user_schema.model_dump()}


def get_hashed_password(password: str):
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pw.decode()


def check_password(password_to_check: str, hash_from_db: str):
    return bcrypt.checkpw(
        password_to_check.encode("utf-8"), hash_from_db.encode("utf-8")
    )


def login_user(login_request: LoginRequestModel, db: Session):
    user = None
    print("username is")
    if login_request.username:
        user: User = get_username(login_request.username, db)
    elif login_request.email:
        user: User = get_email(login_request.email, db)

    if user:
        response = check_user_password(login_request, user)
        return response.model_dump()
    else:
        raise HTTPException(
            status_code=404,
            detail=f"No user with username {login_request.username}",
        )


def check_user_password(
    login_request: LoginRequestModel, user: User
) -> TokenResponseModel:
    if check_password(login_request.password, user.password):
        return get_access_token(user.username)
    else:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password. Please try again!"
        )


def get_access_token(username: str):
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expire
    )
    response = TokenResponseModel(access_token=access_token, token_type="bearer")
    return response
