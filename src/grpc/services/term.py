from src.grpc.compiled.term.v1 import DeleteResponse
from ..compiled.term.v1 import TermServiceBase, ListResponse, Term
from ...gateway.term import term_list, get_term, create_term, delete_term, edit_term
from ...gateway import GatewayException, ItemNotFoundException
from grpclib import GRPCError, Status
from ...term import TermPost, Term as TermDomain
from ..prometheus import RPC_COUNTER, RPC_DURATION


class TermService(TermServiceBase):
    async def list(self) -> ListResponse:
        with RPC_DURATION.labels("TermService/list").time():
            RPC_COUNTER.labels("get").inc()
            terms = term_list()
            return ListResponse(items=list(map(lambda t: Term(id=t.id, name=t.name, definition=t.definition), terms)))

    async def get(self, id: int) -> Term:
        with RPC_DURATION.labels("TermService/get").time():
            RPC_COUNTER.labels("TermService/get").inc()
            try:
                t = get_term(id)
                return Term(id=t.id, name=t.name, definition=t.definition)
            except ItemNotFoundException as e:
                raise GRPCError(Status.NOT_FOUND, str(e))

    async def create(self, name: str, definition: str) -> Term:
        with RPC_DURATION.labels("TermService/create").time():
            RPC_COUNTER.labels("TermService/create").inc()
            try:
                t = create_term(TermPost(name=name, definition=definition))
                return Term(id=t.id, name=t.name, definition=t.definition)
            except GatewayException as e:
                raise GRPCError(Status.FAILED_PRECONDITION, str(e))

    async def delete(self, id: int) -> DeleteResponse:
        with RPC_DURATION.labels("TermService/delete").time():
            RPC_COUNTER.labels("TermService/delete").inc()
            try:
                delete_term(id)
                return DeleteResponse(ok=True)
            except ItemNotFoundException as e:
                raise GRPCError(Status.NOT_FOUND, str(e))

    async def update(self, id: int, name: str, definition: str) -> Term:
        with RPC_DURATION.labels("TermService/update").time():
            RPC_COUNTER.labels("TermService/update").inc()
            try:
                t = edit_term(TermDomain(
                    id=id, name=name, definition=definition))
                return Term(id=t.id, name=t.name, definition=t.definition)
            except ItemNotFoundException as e:
                raise GRPCError(Status.NOT_FOUND, str(e))
