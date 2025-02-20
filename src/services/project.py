from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from src.models.models import Project
from src.schemas.project import ProjectCreate, ProjectUpdate
from src.services.base import BaseService
from src.models.models import Client
from fastapi import HTTPException

class ProjectService(BaseService[Project, ProjectCreate, ProjectUpdate]):
    def __init__(self):
        super().__init__(Project)
    
    def get_by_client(self, db: Session, client_id: int) -> List[Project]:
        return db.query(self.model).filter(self.model.client_id == client_id).all()
    
    def get_active_projects(self, db: Session) -> List[Project]:
        return db.query(self.model).filter(self.model.status == "active").all()
    
    def get_project_with_allocations(self, db: Session, project_id: int) -> Optional[Project]:
        return db.query(self.model)\
            .filter(self.model.id == project_id)\
            .options(joinedload(self.model.allocations))\
            .first()
    
    def update(self, db: Session, id: int, obj_in: ProjectUpdate) -> Optional[Project]:
        # Valida client_id se presente
        if obj_in.client_id is not None:
            client = db.query(Client).filter(Client.id == obj_in.client_id).first()
            if not client:
                raise HTTPException(
                    status_code=400,
                    detail=f"Client con ID {obj_in.client_id} non trovato"
                )
        
        return super().update(db, id, obj_in)

    def delete(self, db: Session, id: int) -> bool:
        """
        Elimina un progetto solo se non ha:
        - Time entries associate
        - Resource allocations attive 
        - Fatture
        """
        project = db.query(self.model).filter(self.model.id == id).first()
        if not project:
            return False

        # Controlla time entries
        if project.time_entries:
            raise HTTPException(
                status_code=400,
                detail="Impossibile eliminare il progetto: esistono time entries associate"
            )

        # Controlla allocations
        if project.allocations:
            raise HTTPException(
                status_code=400,
                detail="Impossibile eliminare il progetto: esistono resource allocations associate"
            )

        # Controlla fatture
        if project.invoices:
            raise HTTPException(
                status_code=400,
                detail="Impossibile eliminare il progetto: esistono fatture associate"
            )

        db.delete(project)
        db.commit()
        return True