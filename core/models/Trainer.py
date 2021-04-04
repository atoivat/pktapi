from .Pokemon import Pokemon
from typing import List

from pydantic.main import BaseModel


class TrainerBase(BaseModel):
    name: str
    username: str

class TrainerCreate(TrainerBase):
    password: str

class Trainer(TrainerBase):
    id: int
    team: List[Pokemon] = []

    class Config:
        orm_mode = True
