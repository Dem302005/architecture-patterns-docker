class DomainError(Exception):
    pass


class ValidationError(DomainError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
