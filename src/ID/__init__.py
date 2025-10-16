from pydantic import BaseModel, Field


class ID(BaseModel):
    id: int = Field(description="ID термина")
