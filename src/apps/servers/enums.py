import enum


class ServerStatus(str, enum.Enum):
    UNPAID = 'UNPAID'
    PAID = 'PAID'
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'
