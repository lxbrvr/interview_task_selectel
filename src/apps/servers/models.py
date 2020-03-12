from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship

from apps.servers.enums import ServerStatus
from core.models import BaseModel


class Rack(BaseModel):
    __tablename__ = 'rack'

    servers = relationship("Server")
    servers_limit = Column(Integer, nullable=False, default=0)


class Server(BaseModel):
    __tablename__ = 'server'

    rack_id = Column(Integer, ForeignKey('rack.id'), nullable=False)
    paid_at = Column(DateTime)
    status = Column(String(7), nullable=False, default=ServerStatus.UNPAID)
