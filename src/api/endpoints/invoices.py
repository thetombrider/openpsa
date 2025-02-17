from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Union
from src.database.database import get_db
from src.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate, InvoiceResponseNoItems
from src.services.invoice import InvoiceService

router = APIRouter()
service = InvoiceService()

@router.post("/", response_model=InvoiceResponse)
async def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    return service.create(db, invoice)

@router.get("/project/{project_id}", response_model=List[Union[InvoiceResponse, InvoiceResponseNoItems]])
async def get_project_invoices(
    project_id: int,
    include_line_items: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    Recupera tutte le fatture per un progetto.
    Se include_line_items=false, non include i line items nella risposta.
    """
    invoices = service.get_by_project(db, project_id)
    response_model = InvoiceResponse if include_line_items else InvoiceResponseNoItems
    return [response_model.model_validate(invoice, from_attributes=True) for invoice in invoices]

@router.get("/unpaid", response_model=List[InvoiceResponseNoItems])
async def get_unpaid_invoices(
    db: Session = Depends(get_db)
):
    return service.get_unpaid_invoices(db)