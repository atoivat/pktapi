from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session


from .. import dependencies as dep

from core.models import Trainer as TrainerModel


router = APIRouter(
    prefix="/trainers",
    tags=["trainers"],
    responses={404: {"description": "Not Found"}}
)

@router.get("/", response_model=List[TrainerModel.Trainer])
async def get_trainers(
    db: Session = Depends(dep.get_db),
    skip: int = 0,
    limit: int = 50
) -> List[TrainerModel.Trainer]:
    return TrainerModel.get_trainers(db, skip=skip, limit=limit)


@router.get("/me", response_model=TrainerModel.Trainer)
async def get_current_trainer(
    trainer: TrainerModel.Trainer = Depends(dep.get_current_trainer),
) -> TrainerModel.Trainer:
    return trainer


@router.post("/create", response_model=TrainerModel.Trainer)
async def create_trainer(
    trainer: TrainerModel.TrainerCreate,
    db: Session = Depends(dep.get_db)
) -> TrainerModel.Trainer:
    return TrainerModel.create_trainer(db, trainer)

