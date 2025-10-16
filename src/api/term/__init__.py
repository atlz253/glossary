from fastapi import APIRouter, HTTPException
from ...term import Term, TermPost
from ...gateway.term import term_list as term_list_gateway, create_term as create_term_gateway
from ...gateway import GatewayException

router = APIRouter(prefix="/term")


@router.get("/list")
def term_list() -> list[Term]:
    return term_list_gateway()


@router.post("/")
def create_term(term: TermPost):
    try:
        result = create_term_gateway(term)
        return result.id
    except GatewayException as e:
        raise HTTPException(status_code=400, detail=str(e))


__all__ = ["router"]
