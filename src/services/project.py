from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from src.models.models import Project
from src.schemas.project import ProjectCreate, ProjectUpdate
from src.services.base import BaseService

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