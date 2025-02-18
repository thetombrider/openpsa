# src/middleware/auth.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.auth.security import verify_token
from src.auth.config import PUBLIC_ROUTES

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Aggiungi logging per debug
        print(f"Method: {request.method}, Path: {request.url.path}")
        print(f"Headers: {request.headers}")

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
                user = await verify_token(token)
                # Aggiungi logging dell'utente
                print(f"User authenticated: {user.email}, Role: {user.role}")
                request.state.user = user
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"detail": e.detail},
                    headers={"WWW-Authenticate": "Bearer"}
                )

            return await call_next(request)
            
        except Exception as e:
            print(f"Authentication error: {str(e)}")  # Debug log
            return JSONResponse(
                status_code=401,
                content={
                    "detail": f"Token non valido: {str(e)}"
                },
                headers={"WWW-Authenticate": "Bearer"}
            )