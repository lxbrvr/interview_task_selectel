import typing as t

from core.serialization.exceptions import ValidationError


class Field:
    def __init__(
            self,
            *,
            load_from: str = None,
            load_to: str = None,
            value_for_missing: str = None,
            default: t.Any = None,
            is_required: bool = True,
            deserialization_only: bool = False,
            serialization_only: bool = False,
            allow_null: bool = False,
            validators=None,
            **kwargs,
    ) -> None:
        self.load_from = load_from
        self.load_to = load_to
        self.value_for_missing = value_for_missing
        self.default = default
        self.is_required = is_required
        self.serialization_only = serialization_only
        self.deserialization_only = deserialization_only
        self.allow_null = allow_null
        self.validators = validators or []

        self.parent = None
        self.name = None

        self.__dict__.update(kwargs)

    def _bind_to_serializer(self, *, name, serializer):
        self.parent = serializer
        self.name = name

    @property
    def root(self):
        root = self

        while root.parent:
            root = root.parent

        return root

    def to_internal_type(self, value: t.Any) -> t.Any:
        return value

    def to_representation(self, value: t.Any) -> t.Any:
        return value

    def serialize(self, value: t.Any) -> t.Any:
        if value is None and self.allow_null:
            return value

        return self.to_representation(value)

    def validate_value(self, value):
        for validator in self.validators:
            validator(value, self.name)

    def deserialize(self, value: t.Any) -> t.Any:
        self.validate_value(value)

        if value is None and self.allow_null:
            return value

        return self.to_internal_type(value)


class StringField(Field):
    def to_internal_type(self, value: t.Any) -> str:
        if not isinstance(value, (str, int, float)):
            raise ValidationError(f"{self.name} should be string type")

        return str(value)

    def to_representation(self, value: t.Any) -> str:
        return str(value)


class DateTimeField(Field):
    def to_representation(self, value):
        return value.isoformat()


class IntegerField(Field):
    def to_internal_type(self, value: t.Any) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValidationError(f'{self.name} should be an integer')

    def to_representation(self, value: t.Any) -> int:
        return int(value)
