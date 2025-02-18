from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from src.models.models import User
from src.schemas.user import UserCreate, UserUpdate
from src.services.base import BaseService
from src.auth.security import get_password_hash

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
    
    def create(self, db: Session, user_in: UserCreate) -> User:
        """
        Crea un nuovo utente con password hashata
        """
        # Converti lo schema in dict ed elimina la password in chiaro
        user_data = user_in.model_dump(exclude={"password"})
        
        # Crea l'hash della password
        user_data["password_hash"] = get_password_hash(user_in.password)
        
        # Crea l'utente con i dati modificati
        db_user = self.model(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user