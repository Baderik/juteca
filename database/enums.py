from enum import Enum


short_weekday = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
full_weekday = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье")


class WeekDay(int, Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

    @property
    def short_title(self):
        return short_weekday[self]

    @property
    def title(self):
        return full_weekday[self]

    @classmethod
    def by_day(cls, day):
        return cls(short_weekday.index(day))
