from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import Todo, User
from schemas import TodoCreate, TodoPublic, TodoUpdate
from serializers import todo_to_public
from team_routes import _get_team_or_404, _require_member

router = APIRouter(prefix="/teams", tags=["todos"])


def _get_todo_or_404(team_id: int, todo_id: int, db: Session) -> Todo:
    _get_team_or_404(team_id, db)
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.team_id == team_id)
        .first()
    )
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.post(
    "/{team_id}/todos",
    response_model=TodoPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_todo(
    team_id: int,
    body: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_member(team_id, current_user, db)
    team = _get_team_or_404(team_id, db)
    todo = Todo(
        team_id=team.id,
        title=body.title,
        done=False,
        created_by=current_user.id,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo_to_public(todo, db)


@router.get("/{team_id}/todos", response_model=list[TodoPublic])
def list_todos(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_member(team_id, current_user, db)
    _get_team_or_404(team_id, db)
    todos = (
        db.query(Todo)
        .filter(Todo.team_id == team_id)
        .order_by(Todo.id.asc())
        .all()
    )
    return [todo_to_public(todo, db) for todo in todos]


@router.patch("/{team_id}/todos/{todo_id}", response_model=TodoPublic)
def update_todo(
    team_id: int,
    todo_id: int,
    body: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_member(team_id, current_user, db)
    todo = _get_todo_or_404(team_id, todo_id, db)
    todo.title = body.title
    db.commit()
    db.refresh(todo)
    return todo_to_public(todo, db)


@router.delete("/{team_id}/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    team_id: int,
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_member(team_id, current_user, db)
    todo = _get_todo_or_404(team_id, todo_id, db)
    db.delete(todo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{team_id}/todos/{todo_id}/done", response_model=TodoPublic)
def mark_todo_done(
    team_id: int,
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_member(team_id, current_user, db)
    todo = _get_todo_or_404(team_id, todo_id, db)
    todo.done = True
    if todo.completed_by is None:
        todo.completed_by = current_user.id
    db.commit()
    db.refresh(todo)
    return todo_to_public(todo, db)
