from dataclasses import asdict, dataclass, replace
from typing import Any, Dict, Type, TypeVar

import ulid

_S = TypeVar("_S")  # Self
_R = TypeVar("_R")  # Role


class ID(str):

    def __init__(self: _S, value: str) -> _S:
        ulid.from_str(value)  # Validation
        str.__init__(value)

    def __eq__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) == ulid.from_str(other)

    def __ne__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) != ulid.from_str(other)

    def __hash__(self: _S) -> int:
        return hash(ulid.from_str(self))

    def __lt__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) < ulid.from_str(other)

    def __le__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) <= ulid.from_str(other)

    def __gt__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) > ulid.from_str(other)

    def __ge__(self: _S, other: _S) -> bool:
        return ulid.from_str(self) >= ulid.from_str(other)


def generate_id() -> ID:
    return ID(ulid.new().str)


@dataclass(eq=False, frozen=True)
class Entity:
    # id: ID = field(default=generate_id())

    def __eq__(self: _S, other: _S) -> bool:
        return ulid.from_str(self.id) == ulid.from_str(other.id)

    def __ne__(self: _S, other: _S) -> bool:
        return ulid.from_str(self.id) != ulid.from_str(other.id)

    def __hash__(self: _S) -> int:
        return hash(ulid.from_str(self))

    def __lt__(self: _S, other: _S) -> bool:
        return ulid.from_str(self.id) < ulid.from_str(other.id)

    def __le__(self: _S, other: _S) -> bool:
        return ulid.from_str(self.id) <= ulid.from_str(other.id)

    def __gt__(self: _S, other: _S) -> bool:
        return ulid.from_str(self.id) > ulid.from_str(other.id)

    def __ge__(self: _S, other: _S) -> bool:
        return ulid.from_str(self.id) >= ulid.from_str(other.id)

    def _update(self: _S, **changes: ...) -> _S:
        return replace(self, **changes)

    def as_role(self: _S, role: Type[_R]) -> _R:
        if issubclass(self.__class__, role):
            raise TypeError(
                f"{role.__name__} is not a {self.__class__.__name__} role object."
            )
        return role(**self.as_dict())

    def as_dict(self: _S) -> Dict[str, Any]:
        return asdict(self)
