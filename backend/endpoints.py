from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from backend.database.connection import get_db
from backend.models.gpu_dto import GPUDTO  
from backend.scraper.models.db_models import GPU as DBGPUModel
from backend.scraper.models.db_models import Price
from backend.scraper.models.db_models import Store
from backend.models.store_dto import StoreDTO
from urllib.parse import urljoin

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/gpus", response_model=List[GPUDTO])
async def get_gpus(db: Session = Depends(get_db)):
    query = (
        select(DBGPUModel.name, DBGPUModel.model, DBGPUModel.link, Price.price, Store.name.label('store_name'), 
               DBGPUModel.manufacturer, Price.date_checked, Store.website_url.label('store_url'),
               DBGPUModel.brand, DBGPUModel.series, DBGPUModel.vram)
        .join(Price, DBGPUModel.id == Price.gpu_id)
        .join(Store, Store.id == Price.store_id)
    )
    results = db.execute(query).fetchall()
    
    return [GPUDTO(
        name=row.name,
        link=urljoin(row.store_url, row.link),
        model=row.model,
        price=str(row.price),
        store=row.store_name,
        manufacturer=row.manufacturer,
        date_checked=row.date_checked,
        brand=row.brand,
        series=row.series,
        vram=row.vram
    ) for row in results]


@router.get("/stores", response_model=List[StoreDTO])
async def get_stores(db: Session = Depends(get_db)):
    query = select(Store)
    results = db.execute(query).fetchall()
    
    return [
        StoreDTO(
            name=row.Store.name,
            store_url=row.Store.website_url,
            logo_url=row.Store.logo_url
        )
        for row in results
    ]
