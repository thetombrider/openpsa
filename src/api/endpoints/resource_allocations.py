from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from src.database.database import get_db
from src.schemas.resource_allocation import ResourceAllocationCreate, ResourceAllocationResponse, ResourceAllocationUpdate
from src.services.resource_allocation import ResourceAllocationService

router = APIRouter()
service = ResourceAllocationService()

@router.post("/", response_model=ResourceAllocationResponse)
async def create_allocation(
    allocation: ResourceAllocationCreate,
    db: Session = Depends(get_db)
):
    return service.create(db, allocation)

@router.get("/user/{user_id}", response_model=List[ResourceAllocationResponse])
async def get_user_allocations(
    user_id: int,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    return service.get_user_allocations(db, user_id, start_date, end_date)

@router.get("/availability/{user_id}")
async def check_user_availability(
    user_id: int,
    start_date: date,
    end_date: date,
    request: Request,
    db: Session = Depends(get_db)
) -> dict:
    available = service.check_availability(db, user_id, start_date, end_date)
    return {
        "available_percentage": available,
        "is_fully_available": available == 1,
        "is_partially_available": 0 < available < 1,
        "is_fully_allocated": available == 0
    }

@router.get("/project/{project_id}", response_model=List[ResourceAllocationResponse])
async def get_project_allocations(
    project_id: int,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """
    Recupera tutte le allocazioni per un progetto specifico.
    Opzionalmente filtra per intervallo di date.
    
    Args:
        project_id: ID del progetto
        start_date: Data iniziale opzionale
        end_date: Data finale opzionale
    """
    return service.get_project_allocations(db, project_id, start_date, end_date)