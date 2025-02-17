from pydantic import BaseModel, Field, field_validator, ValidationInfo
from datetime import date
from typing import Optional
from src.models.models import ConsultantRole, ResourceAllocationStatus

class ResourceAllocationBase(BaseModel):
    status: ResourceAllocationStatus = ResourceAllocationStatus.PLANNED
    user_id: int
    project_id: int
    start_date: date
    end_date: date
    allocation_percentage: float = Field(..., gt=0, le=1)
    role: Optional[ConsultantRole] = None

class ResourceAllocationCreate(ResourceAllocationBase):
    @field_validator('start_date')
    @classmethod
    def validate_allocation_period(cls, v: date, info: ValidationInfo) -> date:
        if not hasattr(info.data, 'user_id'):
            raise ValueError("user_id è richiesto")

        from src.services.resource_allocation import ResourceAllocationService
        from src.database.database import SessionLocal
        
        db = SessionLocal()
        try:
            service = ResourceAllocationService()
            total_allocation = service.check_availability(
                db,
                info.data.user_id,
                v,
                info.data.end_date if hasattr(info.data, 'end_date') else v
            )

            new_allocation = info.data.allocation_percentage
            if total_allocation + new_allocation > 1:
                raise ValueError(
                    f"L'allocazione totale non può superare il 100%. "
                    f"Allocazione disponibile: {(1-total_allocation)*100}%"
                )
        finally:
            db.close()
        
        return v

class ResourceAllocationUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    allocation_percentage: Optional[float] = Field(None, gt=0, le=1)
    role: Optional[ConsultantRole] = None
    status: Optional[ResourceAllocationStatus] = None

class ResourceAllocationResponse(ResourceAllocationBase):
    id: int
    
    class Config:
        orm_mode = True