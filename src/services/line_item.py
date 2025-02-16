from typing import List
from sqlalchemy.orm import Session
from src.models.models import InvoiceLineItem
from src.schemas.invoice import InvoiceLineItemBase
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