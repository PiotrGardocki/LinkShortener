from shortener.appcode.core.type_valid import validate_type, validate_list_of_types
import datetime


class ShortlinkData:
    def __init__(self, does_exist, need_password, belongs_to_user, expiration_date):
        self.set_does_exist(does_exist)
        self.set_if_need_password(need_password)
        self.set_if_belongs_to_user(belongs_to_user)
        self.set_expiration_date(expiration_date)

    def set_does_exist(self, does_exist):
        validate_type(does_exist, bool, 'Type of does_exist must be bool')
        self.does_exist = does_exist

    def set_if_need_password(self, need_password):
        validate_type(need_password, bool, 'Type of need_password must be bool')
        self.does_exist = need_password

    def set_if_belongs_to_user(self, belongs_to_user):
        validate_type(belongs_to_user, bool, 'Type of belongs_to_user must be bool')
        self.does_exist = belongs_to_user

    def set_expiration_date(self, expiration_date):
        validate_list_of_types(expiration_date, [datetime.date, None],
                               'Type of expiration_date must be datetime.date or None')
        self.expiration_date = expiration_date

    def exists(self):
        return self.does_exist

    def does_need_password(self):
        return self.need_password

    def does_belong_to_user(self):
        return self.belongs_to_user

    def get_expiration_date(self):
        return self.expiration_date
