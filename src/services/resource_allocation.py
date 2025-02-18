from typing import List, Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from src.models.models import ResourceAllocation, ResourceAllocationStatus
from src.schemas.resource_allocation import ResourceAllocationCreate, ResourceAllocationUpdate
from src.services.base import BaseService

class ResourceAllocationService(BaseService[ResourceAllocation, ResourceAllocationCreate, ResourceAllocationUpdate]):
    def __init__(self):
        super().__init__(ResourceAllocation)
    
    def get_user_allocations(
        self, 
        db: Session, 
        user_id: int, 
        start_date: Optional[date] = None, 
        end_date: Optional[date] = None
    ) -> List[ResourceAllocation]:
        """
        Recupera tutte le allocazioni di un utente, opzionalmente filtrate per periodo
        """
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
        """
        Verifica la disponibilità di un utente in un periodo
        Ritorna la percentuale media di disponibilità nel periodo
        """
        # Debug log
        print(f"Checking availability for period: {start_date} - {end_date}")
        
        # Recupera tutte le allocazioni nel periodo
        allocations = db.query(ResourceAllocation).filter(
            and_(
                ResourceAllocation.user_id == user_id,
                ResourceAllocation.status.in_([
                    ResourceAllocationStatus.PLANNED,
                    ResourceAllocationStatus.ACTIVE
                ]),
                ResourceAllocation.start_date <= end_date,
                ResourceAllocation.end_date >= start_date
            )
        ).all()

        print(f"Found {len(allocations)} allocations in period")
        
        # Calcola disponibilità giornaliera
        days = []
        current_date = start_date
        while current_date <= end_date:
            day_allocations = [
                a for a in allocations 
                if a.start_date <= current_date <= a.end_date
            ]
            
            daily_allocation = sum(a.allocation_percentage for a in day_allocations)
            daily_availability = max(0, 1 - daily_allocation)
            
            print(f"Date {current_date}: allocated {daily_allocation}, available {daily_availability}")
            days.append(daily_availability)
            current_date += timedelta(days=1)

        # Calcola media disponibilità
        average_availability = sum(days) / len(days)
        print(f"Average availability: {average_availability}")
        
        return average_availability

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