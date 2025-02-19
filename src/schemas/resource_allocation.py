from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional
from .enums import ResourceAllocationStatus
from .consultant_role import ConsultantRoleResponse

class ResourceAllocationBase(BaseModel):
    project_id: int
    consultant_role_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    allocation_percentage: float = Field(default=100.0, ge=0.0, le=100.0)
    status: ResourceAllocationStatus = Field(default=ResourceAllocationStatus.PLANNED)
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ResourceAllocationCreate(ResourceAllocationBase):
    pass

class ResourceAllocationResponse(ResourceAllocationBase):
    id: int
    consultant_role: ConsultantRoleResponse
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

class ResourceAllocationUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    consultant_role_id: Optional[int] = None
    allocation_percentage: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    status: Optional[ResourceAllocationStatus] = None
    notes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)