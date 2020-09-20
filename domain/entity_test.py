from dataclasses import FrozenInstanceError, dataclass
from typing import TypeVar

from domain import entity
from dsl.type import ImmutableSequence

_S = TypeVar("_S")


class IdMock(entity.Id, str):
    def __init__(self: _S, value: str) -> _S:
        str.__init__(value)

    def __eq__(self: _S, other: _S) -> bool:
        return str(self) == str(other)

    def __ne__(self: _S, other: _S) -> bool:
        return str(self) != str(other)

    def __lt__(self: _S, other: _S) -> bool:
        return str(self) < str(other)

    def __le__(self: _S, other: _S) -> bool:
        return str(self) <= str(other)

    def __gt__(self: _S, other: _S) -> bool:
        return str(self) > str(other)

    def __ge__(self: _S, other: _S) -> bool:
        return str(self) >= str(other)

    @classmethod
    def generate(cls):
        return __class__("test")


@dataclass(eq=False, frozen=True)
class EntityClass(entity.Entity):
    id_: entity.Id
    value: str = ""

    def modify_value(self, value: str):
        processed_value = value
        return self._update(value=processed_value)


def test_create_instance():
    created_id = IdMock("create")
    assert created_id == EntityClass(id_=created_id, value="").id_
    assert created_id == EntityClass(**{"id_": created_id, "value": ""}).id_


def test_equal():
    created_id = IdMock("create")
    assert created_id == IdMock("create")
    assert EntityClass(id_=created_id, value="Self") != EntityClass(
        id_=IdMock("other"), value="Other"
    )
    assert EntityClass(id_=created_id, value="Origin") == EntityClass(
        id_=created_id, value="Modified"
    )


def test_do_not_allow_destructive_manipulation_of_the_field():
    try:
        crated_entity = EntityClass(id_=IdMock("create"), value="")
        crated_entity.value = "Mutated!!"
        assert False
    except FrozenInstanceError:
        assert True
    # Syntax Error
    # try:
    #    _ = EntityClass(id=1, value="", mutated="")
    #    assert False
    # except TypeError:
    #    assert True
    try:
        _ = EntityClass(**{"id_": 1, "value": "", "mutated": ""})
        assert False
    except TypeError:
        assert True


def test_create_and_return_a_new_instance_in_the_operation_method():
    created_entity = EntityClass(IdMock("create"), value="")
    modified_entity = created_entity.modify_value(value="Modified!!")
    assert id(created_entity) != id(modified_entity)
    assert created_entity == modified_entity
    assert "Modified!!" == modified_entity.value


def test_export_dict():
    created_id = IdMock("create")
    assert {"id_": created_id, "value": ""} == EntityClass(
        id_=created_id, value=""
    ).as_dict()
    assert EntityClass(**{"id_": created_id, "value": ""}) == EntityClass(
        id_=created_id, value=""
    )


def test_role_object():
    @dataclass(eq=False, frozen=True)
    class Role(EntityClass):
        def role_method(self) -> entity.Id:
            return self.id_

    created_id = IdMock("create")
    created_entity = EntityClass(id_=created_id, value="")
    roled_entity = created_entity.as_role(Role)
    assert created_entity is not roled_entity
    assert created_entity == roled_entity
    assert created_id == roled_entity.role_method()
    try:
        _ = created_entity.as_role(ImmutableSequence)
        assert False
    except TypeError:
        assert True
