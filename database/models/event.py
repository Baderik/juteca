from tortoise import fields

from database.models.core import AbstractBaseModel
from database.enums import WeekDay


class Event(AbstractBaseModel):
    author = fields.ForeignKeyField("models.User", related_name="created_events")
    title = fields.CharField(max_length=256)
    week_day = fields.IntEnumField(WeekDay)
    time = fields.TimeField()
    groups = fields.ManyToManyField("models.Group", related_name="events")
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "events"

    @property
    def head(self) -> str:
        return f"{self.title} #{self.id}"
