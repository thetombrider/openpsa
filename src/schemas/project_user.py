from pydantic import BaseModel, ConfigDict
from typing import Optional
from pydantic.fields import Field, field_validator, ValidationInfo
from src.models.models import ProjectUser
from .consultant_role import ConsultantRoleResponse

class ProjectUserBase(BaseModel):
    project_id: int
    user_id: int
    role_id: Optional[int] = None

class ProjectUserCreate(ProjectUserBase):

    @field_validator('user_id')
    @classmethod
    def validate_user_assignment(cls, v: int, info: ValidationInfo) -> int:
        if not hasattr(info.data, 'project_id'):
            raise ValueError("project_id è richiesto")

        from src.database.database import SessionLocal
        
        db = SessionLocal()
        try:
            # Verifica se l'utente è già assegnato al progetto
            existing = db.query(ProjectUser).filter(
                ProjectUser.user_id == v,
                ProjectUser.project_id == info.data.project_id,
                ProjectUser.is_active == True  # Opzionale: aggiungi se gestisci soft delete
            ).first()
            
            if existing:
                raise ValueError("L'utente è già assegnato a questo progetto")
        finally:
            db.close()
        
        return v

    @field_validator('role_id')
    @classmethod
    def validate_role_exists(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v

        from src.database.database import SessionLocal
        from src.models.models import ConsultantRole
        
        db = SessionLocal()
        try:
            role = db.query(ConsultantRole).get(v)
            if not role:
                raise ValueError("Il ruolo specificato non esiste")
        finally:
            db.close()
        
        return v

class ProjectUserUpdate(BaseModel):
    role_id: Optional[int] = None

class ProjectUserResponse(ProjectUserBase):
    id: int
    role: Optional[ConsultantRoleResponse] = None

    model_config = ConfigDict(from_attributes=True)