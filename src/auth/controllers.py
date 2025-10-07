from fastapi import APIRouter, Request, Depends, UploadFile, File, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from ..rate_limiting import limiter
from .models import RegisterUser, Token, get_user_from_form
from ..database.core import session_dep
from .services import register_user, login_and_get_token

router = APIRouter(prefix="/auth", tags=['auth'])

@router.post("/register", status_code=201)
@limiter.limit("5/houre")
async def register(*,background_tasks: BackgroundTasks, request: Request, session: session_dep, register_user_data: Annotated[RegisterUser, Depends(get_user_from_form)], profile_image: Annotated[ UploadFile, File(...)] = None):
    await register_user(background_tasks, session, register_user_data, profile_image)
    return None

@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: session_dep) -> Token:
    return await login_and_get_token(form_data, session)
