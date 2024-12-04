from tortoise import Model, fields
from abc import abstractmethod


class AbstractBaseModel(Model):
    id = fields.IntField(pk=True)

    @property
    @abstractmethod
    def head(self) -> str:
        pass

    class Meta:
        abstract = True
