from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.invoice import InvoiceLineItemBase
from src.services.line_item import LineItemService

router = APIRouter()
service = LineItemService()

@router.post("/invoice/{invoice_id}/items", response_model=List[InvoiceLineItemBase])
async def add_line_items(
    invoice_id: int,
    line_items: List[InvoiceLineItemBase],
    db: Session = Depends(get_db)
):
    return service.batch_create(db, invoice_id, line_items)

@router.get("/invoice/{invoice_id}/items", response_model=List[InvoiceLineItemBase])
async def get_invoice_items(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    return service.get_by_invoice(db, invoice_id)

@router.put("/items/{item_id}", response_model=InvoiceLineItemBase)
async def update_line_item(
    item_id: int,
    item: InvoiceLineItemBase,
    db: Session = Depends(get_db)
):
    updated_item = service.update(db, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Line item not found")
    return updated_item

@router.delete("/items/{item_id}")
async def delete_line_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    success = service.delete(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Line item not found")
    return {"message": "Line item deleted successfully"}