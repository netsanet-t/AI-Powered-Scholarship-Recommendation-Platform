from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..database.core import Base

class UserSkill(Base):
    __tablename__ = "users_skills"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    skill_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)