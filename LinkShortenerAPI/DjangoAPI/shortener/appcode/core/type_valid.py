class IncorrectType(Exception):
    pass


def validate_type(obj, correct_type, message=None):
    if not isinstance(obj, correct_type):
        if message is None:
            raise IncorrectType('Given type [%s], expected type [%s]' % (type(obj), correct_type))
        else:
            if not isinstance(message, str):
                message = '[Incorrect message]'
            raise IncorrectType('Given type [%s], expected type [%s]; Message: %s' % (type(obj), correct_type, message))
