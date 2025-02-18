# src/api/endpoints/utils.py
from fastapi import APIRouter
from src.models.models import (
    ProjectStatus,
    BillingType,
    ConsultantRole,
    UserRole,
    ResourceAllocationStatus
)

router = APIRouter()

@router.get("/enums", 
    description="Recupera tutti gli enum utilizzati nel sistema",
    response_model=dict,
    responses={
        200: {
            "description": "Enum recuperati con successo",
            "content": {
                "application/json": {
                    "example": {
                        "project_status": ["DRAFT", "ACTIVE", "COMPLETED", "CANCELLED"],
                        "billing_types": ["TIME_AND_MATERIALS", "FIXED_PRICE"],
                        "consultant_roles": ["JUNIOR", "MID", "SENIOR", "MASTER", "PRINCIPAL"],
                        "user_roles": ["ADMIN", "MANAGER", "CONSULTANT"],
                        "resource_allocation_status": ["PLANNED", "ACTIVE", "COMPLETED", "CANCELLED"]
                    }
                }
            }
        }
    }
)
async def get_enums():
    """Recupera gli enum utilizzati nel sistema"""
    return {
        "project_status": [status.value for status in ProjectStatus],
        "billing_types": [btype.value for btype in BillingType],
        "consultant_roles": [role.value for role in ConsultantRole],
        "user_roles": [role.value for role in UserRole],
        "resource_allocation_status": [status.value for status in ResourceAllocationStatus]
    }