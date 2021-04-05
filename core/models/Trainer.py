from typing import List
from pydantic.main import BaseModel
from sqlalchemy.orm.session import Session

from core.models.Pokemon import Pokemon

from core.schemas.Trainer import Trainer as TrainerSchema

from core.services.token import get_password_hash, verify_password

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

def authenticate_trainer(db: Session, username: str, password: str):
    user = get_trainer_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user