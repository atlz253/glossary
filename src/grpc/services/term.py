from ..compiled.term.v1 import TermServiceBase, ListResponse, Term
from ...gateway.term import term_list, get_term
from ...gateway import ItemNotFoundException
from grpclib import GRPCError, Status


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
