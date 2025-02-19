# src/schemas/consultant_role.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ConsultantRoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class ConsultantRoleCreate(ConsultantRoleBase):
    pass

class ConsultantRoleUpdate(ConsultantRoleBase):
    pass

class ConsultantRoleResponse(ConsultantRoleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # precedentemente orm_mode = True