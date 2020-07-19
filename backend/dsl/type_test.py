from dataclasses import asdict, dataclass, field
from typing import Generic, Literal, TypeVar

from dsl.type import Err, Ok, Result, ImmutableSequence

T = TypeVar('T')

# Result


def test_result_ok():
    def result(x) -> Result[Literal['Err'], Literal['Ok']]:
        return Ok('Ok') if x else Err('Err')
    assert result(True)
    assert Ok is type(result(True))
    assert isinstance(result(True), Ok)
    assert 'Ok' == result(True).value


def test_result_err():
    def result(x) -> Result[Literal['Err'], Literal['Ok']]:
        return Ok('Ok') if x else Err('Err')
    assert not result(False)
    assert Err is type(result(False))
    assert isinstance(result(False), Err)
    assert 'Err' == result(False).value


def test_result_fold():
    def result(x) -> Result[Literal['Err'], Literal['Ok']]:
        return Ok('Ok') if x else Err('Err')
    assert 'Ok' == result(True).fold(err=lambda x: None, ok=lambda x: x)
    assert 'Err' == result(False).fold(err=lambda x: x, ok=lambda x: None)

# ImmutableSequence


def test_immutable_sequence_init():
    assert [] == ImmutableSequence() == []
    assert [] == ImmutableSequence([]) == []
    assert [] == ImmutableSequence(()) == []
    assert [] == ImmutableSequence({}) == []
    sequence = ImmutableSequence([0, 1, 2])
    assert type(sequence) == ImmutableSequence
    assert 0 == sequence[0] == 0
    assert [0, 1, 2] == sequence == [0, 1, 2]
    assert (0, 1, 2) != sequence != (0, 1, 2)
    assert {0, 1, 2} != sequence != {0, 1, 2}
    assert [0, 2, 4] == ImmutableSequence(
        element * 2 for element in sequence) == [0, 2, 4]


def test_immutable_sequence_add():
    # immutable + mutalbe
    collection = ImmutableSequence([0, 1, 2])
    im_collection = collection + [3]
    assert im_collection is not collection
    assert type(im_collection) == ImmutableSequence
    assert [0, 1, 2, 3] == im_collection == [0, 1, 2, 3]
    assert [0, 1, 2] == collection == [0, 1, 2]
    assert im_collection != collection

    # immutable + immutable
    other_collection = ImmutableSequence([3, 4, 5])
    ii_collection = collection + other_collection
    assert ii_collection is not collection
    assert ii_collection is not other_collection
    assert type(ii_collection) == ImmutableSequence
    assert [0, 1, 2, 3, 4, 5] == ii_collection == [0, 1, 2, 3, 4, 5]
    assert [0, 1, 2] == collection == [0, 1, 2]
    assert [3, 4, 5] == other_collection == [3, 4, 5]
    assert ii_collection != collection
    assert ii_collection != other_collection


def test_immutable_sequence_add_warning_case():
    # mutable + immutable
    collection = ImmutableSequence([0, 1, 2])
    mi_collection = [3] + collection
    assert mi_collection is not collection
    assert type(mi_collection) != ImmutableSequence
    assert type(mi_collection) == list
    assert [3, 0, 1, 2] == mi_collection == [3, 0, 1, 2]
    assert [0, 1, 2] == collection == [0, 1, 2]
    assert mi_collection != [3]
    assert mi_collection != collection


def test_immutable_sequence_setitem():
    sequence = ImmutableSequence([0, 1, 2])
    try:
        sequence[1] = 9
        assert False
    except TypeError:
        assert True


def test_immutable_sequence_delitem():
    sequence = ImmutableSequence([0, 1, 2])
    try:
        del sequence[1]
        assert False
    except TypeError:
        assert True


def test_immutable_sequence_append():
    sequence = ImmutableSequence([0, 1, 2])
    appended_sequence = sequence.append(3)
    assert appended_sequence is not sequence
    assert type(appended_sequence) == ImmutableSequence
    assert type(sequence) == ImmutableSequence
    assert [0, 1, 2, 3] == appended_sequence == [0, 1, 2, 3]


def test_immutable_sequence_extend():
    sequence = ImmutableSequence([0, 1, 2])
    extend_sequence = [3, 4, 5]
    extended_sequence = sequence.extend(extend_sequence)
    assert extended_sequence is not sequence
    assert extended_sequence is not extend_sequence
    assert type(extended_sequence) == ImmutableSequence
    assert type(sequence) == ImmutableSequence
    assert [0, 1, 2, 3, 4, 5] == extended_sequence == [0, 1, 2, 3, 4, 5]


