from .users.controllers import router as user_router
from .auth.controllers import router as auth_router
from .scholarship.controllers import router as scholarship_router
from fastapi import FastAPI

def register_routers(app: FastAPI):
    app.include_router(user_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(scholarship_router, prefix="/api/v1")
