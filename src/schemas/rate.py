# src/schemas/rate.py
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional
from decimal import Decimal

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

    model_config = ConfigDict(from_attributes=True)

class UserRateAssign(BaseModel):
    user_id: int
    rate_id: int
    valid_from: date
    valid_to: Optional[date] = None