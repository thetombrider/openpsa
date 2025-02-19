# src/services/consultant_role.py
from src.services.base import BaseService
from src.models.models import ConsultantRole
from src.schemas.consultant_role import ConsultantRoleCreate, ConsultantRoleResponse

class ConsultantRoleService(BaseService[ConsultantRole, ConsultantRoleCreate, ConsultantRoleResponse]):
    def __init__(self):
        super().__init__(ConsultantRole)