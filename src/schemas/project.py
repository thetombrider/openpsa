from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
from src.models.models import ProjectStatus, BillingType

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    client_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    status: ProjectStatus = ProjectStatus.DRAFT
    billing_type: BillingType = BillingType.FIXED_PRICE
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
    status: Optional[ProjectStatus] = None
    billing_type: Optional[BillingType] = None
    billing_currency: Optional[str] = None
    billing_notes: Optional[str] = None

    @field_validator('client_id')
    def validate_client_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("client_id deve essere maggiore di 0")
        return v

class ProjectResponse(ProjectBase):
    id: int
    
    class Config:
        orm_mode = True