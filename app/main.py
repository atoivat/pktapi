from datetime import timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.models import PokemonData as PKDataModel, Trainer as TrainerModel
from core.services import token as tk
from core.schemas import Pokemon, Trainer, PokemonData


from . import dependencies as dep
from .routers import trainers



app = FastAPI();

app.include_router(trainers.router)

@app.get("/")
async def healthcheck():
    return {"status": "OK"}


@app.get("/pokedex", response_model=List[PKDataModel.PokemonData])
async def read_pokedex(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(dep.get_db)
) -> List[PKDataModel.PokemonData]:
    return PKDataModel.get_pkdata(db, skip=skip, limit=limit)


@app.post("/token", response_model=tk.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(dep.get_db)
) -> tk.Token:
    trainer = TrainerModel.authenticate_trainer(db, form_data.username, form_data.password)
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=tk.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = tk.create_access_token(
        data={"sub":trainer.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
