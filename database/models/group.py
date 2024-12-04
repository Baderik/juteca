from tortoise import fields

from database.models.core import AbstractBaseModel


class Group(AbstractBaseModel):
    name = fields.CharField(max_length=256)
    desc = fields.TextField(default="")
    owner = fields.ForeignKeyField("models.User", related_name="owned_groups")
    members = fields.ManyToManyField("models.User", related_name="groups")

    @property
    def head(self) -> str:
        return f"{self.name} #{self.id}"

    class Meta:
        table: str = 'groups'
