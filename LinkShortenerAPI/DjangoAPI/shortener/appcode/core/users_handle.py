from shortener.appcode.core.users_interface import UsersInterface
from shortener.appcode.core.type_valid import validate_type
from shortener.appcode.core.db_errors import WrongPassword, UserNotExists, EmailAlreadyTaken, BaseDBError, InvalidToken


class UsersActions:
    def __init__(self, users_interface):
        validate_type(users_interface, UsersInterface,
                      'type of users_interface should be derived from UsersInterface')
        self.db_interface = users_interface

    def create_user(self, email, password):
        try:
            self.db_interface.create_user(email, password)
        except EmailAlreadyTaken as error:
            raise error
        except BaseDBError as error:
            # TODO add some log saving
            raise BaseDBError("Other application error occurred")
        except BaseException as error:
            # TODO add some log saving
            raise BaseException("Other Python error occurred")

    def log_user_in(self, email, password):
        try:
            self.db_interface.log_user_in(email, password)
        except (UserNotExists, WrongPassword) as error:
            raise error
        except BaseDBError as error:
            # TODO add some log saving
            raise BaseDBError("Other application error occurred")
        except BaseException as error:
            # TODO add some log saving
            raise BaseException("Other Python error occurred")

    def log_user_out(self, token):
        try:
            self.db_interface.log_user_out(token)
        except InvalidToken as error:
            raise error
        except BaseDBError as error:
            # TODO add some log saving
            raise BaseDBError("Other application error occurred")
        except BaseException as error:
            # TODO add some log saving
            raise BaseException("Other Python error occurred")

    def delete_user(self, token):
        try:
            self.db_interface.delete_user(token)
        except InvalidToken as error:
            raise error
        except BaseDBError as error:
            # TODO add some log saving
            raise BaseDBError("Other application error occurred")
        except BaseException as error:
            # TODO add some log saving
            raise BaseException("Other Python error occurred")

    def change_user_password(self, token, new_password):
        try:
            self.db_interface.delete_email(token, new_password)
        except InvalidToken as error:
            raise error
        except BaseDBError as error:
            # TODO add some log saving
            raise BaseDBError("Other application error occurred")
        except BaseException as error:
            # TODO add some log saving
            raise BaseException("Other Python error occurred")

    def change_user_email(self, token, new_email):
        try:
            self.db_interface.delete_email(token, new_email)
        except (InvalidToken, EmailAlreadyTaken) as error:
            raise error
        except BaseDBError as error:
            # TODO add some log saving
            raise BaseDBError("Other application error occurred")
        except BaseException as error:
            # TODO add some log saving
            raise BaseException("Other Python error occurred")

    # def get_user_shotlinks_table(self, email, password):
    #     pass
