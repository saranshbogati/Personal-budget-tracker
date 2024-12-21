from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth_token import verify_access_token
from dependency import db_dependency, get_db
from controllers.user import (
    get_all_users,
    create_new_user,
    delete_user,
    edit_user,
    get_user_id,
    login_user,
)
from schemas.user_schema import LoginRequestModel, UserModel
from sqlalchemy.orm import Session


user_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid Token")
        return username
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@user_router.get("")
def fetch_user_list(db: Session = Depends(get_db)):
    result = get_all_users(db)
    return result


@user_router.get("/test")
def test(username=Depends(get_current_user)):
    print(f"username is {username}")


@user_router.put("/{user_id}")
def update_user(user_id: str, user_model: UserModel, db: Session = Depends(get_db)):
    result = edit_user(int(user_id), user_model, db)
    return result


@user_router.delete("/{user_id}")
def remove_user(user_id: str, db: Session = Depends(get_db)):
    result = delete_user(int(user_id), db)
    return result


@user_router.get("/{user_id}")
def fetch_user_id(user_id: str, db: Session = Depends(get_db)):
    result = get_user_id(int(user_id), db)
    return result


@user_router.post("/login")
def login(login_request: LoginRequestModel, db: Session = Depends(get_db)):
    print("eta samma")
    result = login_user(login_request, db)
    return result


@user_router.post("/register")
def make_new_user(user_model: UserModel, db: Session = Depends(get_db)):
    result = create_new_user(user_model, db)
    return result
