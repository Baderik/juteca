from enum import Enum


weekday_str = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")


class WeekDay(int, Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

    @property
    def title(self):
        return weekday_str[self]

    @classmethod
    def by_day(cls, day):
        return cls(weekday_str.index(day))
