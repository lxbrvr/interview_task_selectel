class SerializerError(Exception):
    pass


class ValidationError(SerializerError):
    def __init__(self, details: str) -> None:
        self.details = details

