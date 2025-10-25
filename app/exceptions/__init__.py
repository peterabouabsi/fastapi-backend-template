from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from .http import http_exception_handler
from .request_validation import validation_exception_handler

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)