import dataclasses
from typing import Optional

import domain
from dsl.type import ImmutableSequence


@domain.entity
class EntityClass(domain.Entity):
    value: str = ''

    def modify_value(self, value: str):
        processed_value = value
        return self._update(
            value=processed_value
        )


def test_create_instance():
    assert 1 == EntityClass(id=1, value='').id
    assert 1 == EntityClass(**{'id': 1, 'value': ''}).id


def test_bool():
    assert True if EntityClass(id=1, value='') else False
    assert False if EntityClass(id=0, value='') else True
    assert False if EntityClass(id=None, value='') else True


def test_equal():
    assert EntityClass(id=1, value='Self') != EntityClass(id=2, value='Other')
    assert EntityClass(id=1, value='Origin') == EntityClass(
        id=1, value='Modified')


def test_do_not_allow_destructive_manipulation_of_the_field():
    try:
        entity = EntityClass(id=1, value='')
        entity.value = 'Mutated!!'
        assert False
    except dataclasses.FrozenInstanceError:
        assert True
    try:
        _ = EntityClass(id=1, value='', mutated='')
        assert False
    except TypeError:
        assert True
    try:
        _ = EntityClass(**{'id': 1, 'value': '', 'mutated': ''})
        assert False
    except TypeError:
        assert True


def test_create_and_return_a_new_instance_in_the_operation_method():
    entity = EntityClass(id=1, value='')
    modified_entity = entity.modify_value(value='Modified!!')
    assert id(entity) != id(modified_entity)
    assert entity == modified_entity
    assert 'Modified!!' == modified_entity.value


def test_export_dict():
    assert {'id': 1, 'value': ''} == EntityClass(id=1, value='').as_dict()
    assert {'id': 1, 'value': ''} == EntityClass(
        **{'id': 1, 'value': ''}).as_dict()


def test_role_object():
    @domain.entity
    class Role(EntityClass):
        def role_method(self) -> Optional[int]:
            return self.id
    entity = EntityClass(id=1, value='')
    roled_entity = entity.as_role(Role)
    assert entity is not roled_entity
    assert entity == roled_entity
    assert 1 == roled_entity.role_method()
    try:
        _ = entity.as_role(ImmutableSequence)
        assert False
    except TypeError:
        assert True
