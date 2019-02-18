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


def validate_list_of_types(obj, correct_types, message=None):
    validate_type(correct_types, list, 'correct_types must be list')

    found_correct_type = False
    for type_ in correct_types:
        try:
            validate_type(obj, type_)
            found_correct_type = True
            break
        except IncorrectType:
            pass

    if not found_correct_type:
        raise IncorrectType(('Given type [%s], expected types[' % type(obj)) + correct_types +
                            (']; Message: %s' % message))
