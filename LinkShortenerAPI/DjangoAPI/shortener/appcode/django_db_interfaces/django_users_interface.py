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

    def delete_user(self, token):
        user = self.get_user_for_token(token)
        self.delete_user_by_usersdb_instance(user)

    def change_user_password(self, token, new_password):
        user = self.get_user_for_token(token)

        user.password = new_password
        user.save()
        self.expire_token(token)

    def log_user_in(self, email, password):
        try:
            user = UsersDB.objects.get(email=email)
        except ObjectDoesNotExist:
            raise UserNotExists("User(%s) does not exist" % email)

        if user.password != password:
            raise WrongPassword("Password(%s) is wrong" % password)

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
        self.expire_token(token)

    def extend_token(self, token):
        user = self.get_user_for_token(token)
        user.token_expiration = self.get_token_expiration_time()
        user.save()

    def expire_token(self, token):
        try:
            user = UsersDB.objects.get(token=token)
        except ObjectDoesNotExist:
            raise InvalidToken("Given token is invalid")

        user.token = None
        user.token_expiration = None
        user.save()

    def get_user_for_token(self, token):
        try:
            user = UsersDB.objects.get(token=token)
            if user.token_expiration < datetime.datetime.today():
                self.expire_token(token)
                raise TokenExpired("Given token expired")
            return user
        except ObjectDoesNotExist:
            raise InvalidToken("Given token is invalid")

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
