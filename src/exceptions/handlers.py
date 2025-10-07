from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException, ResponseValidationError
from sqlalchemy.exc import IntegrityError, ProgrammingError
from .exceptions import NEXTstepApiExeption
import asyncpg

async def app_exception_handler(request: Request, exc: NEXTstepApiExeption):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "error": exc.errors()
            # "error": exc.errors()[0].get("msg")
        }
    )

async def responce_validation_exception_handler(requst: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "serialization error",
            "errors": exc.errors()
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=400,
        content={"detail": f"{str(exc.orig)}"}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )
