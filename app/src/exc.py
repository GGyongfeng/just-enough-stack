class ExistenceError(Exception):
    pass


class AlreadyExistsError(ExistenceError):
    pass


class NotExistsError(ExistenceError):
    pass
