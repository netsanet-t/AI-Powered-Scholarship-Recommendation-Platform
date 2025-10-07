from fastapi import HTTPException, Depends
from contextlib import asynccontextmanager
from fastapi import FastAPI

from ..ai_models.model import AsymmetricScholarshipMatcher

_matcher_model: AsymmetricScholarshipMatcher | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _matcher_model
    _matcher_model = AsymmetricScholarshipMatcher()
    yield
    _matcher_model.clear()


def get_matcher():
  if _matcher_model is None:
    raise HTTPException(status_code=404, detail="Model not found")
  return _matcher_model

matcher_model: AsymmetricScholarshipMatcher = Depends(get_matcher)