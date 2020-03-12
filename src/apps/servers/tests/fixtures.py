import pytest

from apps.servers.services import ServerService, RackService
from apps.servers.tests.factories import ServerFactory, RackFactory


@pytest.fixture
def server() -> ServerFactory:
    return ServerFactory()


@pytest.fixture
def rack() -> RackFactory:
    return RackFactory()


@pytest.fixture
def rack_service(rack) -> RackService:
    return RackService().from_obj(rack)


@pytest.fixture
def server_service(server) -> ServerService:
    return ServerService().from_obj(server)
