from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from ..database.core import Base
from ..shared.enums import UserRole
from .user_skill import UserSkill
from .skill import Skill
from .scholarship_match import ScholarshipMatch
from .cv import Cv

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstname: Mapped[str] = mapped_column(String, nullable=False)
    lastname: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(SQLEnum(UserRole), nullable=False, default=UserRole.user)
    profile_image: Mapped[str] = mapped_column(String, nullable=True)


    skills = relationship("Skill", secondary="users_skills", back_populates="users")
    scholarship_matches: Mapped[list["ScholarshipMatch"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    cv: Mapped["Cv"] = relationship(back_populates="user", uselist=False)

    def __repr__(self):
        return f"User(id={self.id}, name={self.firstname}, email={self.email}, role={self.role})"
