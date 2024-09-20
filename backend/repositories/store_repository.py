from sqlalchemy.orm import Session
from sqlalchemy.future import select
from backend.scraper.models.db_models import Store
from backend.models.store_dto import StoreDTO

class StoreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_stores(self):
        query = select(Store)
        results = self.db.execute(query).fetchall()
        
        return [
            StoreDTO(
                name=row.Store.name,
                store_url=row.Store.website_url,
                logo_url=row.Store.logo_url
            )
            for row in results
        ]