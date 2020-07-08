__all__ = []

from dataclasses import asdict, dataclass, field, replace, _process_class
from typing import Optional, TypeVar

S = TypeVar('S')  # Self
R = TypeVar('R')  # Role
Id = int


@dataclass(frozen=True)
class Entity:
    id: Optional[Id] = field(default=None)

    def __bool__(self: S) -> bool:
        return self.id is not None and self.id > 0

    def __eq__(self: S, other) -> bool:
        if not self:
            return False
        if not other:
            return False
        return self.id == other.id

    def _update(self: S, **changes: ...) -> S:
        return replace(self, **changes)

    def as_role(self: S, role: type) -> R:
        if issubclass(self.__class__, role):
            raise TypeError('{ROLE} is not a {SUPER} role object..'.format(
                ROLE=role.__name__, SUPER=self.__class__.__name__))
        return role(**self.as_dict())

    def as_dict(self: S) -> dict:
        return asdict(self)


def entity(cls, /):
    return _process_class(cls=cls, init=True, repr=True, eq=False, order=False, unsafe_hash=False, frozen=True)


def value(cls, /):
    return _process_class(cls=cls, init=True, repr=True, eq=False, order=False, unsafe_hash=False, frozen=True)


@dataclass(frozen=True)
class Error(Exception):
    pass
