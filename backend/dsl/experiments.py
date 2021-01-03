from typing import Type


def callable_object(number: int):
    return number


def test(function: Type[callable_object]):
    return function


print(test(function=callable_object)(number=1))
