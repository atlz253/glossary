from ..compiled.term.v1 import TermServiceBase, ListResponse, Term
from ...gateway.term import term_list


class TermService(TermServiceBase):
    async def list(self) -> "ListResponse":
        terms = term_list()
        return ListResponse(items=list(map(lambda t: Term(id=t.id, name=t.name, definition=t.definition), terms)))
