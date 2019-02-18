from django.db import IntegrityError

from shortener.appcode.core.links_interface import LinksInterface
from shortener.appcode.core.db_errors import *
from shortener.appcode.django_models.links_model import LinksDB
from shortener.appcode.django_models.users_model import UsersDB


class AccessToDjangoLinksDB(LinksInterface):
    def get_longlink_from_shortlink(self, shortlink, password=''):
        row = LinksDB.objects.filter(shortlink__exact=shortlink)
        if not row.exists():
            raise ShortLinkNotExists("shortlink (%s) does not exists" % shortlink)
# TODO: refactor
        row = row.get()
        if password != row.password:
            raise IncorrectPasswordForShortLink("password (%s) is incorrect for shortlink (%s)" % (shortlink, password))

        return row.longlink

    def check_if_shortlink_is_in_db(self, shortlink):
        return LinksDB.objects.filter(shortlink__exact=shortlink).exists()

    def check_if_shortlink_has_password(self, shortlink):
        row = LinksDB.objects.filter(shortlink__exact=shortlink)
        if not row.exists():
            raise ShortLinkNotExists("shortlink (%s) does not exists" % shortlink)

        row = row.get()
        return row.password != ''

# methods for inserting links
    def save_shortlink_and_longlink(self, shortlink, longlink, password=''):
        # link = LinksDB(shortlink=shortlink, longlink=longlink, password=password)
        # link.save()
        try:
            LinksDB.objects.create(shortlink=shortlink, longlink=longlink, password=password)
        except IntegrityError:
            raise ShortLinkAlreadyTaken("shortlink (%s) already exists in database" % shortlink)

# methods for modyfying links
#     def change_shortlink(self, old_shortlink, new_shortlink): pass
#
#     def change_longlink(self, shortlink, old_longlink, new_longlink): pass
#
#     def change_password(self, shortlink, old_password, new_password): pass
