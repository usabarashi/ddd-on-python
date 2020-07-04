from dataclasses import dataclass
from functools import reduce
from typing import Callable, Generic, Literal, TypeVar, Union

T = TypeVar('T')
A = TypeVar('A')
E = TypeVar('E')


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

    def __bool__(self) -> Literal[True]:
        return True


@dataclass(frozen=True)
class Err(Generic[E]):
    value: E

    def __bool__(self) -> Literal[False]:
        return False


Result = Union[Err[E], Ok[T]]


class Collection(list):

    def __init__(self, iterable):
        list.__init__(self, iterable)

    def sort(self, *, key=None, reverse=False):
        return Collection(sorted(self, key=key, reverse=reverse))

    def map(self, *, function: Callable[[T], A]):
        return Collection([function(element) for element in self])

    def reduce(self, *, function: Callable[[T, T], T]) -> T:
        return reduce(function, self)
