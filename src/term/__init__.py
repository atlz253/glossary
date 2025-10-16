from pydantic import BaseModel, Field
from ..ID import ID


class TermPost(BaseModel):
    name: str = Field(min_length=1, max_length=100,
                      description="Название термина")
    definition: str = Field(min_length=1, description="Определение термина")


class Term(TermPost, ID):
    pass
