from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from shortener.appcode.core.links_interface import LinksInterface
from shortener.appcode.core.db_errors import *
from shortener.appcode.django_models.links_model import LinksDB
from shortener.appcode.core.shortlink_data import ShortlinkData

import random
import datetime


class AccessToDjangoLinksDB(LinksInterface):
    def get_longlink_from_shortlink(self, shortlink, password=''):
        try:
            row = LinksDB.objects.get(shortlink=shortlink)
        except ObjectDoesNotExist:
            raise ShortLinkNotExists("shortlink (%s) does not exists" % shortlink)

        if password != row.password:
            raise IncorrectPasswordForShortLink("password (%s) is incorrect for shortlink (%s)" % (shortlink, password))

        return row.longlink

    def get_shortlink_data(self, shortlink):
        try:
            row = LinksDB.objects.get(shortlink=shortlink)
        except ObjectDoesNotExist:
            return ShortlinkData(False, False, False, None)

        has_password = True
        if row.password == '':
            has_password = False

        is_from_user = True
        if row.user is None:
            is_from_user = False

        expiration_date = row.expiration_date

        return ShortlinkData(True, has_password, is_from_user, expiration_date)

    def add_anonymous_shortlink(self, longlink, password=''):
        shortlink_creation_succesful = False
        shortlink = ''

        while not shortlink_creation_succesful:
            try:
                shortlink = AccessToDjangoLinksDB.generate_random_shortlink()
                expire_date = AccessToDjangoLinksDB.get_default_expire_date()
                LinksDB.objects.create(shortlink=shortlink, longlink=longlink,
                                       password=password, expire_date=expire_date)
                shortlink_creation_succesful = True
            except IntegrityError:
                shortlink_creation_succesful = False

        return shortlink

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
