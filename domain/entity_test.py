from dataclasses import dataclass, FrozenInstanceError

from domain import entity
from dsl.type import ImmutableSequence


@dataclass(eq=False, frozen=True)
class EntityClass(entity.Entity):
    id: entity.ID
    value: str = ""

    def modify_value(self, value: str):
        processed_value = value
        return self._update(value=processed_value)


def test_create_instance():
    created_id = entity.generate_id()
    assert created_id == EntityClass(id=created_id, value="").id
    assert created_id == EntityClass(**{"id": created_id, "value": ""}).id


def test_equal():
    created_id = entity.generate_id()
    assert EntityClass(id=created_id, value="Self") != EntityClass(
        id=entity.generate_id(), value="Other")
    assert EntityClass(id=created_id, value="Origin") == EntityClass(
        id=created_id, value="Modified")


def test_do_not_allow_destructive_manipulation_of_the_field():
    try:
        crated_entity = EntityClass(id=entity.generate_id(), value="")
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
        _ = EntityClass(**{"id": 1, "value": "", "mutated": ""})
        assert False
    except TypeError:
        assert True


def test_create_and_return_a_new_instance_in_the_operation_method():
    created_entity = EntityClass(id=entity.generate_id(), value="")
    modified_entity = created_entity.modify_value(value="Modified!!")
    assert id(created_entity) != id(modified_entity)
    assert created_entity == modified_entity
    assert "Modified!!" == modified_entity.value


def test_export_dict():
    created_id = entity.generate_id()
    assert {"id": created_id, "value": ""} == EntityClass(
        id=created_id, value="").as_dict()
    assert {"id": created_id, "value": ""} == EntityClass(
        **{"id": created_id, "value": ""}).as_dict()


def test_role_object():
    @dataclass(eq=False, frozen=True)
    class Role(EntityClass):
        def role_method(self) -> entity.ID:
            return self.id

    created_id = entity.generate_id()
    created_entity = EntityClass(id=created_id, value="")
    roled_entity = created_entity.as_role(Role)
    assert created_entity is not roled_entity
    assert created_entity == roled_entity
    assert created_id == roled_entity.role_method()
    try:
        _ = created_entity.as_role(ImmutableSequence)
        assert False
    except TypeError:
        assert True
