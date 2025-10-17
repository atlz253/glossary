from pydantic import BaseModel, Field


class ExceptionResponse(BaseModel):
    detail: str = Field(description="Описание ошибки")
