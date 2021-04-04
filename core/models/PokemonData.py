from typing import List, Optional

from sqlalchemy.orm import Session

from pydantic import BaseModel, HttpUrl

from ..schemas.PokemonData import PokemonData as PKDataSchema

class PokemonData(BaseModel):
    id: int
    name: str
    types: List[str]
    description: str
    weight: int
    sprite: str

    class Config:
        orm_mode = True


def get_pkdata(db: Session, skip: int = 0, limit: int = 50):
    return db.query(PKDataSchema).offset(skip).limit(limit).all()

# def create_pkdata(db: Session, pkdata: PokemonData):
#     print(pkdata.dict())
#     db_pkdata = PKDataSchema(**pkdata.dict())
#     db.add(db_pkdata)
#     db.commit()
#     db.refresh(db_pkdata)
#     print(db_pkdata)
#     return db_pkdata