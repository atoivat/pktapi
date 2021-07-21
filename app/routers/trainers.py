from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.session import Session

from app import dependencies as dep

from core.models import Trainer as TrainerModel


router = APIRouter(
    prefix="/trainers",
    tags=["trainers"],
    responses={404: {"detail": "Not Found"}}
)


@router.get("/", response_model=List[TrainerModel.TrainerBase])
async def get_trainers(
    db: Session = Depends(dep.get_db),
    skip: int = 0,
    limit: int = 50
):
    return TrainerModel.get_trainers(db, skip=skip, limit=limit)


@router.post("/", response_model=TrainerModel.Trainer)
async def create_trainer(
    trainer: TrainerModel.TrainerCreate,
    db: Session = Depends(dep.get_db)
) -> TrainerModel.Trainer:
    if len(trainer.name.strip()) <= 0 or len(trainer.username.strip()) <= 0:
        raise HTTPException(status_code=400, detail="Empty parameters")
    
    same_username_trainer = TrainerModel.get_trainer_by_username(db, trainer.username)
    if same_username_trainer:
        raise HTTPException(status_code=400, detail="Trainer with this username already exists")

    return TrainerModel.create_trainer(db, trainer)


@router.get("/me", response_model=TrainerModel.Trainer)
async def get_current_trainer(
    trainer: TrainerModel.Trainer = Depends(dep.get_current_trainer),
) -> TrainerModel.Trainer:
    return trainer

@router.delete("/me", response_model=TrainerModel.TrainerBase)
async def delete_current_trainer(
    trainer: TrainerModel.Trainer = Depends(dep.get_current_trainer),
    db: Session = Depends(dep.get_db)
) -> TrainerModel.Trainer:
    db.delete(trainer)
    db.commit()
    return trainer


@router.get("/{username}", response_model=TrainerModel.Trainer)
async def get_trainer(username: str, db: Session = Depends(dep.get_db)):
    trainer = TrainerModel.get_trainer_by_username(db, username)
    if trainer is None:
        raise HTTPException(status_code=404, detail="Trainer not Found")
    return trainer
