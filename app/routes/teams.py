from fastapi import APIRouter, HTTPException, Response

from app.access import CurrentUser, Database, TeamMember
from app.models import Membership, Team, User
from app.schemas import Named, Record

router = APIRouter()


@router.post("/users", response_model=Record, status_code=201)
def create_user(data: Named, db: Database):
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    return user


@router.post("/teams", response_model=Record, status_code=201)
def create_team(data: Named, db: Database, user: CurrentUser):
    team = Team(**data.model_dump())
    db.add(team)
    db.flush()
    db.add(Membership(team_id=team.id, user_id=user.id))
    db.commit()
    return team


@router.post("/teams/{team_id}/members/{user_id}", status_code=204)
def add_member(team_id: str, user_id: str, db: Database, member: TeamMember):
    if db.get(User, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    if db.get(Membership, (team_id, user_id)) is None:
        db.add(Membership(team_id=team_id, user_id=user_id))
        db.commit()
    return Response(status_code=204)
