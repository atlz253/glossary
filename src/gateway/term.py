from ..db import SessionLocal
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from ..db.models import Term as TermMeta
from ..term import Term, TermPost
from . import GatewayException, ItemNotFoundException


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
    m = TermMeta(name=term.name.lower(), definition=term.definition.lower())
    s.add(m)
    s.commit()
    s.refresh(m)
    return Term(id=m.id, name=m.name, definition=m.definition)


def get_term_with_session(id: int, session: Session):
    term = session.scalar(select(TermMeta).where(TermMeta.id == id))
    if (term == None):
        raise ItemNotFoundException(f"Термин с ID {id} не найден")
    else:
        return term


def get_term(id: int):
    term = get_term_with_session(id, SessionLocal())
    return Term(id=term.id, name=term.name, definition=term.definition)


def delete_term(id: int):
    s = SessionLocal()
    term = get_term_with_session(id=id, session=s)
    s.delete(term)
    s.commit()


def edit_term(term: Term):
    s = SessionLocal()
    m = get_term_with_session(id=term.id, session=s)
    m.name = term.name
    m.definition = term.definition
    s.commit()
    s.refresh(m)
    return Term(id=m.id, name=m.name.lower(), definition=m.definition.lower())


__all__ = ["term_list", "create_term", "get_term", "delete_term", "edit_term"]
