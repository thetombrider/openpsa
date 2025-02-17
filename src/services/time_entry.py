from typing import List
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.models.models import TimeEntry
from src.schemas.time_entry import TimeEntryCreate, TimeEntryUpdate
from src.services.base import BaseService

class TimeEntryService(BaseService[TimeEntry, TimeEntryCreate, TimeEntryUpdate]):
    def __init__(self):
        super().__init__(TimeEntry)
        
    def get_by_user_and_date_range(
        self, 
        db: Session, 
        user_id: int, 
        start_date: date, 
        end_date: date
    ) -> List[TimeEntry]:
        return db.query(self.model)\
            .filter(
                self.model.user_id == user_id,
                self.model.date >= start_date,
                self.model.date <= end_date
            ).all()
            
    def get_by_project(self, db: Session, project_id: int) -> List[TimeEntry]:
        return db.query(self.model)\
            .filter(self.model.project_id == project_id)\
            .all()

    def get_weekly_hours(
        self,
        db: Session,
        user_id: int,
        week_start: date,
        week_end: date
    ) -> float:
        """
        Calcola il totale delle ore settimanali per un utente.
        """
        result = db.query(func.sum(TimeEntry.hours))\
            .filter(
                TimeEntry.user_id == user_id,
                TimeEntry.date >= week_start,
                TimeEntry.date <= week_end
            ).scalar()
        return float(result or 0)

    def get_daily_hours(
        self,
        db: Session,
        user_id: int,
        day: date
    ) -> float:
        """
        Calcola il totale delle ore giornaliere per un utente.
        """
        result = db.query(func.sum(TimeEntry.hours))\
            .filter(
                TimeEntry.user_id == user_id,
                func.date(TimeEntry.date) == day
            ).scalar()
        return float(result or 0)

    def create(self, db: Session, time_entry: TimeEntryCreate) -> TimeEntry:
        # Verifica ore giornaliere
        daily_hours = self.get_daily_hours(
            db, 
            time_entry.user_id,
            time_entry.date.date()
        )
        if daily_hours + time_entry.hours > 8:
            raise ValueError(
                f"Il totale delle ore giornaliere non può superare 8. "
                f"Ore già registrate oggi: {daily_hours}"
            )

        return super().create(db, time_entry)