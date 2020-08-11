from dataclasses import dataclass
from functools import reduce
from typing import Any, Callable, Generic, Iterable, Literal, Optional, Sequence, TypeVar, Union

_S = TypeVar('_S')  # Self
_T = TypeVar('_T')
_A = TypeVar('_A')
_B = TypeVar('_B')
_E = TypeVar('_E')  # Err


@dataclass(frozen=True)
class Err(Generic[_E]):
    value: _E

    def __bool__(self) -> Literal[False]:
        return False

    def fold(self, err: Callable[[_E], _A], ok: Callable[[_T], _B]) -> Union[_A, _B]:
        return err(self.value)


@dataclass(frozen=True)
class Ok(Generic[_T]):
    value: _T

    def __bool__(self) -> Literal[True]:
        return True

    def fold(self, err: Callable[[_E], _A], ok: Callable[[_T], _B]) -> Union[_A, _B]:
        return ok(self.value)


Result = Union[Err[_E], Ok[_T]]


class ImmutableSequence(Generic[_T], list):

    # Override the list method

    def __init__(self: _S, iterable: Sequence[_T] = list()) -> _S:
        list.__init__(self, iterable)

    def __add__(self: _S, other: Iterable[_T]) -> _S:
        return ImmutableSequence(list.__add__(self, other))

    def __setitem__(self, slice_: slice, iterable: Iterable[_T]) -> None:
        raise TypeError('Does not support the __setitem__ method')

    def __delitem__(self, slice_: slice) -> None:
        raise TypeError('Does not support the __delitem__ method')

    def append(self: _S, obj: _T) -> _S:
        sequence = list(self)
        list.append(sequence, obj)
        return ImmutableSequence(sequence)

    def extend(self: _S, iterable: Iterable[_T]) -> _S:
        sequence = list(self)
        list.extend(sequence, iterable)
        return ImmutableSequence(sequence)

    def insert(self: _S, index: int, obj: _T) -> _S:
        sequence = list(self)
        list.insert(sequence, index, obj)
        return ImmutableSequence(sequence)

    def remove(self: _S, obj: _T) -> _S:
        sequence = list(self)
        list.remove(sequence, obj)
        return ImmutableSequence(sequence)

    def pop(self: _S, index: int) -> _S:
        sequence = list(self)
        list.pop(sequence, index)
        return ImmutableSequence(sequence)

    def clear(self: _S) -> None:
        raise TypeError('Does not support the clear method')

    def index(self: _S, obj: _T,
              start: Union[int, None] = None, end: Union[int, None] = None) -> int:
        return list.index(self, obj, start, end)

    def count(self: _S, obj: _T) -> int:
        return list.count(self, obj)

    def sort(self: _S, *, key: Optional[Callable[[_T], Any]] = None, reverse: bool = False) -> _S:
        sequence = list(self)
        list.sort(sequence, key=key, reverse=reverse)
        return ImmutableSequence(sequence)

    def reverse(self: _S) -> _S:
        sequence = list(self)
        list.reverse(sequence)
        return ImmutableSequence(sequence)

    def copy(self: _S) -> _S:
        return ImmutableSequence(list(self))

   # Add functional method

    def is_empty(self) -> bool:
        return 0 == len(self)

    def non_empty(self) -> bool:
        return 0 < len(self)

    def size(self) -> int:
        return len(self)

    def map(self: _S, /, *, function: Callable[[_T], _A]) -> _S:
        return ImmutableSequence(function(element) for element in self)

    def reduce(self: _S, /, *, function: Callable[[_T, _T], _T]) -> _S:
        return reduce(function, self)

    def filter(self: _S, /, *, function: Callable[[_T], bool]) -> _S:
        return ImmutableSequence(element for element in self if function(element))
