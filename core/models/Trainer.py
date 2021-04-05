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


# VVV
from passlib.context import CryptContext
from os import environ

SECRET_KEY = environ.get("secretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(TrainerSchema).filter(TrainerSchema.username == username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user



# ^^^


def get_trainers(db: Session, skip: int = 0, limit: int = 50):
    return db.query(TrainerSchema).offset(skip).limit(limit).all()

def get_trainer(db: Session, id: int):
    return db.query(TrainerSchema).filter(TrainerSchema.id == id).first()

def get_trainer_by_username(db: Session, username: str):
    return db.query(TrainerSchema).filter(TrainerSchema.username == username).first()

def create_trainer(db: Session, trainer: TrainerCreate):
    password_hash = get_password_hash(trainer.password)
    db_trainer = TrainerSchema(
        name=trainer.name, 
        username=trainer.username,
        password_hash=password_hash
    )
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer