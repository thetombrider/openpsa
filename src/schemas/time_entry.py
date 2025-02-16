from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TimeEntryBase(BaseModel):
    user_id: int
    project_id: int
    date: datetime
    hours: float
    description: Optional[str] = None

class TimeEntryCreate(TimeEntryBase):
    pass

class TimeEntryUpdate(BaseModel):
    date: Optional[datetime] = None
    hours: Optional[float] = None
    description: Optional[str] = None

class TimeEntryResponse(TimeEntryBase):
    id: int
    
    class Config:
        orm_mode = True