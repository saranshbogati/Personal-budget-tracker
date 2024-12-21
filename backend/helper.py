from typing import TypeVar, Type
from pydantic import BaseModel
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session
from database import Base

# Type variables for generic functions
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)
SQLAlchemyModel = TypeVar("SQLAlchemyModel", bound=Base)


# Pydantic -> SQLAlchemy Conversion
def pydantic_to_sqlalchemy(
    pydantic_obj: PydanticModel, sqlalchemy_model: Type[SQLAlchemyModel]
) -> SQLAlchemyModel:
    model_data = pydantic_obj.model_dump(exclude_unset=True)
    return sqlalchemy_model(**model_data)


# SQLAlchemy -> Pydantic Conversion
def sqlalchemy_to_pydantic(
    sqlalchemy_obj: SQLAlchemyModel, pydantic_model: Type[PydanticModel]
) -> PydanticModel:
    model_data = {
        col.name: getattr(sqlalchemy_obj, col.name)
        for col in sqlalchemy_obj.__table__.columns
    }
    return pydantic_model(**model_data)


def commit_and_return(model: SQLAlchemyModel, db: Session) -> SQLAlchemyModel:
    db.add(model)
    db.commit()
    db.refresh(model)
    return model
