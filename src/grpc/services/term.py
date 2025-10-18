from src.grpc.compiled.term.v1 import DeleteResponse
from ..compiled.term.v1 import TermServiceBase, ListResponse, Term
from ...gateway.term import term_list, get_term, create_term, delete_term, edit_term
from ...gateway import GatewayException, ItemNotFoundException
from grpclib import GRPCError, Status
from ...term import TermPost, Term as TermDomain


class TermService(TermServiceBase):
    async def list(self) -> ListResponse:
        terms = term_list()
        return ListResponse(items=list(map(lambda t: Term(id=t.id, name=t.name, definition=t.definition), terms)))

    async def get(self, id: int) -> Term:
        try:
            t = get_term(id)
            return Term(id=t.id, name=t.name, definition=t.definition)
        except ItemNotFoundException as e:
            raise GRPCError(Status.NOT_FOUND, str(e))

    async def create(self, name: str, definition: str) -> Term:
        try:
            t = create_term(TermPost(name=name, definition=definition))
            return Term(id=t.id, name=t.name, definition=t.definition)
        except GatewayException as e:
            raise GRPCError(Status.FAILED_PRECONDITION, str(e))

    async def delete(self, id: int) -> DeleteResponse:
        try:
            delete_term(id)
            return DeleteResponse(ok=True)
        except ItemNotFoundException as e:
            raise GRPCError(Status.NOT_FOUND, str(e))

    async def update(self, id: int, name: str, definition: str) -> Term:
        try:
            t = edit_term(TermDomain(id=id, name=name, definition=definition))
            return Term(id=t.id, name=t.name, definition=t.definition)
        except ItemNotFoundException as e:
            raise GRPCError(Status.NOT_FOUND, str(e))
