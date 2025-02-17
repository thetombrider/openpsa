from typing import List
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.models.models import ResourceAllocation
from src.schemas.resource_allocation import ResourceAllocationCreate, ResourceAllocationUpdate
from src.services.base import BaseService

class ResourceAllocationService(BaseService[ResourceAllocation, ResourceAllocationCreate, ResourceAllocationUpdate]):
    def __init__(self):
        super().__init__(ResourceAllocation)
    
    def get_user_allocations(
        self, 
        db: Session, 
        user_id: int, 
        start_date: date = None, 
        end_date: date = None
    ) -> List[ResourceAllocation]:
        query = db.query(self.model).filter(self.model.user_id == user_id)
        
        if start_date:
            query = query.filter(self.model.end_date >= start_date)
        if end_date:
            query = query.filter(self.model.start_date <= end_date)
            
        return query.all()
    
    def check_availability(
        self, 
        db: Session, 
        user_id: int, 
        start_date: date, 
        end_date: date
    ) -> float:
        """Calcola la percentuale di disponibilità rimasta nel periodo."""
        allocations = self.get_user_allocations(db, user_id, start_date, end_date)
        total_allocation = sum(a.allocation_percentage for a in allocations)
        return max(0, 1 - total_allocation)

    def get_project_allocations(
        self,
        db: Session,
        project_id: int,
        start_date: date = None,
        end_date: date = None
    ) -> List[ResourceAllocation]:
        """
        Recupera le allocazioni di risorse per un progetto specifico.
        
        Args:
            db: Sessione database
            project_id: ID del progetto
            start_date: Data iniziale opzionale per il filtro
            end_date: Data finale opzionale per il filtro
        """
        query = db.query(self.model).filter(self.model.project_id == project_id)
        
        if start_date and end_date:
            query = query.filter(
                and_(
                    self.model.start_date <= end_date,
                    self.model.end_date >= start_date
                )
            )
        elif start_date:
            query = query.filter(self.model.start_date >= start_date)
        elif end_date:
            query = query.filter(self.model.end_date <= end_date)
            
        return query.all()