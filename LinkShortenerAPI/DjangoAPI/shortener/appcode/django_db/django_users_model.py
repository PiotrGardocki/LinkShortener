from django.db import models, IntegrityError, transaction

from django.core.exceptions import ObjectDoesNotExist

from shortener.appcode.core.users_interface import UsersInterface
from shortener.appcode.core.db_errors import *


class UsersDB(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=30)


class AccessToDjangoUsersDB(UsersInterface):
    def create_user(self, email, password):
        try:
            UsersDB.objects.create(email=email, password=password)
        except IntegrityError:
            raise EmailAlreadyTaken("email(%s) is already taken" % email)

    def delete_user(self, email, password):
        try:
            user = UsersDB.objects.get(email=email)
        except ObjectDoesNotExist:
            raise UserNotExists("user with email(%s) does not exists" % email)

        if user.password != password:
            raise WrongPassword("password(%s) is incorrect for user(%s)" % (password, email))

        deleted_users = UsersDB.objects.filter(email=email, password=password).delete()[0]

        if deleted_users != 1:
            raise OtherDBError("User has not been deleted properly")

    def change_user_password(self, email, old_password, new_password):
        try:
            user = UsersDB.objects.get(email=email)
        except ObjectDoesNotExist:
            raise UserNotExists("user with email(%s) does not exists" % email)

        if user.password != old_password:
            raise WrongPassword("password(%s) is incorrect for user(%s)" % (old_password, email))

        user.password = new_password
        user.save()

    def change_user_email(self, old_email, new_email, password):
        with transaction.atomic():
            self.create_user(new_email, password)
            self.delete_user(old_email, password)

        # self.create_user(new_email, password)
        # try:
        #     self.delete_user(old_email, password)
        # except UserNotExists as error:
        #     self.delete_user(new_email, password)
        #     raise error
        # except WrongPassword as error:
        #     self.delete_user(new_email, password)
        #     raise error


        # try:
        #     user = UsersDB.objects.get(email=old_email)
        # except ObjectDoesNotExist:
        #     raise UserNotExists("user with email(%s) does not exists" % old_email)
        #
        # if user.password != password:
        #     raise WrongPassword("password(%s) is incorrect for user(%s)" % (password, old_email))
        # do zrobienia
        # user.
        # user.save()
