# src/services/team.py
from typing import Optional
from sqlalchemy.orm import Session
from src.services.base import BaseService
from src.models.models import Team, TeamMember
from src.schemas.team import TeamCreate, TeamResponse
from datetime import date

class TeamService(BaseService[Team, TeamCreate, TeamResponse]):
    def __init__(self):
        super().__init__(Team)

    def add_member(
        self, 
        db: Session, 
        team_id: int, 
        user_id: int, 
        role_id: int
    ) -> Optional[TeamMember]:
        # Verifica esistenza team e utente
        team = self.get(db, team_id)
        if not team:
            return None

        # Verifica se l'utente è già nel team
        existing = db.query(TeamMember).filter(
            TeamMember.team_id == team_id,
            TeamMember.user_id == user_id,
            TeamMember.leave_date == None
        ).first()
        
        if existing:
            return None

        # Crea nuovo membro
        member = TeamMember(
            team_id=team_id,
            user_id=user_id,
            role_id=role_id,
            join_date=date.today()
        )
        
        db.add(member)
        db.commit()
        db.refresh(member)
        return member