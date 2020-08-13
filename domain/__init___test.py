from dataclasses import dataclass, FrozenInstanceError
from typing import Optional

import domain
from dsl.type import ImmutableSequence


@dataclass(eq=False, frozen=True)
class EntityClass(domain.Entity):
    value: str = ""

    def modify_value(self, value: str):
        processed_value = value
        return self._update(value=processed_value)


def test_create_instance():
    assert 1 == EntityClass(id_=1, value="").id_
    assert 1 == EntityClass(**{"id_": 1, "value": ""}).id_


def test_bool():
    assert True if EntityClass(id_=1, value="") else False
    assert False if EntityClass(id_=0, value="") else True
    assert False if EntityClass(id_=None, value="") else True


def test_equal():
    assert EntityClass(id_=1, value="Self") != EntityClass(id_=2, value="Other")
    assert EntityClass(id_=1, value="Origin") == EntityClass(id_=1, value="Modified")


def test_do_not_allow_destructive_manipulation_of_the_field():
    try:
        entity = EntityClass(id_=1, value="")
        entity.value = "Mutated!!"
        assert False
    except FrozenInstanceError:
        assert True
    # Syntax Error
    # try:
    #    _ = EntityClass(id_=1, value="", mutated="")
    #    assert False
    # except TypeError:
    #    assert True
    try:
        _ = EntityClass(**{"id_": 1, "value": "", "mutated": ""})
        assert False
    except TypeError:
        assert True


def test_create_and_return_a_new_instance_in_the_operation_method():
    entity = EntityClass(id_=1, value="")
    modified_entity = entity.modify_value(value="Modified!!")
    assert id(entity) != id(modified_entity)
    assert entity == modified_entity
    assert "Modified!!" == modified_entity.value


def test_export_dict():
    assert {"id_": 1, "value": ""} == EntityClass(id_=1, value="").as_dict()
    assert {"id_": 1, "value": ""} == EntityClass(**{"id_": 1, "value": ""}).as_dict()


def test_role_object():
    @dataclass(eq=False, frozen=True)
    class Role(EntityClass):
        def role_method(self) -> Optional[int]:
            return self.id_

    entity = EntityClass(id_=1, value="")
    roled_entity = entity.as_role(Role)
    assert entity is not roled_entity
    assert entity == roled_entity
    assert 1 == roled_entity.role_method()
    try:
        _ = entity.as_role(ImmutableSequence)
        assert False
    except TypeError:
        assert True
