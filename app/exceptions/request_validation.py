from datetime import datetime, timezone

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Build a detailed list of validation errors
        errors = []
        for err in exc.errors():
            field = err.get("loc", ["unknown"])[-1]
            error_type = err.get("type", "")
            msg = err.get("msg", "")
            if error_type == "missing":
                msg = f"The field '{field}' is required."
            errors.append({
                "field": field,
                "error_type": error_type,
                "message": msg
            })

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Validation error",
                "errors": errors,
                "path": str(request.url),
                "method": request.method,
                "timestamp": datetime.now(timezone.utc).isoformat() + "Z"
            }
        )