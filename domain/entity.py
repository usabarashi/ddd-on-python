from abc import ABC, abstractmethod

from dataclasses import asdict, dataclass, replace
from typing import Any, Dict, Type, TypeVar

_S = TypeVar("_S")  # Self
_R = TypeVar("_R")  # Role


class Id(ABC):
    """Id
    """

    @abstractmethod
    def __eq__(self: _S, other: _S) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __ne__(self: _S, other: _S) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __lt__(self: _S, other: _S) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __le__(self: _S, other: _S) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __gt__(self: _S, other: _S) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __ge__(self: _S, other: _S) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def generate(cls: _S) -> _S:
        raise NotImplementedError


@dataclass(eq=False, frozen=True)
class Entity:
    id_: Id

    def __eq__(self: _S, other: _S) -> bool:
        return self.id_ == other.id_

    def __ne__(self: _S, other: _S) -> bool:
        return self.id_ != other.id_

    def __lt__(self: _S, other: _S) -> bool:
        return self.id_ < other.id_

    def __le__(self: _S, other: _S) -> bool:
        return self.id_ <= other.id_

    def __gt__(self: _S, other: _S) -> bool:
        return self.id_ > other.id_

    def __ge__(self: _S, other: _S) -> bool:
        return self.id_ >= other.id_

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
