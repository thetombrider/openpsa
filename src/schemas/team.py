# src/schemas/team.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamMemberBase(BaseModel):
    user_id: int
    role_id: Optional[int] = None
    join_date: date
    leave_date: Optional[date] = None

class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    members: List[TeamMemberBase] = []
    
    class Config:
        orm_mode = True