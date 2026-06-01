import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,32}$")


class UserRegister(BaseModel):
    username: str = Field(min_length=1, max_length=32)
    password: str = Field(min_length=6)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not USERNAME_PATTERN.match(value):
            raise ValueError("invalid username format")
        return value


class UserLogin(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("team name must not be empty")
        if len(stripped) > 50:
            raise ValueError("team name too long")
        return stripped


class TeamPublic(BaseModel):
    id: int
    name: str
    created_by: int
    created_by_username: str


class TeamMemberInvite(BaseModel):
    username: str


class TeamMemberPublic(BaseModel):
    team_id: int
    user_id: int
    role: str


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be empty")
        if len(stripped) > 100:
            raise ValueError("title too long")
        return stripped


class TodoUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("title must not be empty")
        if len(stripped) > 100:
            raise ValueError("title too long")
        return stripped


class TodoPublic(BaseModel):
    id: int
    team_id: int
    title: str
    done: bool
    created_by: int
    created_by_username: str
    completed_by: int | None = None
    completed_by_username: str | None = None
