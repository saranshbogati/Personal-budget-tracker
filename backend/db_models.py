from datetime import datetime, timedelta, timezone
from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, DateTime, Float
from database import Base
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship


# class BaseModel(DeclarativeBase):
#     pass
class BaseDBMOdel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)


class User(BaseDBMOdel):
    __tablename__ = "users"
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)


class Transaction(BaseDBMOdel):
    __tablename__ = "transactions"
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    is_expense = Column(Boolean, default=True, index=True)
    category_id = Column(ForeignKey("category.id"), index=True)
    amount = Column(Float, default=0.0)
    name = Column(String, nullable=False)


class Category(BaseDBMOdel):
    __tablename__ = "category"
    name = Column(String, index=True, unique=True)
    description = Column(String, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))


class Budget(BaseDBMOdel):
    __tablename__ = "budget"
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    amount = Column(Float, default=0.0)


class UserPreference(BaseDBMOdel):
    __tablename__ = "user_preference"
    user_id = Column(Integer, ForeignKey("users.id"))
    currency = Column(String, nullable=True, default="$", index=True)
    theme = Column(String, nullable=True, default="light", index=True)
