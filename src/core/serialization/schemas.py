import typing as t
from collections import abc as abc_collections

from core.serialization.exceptions import ValidationError
from core.serialization.fields import Field


class MetaSchema(type):
    @classmethod
    def get_fields(mcs, attrs: t.Mapping[str, t.Any]):
        return {
            attr: obj
            for attr, obj in attrs.items()
            if isinstance(obj, Field)
        }

    def __new__(
            mcs,
            name: str,
            bases: t.Tuple[t.Type, ...],
            attrs: t.Dict[str, t.Any],
    ) -> type:
        cls = super().__new__(mcs, name, bases, attrs)
        cls.fields_map = mcs.get_fields(attrs)
        return cls


class Schema(metaclass=MetaSchema):
    def __init__(self, context: t.Mapping[str, t.Any] = None) -> None:
        self._bind_fields()
        self.context = context or {}

    def _bind_fields(self) -> None:
        for field_name, field_obj in self.fields_map.items():
            field_obj._bind_to_serializer(name=field_name, serializer=self)

    def serialize(self, data: t.Mapping[str, t.Any]) -> dict:
        if not isinstance(data, abc_collections.Mapping):
            raise ValidationError(f'Expected a dictionary, but got {type(data).__name__}')

        serialized_data = {}

        for field_name, field_obj in self.fields_map.items():
            if field_obj.deserialization_only:
                continue

            load_from = field_obj.load_from or field_name
            loaded_value = data.get(load_from, field_obj.value_for_missing)
            serialized_value = field_obj.serialize(loaded_value)
            load_to = field_obj.load_to or field_name
            serialized_data[load_to] = serialized_value

        return serialized_data

    def deserialize(self, data: t.Mapping[str, t.Any], partial=False) -> dict:
        if not isinstance(data, abc_collections.Mapping):
            raise ValidationError(
                f'Expected a dictionary, but got {type(data).__name__}'
            )

        deserialized_data = {}

        for field_name, field_obj in self.fields_map.items():
            if field_obj.serialization_only:
                continue

            load_from = field_obj.load_from or field_name
            loaded_value = data.get(load_from, field_obj.value_for_missing)

            if not loaded_value and partial:
                continue

            if not loaded_value and field_obj.is_required and not field_obj.default:
                raise ValidationError(details=f'{load_from} field is required.')

            serialized_value = field_obj.deserialize(loaded_value)
            load_to = field_obj.load_to or field_name
            deserialized_data[load_to] = serialized_value
        return deserialized_data

    def serialize_many(
            self,
            objs: t.Sequence[t.Mapping[str, t.Any]],
    ):
        return [self.serialize(o) for o in objs]

    def deserialize_many(
            self,
            objs: t.Sequence[t.Mapping[str, t.Any]],
    ):
        return [self.deserialize(o) for o in objs]
