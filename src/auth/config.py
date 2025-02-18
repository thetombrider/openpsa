from typing import List
from src.models.models import UserRole

# Token settings
JWT_SECRET_KEY = "your-secret-key"  # Sposta in .env
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Public routes che non richiedono autenticazione
PUBLIC_ROUTES: List[str] = [
    "/api/v1/auth/token",
    "/api/v1/auth/register",
    "/api/v1/auth/refresh",
    "/docs",
    "/redoc",
    "/openapi.json"
]

# Permessi per risorsa
PROJECT_PERMISSIONS = {
    "create": ["ADMIN", "MANAGER"],
    "read": ["ADMIN", "MANAGER", "CONSULTANT"],
    "update": ["ADMIN", "MANAGER"],
    "delete": ["ADMIN"]
}

CLIENT_PERMISSIONS = {
    "create": ["ADMIN"],
    "read": ["ADMIN", "MANAGER"],
    "update": ["ADMIN"],
    "delete": ["ADMIN"]
}

USER_PERMISSIONS = {
    "create": [UserRole.ADMIN],
    "read": [UserRole.ADMIN, UserRole.MANAGER],
    "update": [UserRole.ADMIN],
    "delete": [UserRole.ADMIN]
}