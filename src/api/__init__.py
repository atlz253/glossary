from fastapi import FastAPI
from .term import router as term_router


def API():
    app = FastAPI(title="Glossary API")
    app.include_router(term_router)
    return app


__all__ = ["API"]
