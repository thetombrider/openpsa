# src/schemas/consultant_role.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ConsultantRoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class ConsultantRoleCreate(ConsultantRoleBase):
    pass

class ConsultantRoleResponse(ConsultantRoleBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True