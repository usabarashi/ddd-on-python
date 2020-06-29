import json
from abc import ABC
from dataclasses import asdict, dataclass, field, replace, _process_class
from typing import Callable, Generic, Optional, TypeVar

T = TypeVar('T')
A = TypeVar('A')


def entity(cls=None, /, *, init=True, repr=True, eq=False, order=False, unsafe_hash=False, frozen=True):
    def wrap(cls):
        return _process_class(cls=cls, init=init, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen)
    if cls is None:
        return wrap
    else:
        return wrap(cls)


@entity
class Entity(ABC):
    id: Optional[int] = field(default=None)

    def __bool__(self) -> bool:
        return self.id is not None and self.id > 0

    def __eq__(self, other) -> bool:
        if not self.id:
            return False
        if not other.id:
            return False
        return self.id == other.id

    def _modify(self, **changes):
        return replace(self, **changes)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Value(ABC):
    value: any
