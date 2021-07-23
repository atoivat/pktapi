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
    id: int
    data: PokemonData

class PokemonOut(Pokemon):
    trainer: str

class PokemonUpdateIn(BaseModel):
    nickname: Optional[str]
    level: Optional[int]


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
            id=pokemon.id,
            nickname=pokemon.nickname,
            level=pokemon.level, 
            data=pokemon.data, 
            trainer=pokemon.trainer.username
        ) 
        for pokemon in pokemons
    ]


def get_pokemon(db: Session, id: int):
    return db.query(PokemonSchema).filter(PokemonSchema.id == id).first()
 