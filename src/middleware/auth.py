# src/middleware/auth.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.auth.security import verify_token
from src.auth.config import PUBLIC_ROUTES
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token mancante"}
            )

        try:
            token = auth_header.split(" ")[1]
            user = await verify_token(token)
            request.state.user = user
            response = await call_next(request)
            return response
        except HTTPException as he:
            return JSONResponse(
                status_code=he.status_code,
                content={"detail": he.detail}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"detail": f"Errore interno: {str(e)}"}
            )