from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum

class StatusEnum(str, Enum):
    PLANNED = "planned"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class ResourceAllocationBase(BaseModel):
    status: StatusEnum = StatusEnum.PLANNED
    user_id: int
    project_id: int
    start_date: date
    end_date: date
    allocation_percentage: float = Field(..., gt=0, le=1)
    role: Optional[str] = None
    status: StatusEnum = StatusEnum.PLANNED

class ResourceAllocationCreate(ResourceAllocationBase):
    pass

class ResourceAllocationUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    allocation_percentage: Optional[float] = Field(None, gt=0, le=1)
    role: Optional[str] = None
    status: Optional[str] = None

class ResourceAllocationResponse(ResourceAllocationBase):
    id: int
    
    class Config:
        orm_mode = True