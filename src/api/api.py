from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from src.middleware.auth import AuthMiddleware
from src.api.endpoints.projects import router as projects_router
from src.api.endpoints.users import router as users_router
from src.api.endpoints.time_entries import router as time_entries_router
from src.api.endpoints.invoices import router as invoices_router
from src.api.endpoints.resource_allocations import router as allocations_router
from src.api.endpoints.line_items import router as line_items_router
from src.api.endpoints.clients import router as clients_router
from src.api.endpoints.auth import router as auth_router
from src.api.endpoints.utils import router as utils_router

# Importa tutti gli schemi necessari
from src.schemas.auth import Token, LoginRequest
from src.schemas.user import UserCreate, UserResponse

app = FastAPI(
    title="OpenPSA API",
    description="API per la gestione di progetti e risorse",
    version="1.0.0",
    # Aggiungi la configurazione di sicurezza
    openapi_tags=[
        {"name": "Authentication", "description": "Operazioni di autenticazione"},
        {"name": "Users", "description": "Gestione utenti"},
        # ... altri tag
    ],
    swagger_ui_parameters={"persistAuthorization": True}
)

# Configurazione CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware per l'autenticazione
app.add_middleware(AuthMiddleware)

# Configura lo schema OAuth2 per Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# Configura la documentazione OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Aggiungi SOLO lo schema di sicurezza
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Applica la sicurezza globalmente
    openapi_schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Inclusione dei router
app.include_router(projects_router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(time_entries_router, prefix="/api/v1/time-entries", tags=["Time Entries"])
app.include_router(invoices_router, prefix="/api/v1/invoices", tags=["Invoices"])
app.include_router(allocations_router, prefix="/api/v1/allocations", tags=["Resource Allocations"])
app.include_router(line_items_router, prefix="/api/v1/line-items", tags=["Invoice Line Items"])
app.include_router(clients_router, prefix="/api/v1/clients", tags=["Clients"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(utils_router, prefix="/api/v1/utils", tags=["Utilities"])

@app.get("/")
async def root():
    return {"message": "Open PSA API v1.0"}

