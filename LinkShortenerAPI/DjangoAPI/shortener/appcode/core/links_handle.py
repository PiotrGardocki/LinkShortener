from shortener.appcode.core.links_interface import LinksInterface
from shortener.appcode.core.type_valid import validate_type
from shortener.appcode.core.data_validators import validate_shortlink, validate_longlink, validate_link_password
from shortener.appcode.core.db_errors import *


class LinksActions:
    def __init__(self, links_interface):
        validate_type(links_interface, LinksInterface,
                      'Type of links_interface should be derived from LinksInterface')
        self.links_interface = links_interface

    def get_longlink_from_shortlink(self, shortlink, password=''):
        validate_type(shortlink, str, "Type of shortlink must be str")
        validate_type(password, str, "Type of password must be str")

        try:
            longlink = self.links_interface.get_longlink_from_shortlink(shortlink, password)
            return longlink
        except (ShortLinkNotExists, IncorrectPasswordForShortLink) as error:
            raise error

    def get_shortlink_data(self, shortlink):
        validate_type(shortlink, str, "Type of shortlink must be str")

        data = self.links_interface.get_shortlink_data(shortlink)
        return data

    def add_anonymous_shortlink(self, longlink, password=''):
        validate_longlink(longlink)
        validate_link_password(password)

        return self.links_interface.add_anonymous_shortlink(longlink, password)
