from dataclasses import asdict, dataclass, field, replace
from typing import Optional, Type, TypeVar

_S = TypeVar("_S")  # Self
_R = TypeVar("_R")  # Role
Id = int


@dataclass(eq=False, frozen=True)
class Entity:
    id_: Optional[Id] = field(default=None)

    def __bool__(self: _S) -> bool:
        return self.id_ is not None and self.id_ > 0

    def __eq__(self: _S, other) -> bool:
        if not self:
            return False
        if not other:
            return False
        return self.id_ == other.id_

    def _update(self: _S, **changes: ...) -> _S:
        return replace(self, **changes)

    def as_role(self: _S, role: Type[_R]) -> _R:
        if issubclass(self.__class__, role):
            raise TypeError(
                f"{role.__name__} is not a {self.__class__.__name__} role object."
            )
        return role(**self.as_dict())

    def as_dict(self: _S) -> dict:
        return asdict(self)


class Error(Exception):
    pass
