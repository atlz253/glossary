from fastapi import APIRouter, HTTPException

from ..ExceptionResponse import ExceptionResponse
from ...term import Term, TermPost
from ...gateway.term import term_list as term_list_gateway, create_term as create_term_gateway, delete_term as delete_term_gateway, get_term as get_term_gateway, edit_term as edit_term_gateway
from ...gateway import GatewayException, ItemNotFoundException
from ...ID import ID

STRINGS = {
    "term_not_found": "Термин не найден",
    "term_already_exist": "Термин с данным названием уже существует"
}

router = APIRouter(prefix="/term")


@router.get("/list")
def term_list() -> list[Term]:
    return term_list_gateway()


@router.get("/", responses={404: {"model": ExceptionResponse, "description": STRINGS["term_not_found"]}})
def get_term(id: ID):
    try:
        return get_term_gateway(id.id)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", responses={400: {"model": ExceptionResponse, "description": STRINGS["term_already_exist"]}})
def create_term(term: TermPost):
    try:
        return create_term_gateway(term)
    except GatewayException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/", responses={404: {"model": ExceptionResponse, "description": STRINGS["term_not_found"]}})
def edit_term(term: Term):
    try:
        return edit_term_gateway(term)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/", responses={404: {"model": ExceptionResponse, "description": STRINGS["term_not_found"]}})
def delete_term(id: ID):
    try:
        delete_term_gateway(id.id)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


__all__ = ["router"]
