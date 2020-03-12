from core.db import session
from core.serialization.exceptions import ValidationError


class Service:
    model_class = None

    def __init__(self) -> None:
        self.obj = None

    def from_id(self, obj_id: int) -> 'Service':
        obj = session.query(self.model_class).get(obj_id)

        if not obj:
            raise ValidationError('Input data is incorrect.')

        self.obj = obj
        return self

    def from_obj(self, obj) -> 'Service':
        self.obj = obj
        return self
