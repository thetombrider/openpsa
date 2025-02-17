from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.models import Client
from src.schemas.client import ClientCreate, ClientUpdate
from src.services.base import BaseService

class ClientService(BaseService[Client, ClientCreate, ClientUpdate]):
    def __init__(self):
        super().__init__(Client)
    
    def get_by_name(self, db: Session, name: str) -> Optional[Client]:
        return db.query(self.model).filter(self.model.name == name).first()