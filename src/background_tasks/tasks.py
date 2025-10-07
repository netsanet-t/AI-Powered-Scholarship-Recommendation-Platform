from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.entities.scholarship import Scholarship
from src.entities.user import User
from src.entities.scholarship_match import ScholarshipMatch
from src.ai_models.model import AsymmetricScholarshipMatcher
from src.utils.cv_statement import CvToStatement

async def match_user_scholarship(scholarship: Scholarship, matcher_model: AsymmetricScholarshipMatcher, session: AsyncSession) -> None:

  users = (await session.execute(select(User).options(selectinload(User.cv)))).scalars().all()
  for user in users:
    if user.cv is None:
      continue
    cv_steatement = CvToStatement(user.cv.__dict__).get_statement()
    persent=matcher_model.calculate_match_persent(cv_steatement, scholarship.__dict__)
    print(persent)
    if persent <= 30.0:
      continue
    scholarship_match = ScholarshipMatch(user_id=user.id, scholarship_id=scholarship.id, match_persent=persent)
    session.add(scholarship_match)
  await session.commit()

async def match_user_scholarships(user: User, matcher_model: AsymmetricScholarshipMatcher, session: AsyncSession) -> None:
  cv_steatement = CvToStatement(user.cv.__dict__).get_statement()
  scholarships = (await session.execute(select(Scholarship))).scalars().all()
  for scholarship in scholarships:
    persent = matcher_model.calculate_match_persent(cv_steatement, scholarship.__dict__)
    print(persent)
    if persent <= 30.0:
      continue
    scholarship_match = ScholarshipMatch(user_id=user.id, scholarship_id=scholarship.id, match_persent=persent)
    session.add(scholarship_match)
  await session.commit()