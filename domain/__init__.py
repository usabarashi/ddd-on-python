from abc import ABC
from dataclasses import asdict, dataclass, field, replace, _process_class
from typing import Optional, TypeVar

T = TypeVar('T')
A = TypeVar('A')


@dataclass(frozen=True)
class Entity:
    id: Optional[int] = field(default=None)

    def __bool__(self) -> bool:
        return self.id is not None and self.id > 0

    def __eq__(self, other) -> bool:
        if not self:
            return False
        if not other:
            return False
        return self.id == other.id

    def _update(self, **changes):
        return replace(self, **changes)

    def as_role(self, role: type):
        return role(**self.as_dict())

    def as_dict(self) -> dict:
        return asdict(self)


def entity(cls, /):
    return _process_class(cls=cls, init=True, repr=True, eq=False, order=False, unsafe_hash=False, frozen=True)


@dataclass(frozen=True)
class Value(ABC):
    value: any


def value(cls, /):
    return _process_class(cls=cls, init=True, repr=True, eq=False, order=False, unsafe_hash=False, frozen=True)
