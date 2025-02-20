# src/api/endpoints/rates.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from src.database.database import get_db
from src.schemas.rate import (
    CostRateCreate, 
    BillingRateCreate,
    RateResponse,
    UserRateAssign
)
from src.services.rate import CostRateService, BillingRateService
from src.models.models import UserBillingRate, UserCostRate, User

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

@router.get("/billing/{rate_id}", response_model=RateResponse)
async def get_billing_rate(
    rate_id: int,
    db: Session = Depends(get_db)
):
    rate = billing_service.get(db, rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="Tariffa non trovata")
    return rate

@router.get("/cost/{rate_id}", response_model=RateResponse)
async def get_cost_rate(
    rate_id: int,
    db: Session = Depends(get_db)
):
    rate = cost_service.get(db, rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="Tariffa non trovata")
    return rate

@router.delete("/billing/{rate_id}")
async def delete_billing_rate(
    rate_id: int,
    db: Session = Depends(get_db)
):
    success = billing_service.delete(db, rate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tariffa non trovata")
    return {"message": "Tariffa eliminata con successo"}

@router.delete("/cost/{rate_id}")
async def delete_cost_rate(
    rate_id: int,
    db: Session = Depends(get_db)
):
    success = cost_service.delete(db, rate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tariffa non trovata")
    return {"message": "Tariffa eliminata con successo"}

@router.post("/billing/assign", response_model=RateResponse)
async def assign_billing_rate(
    assignment: UserRateAssign,
    db: Session = Depends(get_db)
):
    # Verifica esistenza tariffa
    rate = billing_service.get(db, assignment.rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="Tariffa non trovata")
    
    # Verifica esistenza utente
    user = db.query(User).filter(User.id == assignment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
        
    # Crea l'assegnazione
    user_rate = UserBillingRate(
        user_id=assignment.user_id,
        billing_rate_id=assignment.rate_id,
        valid_from=assignment.valid_from,
        valid_to=assignment.valid_to
    )
    db.add(user_rate)
    db.commit()
    return rate

@router.post("/cost/assign", response_model=RateResponse)
async def assign_cost_rate(
    assignment: UserRateAssign,
    db: Session = Depends(get_db)
):
    # Verifica esistenza tariffa
    rate = cost_service.get(db, assignment.rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="Tariffa non trovata")
    
    # Verifica esistenza utente
    user = db.query(User).filter(User.id == assignment.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
        
    # Crea l'assegnazione
    user_rate = UserCostRate(
        user_id=assignment.user_id,
        cost_rate_id=assignment.rate_id,
        valid_from=assignment.valid_from,
        valid_to=assignment.valid_to
    )
    db.add(user_rate)
    db.commit()
    return rate