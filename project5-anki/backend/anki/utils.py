from .exceptions import StringLengthTooLongError


def check_string_length(variable, max_length):
    if len(variable) > max_length:
        raise StringLengthTooLongError(len(variable), max_length)
