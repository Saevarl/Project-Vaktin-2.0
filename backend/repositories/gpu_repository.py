from sqlalchemy.orm import Session
from sqlalchemy.future import select
from backend.scraper.models.db_models import GPU, GPUModel, Price, Store
from backend.models.gpu_dto import GPUDTO
from urllib.parse import urljoin

class GPURepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_gpus(self):
        query = (
            select(GPU.name, GPU.link, GPU.manufacturer, Price.price, Store.name.label('store_name'), 
                   Price.date_checked, Store.website_url.label('store_url'),
                   GPUModel.model, GPUModel.brand, 
                   GPUModel.series, GPUModel.vram, GPUModel.benchmark_score)
            .join(GPU.model)
            .join(GPU.prices)
            .join(Price.store)
        )
        results = self.db.execute(query).fetchall()
        
        return [GPUDTO(
            name=row.name,
            link=urljoin(row.store_url, row.link) if row.link else None,
            model=row.model,
            price=str(row.price),
            store=row.store_name,
            manufacturer=row.manufacturer,
            date_checked=row.date_checked,
            brand=row.brand,
            series=row.series,
            vram=row.vram,
            benchmark_score=row.benchmark_score
        ) for row in results]