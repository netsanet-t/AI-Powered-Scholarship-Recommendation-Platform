from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..database.core import Base


class ScholarshipMatch(Base):
  __tablename__ = "scholarship_matchs"
  id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  match_persent: Mapped[float] = mapped_column(Float, nullable=False)

  user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
  user: Mapped["User"] = relationship(back_populates="scholarship_matches")
  
  scholarship_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scholarships.id"), nullable=False)
  scholarship: Mapped["Scholarship"] = relationship(back_populates="scholarship_matches")

