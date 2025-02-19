from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import Optional
from .enums import ResourceAllocationStatus
from .consultant_role import ConsultantRoleResponse

class ResourceAllocationBase(BaseModel):
    project_id: int
    user_id: int
    allocation_percentage: float
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ResourceAllocationStatus] = None
    
    model_config = ConfigDict(from_attributes=True)

class ResourceAllocationCreate(ResourceAllocationBase):
    pass

class ResourceAllocationResponse(ResourceAllocationBase):
    id: int
    role: Optional[ConsultantRoleResponse] = None

class ResourceAllocationUpdate(BaseModel):
    allocation_percentage: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ResourceAllocationStatus] = None
    role_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)