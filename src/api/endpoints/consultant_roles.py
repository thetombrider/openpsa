# src/api/endpoints/consultant_roles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.consultant_role import ConsultantRoleCreate, ConsultantRoleResponse
from src.services.consultant_role import ConsultantRoleService

router = APIRouter()
service = ConsultantRoleService()

@router.post("/", response_model=ConsultantRoleResponse)
async def create_role(
    role: ConsultantRoleCreate,
    db: Session = Depends(get_db)
):
    return service.create(db, role)

@router.get("/", response_model=List[ConsultantRoleResponse])
async def get_roles(
    db: Session = Depends(get_db)
):
    return service.list(db)

@router.get("/{role_id}", response_model=ConsultantRoleResponse)
async def get_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    role = service.get(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role