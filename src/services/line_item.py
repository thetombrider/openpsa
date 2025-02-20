from decimal import Decimal
from typing import List
from sqlalchemy.orm import Session
from src.models.models import InvoiceLineItem, BillingRate
from fastapi import HTTPException
from src.schemas.invoice import InvoiceLineItemBase, InvoiceLineItemCreate
from src.services.base import BaseService

class LineItemService(BaseService[InvoiceLineItem, InvoiceLineItemBase, InvoiceLineItemBase]):
    def __init__(self):
        super().__init__(InvoiceLineItem)
    
    def get_by_invoice(self, db: Session, invoice_id: int) -> List[InvoiceLineItem]:
        return db.query(self.model)\
            .filter(self.model.invoice_id == invoice_id)\
            .all()
    
    def batch_create(
        self, 
        db: Session, 
        invoice_id: int, 
        line_items: List[InvoiceLineItemBase]
    ) -> List[InvoiceLineItem]:
        db_items = []
        for item in line_items:
            db_item = self.model(
                **item.model_dump(),
                invoice_id=invoice_id
            )
            db.add(db_item)
            db_items.append(db_item)
        
        db.commit()
        for item in db_items:
            db.refresh(item)
        return db_items

    def create(self, db: Session, obj_in: InvoiceLineItemCreate) -> InvoiceLineItem:
        obj_data = obj_in.model_dump()
        
        # Se c'è un billing_rate_id, usa quel rate
        if obj_data.get('billing_rate_id'):
            billing_rate = db.query(BillingRate).get(obj_data['billing_rate_id'])
            if not billing_rate:
                raise HTTPException(
                    status_code=404,
                    detail="BillingRate non trovato"
                )
            obj_data['rate'] = billing_rate.rate
        
        # Calcola l'amount
        amount = Decimal(str(obj_data["quantity"])) * Decimal(str(obj_data["rate"]))
        obj_data["amount"] = amount
        
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, id: int, obj_in: InvoiceLineItemBase) -> InvoiceLineItem:
        """Aggiorna un line item ricalcolando l'amount"""
        db_obj = self.get(db, id)
        if not db_obj:
            return None
            
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Se quantity o rate cambiano, ricalcola amount
        if "quantity" in update_data or "rate" in update_data:
            quantity = update_data.get("quantity", db_obj.quantity)
            rate = update_data.get("rate", db_obj.rate)
            update_data["amount"] = Decimal(str(quantity)) * Decimal(str(rate))
            
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj