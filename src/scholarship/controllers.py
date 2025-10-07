from fastapi import APIRouter, Query, status, BackgroundTasks
from uuid import UUID

from ..database.core import session_dep
from .model import ScholarshipListResponse, ScholarshipOneResponse, ScholarshipCreate, MatchedScholarshipListResponse
from ..auth.services import current_user
from ..shared.model import Parameters
from .services import get_all_scholarships, get_one_scholarship, create_new_scholarship, get_users_matched_scholarships, rematch
from ..dependencies.dependencies import matcher_model
from ..ai_models.model import AsymmetricScholarshipMatcher

router = APIRouter(
    prefix="/scholarship",
    tags=["scholarship"]
)


@router.get("", response_model=ScholarshipListResponse)
async def get_scholarships(session: session_dep, params: Parameters = Query()):
    results = await get_all_scholarships(session, params)
    return {"count": len(results), "results": results}

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_scholarship(current_user: current_user, sesssion: session_dep, scholarship_data: ScholarshipCreate, background_tasks: BackgroundTasks, matcher_model: AsymmetricScholarshipMatcher = matcher_model):
    await create_new_scholarship(current_user, sesssion, scholarship_data, background_tasks, matcher_model)
    return None

@router.get("/matched-scholarships", response_model=MatchedScholarshipListResponse)
async def get_scholarship_matches(current_user: current_user, session: session_dep) -> MatchedScholarshipListResponse:
    matches = await get_users_matched_scholarships(current_user.get_uuid(), session)
    return {"count": len(matches), "results": matches}

@router.post("/rematch", status_code=status.HTTP_201_CREATED)
async def rematch_scholarship(current_user: current_user, session: session_dep, background_tasks:BackgroundTasks, matcher_model: AsymmetricScholarshipMatcher = matcher_model) -> None:
    await rematch(current_user.get_uuid(), session, matcher_model, background_tasks)
    return None

@router.get("/{id}", response_model=ScholarshipOneResponse)
async def get_scholarship(id: UUID, session: session_dep):
    result = await get_one_scholarship(id, session)
    return {"result": result}
