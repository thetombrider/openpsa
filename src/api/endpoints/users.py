from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.user import UserCreate, UserResponse, UserUpdate
from src.services.user import UserService
from src.models.models import UserRole

router = APIRouter()
service = UserService()

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return service.create(db, user)

@router.get("/{user_id}/projects", response_model=UserResponse)
async def get_user_with_projects(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = service.get_user_with_projects(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/consultants", response_model=List[UserResponse])
async def get_active_consultants(
    db: Session = Depends(get_db)
):
    return service.get_active_consultants(db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Recupera un utente specifico tramite il suo ID.
    
    Args:
        user_id: ID dell'utente da recuperare
        
    Raises:
        HTTPException: 404 se l'utente non esiste
    """
    user = service.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="Utente non trovato"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    Aggiorna un utente esistente.
    
    Args:
        user_id: ID dell'utente da aggiornare
        user: Dati di aggiornamento
        
    Raises:
        HTTPException: 404 se l'utente non esiste
    """
    updated_user = service.update(db, user_id, user)
    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="Utente non trovato"
        )
    return updated_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un utente.
    
    Args:
        user_id: ID dell'utente da eliminare
        
    Raises:
        HTTPException: 404 se l'utente non esiste
    """
    success = service.delete(db, user_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Utente non trovato"
        )
    return {"message": "Utente eliminato con successo"}