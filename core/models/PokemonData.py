from typing import List

from sqlalchemy.orm import Session

from pydantic import BaseModel

from core.schemas.PokemonData import PokemonData as PKDataSchema

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

def get_pkdata_by_id(db: Session, id: int):
    return db.query(PKDataSchema).filter(PKDataSchema.id==id).first()

# def create_pkdata(db: Session, pkdata: PokemonData):
#     print(pkdata.dict())
#     db_pkdata = PKDataSchema(**pkdata.dict())
#     db.add(db_pkdata)
#     db.commit()
#     db.refresh(db_pkdata)
#     print(db_pkdata)
#     return db_pkdata