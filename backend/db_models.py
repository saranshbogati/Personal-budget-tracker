from sqlalchemy import Boolean, Column, Integer, ForeignKey, String
from database import Base

# from sqlalchemy.orm import DeclarativeBase


# class BaseModel(DeclarativeBase):
#     pass


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
