import factory

from apps.servers.models import Server, Rack
from core.db import session


class ServerFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Server
        sqlalchemy_session = session


class RackFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Rack
        sqlalchemy_session = session

