class RecordNotFoundError(ValueError):
    pass


class AlreadyExistsError(ValueError):
    pass


class DatabaseNotFound(ConnectionError):
    pass


class AreYouSure(ValueError):
    pass
