from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, delete
from sqlalchemy.orm import selectinload
from uuid import UUID

from src.exceptions.exceptions import NotFoundExeption
from src.users.services import get_user
from src.shared.model import Parameters
from src.auth.models import TokenData
from src.entities.scholarship import Scholarship
from src.entities.scholarship_match import ScholarshipMatch
from src.scholarship.model import ScholarshipCreate
from src.ai_models.model import AsymmetricScholarshipMatcher
from src.background_tasks.tasks import match_user_scholarship, match_user_scholarships

async def get_all_scholarships(session: AsyncSession, params: Parameters):
    query = select(Scholarship).limit(params.limit).offset(params.offset)
    results = await session.execute(query)
    return results.scalars().all()

async def get_one_scholarship(id: UUID, session: AsyncSession):
    query = select(Scholarship).where(Scholarship.id == id)
    res = await session.execute(query)
    result = res.scalar_one_or_none()
    if result is None:
        raise NotFoundExeption(name=f"scholarship with id {id}")
    return result

async def create_new_scholarship(current_user: TokenData,session: AsyncSession, scholarahip_data: ScholarshipCreate, background_tasks: BackgroundTasks,matcher_model: AsymmetricScholarshipMatcher):
    new_scholarship = Scholarship(**scholarahip_data.model_dump())
    user = await get_user(session, current_user.get_uuid())
    background_tasks.add_task(match_user_scholarship, new_scholarship, matcher_model, session)
    session.add(new_scholarship)
    await session.commit()

async def get_users_matched_scholarships(user_id: UUID, session: AsyncSession):
    query =  (
    select(ScholarshipMatch)
    .options(selectinload(ScholarshipMatch.scholarship))
    .where(ScholarshipMatch.user_id == user_id)
    .order_by(desc(ScholarshipMatch.match_persent))
    )
    matches = (await session.execute(query)).scalars().all()
    return matches

async def rematch(user_id: UUID, session: AsyncSession, matcher_model: AsymmetricScholarshipMatcher, background_tasks: BackgroundTasks):
    delete_query = delete(ScholarshipMatch).where(ScholarshipMatch.user_id == user_id)
    await session.execute(delete_query)
    await session.commit()
    user = await get_user(session, user_id)
    background_tasks.add_task(match_user_scholarships, user, matcher_model, session)
    return