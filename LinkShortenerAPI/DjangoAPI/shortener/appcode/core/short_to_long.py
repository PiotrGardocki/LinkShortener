from shortener.appcode.core.links_db_access import LinksDBInterface
from shortener.appcode.core.type_valid import validate_type
from shortener.appcode.core.db_errors import ShortLinkNotExists, IncorrectPasswordForShortLink, BaseDBError


class ShortToLongLinkTranslator:
    def __init__(self, links_interface):
        validate_type(links_interface, LinksDBInterface,
                      'type of links_interface should be derived from LinksDBInterface')
        self.db_interface = links_interface

    def translate_shortlink_to_longlink(self, shortlink, password=''):
        validate_type(shortlink, str, 'shortlink must be str type')
        validate_type(password, str, 'password must be str type')

        try:
            longlink = self.db_interface.get_longlink_from_shortlink(shortlink, password)
            return longlink
        except ShortLinkNotExists as error:
            raise error
        except IncorrectPasswordForShortLink as error:
            raise error
        except BaseDBError as error:
            # TODO add some log saving
            raise BaseDBError("Other application error occurred")
        except BaseException as error:
            # TODO add some log saving
            raise BaseException("Other Python error occurred")

    def check_if_shortlink_requires_password(self, shortlink):
        validate_type(shortlink, str, 'shortlink must be str type')

        try:
            requires = self.db_interface.check_if_shortlink_has_password(shortlink)
            return requires
        except ShortLinkNotExists as error:
            raise error
        except BaseDBError as error:
            # TODO add some log saving
            raise BaseDBError("Other application error occurred")
        except BaseException as error:
            # TODO add some log saving
            raise BaseException("Other Python error occurred")
