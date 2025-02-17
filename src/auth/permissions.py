from functools import wraps
from typing import List
from fastapi import HTTPException, Depends
from src.models.models import UserRole, User
from src.auth.security import get_current_user

def require_roles(roles: List[UserRole]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if current_user.role not in roles:
                raise HTTPException(
                    status_code=403,
                    detail="Permesso negato: ruolo non autorizzato"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator