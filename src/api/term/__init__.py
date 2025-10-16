from fastapi import APIRouter
from ...term import Term

router = APIRouter(prefix="/term")


@router.get("/")
def term_list() -> list[Term]:
    return []


__all__ = ["router"]
