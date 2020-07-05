from dataclasses import dataclass
from functools import reduce
from typing import Callable, Generic, List, Literal, TypeVar, Union

T = TypeVar('T')
A = TypeVar('A')
B = TypeVar('B')
E = TypeVar('E')


@dataclass(frozen=True)
class Err(Generic[E]):
    value: E

    def __bool__(self) -> Literal[False]:
        return False

    def result(self, err: Callable[[E], A], ok: Callable[[T], B]):
        return err(self.value)


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

    def __bool__(self) -> Literal[True]:
        return True

    def result(self, err: Callable[[E], A], ok: Callable[[T], B]):
        return ok(self.value)


Result = Union[Err[E], Ok[T]]


class Collection(Generic[T], list):

    def __init__(self, iterable: List[T]):
        list.__init__(self, iterable)

    def size(self) -> int:
        return len(self)

    def add(self, value: T):
        if not self:
            return Collection([value])
        return Collection(self.append(value))

    def delete(self, value: T):
        if not self:
            return self
        return self.filter(function=lambda element: element != value)

    def sort(self, *, key=None, reverse=False):
        return Collection[T](sorted(self, key=key, reverse=reverse))

    def filter(self, *, function: Callable[[T], bool]):
        return Collection[T]([element for element in self if function(element)])

    def map(self, *, function: Callable[[T], A]):
        return Collection[A]([function(element) for element in self])

    def reduce(self, *, function: Callable[[T, T], T]) -> T:
        return reduce(function, self)
