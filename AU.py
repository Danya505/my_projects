from uuid import UUID
from typing import Sequence


class PeriodActiveUsers:
    def __init__(self, accumulation_period: int) -> None:
        """
        Инициализирует объект для подсчета числа уникальных пользователей.

        Args:
            accumulation_period: период времени, для которого необходимо
            подсчитать число уникальных пользователей.

        Raises:
            TypeError, если accumulation_period не может быть округлено и
            использовано для получения целого числа.
            ValueError, если после округления accumulation_period - число,
            меньшее 1.
        """
        if not ((isinstance(accumulation_period, int)
                 or isinstance(accumulation_period, float))):
            raise TypeError
        self._accumulation_period = round(accumulation_period)
        if self._accumulation_period < 1:
            raise ValueError
        self._daily_users = []
        self._unique_users_amount = 0
        self._current_day = 0

    def add_active_users_for_curr_day(self, users: Sequence[UUID]) -> None:
        """
        Обновляет метрику на основании данных о посещении ресурса для текущего
        дня.

        Args:
            users: последовательность UUID пользователей, посетивших ресурс
                в данный день.
        """
        current_day_users = set(users)
        if self._current_day == self._accumulation_period:
            del self._daily_users[0]
            self._daily_users.append(current_day_users)
            self._current_day = self._accumulation_period
        else:
            self._current_day += 1
            self._daily_users.append(current_day_users)

    @property
    def unique_users_amount(self) -> int:
        """Число уникальных пользователей за последние accumulation_period
        дней."""
        if len(self._daily_users) != 0:
            return 0
        unique_users = set.union(*self._daily_users)
        self._unique_users_amount = len(unique_users)
        return self._unique_users_amount

    @property
    def accumulation_period(self) -> int:
        """Период расчета метрики: accumulation_period."""
        return self._accumulation_period
