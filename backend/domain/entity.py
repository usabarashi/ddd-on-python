from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, replace
from typing import Any, Dict, Type, TypeVar

_T = TypeVar("_T", covariant=True)


class Id(ABC):
    """Id
    """

    @abstractmethod
    def __eq__(self, other: Id) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __ne__(self, other: Id) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other: Id) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __le__(self, other: Id) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __gt__(self, other: Id) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __ge__(self, other: Id) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def generate(cls) -> Id:
        raise NotImplementedError


@dataclass(eq=False, frozen=True)
class Entity:
    id_: Id

    def __eq__(self, other: Entity) -> bool:
        return self.id_ == other.id_

    def __ne__(self, other: Entity) -> bool:
        return self.id_ != other.id_

    def __lt__(self, other: Entity) -> bool:
        return self.id_ < other.id_

    def __le__(self, other: Entity) -> bool:
        return self.id_ <= other.id_

    def __gt__(self, other: Entity) -> bool:
        return self.id_ > other.id_

    def __ge__(self, other: Entity) -> bool:
        return self.id_ >= other.id_

    def _update(self, **changes: Any):
        return replace(self, **changes)

    def as_role(self, role: Type[_T]) -> _T:
        if issubclass(self.__class__, role):
            raise TypeError(
                f"{role.__name__} is not a {self.__class__.__name__} role object."
            )
        return role(**self.as_dict())

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)