def test_immutable_sequence_insert():
    sequence = ImmutableSequence([0, 1, 2])
    inserted_sequence = sequence.insert(1, 9)
    assert inserted_sequence is not sequence
    assert type(inserted_sequence) == ImmutableSequence
    assert type(sequence) == ImmutableSequence
    assert [0, 9, 1, 2] == inserted_sequence == [0, 9, 1, 2]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_immutable_sequence_remove():
    sequence = ImmutableSequence([0, 1, 2])
    removed_sequence = sequence.remove(1)
    assert removed_sequence is not sequence
    assert type(removed_sequence) == ImmutableSequence
    assert type(sequence) == ImmutableSequence
    assert [0, 2] == removed_sequence == [0, 2]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_immutable_sequence_pop():
    sequence = ImmutableSequence([0, 1, 2])
    poped_sequence = sequence.pop(1)
    assert poped_sequence is not sequence
    assert type(poped_sequence) == ImmutableSequence
    assert type(sequence) == ImmutableSequence
    assert [0, 2] == poped_sequence == [0, 2]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_immutable_sequence_index():
    sequence = ImmutableSequence([0, 1, 2])
    index = sequence.index(1, 0, 2)
    assert type(sequence) == ImmutableSequence
    assert 1 == index
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_immutable_sequence_clear():
    sequence = ImmutableSequence([0, 1, 2])
    try:
        sequence.clear()
        assert False
    except TypeError:
        assert True


def test_immutable_sequence_count():
    sequence = ImmutableSequence([0, 1, 2])
    assert 1 == sequence.count(0)
    assert type(sequence)
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_immutable_sequence_sort():
    sequence = ImmutableSequence([0, 1, 2])
    sorted_sequence = sequence.sort(reverse=True)
    assert sorted_sequence is not sequence
    assert type(sorted_sequence) == ImmutableSequence
    assert type(sequence) == ImmutableSequence
    assert [2, 1, 0] == sorted_sequence == [2, 1, 0]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_immutable_sequence_reverse():
    sequence = ImmutableSequence([0, 1, 2])
    reversed_sequence = sequence.reverse()
    assert reversed_sequence is not sequence
    assert type(reversed_sequence) == ImmutableSequence
    assert type(sequence) == ImmutableSequence
    assert [2, 1, 0] == reversed_sequence == [2, 1, 0]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_immutable_sequence_copy():
    sequence = ImmutableSequence([0, 1, 2])
    copied_sequence = sequence.copy()
    assert copied_sequence is not sequence
    assert type(copied_sequence) == ImmutableSequence
    assert type(sequence) == ImmutableSequence
    assert copied_sequence == sequence == copied_sequence
    assert [0, 1, 2] == copied_sequence == [0, 1, 2]
    assert [0, 1, 2] == sequence == [0, 1, 2]


def test_immutable_sequence_empty():
    sequence = ImmutableSequence([0, 1, 2])
    assert False is sequence.is_empty()


def test_immutable_sequence_non_empty():
    sequence = ImmutableSequence([0, 1, 2])
    assert True is sequence.non_empty()


def test_immutable_sequence_size():
    sequence = ImmutableSequence([0, 1, 2])
    assert 3 == sequence.size()


def test_immutable_sequence_map():
    sequence = ImmutableSequence([0, 1, 2])
    mapped_sequence = sequence.map(function=lambda x: x * 2)
    assert mapped_sequence is not sequence
    assert [0, 2, 4] == mapped_sequence


def test_immutable_sequence_redece():
    sequence = ImmutableSequence([0, 1, 2])
    reduced_sequence = sequence\
        .reduce(function=lambda left, right: left * right)
    assert reduced_sequence is not sequence
    assert 0 == reduced_sequence


def test_immutable_sequence_dataclass():
    @dataclass(frozen=True)
    class SeqEntity(Generic[T]):
        value: ImmutableSequence[T] = field(default_factory=ImmutableSequence)
    entity = SeqEntity()
    dict_entity = asdict(entity)
    entity_from_dict = SeqEntity(**dict_entity)
    assert {'value': []} == dict_entity == {'value': []}
    assert entity_from_dict == entity == entity_from_dict
