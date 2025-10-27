from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base

DATABASE_URL = "sqlite:////data/app.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True)


def create_database():
    Base.metadata.create_all(bind=engine)


__all__ = ["SessionLocal", "create_database"]
