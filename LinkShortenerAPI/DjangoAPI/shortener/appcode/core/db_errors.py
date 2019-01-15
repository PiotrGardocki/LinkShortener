class BaseDBError(Exception):
    pass


class DBConnectionError(BaseDBError):
    pass


class ShortLinkNotExists(BaseDBError):
    pass


class IncorrectPasswordForShortLink(BaseDBError):
    pass


class ShortLinkAlreadyTaken(BaseDBError):
    pass
