from typing import Type
from fastapi import Body, Depends, HTTPException, Request
from pydantic import BaseModel, ValidationError

def ParseDecryptedBody(model: Type[BaseModel]):
    async def dependency(
        request: Request,
        _: model = Body(...)  # For Swagger documentation
    ) -> BaseModel:
        try:
            data = await request.json()
            return model.model_validate(data)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid request body: {str(e)}")
    return Depends(dependency)