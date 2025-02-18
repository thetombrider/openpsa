from pydantic import BaseModel, Field, field_validator, ValidationInfo, model_validator
from datetime import date
from typing import Optional, Any
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
    @model_validator(mode='after')
    def validate_allocation(self) -> 'ResourceAllocationCreate':
        """Validazione completa del modello dopo che tutti i campi sono popolati"""
        try:
            # Verifica date
            if self.end_date < self.start_date:
                raise ValueError("La data di fine deve essere successiva alla data di inizio")
            
            # Verifica disponibilità
            from src.services.resource_allocation import ResourceAllocationService
            from src.database.database import SessionLocal
            
            with SessionLocal() as db:
                service = ResourceAllocationService()
                total_allocation = service.check_availability(
                    db,
                    self.user_id,
                    self.start_date,
                    self.end_date
                )

                if total_allocation + self.allocation_percentage > 1:
                    raise ValueError(
                        f"L'allocazione totale non può superare il 100%. "
                        f"Allocazione disponibile: {(1-total_allocation)*100}%"
                    )

            return self
            
        except Exception as e:
            raise ValueError(str(e))

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