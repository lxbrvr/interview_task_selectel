import typing as t
import importlib

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask


Base = declarative_base()
Session = sessionmaker()
session = scoped_session(Session)


def cleanup_session(_) -> None:
    session.remove()


def setup_sqla(app: Flask, model_paths: t.List[str]) -> None:
    _ = [importlib.import_module(m) for m in model_paths]
    engine = sqlalchemy.create_engine(app.config['DATABASE_URI'])
    Session.configure(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.teardown_appcontext(cleanup_session)

