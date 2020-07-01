from domain.type import Err, Literal, Ok, Result


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
