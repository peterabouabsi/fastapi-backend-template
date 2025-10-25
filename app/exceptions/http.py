from datetime import datetime, timezone

from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException):
    status_code = exc.status_code
    message = exc.detail

    # Hide details for internal server errors but log them
    if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        print(f"[ERROR] {request.method} {request.url} - {exc}")
        message = "Internal server error."

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "status_code": status_code,
            "message": message,
            "path": str(request.url),
            "method": request.method,
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
        }
    )