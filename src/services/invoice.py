from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session, joinedload
from src.models.models import Invoice
from src.schemas.invoice import InvoiceCreate, InvoiceUpdate
from src.services.base import BaseService

class InvoiceService(BaseService[Invoice, InvoiceCreate, InvoiceUpdate]):
    def __init__(self):
        super().__init__(Invoice)
    
    def get_project_invoices(
        self, 
        db: Session, 
        project_id: int, 
        include_line_items: bool = False
    ) -> List[Invoice]:
        query = db.query(self.model)\
            .filter(self.model.project_id == project_id)
            
        if include_line_items:
            query = query.options(joinedload(self.model.line_items))
            
        return query.all()
    
    def get_unpaid_invoices(self, db: Session) -> List[Invoice]:
        return db.query(self.model)\
            .filter(self.model.paid == False)\
            .filter(self.model.due_date <= date.today())\
            .all()