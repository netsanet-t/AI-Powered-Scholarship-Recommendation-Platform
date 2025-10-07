from fastapi import APIRouter, Form, File, UploadFile
from typing import Annotated

from ..auth.services import current_user
from .model import UserResponseWithCv, UserUpdate, PasswordResetModel, CvUpdate
from ..entities.user import User
from .services import (get_user, update_user, change_password, update_user_details, get_user_with_matched_scholarships, pasrse_upload_cv, update_user_cv, get_cv)
from ..database.core import session_dep

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get('/me', response_model=UserResponseWithCv)
async def get_user_current(current_user: current_user, session: session_dep) -> User:
    user = await get_user(session, current_user.get_uuid())
    return user

@router.patch('/me')
async def update_user_current(current_user: current_user, update_data: Annotated[UserUpdate, Form()], session: session_dep) -> None:
    await update_user(session, update_data, current_user.get_uuid())
    return None

@router.post('/me/change-password')
def change_password_current(current_user: current_user, password_data: Annotated[PasswordResetModel, Form()], session: session_dep) -> None:
    change_password(session, current_user.get_uuid(), password_data)
    return None

@router.patch("/me/detail")
async def update_user_current_details(*, current_user: current_user, skills: Annotated[list[str], Form()] = None, session: session_dep) -> None:
    await update_user_details(session, current_user.get_uuid(), skills)
    return None

# Cv Controllers
@router.patch("/me/cv", status_code=201)
async def update_cv(*, current_user: current_user, cv: CvUpdate, session: session_dep) -> None:
    await update_user_cv(session, current_user.get_uuid(), cv)
    return None

@router.post("/me/upload-cv", status_code=201)
async def upload_cv(*, current_user: current_user, cv: get_cv, session: session_dep) -> None:
    await pasrse_upload_cv(session, current_user.get_uuid(), cv)
    return None