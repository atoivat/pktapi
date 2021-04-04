from .PokemonData import PokemonData

from pydantic import BaseModel


class PokemonBase(BaseModel):
    nickname: str
    level: int

class PokemonCreate(PokemonBase):
    data_id: int
    trainer_id: int

class Pokemon(PokemonBase):
    data: PokemonData

    class Config:
        orm_mode = True
