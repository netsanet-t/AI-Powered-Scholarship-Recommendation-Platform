from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, UploadFile, BackgroundTasks, status
from typing import Annotated
from passlib.context import CryptContext
import jwt
from jwt import PyJWTError
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID, uuid4
from ..logging import logging
from .models import Token, TokenData, RegisterUser
from ..entities.user import User, UserRole
from ..exceptions.exceptions import IncorrectCredentials

from datetime import timedelta, datetime, timezone
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXP_MIN = os.getenv("TOKEN_EXP_MIN")

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

def varify_password(plain_password, hashed_password):
    return pwd_context.verify_and_update(plain_password, hashed_password)[0]

def get_password_hash(password: str):
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str, session: AsyncSession) -> User | bool:
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user or not varify_password(password, user.hashed_password):
        logging.warning(f"failed authentication attempt for username: {username}")
        raise IncorrectCredentials(detail="Incorrect Credentials")
    return user

def create_access_token(username: str, role: UserRole, user_id: UUID, expire_date: timedelta):
    data_to_encode = {
        "sub": username,
        "id": str(user_id),
        "role": role,
        "exp": datetime.now(timezone.utc) + expire_date
    }
    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)

def varify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('id')
        role = payload.get('role')
        return TokenData(user_id=user_id, role=role)
    except PyJWTError as e:
        logging.error(f"Token varification failed: {str(e)}")
        raise IncorrectCredentials(detail="Invalid token")
    
def save_user_image(unique_filename: str, image: bytes) -> bool:
    project_root = Path(__file__).resolve().parent.parent.parent
    upload_dir = project_root / "public/images"
    upload_dir.mkdir(parents=True, exist_ok=True)  # Just to be safe
 
    with open(upload_dir / unique_filename, 'wb') as f:
        f.write(image)
    return True

async def register_user(background_tasks: BackgroundTasks, session: AsyncSession, registering_user: RegisterUser, image: UploadFile) -> None:
    try:
        if image is not None:
            ext = os.path.splitext(image.filename)[1]
            unique_filename = f"{uuid4()}{ext}"
            image_data = image.file.read()

            background_tasks.add_task(save_user_image, unique_filename, image_data)
        else:
            unique_filename = None
            
        registering_user.password = get_password_hash(registering_user.password)
        user_create_model = User(
            id=uuid4(),
            **registering_user.model_dump(exclude={"password"}),
            hashed_password = registering_user.password,
            profile_image= unique_filename
        )


        session.add(user_create_model)
        await session.commit()
    except Exception as e:
        logging.error(f"failed to register user: {registering_user.email}. Error: {str(e)}")
        raise

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
    return varify_token(token)

current_user = Annotated[TokenData, Depends(get_current_user)]

async def login_and_get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)

    token = create_access_token(user.username, user.role, user.id, timedelta(minutes=int(TOKEN_EXP_MIN)))
    return Token(access_token=token, token_type="bearer")