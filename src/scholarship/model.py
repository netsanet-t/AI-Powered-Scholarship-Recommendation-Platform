from pydantic import BaseModel, Field
from uuid import UUID

class ScholarshipModel(BaseModel):
    pass

class ScholarshipResponse(ScholarshipModel):
    id: UUID
    name: str
    description: str
    is_fully_funded: bool
    study_level: str | None = None
    field_of_study: str | None = None
    eligible_nationalities: str | None = None
    requirements: str | None = None
    country: str | None = None

    class config:
        orm_mode = True

class ScholarshipMatches(BaseModel):
    id: UUID
    match_persent: float
    scholarship: ScholarshipResponse

class ScholarshipCreate(ScholarshipModel):
    name: str
    description: str
    requirements: str
    is_fully_funded: bool
    study_level: str | None = None
    field_of_study: str | None = None
    eligible_nationalities: str | None = None
    country: str | None = None


class ScholarshipListResponse(BaseModel):
    status: str = "success"
    count: int
    results: list[ScholarshipResponse]

class MatchedScholarshipListResponse(BaseModel):
    status: str = "success"
    count: int
    results: list[ScholarshipMatches]

class ScholarshipOneResponse(BaseModel):
    status: str = "success"
    result: ScholarshipResponse
    