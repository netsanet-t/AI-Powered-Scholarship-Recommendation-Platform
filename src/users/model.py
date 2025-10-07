from pydantic import BaseModel
from uuid import UUID
from fastapi import Form
from typing import Annotated

from ..shared.enums import UserRole

class Cv(BaseModel):
    skills: str | None = None
    university: str | None = None
    degree: str | None = None
    major: str | None = None
    graduation_year: str | None = None
    gpa: str | None = None
    nationality: str | None = None
    gender: str | None = None
    date_of_birth: str | None = None

class CvUpdate(Cv):
    pass


class UserResponse(BaseModel):
    id: UUID
    firstname: str
    lastname: str
    username: str
    email: str
    role: UserRole
    profile_image: str | None

    class config:
        orm_mode = True

class UserResponseWithCv(UserResponse):
    cv: Cv | None

class UserUpdate(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    username: str | None = None
    email: str | None = None

class PasswordResetModel(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
