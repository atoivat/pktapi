from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from dotenv import load_dotenv
import os

from .. import dependencies as dep

from core.models import Trainer as TrainerModel

load_dotenv()

SECRET_KEY = os.getenv("secretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



router = APIRouter(
    prefix="/trainers",
    tags=["trainers"],
    responses={404: {"description": "Not Found"}}
)

@router.get("/", response_model=List[TrainerModel.Trainer])
async def get_trainers(db: Session = Depends(dep.get_db), skip: int = 0, limit: int = 50) -> List[TrainerModel.Trainer]:
    return TrainerModel.get_trainers(db, skip=skip, limit=limit)