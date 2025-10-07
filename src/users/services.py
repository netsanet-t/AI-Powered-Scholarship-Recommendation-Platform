from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from uuid import UUID
from fastapi import HTTPException, UploadFile, Depends, File
from typing import Annotated
import json

from .model import PasswordResetModel, UserUpdate, CvUpdate
from ..entities.user import User
from ..entities.skill import Skill
from ..entities.cv import Cv
from ..entities.scholarship_match import ScholarshipMatch
from ..auth.services import varify_password, get_password_hash
import logging
from ..exceptions.exceptions import NotFoundExeption, NEXTstepApiExeption

from ..utils.cv_parser import CvParser
from ..utils.cv_statement import CvToStatement

async def get_user(session: AsyncSession, user_id: str) -> User:
    query = select(User).options(selectinload(User.skills)).options(selectinload(User.cv)).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        logging.error(f"user not found for id: {user_id}")
        raise NotFoundExeption(name="user")
    logging.error(f"successfully retrived user with id: {user_id}")
    return user

async def get_user_with_matched_scholarships(session: AsyncSession, user_id: str):
    query = select(User).options(selectinload(User.scholarship_matches).selectinload(ScholarshipMatch.scholarship)).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        logging.error(f"user not found for id: {user_id}")
        raise NotFoundExeption(name="user")
    logging.error(f"successfully retrived user with id: {user_id}")
    return user

async def update_user(session: AsyncSession, update_data: UserUpdate, user_id: UUID) -> None:
    try:
        user_model = await get_user(session, user_id)
        for key, value in update_data.model_dump(exclude_unset=True).items():
            if value is None:
                continue
            setattr(user_model, key, value)

        session.add(user_model)
        await session.commit()
        return True
    except NEXTstepApiExeption:
        raise
    except Exception as e:
        await session.rollback()
        logging.error(f"error acured suring the update of user ID: {user_id}. Error: {e}")
        raise HTTPException(status_code=500, detail="internal server error")
    
async def change_password(session: AsyncSession, user_id: UUID, password_data: PasswordResetModel) -> None:
    try:
        user = await get_user(session, user_id)
        
        if not varify_password(password_data.old_password, user.hashed_password):
            logging.error(f"password doesn't match during password change session for user id: {user.id}")
            raise HTTPException(status_code=401, detail="incorrect old password")
        
        if password_data.new_password != password_data.confirm_password:
            logging.error(f"password doesn't match during password change session for user id: {user.id}")
            raise HTTPException(status_code=401, detail="passwords don't match")
        
        user.hashed_password = get_password_hash(password_data.new_password)
        session.add(user)
        await session.commit()
        logging.info(f"succefully changed password og user ID: {user_id}")
    except Exception as e:
        logging.error(f"error acured during the password change of user ID: {user_id}. Error: {e}")
        raise HTTPException(status_code=500, detail="internal server error")

async def update_user_details(session: AsyncSession, user_id: UUID, skills: list[str]) -> None:
    try:
        user = await get_user(session, user_id)
        if not skills:
            logging.info(f"no skills provided for user ID: {user_id}")
            user.skills = []
            session.add(user)
            await session.commit()
            return
        
        skill_models = await add_get_skills(session, skills)
        user.skills = skill_models
        session.add(user)
        await session.commit()
        logging.info(f"succefully updated user ID: {user_id}")
    except Exception as e:
        logging.error(f"error acured auring the update of user ID: {user_id}. Error: {e}")
        raise HTTPException(status_code=500, detail="internal server error")

async def add_get_skills(session: AsyncSession, skills: list[str]) -> list[Skill]:
    try:
        skill_models = []
        for skill in skills:
            query = select(Skill).where(Skill.name == skill)
            result = await session.execute(query)
            skill_model = result.scalar_one_or_none()
            if not skill_model:
                skill_model = Skill(name=skill)
                session.add(skill_model)
            if skill_model not in skill_models:
                skill_models.append(skill_model)
        await session.commit()
        return skill_models
    except Exception as e:
        logging.error(f"error during the update of user ID detailes: Error: {e}")
        raise HTTPException(status_code=500, detail="internal server error")
    
async def update_user_cv(session: AsyncSession, user_id: UUID, cv: CvUpdate) -> None:
    try:
        user = await get_user(session, user_id)
        if not user.cv:
            raise NotFoundExeption(name="cv")
        cv_update_data = cv.model_dump(exclude_unset=True)
        for key, value in cv_update_data.items():
            setattr(user.cv, key, value)
        session.add(user.cv)
        await session.commit()
    except NEXTstepApiExeption:
        raise
    except Exception as e:
        logging.error(f"error during the update of user ID detailes: Error: {e}")
        raise HTTPException(status_code=500, detail="internal server error")
    
async def pasrse_upload_cv(session: AsyncSession, user_id: UUID, cv: UploadFile) -> None:
    try:
        user = await get_user(session, user_id)
        if user.cv:
            query = delete(Cv).where(Cv.id == user.cv.id)
            await session.execute(query)
            await session.commit()

        cv_parser = CvParser(cv.file)
        result = cv_parser.get_result()
        result.update({"skills": json.dumps(result.get("skills"))})
        cv = Cv(**result, user_id=user_id)
        session.add(cv)
        await session.commit()
    except IntegrityError as e:
        logging.error(f"error during the update of user ID detailes: Error: {e}")
        raise HTTPException(status_code=500, detail="internal server error")
    
    
def validate_cv(cv: UploadFile = File(...)):
    size = ((cv.size / 8) /  1024) / 1024
    print(size)
    if cv is None:
        raise HTTPException(status_code=400, detail="cv is required")
    if cv.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="cv must be a pdf")
    if size > 2:
        raise HTTPException(status_code=400, detail="cv size must be less than 5MB")
    return cv

get_cv = Annotated[UploadFile, Depends(validate_cv)]