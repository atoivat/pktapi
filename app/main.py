from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session


from core.models import PokemonData as PKData
from core.database import SessionLocal

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI();

@app.get("/pokedex", response_model=List[PKData.PokemonData])
async def read_pokedex(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)) -> List[PKData.PokemonData]:
    return PKData.get_pkdata(db, skip=skip, limit=limit)

# @app.post("/pokedex", response_model=PKData.PokemonData)
# async def create_pokedex_entry(pokemon_data: PKData.PokemonData, db: Session = Depends(get_db)) -> PKData.PokemonData:
#     return PKData.create_pkdata(db, pokemon_data)