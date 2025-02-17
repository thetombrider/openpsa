from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.auth.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    create_token_pair,
    verify_refresh_token,
    get_password_hash
)
from src.schemas.user import UserBase, UserCreate
from src.models.models import User
from datetime import timedelta

router = APIRouter()

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Email o password non corretti"
        )
    
    # Crea coppia di token
    access_token, refresh_token = create_token_pair(
        {"sub": user.email, "role": user.role.value}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh_token(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Rinnova l'access token usando un refresh token valido
    """
    # Verifica il refresh token
    payload = verify_refresh_token(token)
    
    # Recupera l'utente
    user = db.query(User).filter(User.email == payload["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Utente non trovato"
        )
    
    # Crea nuovo access token
    access_token = create_access_token(
        {"sub": user.email, "role": user.role.value}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/register")
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Verifica se l'utente esiste già
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email già registrata"
        )
    
    # Crea il nuovo utente con password hashata
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_password,
        role=user_data.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "Utente registrato con successo"}