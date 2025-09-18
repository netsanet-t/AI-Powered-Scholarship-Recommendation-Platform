from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException, ResponseValidationError
from sqlalchemy.exc import IntegrityError
from .exceptions import NEXTstepApiExeption
from .handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    responce_validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler,
)

def register_app_exceptions(app: FastAPI):
    app.add_exception_handler(NEXTstepApiExeption, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ResponseValidationError, responce_validation_exception_handler)
    app.add_exception_handler(IntegrityError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)