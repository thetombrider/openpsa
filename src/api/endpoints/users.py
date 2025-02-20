from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.user import UserCreate, UserResponse, UserUpdate, UserUpdateResponse
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
    request: Request,
    db: Session = Depends(get_db)
):
    user = service.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Utente {user_id} non trovato"
        )
    return user

@router.put("/{user_id}", response_model=UserUpdateResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Aggiorna un utente esistente.
    Se l'email viene modificata, vengono generati nuovi token di accesso.
    """
    updated_user = service.update(db, user_id, user)
    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="Utente non trovato"
        )
    
    # Prepara la risposta base
    response_data = {
        "id": updated_user.id,
        "email": updated_user.email,
        "name": updated_user.name,
        "role": updated_user.role,
        "hourly_rate": updated_user.hourly_rate,
        "created_at": updated_user.created_at
    }
    
    # Se l'email è cambiata, aggiungi i nuovi token
    if hasattr(user, 'email') and user.email:
        from src.auth.security import create_token_pair
        access_token, refresh_token = create_token_pair({
            "sub": updated_user.email,
            "role": updated_user.role.value
        })
        response_data.update({
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    
    return UserUpdateResponse(**response_data)

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