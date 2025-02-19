# src/services/rate.py
from typing import List
from sqlalchemy.orm import Session
from src.services.base import BaseService
from src.models.models import CostRate, BillingRate
from src.schemas.rate import CostRateCreate, BillingRateCreate

class CostRateService(BaseService[CostRate, CostRateCreate, CostRateCreate]):
    def __init__(self):
        super().__init__(CostRate)

    def get_user_rates(self, db: Session, user_id: int) -> List[CostRate]:
        return db.query(self.model)\
            .join(self.model.user_cost_rates)\
            .filter(self.model.user_cost_rates.any(user_id=user_id))\
            .all()

class BillingRateService(BaseService[BillingRate, BillingRateCreate, BillingRateCreate]):
    def __init__(self):
        super().__init__(BillingRate)

    def get_user_rates(self, db: Session, user_id: int) -> List[BillingRate]:
        return db.query(self.model)\
            .join(self.model.user_billing_rates)\
            .filter(self.model.user_billing_rates.any(user_id=user_id))\
            .all()