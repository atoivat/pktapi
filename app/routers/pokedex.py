from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from app import dependencies
from core.models import PokemonData as PKDataModel

router = APIRouter(
    prefix="/pokedex",
    tags=["pokedex"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/", response_model=List[PKDataModel.PokemonData])
async def get_pokedex(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(dependencies.get_db)
) -> List[PKDataModel.PokemonData]:
    return PKDataModel.get_pkdata(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=PKDataModel.PokemonData)
async def get_pokemon_data(id: int, db: Session = Depends(dependencies.get_db)):
    pokemon = PKDataModel.get_pkdata_by_id(db, id)
    if pokemon is None:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return pokemon
