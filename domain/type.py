from dataclasses import dataclass
from typing import Generic, Literal, TypeVar, Union

T = TypeVar('T')
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
