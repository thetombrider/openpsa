# src/api/endpoints/rates.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.rate import (
    CostRateCreate, 
    BillingRateCreate,
    RateResponse
)
from src.services.rate import CostRateService, BillingRateService

router = APIRouter()
cost_service = CostRateService()
billing_service = BillingRateService()

@router.post("/cost", response_model=RateResponse)
async def create_cost_rate(
    rate: CostRateCreate,
    db: Session = Depends(get_db)
):
    return cost_service.create(db, rate)

@router.post("/billing", response_model=RateResponse)
async def create_billing_rate(
    rate: BillingRateCreate,
    db: Session = Depends(get_db)
):
    return billing_service.create(db, rate)

@router.get("/user/{user_id}/cost", response_model=List[RateResponse])
async def get_user_cost_rates(
    user_id: int,
    db: Session = Depends(get_db)
):
    return cost_service.get_user_rates(db, user_id)

@router.get("/user/{user_id}/billing", response_model=List[RateResponse])
async def get_user_billing_rates(
    user_id: int,
    db: Session = Depends(get_db)
):
    return billing_service.get_user_rates(db, user_id)