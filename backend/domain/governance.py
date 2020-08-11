from enum import Enum
from datetime import datetime
from typing import Generic, TypeVar

import domain

_T = TypeVar('_T')


@domain.value
class BussinessDateTime(datetime):
    class WeekDay(Enum):
        MON = 0
        TUE = 1
        WEB = 2
        THU = 3
        FRI = 4
        SAT = 5
        SUN = 6

    def __init__(self, value):
        datetime.__init__(self, value)

    @property
    def fiscal_year(self) -> datetime.year:
        """会計年度"""
        raise NotImplementedError

    def is_bussiness_date(self) -> bool:
        """営業日か否かを判定する"""
        if self.weekday() == self.WeekDay.SAT:
            return False
        if self.weekday() == self.WeekDay.SUN:
            return False
        return True

    def is_bussiness_time(self) -> bool:
        """営業時間か否かを判定する"""
        raise NotImplementedError


class Duties(Enum):
    """業務分掌"""
    MANAGEMENT_DEPARTMENT = 0
    PLANNING_DEPARTMENT = 1
    MANUFACTURING_DEPARTMENT = 2
    SALES_DEPARTMENT = 3
