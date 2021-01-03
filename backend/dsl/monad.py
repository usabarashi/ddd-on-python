import dataclasses
from typing import Callable, Generic, Iterable, Optional, TypeVar

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class Option(Generic[T]):
    value: Optional[T]

    def is_normal(self) -> bool:
        return self.value is not None

    def is_abnormal(self) -> bool:
        return self.value is None


def do_option(generator: Callable[[], Iterable[Option]]):
    """do記法"""
    iterator = generator()

    def recur(iterator, prev):
        try:
            ma = iterator.send(prev)
        except StopIteration as last:
            return last.value
        done = True if ma == None else False

        def cb(a):
            if not done:
                return recur(iterator, a)
            else:
                return ma.__class__.pure(a)

        return ma.bind(cb)

    return


@do_option
def usecase():
    a = yield Option[int](1)
    b = yield Option[int](2)
    return a + b


print(usecase)
