from shortener.appcode.core.type_valid import validate_type
from shortener.appcode.core.db_errors import ValidationError


def check_for_required_characters(string, characters):
    for char in string:
        valid = False

        for to_check in characters:
            if char == to_check:
                valid = True
                break

        if not valid:
            return False

    return True


def validate_shortlink(shortlink):
    validate_type(shortlink, str, 'Type of shortlink must be str')

    shortlink_length = len(shortlink)
    if shortlink_length < 4 or shortlink_length > 40:
        raise ValidationError('Shortlink\'s length must be in range(4, 40)')

    if not check_for_required_characters(shortlink, 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        raise ValidationError('Invalid characters for shortlink')


def validate_longlink(longlink):
    validate_type(longlink, str, 'Type of longlink must be str')

    shortlink_length = len(longlink)
    if shortlink_length < 1 or shortlink_length > 400:
        raise ValidationError('Longlink\'s length must be in range(1, 400)')

    if not check_for_required_characters(longlink,
                                         'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/:?=&_@#.'):
        raise ValidationError('Invalid characters for longlink')


def validate_user_password(password):
    validate_type(password, str, 'Type of password must be str')

    shortlink_length = len(password)
    if shortlink_length < 5 or shortlink_length > 30:
        raise ValidationError('Password\'s length must be in range(5, 30)')

    if not check_for_required_characters(password,
                                         'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_'):
        raise ValidationError('Invalid characters for user\'s password')


def validate_link_password(password):
    validate_type(password, str, 'Type of password must be str')

    shortlink_length = len(password)
    if shortlink_length > 30:
        raise ValidationError('Password\'s length must be in range(0, 30)')

    if not check_for_required_characters(password,
                                         'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_'):
        raise ValidationError('Invalid characters for link\'s password')
