from socketio import AsyncServer

sio = AsyncServer(async_mode="asgi", logger=True)
