from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from src.services.client import ClientService

router = APIRouter()
service = ClientService()

@router.post("/", response_model=ClientResponse)
async def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    return service.create(db, client)

@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    client = service.get(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/", response_model=List[ClientResponse])
async def list_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return service.list(db, skip=skip, limit=limit)

@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client: ClientUpdate,
    db: Session = Depends(get_db)
):
    updated_client = service.update(db, client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client

@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    success = service.delete(db, client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}