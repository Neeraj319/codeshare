from tortoise import fields
from tortoise.models import Model
from auth.models import User


class Language(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Code(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', on_delete=fields.CASCADE)
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)
