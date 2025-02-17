from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import AuthenticationMiddleware
from src.api.endpoints.projects import router as projects_router
from src.api.endpoints.users import router as users_router
from src.api.endpoints.time_entries import router as time_entries_router
from src.api.endpoints.invoices import router as invoices_router
from src.api.endpoints.resource_allocations import router as allocations_router
from src.api.endpoints.line_items import router as line_items_router
from src.api.endpoints.clients import router as clients_router
from src.api.endpoints.auth import router as auth_router
from src.auth.security import get_current_user

app = FastAPI(
    title="OpenPSA API",
    description="API per la gestione di progetti e risorse",
    version="1.0.0"
)

# Configurazione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware per gestire l'autenticazione
app.add_middleware(AuthenticationMiddleware, backend=get_current_user)

# Inclusione dei router
app.include_router(projects_router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(time_entries_router, prefix="/api/v1/time-entries", tags=["Time Entries"])
app.include_router(invoices_router, prefix="/api/v1/invoices", tags=["Invoices"])
app.include_router(allocations_router, prefix="/api/v1/allocations", tags=["Resource Allocations"])
app.include_router(line_items_router, prefix="/api/v1/line-items", tags=["Invoice Line Items"])
app.include_router(clients_router, prefix="/api/v1/clients", tags=["Clients"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "OpenPSA API v1.0"}