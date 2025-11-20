import asyncio
from grpclib.server import Server
from .services.term import TermService
from prometheus_client import start_http_server

start_http_server(8001)


async def main():
    server = Server([TermService()])
    await server.start("0.0.0.0", 50051)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
