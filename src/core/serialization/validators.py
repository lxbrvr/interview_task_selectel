from core.serialization.exceptions import ValidationError


class OneOf:
    def __init__(self, choices=None):
        self.choices = choices or []

    def __call__(self, value, field_name):
        if value not in self.choices:
            raise ValidationError(details=f'{field_name} should be one of {self.choices}')
