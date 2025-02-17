from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Annotated
from datetime import date
from typing import Optional, List
from decimal import Decimal

class InvoiceLineItemBase(BaseModel):
    description: str
    quantity: float
    rate: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]

class InvoiceLineItemCreate(InvoiceLineItemBase):
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

class InvoiceBase(BaseModel):
    project_id: int
    invoice_number: str
    invoice_date: date
    due_date: date = None
    amount: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    notes: Optional[str] = None
    line_items: List[InvoiceLineItemBase]

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    due_date: Optional[date] = None
    paid: Optional[bool] = None
    paid_date: Optional[date] = None
    notes: Optional[str] = None

class InvoiceResponse(InvoiceBase):
    id: int
    paid: bool = False
    paid_date: Optional[date] = None
    
    class Config:
        orm_mode = True