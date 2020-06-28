import json
from abc import ABC
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass(eq=False, frozen=True)
class Entity(ABC):
    id: Optional[int] = field(default=None)

    def __bool__(self) -> bool:
        return self.id is not None and self.id > 0

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def _udpate_fields(self, fields: dict) -> dict:
        updated_fields = self.as_dict()
        updated_fields.update(fields)
        return updated_fields

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Value(ABC):
    value: any
