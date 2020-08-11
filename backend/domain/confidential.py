from functools import reduce
from typing import Generic, TypeVar

import domain
from domain import employee, governance
from dsl.type import ImmutableSequence, Result

_T = TypeVar('_T')


@domain.entity
class Confidential(Generic[_T]):
    """機密"""
    value: _T
    viewable_duties: ImmutableSequence[governance.Duties]

    def visible(self, duties: ImmutableSequence[governance.Duties]) -> bool:
        """閲覧可否を判定する"""
        return reduce(
            function=lambda left, right: left or right,
            sequence=(viewer_duties in self.viewable_duties
                      for viewer_duties in duties),
            initial=False
        )

    def get(self, duties: ImmutableSequence[governance.Duties]) -> _T:
        """閲覧する"""
        if self.visible(duties=duties):
            return self.value
        raise PermissionError


class Error(domain.Error):
    pass


class ConfidentialPermissionError(Error):
    """職務権限エラー"""
    pass


class ViewerRole(employee.Employee):
    """閲覧者"""

    def view(self, confidential: Confidential[_T]) -> Result[ConfidentialPermissionError, _T]:
        """閲覧する"""
        if confidential.visible(duties=self.duties):
            return confidential.get(duties=self.duties)
        else:
            return ConfidentialPermissionError