from tortoise import fields
from tortoise.models import Model


class Code(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    language = fields.ForeignKeyField(
        'models.Language', on_delete=fields.CASCADE)
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE)
