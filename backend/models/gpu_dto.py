from pydantic import BaseModel
from datetime import date
from typing import Optional

class GPUDTO(BaseModel):
    name: str
    link: Optional[str] = None
    model: str
    price: str
    store: str
    manufacturer: str
    date_checked: date
    brand: str
    series: Optional[str] = None
    vram: Optional[str] = None
    benchmark_score: Optional[int] = None

    class Config:
        from_attributes = True