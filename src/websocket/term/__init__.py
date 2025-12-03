from .. import sio
from ...gateway.term import term_list as term_list_gateway, create_term as create_term_gateway, delete_term as delete_term_gateway, get_term as get_term_gateway, edit_term as edit_term_gateway
from ...gateway import ItemNotFoundException, GatewayException, TimeoutException
from ...term import TermPost, Term
from pydantic import ValidationError
from ..prometheus import WS_MESSAGES_TOTAL, WS_ERRORS_TOTAL, WS_EVENT_DURATION

EVENTS = {
    "error": "error",
    "term_list_response": "term_list_response",
    "get_term_response": "get_term_response",
    "create_term_response": "create_term_response",
    "edit_term_response": "edit_term_response",
    "delete_term_response": "delete_term_response"
}


@sio.event
async def term_list(sid: str, data=None):
    try:
        await sio.emit(EVENTS["term_list_response"], list(map(lambda t: t.to_dict(), term_list_gateway())), to=sid)
    except TimeoutException as e:
        WS_ERRORS_TOTAL.labels(event="get_term").inc()
        await sio.emit(EVENTS["error"], {"message": str(e)}, to=sid)


@sio.event
async def get_term(sid: str, data: dict):
    with WS_EVENT_DURATION.labels(event="get_term").time():
        WS_MESSAGES_TOTAL.labels(event="get_term").inc()
        if data.get("id") == None:
            await sio.emit(EVENTS["error"], {"message": "в теле запроса отсутствует id"}, to=sid)
        else:
            try:
                term = get_term_gateway(data["id"])
                await sio.emit(EVENTS["get_term_response"], term.to_dict(), to=sid)
            except ItemNotFoundException as error:
                WS_ERRORS_TOTAL.labels(event="get_term").inc()
                await sio.emit(EVENTS["error"], {"message": str(error)}, to=sid)
            except TimeoutException as e:
                WS_ERRORS_TOTAL.labels(event="get_term").inc()
                await sio.emit(EVENTS["error"], {"message": str(e)}, to=sid)


@sio.event
async def create_term(sid: str, data: dict):
    with WS_EVENT_DURATION.labels(event="create_term").time():
        WS_MESSAGES_TOTAL.labels(event="create_term").inc()
        try:
            term = create_term_gateway(TermPost(**data))
            await sio.emit(EVENTS["create_term_response"], term.to_dict(), to=sid)
        except ValidationError:
            WS_ERRORS_TOTAL.labels(event="create_term").inc()
            await sio.emit(EVENTS["error"], {"message": "Ошибка валидации"}, to=sid)
        except TimeoutException as e:
            WS_ERRORS_TOTAL.labels(event="get_term").inc()
            await sio.emit(EVENTS["error"], {"message": str(e)}, to=sid)
        except GatewayException as error:
            WS_ERRORS_TOTAL.labels(event="create_term").inc()
            await sio.emit(EVENTS["error"], {"message": str(error)}, to=sid)


@sio.event
async def edit_term(sid: str, data: dict):
    with WS_EVENT_DURATION.labels(event="edit_term").time():
        WS_MESSAGES_TOTAL.labels(event="edit_term").inc()
        try:
            term = edit_term_gateway(Term(**data))
            await sio.emit(EVENTS["edit_term_response"], term.to_dict(), to=sid)
        except ValidationError:
            WS_ERRORS_TOTAL.labels(event="edit_term").inc()
            await sio.emit(EVENTS["error"], {"message": "Ошибка валидации"}, to=sid)
        except ItemNotFoundException as error:
            WS_ERRORS_TOTAL.labels(event="edit_term").inc()
            await sio.emit(EVENTS["error"], {"message": str(error)}, to=sid)
        except TimeoutException as e:
            WS_ERRORS_TOTAL.labels(event="get_term").inc()
            await sio.emit(EVENTS["error"], {"message": str(e)}, to=sid)


@sio.event
async def delete_term(sid: str, data: dict):
    with WS_EVENT_DURATION.labels(event="delete_term").time():
        WS_MESSAGES_TOTAL.labels(event="delete_term").inc()
        if data.get("id") == None:
            await sio.emit(EVENTS["error"], {"message": "в теле запроса отсутствует id"}, to=sid)
        else:
            try:
                delete_term_gateway(data["id"])
                await sio.emit(EVENTS["delete_term_response"], {"status": "ok"}, to=sid)
            except ItemNotFoundException as error:
                WS_ERRORS_TOTAL.labels(event="delete_term").inc()
                await sio.emit(EVENTS["error"], {"message": str(error)}, to=sid)
            except TimeoutException as e:
                WS_ERRORS_TOTAL.labels(event="get_term").inc()
                await sio.emit(EVENTS["error"], {"message": str(e)}, to=sid)
