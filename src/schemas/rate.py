# src/schemas/rate.py
from pydantic import BaseModel
from pydantic.types import Decimal
from datetime import date, datetime
from typing import Optional

class RateBase(BaseModel):
    name: str
    description: Optional[str] = None
    rate: Decimal
    currency: str = "EUR"
    valid_from: date
    valid_to: Optional[date] = None

class CostRateCreate(RateBase):
    pass

class BillingRateCreate(RateBase):
    pass

class RateResponse(RateBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True