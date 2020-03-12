from unittest.mock import patch

import pytest

from apps.servers.enums import ServerStatus


def test_success_is_deleted(server_service, db_session):
    server_service.obj.status = ServerStatus.DELETED
    db_session.commit()

    assert server_service.is_deleted


def test_fail_is_deleted(server_service, db_session):
    server_service.obj.status = ServerStatus.ACTIVE
    db_session.commit()

    assert not server_service.is_deleted


@pytest.mark.parametrize(
    'method_name, expected_status', [
        ('mark_as_paid', ServerStatus.PAID),
        ('mark_as_unpaid', ServerStatus.UNPAID),
        ('mark_as_active', ServerStatus.ACTIVE),
        ('mark_as_deleted', ServerStatus.DELETED),
    ]
)
def test_mark_as_paid(method_name, expected_status, server_service, db_session):
    with patch('apps.servers.services.session', db_session):
        getattr(server_service, method_name)()
        assert server_service.obj.status == expected_status


@pytest.mark.parametrize(
    'status, expected_status', [
        (ServerStatus.PAID, ServerStatus.PAID),
        (ServerStatus.UNPAID, ServerStatus.UNPAID),
        (ServerStatus.ACTIVE, ServerStatus.ACTIVE),
        (ServerStatus.DELETED, ServerStatus.DELETED),
    ]
)
def test_change_status(status, expected_status, server_service, db_session):
    with patch('apps.servers.services.session', db_session):
        server_service.change_status(status)
        assert server_service.obj.status == expected_status
