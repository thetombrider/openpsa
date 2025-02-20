# src/schemas/consultant_role.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ConsultantRoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class ConsultantRoleCreate(ConsultantRoleBase):
    pass

class ConsultantRoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ConsultantRoleResponse(ConsultantRoleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True