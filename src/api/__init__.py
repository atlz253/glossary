from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .term import router as term_router
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.metrics import latency
from ..gateway import TimeoutException


def API():
    app = FastAPI(title="Glossary API")
    app.include_router(term_router)
    Instrumentator().add(latency(should_include_method=True, should_include_handler=True,
                                 should_include_status=True)).instrument(app).expose(app)

    @app.exception_handler(TimeoutException)
    async def gateway_timeout_handler(request: Request, exception: TimeoutException):
        return JSONResponse(status_code=503, content={"detail": str(exception)})

    return app


__all__ = ["API"]
