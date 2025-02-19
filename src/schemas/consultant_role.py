# src/schemas/consultant_role.py
from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)