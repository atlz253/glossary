from ..db import SessionLocal
from sqlalchemy import select
from ..db.models import Term as TermMeta
from ..term import Term, TermPost
from . import GatewayException


def term_list():
    s = SessionLocal()
    terms = s.scalars(select(TermMeta)).all()
    return list(map(lambda t: Term(id=t.id, name=t.name, definition=t.definition), terms))


def is_term_with_name_exist(name: str):
    return SessionLocal().scalar(select(TermMeta).where(TermMeta.name == name)) != None


def create_term(term: TermPost):
    if (is_term_with_name_exist(term.name)):
        raise GatewayException(
            f"Термин с названием {term.name} уже существует")
    s = SessionLocal()
    m = TermMeta(name=term.name, definition=term.definition)
    s.add(m)
    s.commit()
    s.refresh(m)
    return Term(id=m.id, name=m.name, definition=m.definition)


__all__ = ["term_list", "create_term"]
