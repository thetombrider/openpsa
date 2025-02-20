# src/services/consultant_role.py
from src.services.base import BaseService
from src.models.models import ConsultantRole
from src.schemas.consultant_role import ConsultantRoleCreate, ConsultantRoleUpdate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session

class ConsultantRoleService(BaseService[ConsultantRole, ConsultantRoleCreate, ConsultantRoleUpdate]):
    def __init__(self):
        super().__init__(ConsultantRole)

    def create(self, db: Session, obj_in: ConsultantRoleCreate) -> ConsultantRole:
        try:
            db_obj = self.model(**obj_in.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            if "consultant_roles_name_key" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Un ruolo con questo nome esiste già"
                )
            raise HTTPException(
                status_code=400,
                detail="Errore nella creazione del ruolo"
            )

    def update(self, db: Session, id: int, obj_in: ConsultantRoleUpdate) -> ConsultantRole:
        try:
            return super().update(db, id, obj_in)
        except IntegrityError as e:
            db.rollback()
            if "consultant_roles_name_key" in str(e):
                raise HTTPException(
                    status_code=400,
                    detail="Un ruolo con questo nome esiste già"
                )
            raise HTTPException(
                status_code=400,
                detail="Errore nell'aggiornamento del ruolo"
            )
            
    def delete(self, db: Session, id: int) -> bool:
        try:
            return super().delete(db, id)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Impossibile eliminare il ruolo: è ancora in uso"
            )