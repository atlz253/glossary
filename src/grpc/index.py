import asyncio
from grpclib.server import Server
from .services.term import TermService


async def main():
    server = Server([TermService()])
    await server.start("0.0.0.0", 50051)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
