from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Optional
from src.models.models import ConsultantRole, ProjectUser

class ProjectUserBase(BaseModel):
    project_id: int
    user_id: int
    role: Optional[ConsultantRole] = None

class ProjectUserCreate(ProjectUserBase):
    @field_validator('user_id')
    @classmethod
    def validate_user_assignment(cls, v: int, info: ValidationInfo) -> int:
        if not hasattr(info.data, 'project_id'):
            raise ValueError("project_id è richiesto")

        from src.services.project import ProjectService
        from src.database.database import SessionLocal
        
        db = SessionLocal()
        try:
            # Verifica se l'utente è già assegnato al progetto
            existing = db.query(ProjectUser).filter(
                ProjectUser.user_id == v,
                ProjectUser.project_id == info.data.project_id
            ).first()
            
            if existing:
                raise ValueError("L'utente è già assegnato a questo progetto")
        finally:
            db.close()
        
        return v

class ProjectUserUpdate(BaseModel):
    role: Optional[ConsultantRole] = None

class ProjectUserResponse(ProjectUserBase):
    class Config:
        orm_mode = True