from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.user import UserCreate, UserResponse, UserUpdate
from src.services.user import UserService

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