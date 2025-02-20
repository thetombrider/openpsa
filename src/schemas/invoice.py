from pydantic import BaseModel, Field, model_validator, field_validator, ValidationInfo
from typing import Annotated, Optional, List
from datetime import date
from decimal import Decimal

class InvoiceLineItemBase(BaseModel):
    description: str
    quantity: Decimal = Field(gt=0, description="Deve essere maggiore di zero")
    rate: Decimal = Field(gt=0, description="Deve essere maggiore di zero")

class InvoiceLineItemCreate(InvoiceLineItemBase):
    billing_rate_id: Optional[int] = None
    description: str
    quantity: Decimal
    rate: Optional[Decimal] = None  # Opzionale se viene preso da billing_rate

    @field_validator('rate')
    @classmethod
    def validate_rate(cls, v: Optional[Decimal], info: ValidationInfo) -> Decimal:
        if v is None and info.data.get('billing_rate_id') is None:
            raise ValueError("Devi specificare o rate o billing_rate_id")
        return v

    @field_validator('quantity')
    @classmethod
    def validate_time_entries(cls, v: float, info: ValidationInfo) -> float:
        if not hasattr(info.data, 'time_entries'):
            return v

        total_hours = sum(entry.hours for entry in info.data.time_entries)
        if v > total_hours:
            raise ValueError(
                f"Non puoi fatturare più ore di quelle registrate. "
                f"Ore registrate: {total_hours}"
            )
        return v

class InvoiceCreate(BaseModel):
    project_id: int
    invoice_number: str = Field(min_length=1, max_length=50)
    invoice_date: date
    due_date: date
    notes: Optional[str] = None
    line_items: List[InvoiceLineItemBase]

    @model_validator(mode='after')
    def validate_dates_and_invoice(self) -> 'InvoiceCreate':
        if self.due_date < self.invoice_date:
            raise ValueError("La data di scadenza deve essere successiva alla data fattura")
        
        if self.invoice_number.lower() == 'string':
            raise ValueError("Il numero fattura non può essere 'string'")
            
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "project_id": 1,
                "invoice_number": "2024/001",
                "invoice_date": "2024-02-18",
                "due_date": "2024-03-18",
                "notes": "Prima fattura",  # Rimosso amount
                "line_items": [
                    {
                        "description": "Consulenza",
                        "quantity": "8",
                        "rate": "125.00"
                    }
                ]
            }
        }
    }

class InvoiceUpdate(BaseModel):
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    amount: Optional[Decimal] = None
    paid: Optional[bool] = None
    paid_date: Optional[date] = None
    notes: Optional[str] = None

class InvoiceResponseNoItems(BaseModel):
    id: int
    project_id: int
    invoice_number: str
    invoice_date: date
    due_date: date
    amount: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    notes: Optional[str] = None
    paid: bool = False
    paid_date: Optional[date] = None
    
    class Config:
        orm_mode = True

class InvoiceLineItemResponse(InvoiceLineItemBase):
    id: int
    invoice_id: int
    amount: Decimal  # Solo nella risposta, calcolato dal service

    class Config:
        from_attributes = True

class InvoiceBase(BaseModel):
    project_id: int
    invoice_number: str
    invoice_date: date
    due_date: date = None
    amount: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    notes: Optional[str] = None
    line_items: List[InvoiceLineItemBase] = None

class InvoiceResponse(InvoiceBase):
    id: int
    
    class Config:
        from_attributes = True