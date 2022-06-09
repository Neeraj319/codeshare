from tortoise import fields
from tortoise.models import Model


class Language(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name
