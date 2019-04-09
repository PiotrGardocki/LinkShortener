# base errors


class BaseDBError(Exception): pass


class DBConnectionError(BaseDBError): pass


class OtherDBError(BaseDBError): pass


# links errors


class ShortLinkNotExists(BaseDBError): pass


class IncorrectPasswordForShortLink(BaseDBError): pass


class ShortLinkAlreadyTaken(BaseDBError): pass


# users errors

class IncorrectUserData(BaseDBError): pass


class EmailAlreadyTaken(BaseDBError): pass


class InvalidToken(BaseDBError): pass


# validation errors


class ValidationError(BaseDBError): pass
