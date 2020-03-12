from core.serialization import fields
from core.serialization.schemas import Schema


class RackSchema(Schema):
    id = fields.IntegerField(serialization_only=True)
    created_at = fields.DateTimeField(serialization_only=True)
    updated_at = fields.DateTimeField(serialization_only=True)
    servers_limit = fields.IntegerField()


class ServerSchema(Schema):
    id = fields.IntegerField(serialization_only=True)
    created_at = fields.DateTimeField(serialization_only=True)
    updated_at = fields.DateTimeField(serialization_only=True,)
    rack_id = fields.IntegerField()
    paid_at = fields.DateTimeField(serialization_only=True, allow_null=True)
    status = fields.StringField(serialization_only=True)


class PurchaseSchema(Schema):
    server_id = fields.IntegerField(deserialization_only=True)
    id = fields.IntegerField(serialization_only=True, load_to='server_id')
    paid_at = fields.DateTimeField(serialization_only=True)


