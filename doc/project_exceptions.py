class DigitException(Exception):
    pass


def isdigit(data):
    if str(data).isdigit():
        return data
    else:
        raise DigitException
