from typing import List, Optional
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from src.models.models import Invoice, InvoiceLineItem
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

    def get_by_project(self, db: Session, project_id: int) -> List[Invoice]:
        query = db.query(Invoice).filter(Invoice.project_id == project_id)
        return query.all()
    
    def create(self, db: Session, invoice_in: InvoiceCreate) -> Invoice:
        """Crea una nuova fattura con i suoi line items"""
        
        # Verifica unicità numero fattura
        existing = db.query(Invoice).filter(
            Invoice.invoice_number == invoice_in.invoice_number
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Numero fattura '{invoice_in.invoice_number}' già utilizzato"
            )
        
        # Calcola il totale dai line items
        total = sum(item.quantity * item.rate for item in invoice_in.line_items)
        
        # Crea la fattura con il totale calcolato
        db_invoice = Invoice(
            project_id=invoice_in.project_id,
            invoice_number=invoice_in.invoice_number,
            invoice_date=invoice_in.invoice_date,
            due_date=invoice_in.due_date,
            amount=total,  # Usa il totale calcolato
            notes=invoice_in.notes
        )
        db.add(db_invoice)
        db.flush()  # Ottieni l'ID della fattura
        
        # Crea i line items
        total_amount = Decimal('0')
        for item in invoice_in.line_items:
            quantity = Decimal(str(item.quantity))
            rate = Decimal(str(item.rate))
            amount = quantity * rate
            
            line_item = InvoiceLineItem(
                invoice_id=db_invoice.id,
                description=item.description,
                quantity=quantity,
                rate=rate,
                amount=amount
            )
            total_amount += amount
            db.add(line_item)
        
        # Aggiorna l'importo totale della fattura
        db_invoice.amount = total_amount
        db.commit()
        db.refresh(db_invoice)
        return db_invoice