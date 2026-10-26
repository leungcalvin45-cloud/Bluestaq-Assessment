from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Membership, Team, User

Database = Annotated[Session, Depends(get_db)]


def current_user(db: Database, x_user_id: Annotated[str, Header()]):
    user = db.get(User, x_user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Unknown user")
    return user


CurrentUser = Annotated[User, Depends(current_user)]


def require_member(team_id: str, db: Database, user: CurrentUser):
    if db.get(Team, team_id) is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if db.get(Membership, (team_id, user.id)) is None:
        raise HTTPException(status_code=403, detail="Team membership required")
    return user


TeamMember = Annotated[User, Depends(require_member)]
