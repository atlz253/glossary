from .Base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Term(Base):
    __tablename__ = "terms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    definition: Mapped[str] = mapped_column(String())
