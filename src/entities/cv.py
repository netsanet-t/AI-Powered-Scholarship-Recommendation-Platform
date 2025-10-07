from ..database.core import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Cv(Base):
  __tablename__ = "cv"
  
  id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
  user: Mapped["User"] = relationship(back_populates="cv")

  skills: Mapped[str] = mapped_column(String, nullable=True)
  university: Mapped[str] = mapped_column(String, nullable=True)
  degree: Mapped[str] = mapped_column(String, nullable=True)
  major: Mapped[str] = mapped_column(String, nullable=True)
  graduation_year: Mapped[str] = mapped_column(String, nullable=True)
  gpa: Mapped[str] = mapped_column(String, nullable=True)
  nationality: Mapped[str] = mapped_column(String, nullable=True)
  gender: Mapped[str] = mapped_column(String, nullable=True)
  date_of_birth: Mapped[str] = mapped_column(String, nullable=True)
