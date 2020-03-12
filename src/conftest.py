import importlib

import pytest
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from app_test import app as test_app
from core.db import Base


_ = [importlib.import_module(m) for m in test_app.config['MODEL_PATHS']]
engine = sqlalchemy.create_engine(test_app.config['DATABASE_URI'])
Base.metadata.create_all(engine)
Session = sessionmaker()


@pytest.fixture(scope='module')
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope='function')
def db_session(connection):
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()


@pytest.fixture
def app():
    return test_app


@pytest.fixture
def client(app):
    return app.test_client()


pytest_plugins = [
    'apps.servers.tests.fixtures',
]
