from . import term
from . import sio
from socketio import ASGIApp
from .prometheus import WS_CONNECTIONS
from prometheus_client import start_http_server

start_http_server(8002)

app = ASGIApp(sio)


@sio.event
async def connect(sid: str, data: dict):
    WS_CONNECTIONS.inc()


@sio.event
async def disconnect(sid: str):
    WS_CONNECTIONS.dec()
