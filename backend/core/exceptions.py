from typing import Any, Callable, Coroutine
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


class JSONException(Exception):
    """Custom JSON exception to standardize API error responses."""

    def __init__(self, message: Any, status_code: int = HTTP_400_BAD_REQUEST):
        """
        message can be:
        - str → {"message": "<msg>"}
        - dict → {"message": {"title": ..., "description": ...}}
        status_code defaults to 400 but can be overridden.
        """
        self.message = message
        self.status_code = status_code


# Define the expected exception handler type
ExceptionHandlerType = Callable[[Request, Exception], Coroutine[Any, Any, JSONResponse]]


async def json_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles all JSONException raised manually."""
    if not isinstance(exc, JSONException):
        raise exc
    return JSONResponse(
        status_code=exc.status_code,  # <-- this sets the actual HTTP status
        content={"success": False, "message": exc.message},
    )


async def validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handles FastAPI validation errors with our JSON format."""
    if not isinstance(exc, RequestValidationError):
        raise exc
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"success": False, "message": exc.errors()},
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles all unexpected exceptions in our JSON format."""
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": str(exc) or "Internal server error"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Attach all custom exception handlers to FastAPI app."""
    app.add_exception_handler(JSONException, json_exception_handler)  # type: ExceptionHandlerType
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ExceptionHandlerType
    app.add_exception_handler(Exception, generic_exception_handler)  # type: ExceptionHandlerType
