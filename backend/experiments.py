import pprint


class UserDefineError(Exception):
    pass


class MoreError(UserDefineError):
    pass


try:
    raise MoreError('モア')
except Exception as error:
    pprint.pprint(error)
