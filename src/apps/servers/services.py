import datetime
import threading
import time
import random

from flask import current_app

from apps.servers.enums import ServerStatus
from apps.servers.models import Rack, Server
from core.db import session
from core.serialization.exceptions import ValidationError
from core.services import Service


class RackService(Service):
    model_class = Rack

    def has_free_slots(self) -> bool:
        return len(self.obj.servers) < self.obj.servers_limit

    def add_server(self, server: Server) -> None:
        if not self.has_free_slots():
            raise ValidationError('The rack has not free slots')

        session.add(server)
        session.commit()

        current_app.logger.info(f'В стойку с идентификатором {self.obj.id} добавлен сервер')


class ServerService(Service):
    model_class = Server

    def _pay_imitation(self, server_id: int) -> None:
        time.sleep(random.randint(5, 15))
        obj = session.query(Server).get(server_id)
        obj.status = ServerStatus.ACTIVE
        session.commit()

        current_app.logger.info(f'Сервер с идентификатором {self.obj.id} стал активен')

    def pay(self) -> None:
        if self.is_deleted:
            raise ValidationError('Server is deleted.')

        # имитация оплаты
        threading.Thread(
            target=self._pay_imitation,
            kwargs={'server_id': self.obj.id},
        ).start()

        self.mark_as_paid()
        self.obj.paid_at = datetime.datetime.now()
        session.commit()

        current_app.logger.debug(f'Оплачен сервер с идентификатором {self.obj.id}')

    @property
    def is_deleted(self) -> bool:
        return self.obj.status == ServerStatus.DELETED

    def mark_as_paid(self) -> None:
        self.change_status(ServerStatus.PAID)

    def mark_as_unpaid(self) -> None:
        self.change_status(ServerStatus.UNPAID)

    def mark_as_active(self) -> None:
        self.change_status(ServerStatus.ACTIVE)

    def mark_as_deleted(self) -> None:
        self.change_status(ServerStatus.DELETED)

    def change_status(self, status: str) -> None:
        if self.is_deleted:
            raise ValidationError('Server is deleted.')

        self.obj.status = status
        session.commit()

        current_app.logger.info(f'Сервер с идентификатором {self.obj.id} изменил статус на {status}')
