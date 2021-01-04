from __future__ import annotations

import inspect
import traceback
from dataclasses import dataclass
from functools import reduce
from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Literal,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
_A = TypeVar("_A")
_B = TypeVar("_B")
_E = TypeVar("_E", covariant=True)  # Err


@dataclass(eq=False, frozen=True)
class Err(Generic[_E]):
    """失敗型"""

    value: _E

    def __bool__(self) -> Literal[False]:
        return False

    def fold(self, err: Callable[[_E], _A], ok: Callable[[_T], _B]) -> Union[_A, _B]:
        return err(self.value)


@dataclass(eq=False, frozen=True)
class Ok(Generic[_T]):
    """成功型"""

    value: _T

    def __bool__(self) -> Literal[True]:
        return True

    def fold(self, err: Callable[[_E], _A], ok: Callable[[_T], _B]) -> Union[_A, _B]:
        return ok(self.value)


# 結果型エイリアス: 純粋関数の戻り値型として用いる
Result = Union[Err[_E], Ok[_T]]


def try_out(function: Callable[..., _T]) -> Callable[..., Result[Exception, _T]]:
    """試行デコレーター

    状態異存のある関数の失敗を型検査におさめるために用いる
    
    成功時: Ok型を返却する
    失敗時: Err型を返却する
    """

    def process(*args: Any, **kwargs: Any) -> Result[Exception, _T]:
        try:
            return Ok(value=function(*args, **kwargs))
        except Exception as error:
            error.args = error.args + (
                inspect.currentframe().f_code.co_name,
                args,
                kwargs,
                traceback.format_exc(),
            )
            return Err(value=error)

    return process


class Vector(Sequence[_T]):
    """不変リスト"""

    # Sequence method

    # FIXME: delete Tuple[()]
    def __init__(self, items: Optional[Union[list[_T], tuple[_T], tuple[()]]] = None):
        if items is None:
            items = list()
        list[_T](items)

    # def __getitem__(self, i: int) -> _T_co: ...
    # def __getitem__(self, s: slice) -> Sequence[_T_co]: ...

    def index(self, value: _T, start: int, stop: int) -> int:
        return list[_T].index(list(self), value, start, stop)

    def count(self, value: _T) -> int:
        return list[_T].count(list(self), value)

    def reverse(self) -> Vector[_T]:
        sequence = list(self)
        sequence.reverse()
        return __class__(sequence)

    # def __contains__(self, x: object) -> bool: ...
    # def __iter__(self) -> Iterator[_T_co]: ...
    # def __reversed__(self) -> Iterator[_T_co]: ..

    # Base method

    def __add__(self, other: Iterable[_T]) -> Vector[_T]:
        return __class__(list(self).__add__(list(other)))

    def append(self, obj: _T) -> Vector[_T]:
        sequence = list(self)
        sequence.append(obj)
        return __class__(sequence)

    def extend(self, items: Iterable[_T]) -> Vector[_T]:
        sequence = list(self)
        sequence.extend(items)
        return __class__(sequence)

    def insert(self, index: int, obj: _T) -> Vector[_T]:
        sequence = list(self)
        sequence.insert(index, obj)
        return __class__(sequence)

    def remove(self, obj: _T) -> Vector[_T]:
        sequence = list(self)
        sequence.remove(obj)
        return __class__(sequence)

    def sort(
        self, *, key: Callable[[_T], SupportsLessThan], reverse: bool = ...
    ) -> Vector[_T]:
        sequence = list(self)
        sequence.sort(key, reverse)
        return __class__(sequence)

    def copy(self) -> Vector[_T]:
        return __class__(list(self))

    # Add functional method

    def is_empty(self) -> bool:
        return 0 == len(self)

    def non_empty(self) -> bool:
        return 0 < len(self)

    def size(self) -> int:
        return len(self)

    # FP mehod

    def map(self, /, *, function: Callable[[_T], _A]) -> Vector[_A]:
        return __class__([function(element) for element in self])

    def reduce(self, function: Callable[[_T, Any], _T], initial: _T) -> _T:
        return reduce(function, list(self), initial)

    def filter(self, /, *, function: Callable[[_T], bool]) -> Vector[_T]:
        return __class__([element for element in self if function(element)])

