from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from typing import Any, Callable, Generic, Iterable, Literal, Optional, Sequence, TypeVar, Union

S = TypeVar('S')  # Self
T = TypeVar('T')
A = TypeVar('A')
B = TypeVar('B')
E = TypeVar('E')  # Err


@dataclass(frozen=True)
class Err(Generic[E]):
    value: E

    def __bool__(self) -> Literal[False]:
        return False

    def fold(self, err: Callable[[E], A], ok: Callable[[T], B]) -> Union[A, B]:
        return err(self.value)


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T

    def __bool__(self) -> Literal[True]:
        return True

    def fold(self, err: Callable[[E], A], ok: Callable[[T], B]) -> Union[A, B]:
        return ok(self.value)


Result = Union[Err[E], Ok[T]]


class ImmutableSequence(Generic[T], list):

    # Override the list method

    def __init__(self: S, iterable: Sequence[T] = list()) -> S:
        list.__init__(self, iterable)

    def __add__(self: S, other: Iterable[T]) -> S:
        return ImmutableSequence(list.__add__(self, other))

    def __setitem__(self, slice: slice, iterable: Iterable[T]) -> None:
        raise TypeError('Does not support the __setitem__ method')

    def __delitem__(self, slice: slice) -> None:
        raise TypeError('Does not support the __delitem__ method')

    def append(self: S, obj: T) -> S:
        sequence = list(self)
        list.append(sequence, obj)
        return ImmutableSequence(sequence)

    def extend(self: S, iterable: Iterable[T]) -> S:
        sequence = list(self)
        list.extend(sequence, iterable)
        return ImmutableSequence(sequence)

    def insert(self: S, index: int, obj: T) -> S:
        sequence = list(self)
        list.insert(sequence, index, obj)
        return ImmutableSequence(sequence)

    def remove(self: S, obj: T) -> S:
        sequence = list(self)
        list.remove(sequence, obj)
        return ImmutableSequence(sequence)

    def pop(self: S, index: int) -> S:
        sequence = list(self)
        list.pop(sequence, index)
        return ImmutableSequence(sequence)

    def clear(self: S) -> None:
        raise TypeError('Does not support the clear method')

    def index(self: S, obj: T, start: Union[int, None] = None, end: Union[int, None] = None) -> int:
        return list.index(self, obj, start, end)

    def count(self: S, obj: T) -> int:
        return list.count(self, obj)

    def sort(self: S, *, key: Optional[Callable[[T], Any]] = None, reverse: bool = False) -> S:
        sequence = list(self)
        list.sort(sequence, key=key, reverse=reverse)
        return ImmutableSequence(sequence)

    def reverse(self: S) -> S:
        sequence = list(self)
        list.reverse(sequence)
        return ImmutableSequence(sequence)

    def copy(self: S) -> S:
        return ImmutableSequence(list(self))

   # Add functional method

    def is_empty(self) -> bool:
        return 0 == len(self)

    def non_empty(self) -> bool:
        return 0 < len(self)

    def size(self) -> int:
        return len(self)

    def map(self: S, /, *, function: Callable[[T], A]) -> S:
        return ImmutableSequence(function(element) for element in self)

    def reduce(self: S, /, *, function: Callable[[T, T], T]) -> S:
        return reduce(function, self)
