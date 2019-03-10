class IncorrectType(Exception):
    pass


def validate_type(obj, correct_types, message=None):
    if not isinstance(obj, correct_types):
        if message is None:
            raise IncorrectType('Given type: [%s], expected type(s): [%s]' % (type(obj), str(correct_types)))
        else:
            if not isinstance(message, str):
                message = '[Incorrect message]'
            raise IncorrectType('Given type: [%s], expected type(s): [%s]; Message: %s' %
                                (type(obj), str(correct_types), message))
