from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.connection import get_db
from backend.models.gpu_dto import GPUDTO
from backend.models.store_dto import StoreDTO
from backend.repositories.gpu_repository import GPURepository
from backend.repositories.store_repository import StoreRepository

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/gpus", response_model=List[GPUDTO])
async def get_gpus(db: Session = Depends(get_db)):
    gpu_repo = GPURepository(db)
    return gpu_repo.get_all_gpus()

@router.get("/stores", response_model=List[StoreDTO])
async def get_stores(db: Session = Depends(get_db)):
    store_repo = StoreRepository(db)
    return store_repo.get_all_stores()