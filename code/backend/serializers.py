from sqlalchemy.orm import Session

from models import Team, Todo, User
from schemas import TeamPublic, TodoPublic


def _username_for(db: Session, user_id: int | None) -> str | None:
    if user_id is None:
        return None
    user = db.query(User).filter(User.id == user_id).first()
    return user.username if user is not None else None


def team_to_public(team: Team, db: Session) -> TeamPublic:
    return TeamPublic(
        id=team.id,
        name=team.name,
        created_by=team.created_by,
        created_by_username=_username_for(db, team.created_by) or "unknown",
    )


def todo_to_public(todo: Todo, db: Session) -> TodoPublic:
    return TodoPublic(
        id=todo.id,
        team_id=todo.team_id,
        title=todo.title,
        done=todo.done,
        created_by=todo.created_by,
        created_by_username=_username_for(db, todo.created_by) or "unknown",
        completed_by=todo.completed_by,
        completed_by_username=_username_for(db, todo.completed_by),
    )
