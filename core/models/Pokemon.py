from typing import List, Optional
from sqlalchemy.orm.session import Session
from .PokemonData import PokemonData

from pydantic import BaseModel

from core.schemas.Pokemon import Pokemon as PokemonSchema

class PokemonBase(BaseModel):
    nickname: Optional[str]
    level: int
    class Config:
        orm_mode = True

class PokemonCreate(PokemonBase):
    data_id: int

class Pokemon(PokemonBase):
    data: PokemonData

class PokemonOut(Pokemon):
    trainer: str


def create_pokemon(db: Session, pokemon: PokemonCreate, trainer_id: int):
    db_pokemon = PokemonSchema(
        nickname=pokemon.nickname,
        level=pokemon.level,
        trainer_id=trainer_id,
        data_id=pokemon.data_id
    )
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon


def get_pokemons(db: Session, skip: int = 0, limit: int = 50) -> List[PokemonOut]:
    pokemons: List[Pokemon] = db.query(PokemonSchema).offset(skip).limit(limit).all()
    return [
        PokemonOut(
            nickname=pokemon.nickname,
            level=pokemon.level, 
            data=pokemon.data, 
            trainer=pokemon.trainer.name
        ) 
        for pokemon in pokemons
    ]
