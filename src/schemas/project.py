from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    client_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    status: str = "active"
    billing_type: str = "time_and_materials"
    billing_currency: str = "EUR"
    billing_notes: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    client_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    status: Optional[str] = None
    billing_type: Optional[str] = None
    billing_currency: Optional[str] = None
    billing_notes: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    
    class Config:
        orm_mode = True