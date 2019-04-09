from shortener.appcode.core.links_interface import LinksInterface
from shortener.appcode.core.users_interface import UsersInterface
from shortener.appcode.core.type_valid import validate_type
from shortener.appcode.core.data_validators import validate_shortlink, validate_longlink, validate_link_password
from shortener.appcode.core.db_errors import *

import random
import datetime


class LinksActions:
    def __init__(self, links_interface, users_interface):
        validate_type(links_interface, LinksInterface,
                      'Type of links_interface should be derived from LinksInterface')
        validate_type(users_interface, UsersInterface,
                      'Type of users_interface should be derived from UsersInterface')
        self.links_interface = links_interface
        self.users_interface = users_interface

    def add_link(self, longlink, link_password='', shortlink=None, user_token=None, expiration_date=None):
        if shortlink is not None:
            validate_shortlink(shortlink)

        validate_longlink(longlink)

        validate_link_password(link_password)

        if user_token is not None:
            expiration_date = self.get_default_expire_date()

        try:
            shortlink = self.links_interface.add_link(longlink, link_password, shortlink, user_token, expiration_date)
            if user_token is not None:
                self.users_interface.refresh_token(user_token)
            return shortlink
        except (ShortLinkAlreadyTaken, InvalidToken) as error:
            raise error

    def delete_link(self, user_token, shortlink):
        try:
            self.links_interface.delete_link(user_token, shortlink)
            self.users_interface.refresh_token(user_token)
        except (InvalidToken, ShortLinkNotExists) as error:
            raise error

    def modify_shortlink(self, user_token, old_shortlink, new_shortlink):
        validate_shortlink(new_shortlink)

        try:
            self.links_interface.modify_shortlink(user_token, old_shortlink, new_shortlink)
            self.users_interface.refresh_token(user_token)
        except (ShortLinkAlreadyTaken,  InvalidToken, ShortLinkNotExists) as error:
            raise error

    def modify_longlink(self, user_token, shortlink, new_longlink):
        validate_longlink(new_longlink)

        try:
            self.links_interface.modify_longlink(user_token, shortlink, new_longlink)
            self.users_interface.refresh_token(user_token)
        except (InvalidToken, ShortLinkNotExists) as error:
            raise error

    def modify_link_password(self, user_token, shortlink, new_password):
        validate_link_password(new_password)

        try:
            self.links_interface.modify_link_password(user_token, shortlink, new_password)
            self.users_interface.refresh_token(user_token)
        except (InvalidToken, ShortLinkNotExists) as error:
            raise error

    def get_longlink_from_shortlink(self, shortlink, password=''):
        try:
            longlink = self.links_interface.get_longlink_from_shortlink(shortlink, password)
            return longlink
        except (IncorrectPasswordForShortLink, ShortLinkNotExists) as error:
            raise error

    def get_shortlink_data(self, shortlink):
        data = self.links_interface.get_shortlink_data(shortlink)
        return data

    def get_user_shortlinks_table(self, user_token):
        try:
            shortlinks_table = self.links_interface.get_user_shortlinks_table(user_token)
            self.users_interface.refresh_token(user_token)
            return shortlinks_table
        except InvalidToken as error:
            raise error

    @staticmethod
    def generate_random_shortlink():
        letters = list('abcdefghijklmnopqrstuvwxyz0123456789')
        shortlink = ''

        for i in range(6):
            shortlink += random.choice(letters)
        # shortlink = random.choices(letters, k=6)

        return shortlink

    @staticmethod
    def get_default_expire_date():
        return datetime.date.today() + datetime.timedelta(days=7)
