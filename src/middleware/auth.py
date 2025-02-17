# src/middleware/auth.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.auth.security import verify_token, PUBLIC_ROUTES

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # Verifica se il path è pubblico
        if path in PUBLIC_ROUTES or any(
            path.startswith(public_route) 
            for public_route in ["/docs/", "/redoc/", "/openapi."]
        ):
            return await call_next(request)

        try:
            # Verifica il token per tutte le altre route
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JSONResponse(
                    status_code=401,
                    content={
                        "detail": "Token di autenticazione mancante"
                    },
                    headers={"WWW-Authenticate": "Bearer"}
                )

            # Estrai e verifica il token
            token = auth_header.split(' ')[1]
            try:
                request.state.user = await verify_token(token)
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"detail": e.detail},
                    headers={"WWW-Authenticate": "Bearer"}
                )

            return await call_next(request)
            
        except Exception as e:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Errore di autenticazione"
                },
                headers={"WWW-Authenticate": "Bearer"}
            )