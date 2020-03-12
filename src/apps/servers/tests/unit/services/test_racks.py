import pytest

from core.serialization.exceptions import ValidationError


def test_fail_add_server(rack_service, db_session, server):
    with pytest.raises(ValidationError):
        rack_service.obj.servers_limit = 0
        rack_service.add_server(server)
        db_session.commit()
