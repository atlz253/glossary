from fastapi import FastAPI
from .term import router as term_router
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_fastapi_instrumentator.metrics import latency


def API():
    app = FastAPI(title="Glossary API")
    app.include_router(term_router)
    Instrumentator().add(latency(should_include_method=True, should_include_handler=True,
                                 should_include_status=True)).instrument(app).expose(app)
    return app


__all__ = ["API"]
