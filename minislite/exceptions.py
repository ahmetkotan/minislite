class RecordNotFoundError(ValueError):
    pass


class AlreadyExistsError(ValueError):
    pass


class DatabaseNotFoundError(ConnectionError):
    pass


class AreYouSureError(ValueError):
    pass


class WhereOperatorError(ValueError):
    pass
