from fastapi import FastAPI
from database import engine, Base
from routers.user import user_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/api/v1/user", tags=["Users"])
