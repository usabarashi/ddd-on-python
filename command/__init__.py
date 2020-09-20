from typing import Awaitable, Callable, TypeVar

_T = TypeVar("_T")


async def transaction(
    function: Callable[..., Awaitable[_T]]
) -> Callable[..., Awaitable[_T]]:
    raise NotImplementedError


class TransactionTrait:
    @staticmethod
    async def transaction(
        function: Callable[..., Awaitable[_T]]
    ) -> Callable[..., Awaitable[_T]]:
        raise NotImplementedError

    @staticmethod
    async def transaction_read_only(
        function: Callable[..., Awaitable[_T]]
    ) -> Callable[..., Awaitable[_T]]:
        raise NotImplementedError
