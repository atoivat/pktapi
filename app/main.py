from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.models import Trainer as TrainerModel
from core.services import token as tk
from core.schemas import Pokemon, Trainer, PokemonData


from app import dependencies as dep
from app.routers import pokedex, trainers, pokemons


app = FastAPI()

app.include_router(trainers.router)
app.include_router(pokedex.router)
app.include_router(pokemons.router)


@app.get("/")
async def healthcheck():
    return {"status": "OK"}


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
        data={"sub": trainer.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
