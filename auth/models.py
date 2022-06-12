from tortoise.models import Model
from tortoise import fields


class User(Model):
    """
    user model
    """

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=400)
    is_admin = fields.BooleanField(default=False)
    profile_picture = fields.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return self.username
