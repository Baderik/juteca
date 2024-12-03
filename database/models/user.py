from tortoise import fields

from database.models.core import AbstractBaseModel
from database.models.group import Group


class User(AbstractBaseModel):
    telegram_id = fields.IntField()
    chat_id = fields.IntField(null=True)
    username = fields.CharField(max_length=32, null=True)
    owned_groups: fields.ReverseRelation[Group]
    groups: fields.ManyToManyRelation[Group]

    async def update_chat_data(self, chat_id: int, username: str):
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
    def is_active(self):
        return self.chat_id is not None
