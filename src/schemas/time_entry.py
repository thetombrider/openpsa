from pydantic import BaseModel, Field, field_validator, ValidationInfo
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from src.models.models import TimeEntry

class TimeEntryBase(BaseModel):
    user_id: int
    project_id: int
    date: datetime
    hours: float = Field(..., gt=0, le=8)
    description: Optional[str] = None

class TimeEntryCreate(TimeEntryBase):
    @field_validator('hours')
    @classmethod
    def validate_hours_constraints(cls, v: float, info: ValidationInfo) -> float:
        # Validazione base delle ore giornaliere
        if v <= 0 or v > 8:
            raise ValueError("Le ore giornaliere devono essere comprese tra 0 e 8")

        # Ottieni user_id e date dai dati validati
        user_id = getattr(info.data, 'user_id', None)
        date_value = getattr(info.data, 'date', None)

        if user_id is None or date_value is None:
            return v

        # Calcola inizio e fine settimana
        week_start = date_value - timedelta(days=date_value.weekday())
        week_end = week_start + timedelta(days=4)

        from src.services.time_entry import TimeEntryService
        from src.database.database import SessionLocal
        
        db = SessionLocal()
        try:
            service = TimeEntryService()
            weekly_hours = service.get_weekly_hours(
                db, 
                user_id,
                week_start.date(), 
                week_end.date()
            )

            total_hours = weekly_hours + v
            if total_hours > 40:
                raise ValueError(
                    f"Il totale delle ore settimanali non può superare 40. "
                    f"Ore già registrate questa settimana: {weekly_hours}"
                )

        finally:
            db.close()
        
        return v

class TimeEntryUpdate(BaseModel):
    date: Optional[datetime] = None
    hours: Optional[float] = Field(None, gt=0, le=8)
    description: Optional[str] = None

class TimeEntryResponse(TimeEntryBase):
    id: int
    
    class Config:
        orm_mode = True