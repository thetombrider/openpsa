from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from src.database.database import get_db
from src.schemas.time_entry import TimeEntryCreate, TimeEntryResponse, TimeEntryUpdate
from src.services.time_entry import TimeEntryService

router = APIRouter()
service = TimeEntryService()

@router.post("/", response_model=TimeEntryResponse)
async def create_time_entry(
    time_entry: TimeEntryCreate,
    db: Session = Depends(get_db)
):
    return service.create(db, time_entry)

@router.get("/user/{user_id}", response_model=List[TimeEntryResponse])
async def get_user_time_entries(
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    Recupera le time entry di un utente.
    Se non vengono specificate le date, restituisce tutte le time entry.
    
    Args:
        user_id: ID dell'utente
        start_date: Data iniziale opzionale
        end_date: Data finale opzionale
    """
    return service.get_by_user_and_date_range(db, user_id, start_date, end_date)

@router.get("/project/{project_id}", response_model=List[TimeEntryResponse])
async def get_project_time_entries(
    project_id: int,
    db: Session = Depends(get_db)
):
    return service.get_by_project(db, project_id)

@router.delete("/{time_entry_id}")
async def delete_time_entry(
    time_entry_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una time entry dato il suo ID.
    Restituisce un messaggio di successo o un errore 404 se non trovata.
    """
    success = service.delete(db, time_entry_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Time entry non trovata"
        )
    return {"message": "Time entry eliminata con successo"}