from pydantic import BaseModel
from datetime import date

class GPUDTO(BaseModel):
    name: str
    link: str
    model: str
    price: str
    store: str
    manufacturer: str
    date_checked: date
    brand: str
    series: str
    vram: str

    class Config:
        from_attributes = True