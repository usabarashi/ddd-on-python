from typing import Awaitable, Callable, TypeVar

import command

_T = TypeVar("_T")


class TransactionTraitMock(command.TransactionTrait):
    @staticmethod
    async def transaction(
        function: Callable[..., Awaitable[_T]]
    ) -> Callable[..., Awaitable[_T]]:
        return function

    @staticmethod
    async def transaction_read_only(
        function: Callable[..., Awaitable[_T]]
    ) -> Callable[..., Awaitable[_T]]:
        return function
