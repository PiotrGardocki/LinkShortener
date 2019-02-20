from shortener.appcode.core.users_links_interface import UsersLinksInterface
from shortener.appcode.core.type_valid import validate_type
from shortener.appcode.core.db_errors import *


class UsersLinksActions:
    def __init__(self, users_links_interface):
        validate_type(users_links_interface, UsersLinksInterface,
                      'Type of users_links_interface should be derived from UsersLinksInterface')
        self.users_links_interface = users_links_interface

    def add_link(self, user_token, shortlink, longlink, password=''):
        validate_type(user_token, str, 'Type of user_token must be str')
        validate_type(shortlink, str, 'Type of shortlink must be str')
        validate_type(longlink, str, 'Type of longlink must be str')
        validate_type(password, str, 'Type of password must be str')

        try:
            self.users_links_interface.add_link(user_token, shortlink, longlink, password)
        except (InvalidToken, TokenExpired, ShortLinkAlreadyTaken) as error:
            raise error

    def add_random_link(self, user_token, longlink, password=''):
        validate_type(user_token, str, 'Type of user_token must be str')
        validate_type(longlink, str, 'Type of longlink must be str')
        validate_type(password, str, 'Type of password must be str')

        try:
            shortlink = self.users_links_interface.add_random_link(user_token, longlink, password)
            return shortlink
        except (InvalidToken, TokenExpired) as error:
            raise error

    def delete_link(self, user_token, shortlink):
        validate_type(user_token, str, 'Type of user_token must be str')
        validate_type(shortlink, str, 'Type of shortlink must be str')

        try:
            self.users_links_interface.delete_link(user_token, shortlink)
        except (InvalidToken, TokenExpired, ShortLinkNotExists) as error:
            raise error

    def modify_shortlink(self, user_token, old_shortlink, new_shortlink):
        validate_type(user_token, str, 'Type of user_token must be str')
        validate_type(old_shortlink, str, 'Type of old_shortlink must be str')
        validate_type(new_shortlink, str, 'Type of new_shortlink must be str')

        try:
            self.users_links_interface.modify_shortlink(user_token, old_shortlink, new_shortlink)
        except (InvalidToken, TokenExpired, ShortLinkNotExists, ShortLinkAlreadyTaken) as error:
            raise error

    def modify_longlink(self, user_token, shortlink, new_longlink):
        validate_type(user_token, str, 'Type of user_token must be str')
        validate_type(shortlink, str, 'Type of shortlink must be str')
        validate_type(new_longlink, str, 'Type of new_longlik must be str')

        try:
            self.users_links_interface.modify_longlink(user_token, shortlink, new_longlink)
        except (InvalidToken, TokenExpired, ShortLinkNotExists) as error:
            raise error

    def modify_password(self, user_token, shortlink, new_password):
        validate_type(user_token, str, 'Type of user_token must be str')
        validate_type(shortlink, str, 'Type of shortlink must be str')
        validate_type(new_password, str, 'Type of new_password must be str')

        try:
            self.users_links_interface.modify_password(user_token, shortlink, new_password)
        except (InvalidToken, TokenExpired, ShortLinkNotExists) as error:
            raise error

    def change_user_email(self, user_token, new_email):
        validate_type(user_token, str, 'Type of user_token must be str')
        validate_type(new_email, str, 'Type of new_email must be str')

        try:
            self.users_links_interface.change_user_email(user_token, new_email)
        except (InvalidToken, TokenExpired, EmailAlreadyTaken) as error:
            raise error

    def get_user_shotlinks_table(self, user_token):
        validate_type(user_token, str, 'Type of user_token must be str')

        try:
            table = self.users_links_interface.get_user_shortlinks_table(user_token)
            return table
        except (InvalidToken, TokenExpired) as error:
            raise error
