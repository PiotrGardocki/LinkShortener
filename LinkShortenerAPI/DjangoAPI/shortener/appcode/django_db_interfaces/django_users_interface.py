from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist

from shortener.appcode.core.users_interface import UsersInterface
from shortener.appcode.core.db_errors import *
from shortener.appcode.django_models.users_model import UsersDB

import datetime
import random


class AccessToDjangoUsersDB(UsersInterface):
    def create_user(self, email, password):
        self.create_and_get_usersdb_instance(email, password)

    def log_user_in(self, email, password):
        try:
            user = UsersDB.objects.get(email=email)
        except ObjectDoesNotExist:
            raise IncorrectUserData("Incorrect user's data")

        if user.password != password:
            raise IncorrectUserData("Incorrect user's data")

        token_creation_succesful = False
        while not token_creation_succesful:
            try:
                user.token = self.generate_token_for_user()
                expiration_time = self.get_token_expiration_time()
                user.token_expiration = expiration_time
                user.save()
                token_creation_succesful = True
            except IntegrityError:
                token_creation_succesful = False

        return user.token

    def log_user_out(self, token):
        try:
            user = UsersDB.objects.get(token=token)
        except ObjectDoesNotExist:
            raise InvalidToken("Given token is invalid")

        user.token = None
        user.token_expiration = None
        user.save()

    def delete_user(self, token):
        user = self.get_usersdb_instance_for_token(token)
        self.delete_user_by_usersdb_instance(user)

    def change_user_password(self, token, new_password):
        user = self.get_usersdb_instance_for_token(token)

        user.password = new_password
        user.save()

    def change_user_email(self, token, new_email):
        old_user = self.get_usersdb_instance_for_token(token)
        password = old_user.password

        with transaction.atomic():
            new_user = self.create_and_get_usersdb_instance(new_email, password)
            old_user.linksdb_set.all().update(user=new_user)
            self.delete_user_by_usersdb_instance(old_user)

    def validate_token(self, token):
        self.get_usersdb_instance_for_token(token)

    def refresh_token(self, token):
        user = self.get_usersdb_instance_for_token(token)
        user.token_expiration = self.get_token_expiration_time()
        user.save()

    @staticmethod
    def generate_token_for_user():
        letters = list('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        token = ''

        for i in range(30):
            token += random.choice(letters)
        # shortlink = random.choices(letters, k=30)

        return token

    @staticmethod
    def get_token_expiration_time():
        return datetime.datetime.today() + datetime.timedelta(minutes=10)

    def create_and_get_usersdb_instance(self, email, password):
        try:
            return UsersDB.objects.create(email=email, password=password)
        except IntegrityError:
            raise EmailAlreadyTaken("Email(%s) is already taken" % email)

    def delete_user_by_usersdb_instance(self, user):
        num_of_deleted_users = user.delete()[1]['shortener.UsersDB']

        if num_of_deleted_users != 1:
            raise OtherDBError("User has not been deleted properly")

    def get_usersdb_instance_for_token(self, token):
        try:
            user = UsersDB.objects.get(token=token)
            if user.token_expiration < datetime.datetime.today():
                self.log_user_out(token)
                raise InvalidToken("Given token is invalid")
            return user
        except ObjectDoesNotExist:
            raise InvalidToken("Given token is invalid")
