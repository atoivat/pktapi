from .PokemonData import PokemonData
from .Trainer import Trainer

from pydantic import BaseModel


class PokemonBase(BaseModel):
    nickname: str
    level: int

class PokemonCreate(PokemonBase):
    data_id: int
    trainer_id: int

class Pokemon(PokemonBase):
    trainer: Trainer
    data: PokemonData

    class Config:
        orm_mode = True
