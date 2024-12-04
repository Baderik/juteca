from tortoise import fields

from database.models.core import AbstractBaseModel
from database.models.group import Group
from database.models.event import Event


class User(AbstractBaseModel):
    telegram_id = fields.IntField()
    chat_id = fields.IntField(null=True)
    username = fields.CharField(max_length=32, null=True)
    owned_groups: fields.ReverseRelation[Group]
    groups: fields.ManyToManyRelation[Group]
    created_events: fields.ReverseRelation[Event]
    events: fields.ManyToManyRelation[Event]

    async def update_chat_data(self, chat_id: int, username: str) -> None:
        need_save = False
        if self.username != username:
            self.username = username
            need_save = True
        if self.chat_id != chat_id:
            self.chat_id = chat_id
            need_save = True

        if need_save:
            await self.save()

    @property
    def is_active(self) -> bool:
        return self.chat_id is not None

    @property
    def head(self) -> str:
        return f"{self.username} #{self.telegram_id}"
