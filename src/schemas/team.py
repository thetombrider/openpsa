# src/schemas/team.py
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List
from .consultant_role import ConsultantRoleResponse

class TeamMemberBase(BaseModel):
    user_id: int
    role_id: Optional[int] = None
    join_date: date
    leave_date: Optional[date] = None

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamMemberResponse(TeamMemberBase):
    id: int
    role: Optional[ConsultantRoleResponse] = None

    model_config = ConfigDict(from_attributes=True)

class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    members: List[TeamMemberResponse] = []

    model_config = ConfigDict(from_attributes=True)