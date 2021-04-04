from typing import List

from pydantic.main import BaseModel

from sqlalchemy.orm.session import Session

from .Pokemon import Pokemon

from ..schemas.Trainer import Trainer as TrainerSchema
from ..schemas.Pokemon import Pokemon as PokemonSchema

class TrainerBase(BaseModel):
    name: str
    username: str

class TrainerCreate(TrainerBase):
    password: str

class TrainerInDB(TrainerBase):
    id: int
    password_hash: str

class Trainer(TrainerBase):
    id: int
    team: List[Pokemon] = []

    class Config:
        orm_mode = True


def get_trainers(db: Session, skip: int = 0, limit: int = 50):
    return db.query(TrainerSchema).offset(skip).limit(limit).all()

def get_trainer(db: Session, id: int):
    return db.query(TrainerSchema).filter(TrainerSchema.id == id).first()

def get_trainer_by_username(db: Session, username: str):
    return db.query(TrainerSchema).filter(TrainerSchema.username == username).first()