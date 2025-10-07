from sqlalchemy import String, Text, ARRAY, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..database.core import Base

class Scholarship(Base):
    __tablename__ = 'scholarships'
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), unique=True ,nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    study_level: Mapped[str] = mapped_column(String(100), nullable=True)
    field_of_study: Mapped[str] = mapped_column(String(255), nullable=True)
    eligible_nationalities: Mapped[str] = mapped_column(Text, nullable=True)
    requirements: Mapped[str] = mapped_column(Text, nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    is_fully_funded: Mapped[bool] = mapped_column(Boolean, default=False)

    scholarship_matches: Mapped[list["ScholarshipMatch"]] = relationship(back_populates="scholarship")