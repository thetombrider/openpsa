from typing import List
from datetime import date
from sqlalchemy.orm import Session
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