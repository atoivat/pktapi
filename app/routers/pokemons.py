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


@router.get("/{id}", response_model=PokemonModel.PokemonOut)
async def get_pokemon(id: int, db: Session = Depends(dep.get_db)):
    pokemon = PokemonModel.get_pokemon(db, id)
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return PokemonModel.PokemonOut(
        id=pokemon.id,
        nickname=pokemon.nickname,
        level=pokemon.level, 
        data=pokemon.data, 
        trainer=pokemon.trainer.username
    )


@router.put("/{id}", response_model=PokemonModel.Pokemon)
async def update_pokemon(
    id: int,
    update_data: PokemonModel.PokemonUpdateIn,
    trainer: TrainerModel.Trainer = Depends(dep.get_current_trainer),
    db: Session = Depends(dep.get_db)
):
    pokemon = PokemonModel.get_pokemon(db, id)
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    if pokemon.trainer_id != trainer.id:
        raise HTTPException(status_code=403, detail="Cannot update this pokemon")
    if update_data.level is not None and update_data.level <= 0:
        raise HTTPException(status_code=400, detail="Invalid parameters")

    if update_data.nickname is not None:
        if len(update_data.nickname.strip()) > 0:
            pokemon.nickname = update_data.nickname.strip()
        else:
            pokemon.nickname = None

    if update_data.level is not None:
        pokemon.level = update_data.level

    db.commit()
    db.refresh(pokemon)
    return pokemon