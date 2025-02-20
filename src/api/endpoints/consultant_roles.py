# src/api/endpoints/consultant_roles.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.consultant_role import (
    ConsultantRoleCreate, 
    ConsultantRoleResponse,
    ConsultantRoleUpdate
)
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

@router.put("/{role_id}", response_model=ConsultantRoleResponse)
async def update_role(
    role_id: int,
    role: ConsultantRoleUpdate,
    db: Session = Depends(get_db)
):
    updated_role = service.update(db, role_id, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="Ruolo non trovato")
    return updated_role

@router.delete("/{role_id}")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    success = service.delete(db, role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ruolo non trovato")
    return {"message": "Ruolo eliminato con successo"}