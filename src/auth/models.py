from pydantic import BaseModel, EmailStr
from uuid import UUID
from fastapi import Form

from ..shared.enums import UserRole

class RegisterUser(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.user

def get_user_from_form(
    firstname: str = Form(...),
    lastname: str = Form(...),
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    role: UserRole = Form(UserRole.user)
) -> RegisterUser:
    return RegisterUser(
        firstname=firstname,
        lastname=lastname,
        username=username,
        email=email,
        password=password,
        role=role
    )

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None
    role: str | None = None

    def get_uuid(self) -> UUID | None:
        if self.user_id:
            return UUID(self.user_id)
        return None