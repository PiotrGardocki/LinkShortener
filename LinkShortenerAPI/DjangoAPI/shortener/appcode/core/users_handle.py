from shortener.appcode.core.users_interface import UsersInterface
from shortener.appcode.core.type_valid import validate_type
from shortener.appcode.core.data_validators import validate_user_password
from shortener.appcode.core.db_errors import *


class UsersActions:
    def __init__(self, users_interface):
        validate_type(users_interface, UsersInterface,
                      'Type of users_interface should be derived from UsersInterface')
        self.users_interface = users_interface

    def create_user(self, email, password):
        validate_type(email, str, 'Type of email must be str')
        validate_user_password(password)

        email = email.strip()

        try:
            self.users_interface.create_user(email, password)
        except EmailAlreadyTaken as error:
            raise error

    def log_user_in(self, email, password):
        validate_type(email, str, 'Type of email must be str')
        validate_type(password, str, 'Type of password must be str')

        email = email.strip()

        try:
            return self.users_interface.log_user_in(email, password)
        except (UserNotExists, WrongPassword) as error:
            raise error

    def log_user_out(self, token):
        validate_type(token, str, 'Type of token must be str')

        try:
            self.users_interface.log_user_out(token)
        except InvalidToken as error:
            raise error

    def delete_user(self, token):
        validate_type(token, str, 'Type of token must be str')

        try:
            self.users_interface.delete_user(token)
        except (InvalidToken, TokenExpired) as error:
            raise error

    def change_user_password(self, token, new_password):
        validate_type(token, str, 'Type of token must be str')
        validate_user_password(new_password)

        try:
            self.users_interface.change_user_password(token, new_password)
        except (InvalidToken, TokenExpired) as error:
            raise error
