from typing import Literal

from dsl.type import Collection, Err, Ok, Result


def test_result_ok():
    def result(x) -> Result[Literal['Err'], Literal['Ok']]:
        return Ok('Ok') if x else Err('Err')
    assert result(True)
    assert type(result(True)) is Ok
    assert isinstance(result(True), Ok)
    assert result(True).value == 'Ok'


def test_result_err():
    def result(x) -> Result[Literal['Err'], Literal['Ok']]:
        return Ok('Ok') if x else Err('Err')
    assert not result(False)
    assert type(result(False)) is Err
    assert isinstance(result(False), Err)
    assert result(False).value == 'Err'


def test_collection():
    collection = Collection([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert type(collection) == Collection
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == collection


def test_collection_sort():
    collection = Collection([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    sorted_collection = collection.sort()
    assert id(sorted_collection) != id(collection)
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == sorted_collection
    sorted_collection = collection.sort(key=None)
    assert id(sorted_collection) != id(collection)
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == sorted_collection
    sorted_collection = collection.sort(key=lambda x: x)
    assert id(sorted_collection) != id(collection)
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == sorted_collection
    sorted_collection = collection.sort(reverse=False)
    assert id(sorted_collection) != id(collection)
    assert [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] == sorted_collection
    sorted_collection = collection.sort(reverse=True)
    assert id(sorted_collection) != id(collection)
    assert [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] == sorted_collection
    sorted_collection = collection.sort(key=lambda x: x, reverse=True)
    assert id(sorted_collection) != id(collection)
    assert [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] == sorted_collection


def test_collection_map():
    collection = Collection([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    mapped_collection = collection.map(function=lambda x: x * 2)
    assert id(mapped_collection) != id(collection)
    assert [0, 2, 4, 6, 8, 10, 12, 14, 16, 18] == mapped_collection


def test_collection_recude():
    collection = Collection([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    reduced_collection = collection.reduce(
        function=lambda left, right: left * right)
    assert id(reduced_collection) != id(collection)
    assert 0 == reduced_collection
