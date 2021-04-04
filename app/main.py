from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from core.models import PokemonData as PKDataModel



from . import dependencies as dep
from .routers import trainers



app = FastAPI();

app.include_router(trainers.router)



@app.get("/pokedex", response_model=List[PKDataModel.PokemonData])
async def read_pokedex(skip: int = 0, limit: int = 50, db: Session = Depends(dep.get_db)) -> List[PKDataModel.PokemonData]:
    return PKDataModel.get_pkdata(db, skip=skip, limit=limit)

# @app.post("/pokedex", response_model=PKData.PokemonData)
# async def create_pokedex_entry(pokemon_data: PKData.PokemonData, db: Session = Depends(get_db)) -> PKData.PokemonData:
#     return PKData.create_pkdata(db, pokemon_data)