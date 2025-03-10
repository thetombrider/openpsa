from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from src.models.models import User, UserRole
from src.schemas.user import UserCreate, UserUpdate
from src.services.base import BaseService
from src.auth.security import get_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

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
            .filter(self.model.role == UserRole.CONSULTANT)\
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

    def get(self, db: Session, id: int) -> Optional[User]:
        """Override del metodo get per aggiungere logging"""
        user = db.query(self.model).filter(self.model.id == id).first()
        if not user:
            print(f"User {id} not found in database")  # Debug log
        return user

    def update(self, db: Session, id: int, user_in: UserUpdate) -> Optional[User]:
        """
        Aggiorna un utente e gestisce il cambio email
        """
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return None
            
        # Salva la vecchia email per il check
        old_email = db_obj.email
        
        # Aggiorna l'oggetto
        obj_data = jsonable_encoder(db_obj)
        update_data = user_in.model_dump(exclude_unset=True)
        
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        
        # Se l'email è cambiata, verifica che non esista già
        if 'email' in update_data and old_email != update_data['email']:
            existing = db.query(self.model).filter(
                self.model.email == update_data['email']
            ).first()
            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Email già in uso"
                )
                
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj