from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Union
from decimal import Decimal

from src.database.database import get_db
from src.schemas.invoice import (
    InvoiceCreate, 
    InvoiceResponse, 
    InvoiceUpdate,
    InvoiceResponseNoItems
)
from src.services.invoice import InvoiceService

router = APIRouter()
service = InvoiceService()

@router.post("/", response_model=InvoiceResponse,
    responses={
        201: {
            "description": "Fattura creata con successo",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "project_id": 1,
                        "invoice_number": "2024/001",
                        "invoice_date": "2024-02-18",
                        "due_date": "2024-03-18",
                        "amount": "1000.00",  # Calcolato automaticamente
                        "notes": "Prima fattura",
                        "line_items": [
                            {
                                "id": 1,
                                "description": "Consulenza",
                                "quantity": "8.00",
                                "rate": "125.00",
                                "amount": "1000.00"
                            }
                        ]
                    }
                }
            }
        },
        400: {
            "description": "Errore di validazione",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Numero fattura già utilizzato"
                    }
                }
            }
        }
    }
)
async def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nuova fattura.
    Il totale viene calcolato automaticamente dai line items.
    """
    try:
        return service.create(db, invoice)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Errore nella creazione della fattura: {str(e)}"
        )

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

@router.put("/{invoice_id}", response_model=InvoiceResponse)
async def update_invoice(
    invoice_id: int,
    invoice: InvoiceUpdate,
    db: Session = Depends(get_db)
):
    """
    Aggiorna una fattura esistente.
    Solleva 404 se la fattura non esiste.
    """
    updated_invoice = service.update(db, invoice_id, invoice)
    if not updated_invoice:
        raise HTTPException(
            status_code=404,
            detail=f"Fattura {invoice_id} non trovata"
        )
    return updated_invoice

@router.delete("/{invoice_id}")
async def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina una fattura.
    Solleva 404 se la fattura non esiste.
    """
    success = service.delete(db, invoice_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Fattura {invoice_id} non trovata"
        )
    return {"message": "Fattura eliminata con successo"}

