from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist

from shortener.appcode.core.users_links_interface import UsersLinksInterface
from shortener.appcode.core.db_errors import *
from shortener.appcode.django_db_interfaces.django_users_interface import AccessToDjangoUsersDB
from shortener.appcode.django_db_interfaces.django_links_interface import AccessToDjangoLinksDB
from shortener.appcode.core.shortlinks_table import ShortlinksTable


class AccessToDjangoUsersLinksDB(UsersLinksInterface):
    def add_link(self, user_token, shortlink, longlink, password=''):
        user = self.get_user_for_token(user_token)
        self.add_link_for_usersdb_instance(user, shortlink, longlink, password)

    def add_random_link(self, user_token, longlink, password=''):
        user = self.get_user_for_token(user_token)

        shortlink_creation_succesful = False
        shortlink = ''

        while not shortlink_creation_succesful:
            try:
                shortlink = AccessToDjangoLinksDB.generate_random_shortlink()
                user.linksdb_set.create(shortlink=shortlink, longlink=longlink, password=password)
                shortlink_creation_succesful = True
            except IntegrityError:
                shortlink_creation_succesful = False

        return shortlink

    def delete_link(self, user_token, shortlink):
        self.delete_link_for_usersdb_instance(self.get_user_for_token(user_token), shortlink)

    def modify_shortlink(self, user_token, old_shortlink, new_shortlink):
        user = self.get_user_for_token(user_token)
        link = self.get_shortlink_from_usersdb_instance(user, old_shortlink)
        with transaction.atomic():
            self.add_link_for_usersdb_instance(user, new_shortlink, link.longlink, link.password)
            self.delete_link_for_usersdb_instance(user, old_shortlink)

    def modify_longlink(self, user_token, shortlink, new_longlink):
        link = self.get_shortlink_from_usersdb_instance(self.get_user_for_token(user_token), shortlink)
        link.longlink = new_longlink
        link.save()

    def modify_password(self, user_token, shortlink, new_password):
        link = self.get_shortlink_from_usersdb_instance(self.get_user_for_token(user_token), shortlink)
        link.password = new_password
        link.save()

    def change_user_email(self, user_token, new_email):
        old_user = self.get_user_for_token(user_token)
        password = old_user.password

        users_interface = AccessToDjangoUsersDB()

        with transaction.atomic():
            new_user = users_interface.create_and_get_usersdb_instance(new_email, password)
            old_user.linksdb_set.all().update(user=new_user)
            users_interface.delete_user_by_usersdb_instance(old_user)

    def get_user_shortlinks_table(self, user_token):
        user = self.get_user_for_token(user_token)
        shortlinks_table = ShortlinksTable()

        for link in user.linksdb_set.all():
            shortlinks_table.add_shortlink(link.shortlink, link.longlink, link.password)

        return shortlinks_table

    def get_user_for_token(self, token):
        return AccessToDjangoUsersDB().get_user_for_token(token)

    def get_shortlink_from_usersdb_instance(self, user, shortlink):
        try:
            return user.linksdb_set.get(shortlink=shortlink)
        except ObjectDoesNotExist:
            raise ShortLinkNotExists('Shortlink(%s) does not exist')

    def add_link_for_usersdb_instance(self, user, shortlink, longlink, password):
        try:
            user.linksdb_set.create(shortlink=shortlink, longlink=longlink, password=password)
        except IntegrityError:
            raise ShortLinkAlreadyTaken('Shortlink(%s) is already taken' % shortlink)

    def delete_link_for_usersdb_instance(self, user, shortlink):
        link = self.get_shortlink_from_usersdb_instance(user, shortlink)
        num_of_deleted_links = link.delete()[0]

        if num_of_deleted_links != 1:
            raise OtherDBError("Shortlink has not been deleted properly")
