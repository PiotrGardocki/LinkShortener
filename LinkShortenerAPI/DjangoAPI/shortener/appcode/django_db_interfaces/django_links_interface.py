from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist

from shortener.appcode.core.links_interface import LinksInterface
from shortener.appcode.core.links_handle import LinksActions
from shortener.appcode.core.db_errors import *
from shortener.appcode.django_models.links_model import LinksDB
from shortener.appcode.core.shortlink_data import ShortlinkData
from shortener.appcode.core.shortlinks_table import ShortlinksTable
from shortener.appcode.django_db_interfaces.django_users_interface import AccessToDjangoUsersDB


class AccessToDjangoLinksDB(LinksInterface):
    def add_link(self, longlink, link_password='', shortlink=None, user_token=None, expiration_date=None):
        if user_token is None:
            return self.add_link_for_user(longlink, link_password, shortlink, user_token)
        else:
            return self.add_link_for_anonymous(longlink, link_password, expiration_date)

    def delete_link(self, user_token, shortlink):
        user = AccessToDjangoUsersDB().get_usersdb_instance_for_token(user_token)
        link = self.get_shortlink_from_usersdb_instance(user, shortlink)

        num_of_deleted_links = link.delete()[1]['shortener.LinksDB']

        if num_of_deleted_links != 1:
            raise OtherDBError("Link has not been deleted properly")

    def modify_shortlink(self, user_token, old_shortlink, new_shortlink):
        user = AccessToDjangoUsersDB().get_usersdb_instance_for_token(user_token)
        link = self.get_shortlink_from_usersdb_instance(user, old_shortlink)

        with transaction.atomic():
            self.add_link_for_user(link.longlink, link.password, new_shortlink, user_token)
            self.delete_link(user_token, old_shortlink)

    def modify_longlink(self, user_token, shortlink, new_longlink):
        user = AccessToDjangoUsersDB().get_usersdb_instance_for_token(user_token)
        link = self.get_shortlink_from_usersdb_instance(user, shortlink)

        link.longlink = new_longlink
        link.save()

    def modify_link_password(self, user_token, shortlink, new_password):
        user = AccessToDjangoUsersDB().get_usersdb_instance_for_token(user_token)
        link = self.get_shortlink_from_usersdb_instance(user, shortlink)

        link.password = new_password
        link.save()

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

    def get_user_shortlinks_table(self, user_token):
        user = AccessToDjangoUsersDB().get_usersdb_instance_for_token(user_token)
        shortlinks_table = ShortlinksTable()

        for link in user.linksdb_set.all():
            shortlinks_table.add_shortlink(link.shortlink, link.longlink, link.password)

        return shortlinks_table

    def get_shortlink_from_usersdb_instance(self, user, shortlink):
        try:
            return user.linksdb_set.get(shortlink=shortlink)
        except ObjectDoesNotExist:
            raise ShortLinkNotExists('Shortlink(%s) does not exist')

    def add_link_for_user(self, longlink, link_password, shortlink, user_token):
        user = AccessToDjangoUsersDB().get_usersdb_instance_for_token(user_token)

        try:
            if shortlink is None:
                with transaction.atomic():
                    link = self.add_random_link_get_linksdb_instance(longlink, link_password)
                    link.user = user
                    link.save()
            else:
                link = user.linksdb_set.create(shortlink=shortlink, longlink=longlink, password=link_password)
        except IntegrityError:
            raise ShortLinkAlreadyTaken('Shortlink(%s) is already taken' % shortlink)

        return link.shortlink

    def add_link_for_anonymous(self, longlink, link_password, expiration_date):
        with transaction.atomic():
            link = self.add_random_link_get_linksdb_instance(longlink, link_password)
            link.expiration_date = expiration_date
            link.save()

    def add_random_link_get_linksdb_instance(self, longlink, link_password):
        shortlink_creation_succesful = False

        while not shortlink_creation_succesful:
            try:
                shortlink = LinksActions.generate_random_shortlink()
                linksdb_instance = LinksDB.objects.create(shortlink=shortlink, longlink=longlink,
                                                          password=link_password)
                shortlink_creation_succesful = True
            except IntegrityError:
                shortlink_creation_succesful = False

        return linksdb_instance
