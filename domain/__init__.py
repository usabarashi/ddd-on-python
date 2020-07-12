from dataclasses import asdict, dataclass, field, replace, _process_class
from typing import Optional, TypeVar

_S = TypeVar('_S')  # Self
_R = TypeVar('_R')  # Role
Id = int


@dataclass(frozen=True)
class Entity:
    id: Optional[Id] = field(default=None)

    def __bool__(self: _S) -> bool:
        return self.id is not None and self.id > 0

    def __eq__(self: _S, other) -> bool:
        if not self:
            return False
        if not other:
            return False
        return self.id == other.id

    def _update(self: _S, **changes: ...) -> _S:
        return replace(self, **changes)

    def as_role(self: _S, role: type) -> _R:
        if issubclass(self.__class__, role):
            raise TypeError(
                f'{role.__name__} is not a {self.__class__.__name__} role object.')
        return role(**self.as_dict())

    def as_dict(self: _S) -> dict:
        return asdict(self)


def entity(cls, /):
    return _process_class(cls=cls, init=True,
                          repr=True, eq=False, order=False, unsafe_hash=False, frozen=True)


def value(cls, /):
    return _process_class(cls=cls, init=True,
                          repr=True, eq=False, order=False, unsafe_hash=False, frozen=True)


class Error(Exception):
    pass
