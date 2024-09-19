from pydantic import BaseModel
from datetime import date

class StoreDTO(BaseModel):
    name: str
    store_url: str
    logo_url: str

    class Config:
        from_attributes = True
      