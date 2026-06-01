from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import Team, TeamMember, User
from schemas import TeamCreate, TeamMemberInvite, TeamMemberPublic, TeamPublic
from serializers import team_to_public

router = APIRouter(prefix="/teams", tags=["teams"])

ROLE_OWNER = "owner"
ROLE_MEMBER = "member"


def _get_team_or_404(team_id: int, db: Session) -> Team:
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


def _get_membership(team_id: int, user_id: int, db: Session) -> TeamMember | None:
    return (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id)
        .first()
    )


def _require_member(team_id: int, user: User, db: Session) -> TeamMember:
    team = _get_team_or_404(team_id, db)
    membership = _get_membership(team.id, user.id, db)
    if membership is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a team member")
    return membership


def _require_owner(team_id: int, user: User, db: Session) -> TeamMember:
    membership = _require_member(team_id, user, db)
    if membership.role != ROLE_OWNER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Owner required")
    return membership


@router.post("", response_model=TeamPublic, status_code=status.HTTP_201_CREATED)
def create_team(
    body: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(Team).filter(Team.name == body.name).first()
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Team name already exists",
        )
    team = Team(name=body.name, created_by=current_user.id)
    db.add(team)
    db.flush()
    db.add(
        TeamMember(team_id=team.id, user_id=current_user.id, role=ROLE_OWNER),
    )
    db.commit()
    db.refresh(team)
    return team_to_public(team, db)


@router.get("", response_model=list[TeamPublic])
def list_teams(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    teams = (
        db.query(Team)
        .join(TeamMember, TeamMember.team_id == Team.id)
        .filter(TeamMember.user_id == current_user.id)
        .order_by(Team.id.asc())
        .all()
    )
    return [team_to_public(team, db) for team in teams]


@router.get("/{team_id}", response_model=TeamPublic)
def get_team(
    team_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_member(team_id, current_user, db)
    team = _get_team_or_404(team_id, db)
    return team_to_public(team, db)


@router.post(
    "/{team_id}/members",
    response_model=TeamMemberPublic,
    status_code=status.HTTP_201_CREATED,
)
def invite_member(
    team_id: int,
    body: TeamMemberInvite,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_owner(team_id, current_user, db)
    team = _get_team_or_404(team_id, db)
    invitee = db.query(User).filter(User.username == body.username).first()
    if invitee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    existing = _get_membership(team.id, invitee.id, db)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already a team member",
        )
    membership = TeamMember(team_id=team.id, user_id=invitee.id, role=ROLE_MEMBER)
    db.add(membership)
    db.commit()
    return TeamMemberPublic(
        team_id=team.id,
        user_id=invitee.id,
        role=ROLE_MEMBER,
    )
