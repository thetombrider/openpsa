from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from src.models.models import User
from src.schemas.user import UserCreate, UserUpdate
from src.services.base import BaseService

class UserService(BaseService[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()
    
    def get_user_with_projects(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(self.model)\
            .filter(self.model.id == user_id)\
            .options(joinedload(self.model.projects))\
            .first()
            
    def get_active_consultants(self, db: Session) -> List[User]:
        return db.query(self.model)\
            .filter(self.model.role == "consultant")\
            .all()