from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.models.models import User, UserRole
from src.database.database import get_db
import logging
from src.auth.config import (
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    PUBLIC_ROUTES
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "token_type": "refresh"
    })
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def create_token_pair(user_data: dict) -> Tuple[str, str]:
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    return access_token, refresh_token

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenziali non valide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Utente disattivato"
        )
    return current_user

async def verify_token(token: str) -> User:
    """
    Verifica il token JWT e restituisce l'utente
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Token non valido"
            )
            
        db = next(get_db())
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Utente non trovato"
            )
            
        return user
        
    except JWTError as je:
        raise HTTPException(
            status_code=401,
            detail=f"Token non valido: {str(je)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Errore di autenticazione: {str(e)}"
        )

def verify_refresh_token(token: str) -> dict:
    """
    Verifica che il token sia un refresh token valido
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        # Verifica che sia un refresh token
        if payload.get("token_type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Token non valido: non è un refresh token"
            )
            
        # Verifica presenza email
        if not payload.get("sub"):
            raise HTTPException(
                status_code=401,
                detail="Token non valido: manca l'identificativo utente"
            )
            
        return payload
        
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token non valido o scaduto"
        )