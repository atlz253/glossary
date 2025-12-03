from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base

POOL_SIZE = 20
DATABASE_URL = "postgresql+psycopg2://glossary:glossary@postgres:5432/glossary"

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    future=True,
)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True)


def create_database():
    Base.metadata.create_all(bind=engine)


__all__ = ["SessionLocal", "create_database", "POOL_SIZE"]
