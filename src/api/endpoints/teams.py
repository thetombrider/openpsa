# src/api/endpoints/teams.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.schemas.team import TeamCreate, TeamResponse
from src.services.team import TeamService

router = APIRouter()
service = TeamService()

@router.post("/", response_model=TeamResponse)
async def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db)
):
    return service.create(db, team)

@router.get("/", response_model=List[TeamResponse])
async def get_teams(
    db: Session = Depends(get_db)
):
    return service.list(db)

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    team = service.get(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.post("/{team_id}/members/{user_id}")
async def add_team_member(
    team_id: int,
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db)
):
    member = service.add_member(db, team_id, user_id, role_id)
    if not member:
        raise HTTPException(status_code=400, detail="Could not add member")
    return {"message": "Member added successfully"}