from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate
from src.services.invoice import InvoiceService

router = APIRouter()
service = InvoiceService()

@router.post("/", response_model=InvoiceResponse)
async def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    return service.create(db, invoice)

@router.get("/project/{project_id}", response_model=List[InvoiceResponse])
async def get_project_invoices(
    project_id: int,
    include_line_items: bool = False,
    db: Session = Depends(get_db)
):
    return service.get_project_invoices(db, project_id, include_line_items)

@router.get("/unpaid", response_model=List[InvoiceResponse])
async def get_unpaid_invoices(
    db: Session = Depends(get_db)
):
    return service.get_unpaid_invoices(db)