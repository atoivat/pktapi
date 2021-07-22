from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError

from core.models import Pokemon as PokemonModel, Trainer as TrainerModel
import app.dependencies as dep

router = APIRouter(
    prefix="/pokemons",
    tags=["pokemons"],
    responses={404: {"detail": "Not Found"}}
)


@router.get("/", response_model=List[PokemonModel.PokemonOut])
async def get_pokemons(
    db: Session = Depends(dep.get_db),
    skip: int = 0,
    limit: int = 50
):
    return PokemonModel.get_pokemons(db, skip=skip, limit=limit)


@router.post("/", response_model=PokemonModel.Pokemon)
async def create_pokemon(
    pokemon: PokemonModel.PokemonCreate,
    db: Session = Depends(dep.get_db),
    trainer: TrainerModel.Trainer = Depends(dep.get_current_trainer)
):
    if pokemon.level <= 0:
        HTTPException(status_code=400, detail="Invalid parameters")
    
    if pokemon.nickname is not None:
        # String validation
        pokemon.nickname = pokemon.nickname.strip()
        if len(pokemon.nickname) == 0:
            pokemon.nickname = None
    
    try:
        return PokemonModel.create_pokemon(db, pokemon, trainer_id=trainer.id)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Invalid parameters")
