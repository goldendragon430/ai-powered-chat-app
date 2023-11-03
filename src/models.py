from tortoise import fields, models

from src.enums import ModelNameEnum, RoleEnum


class Interaction(models.Model):
    id = fields.UUIDField(pk=True)
    ai_model_name = fields.CharEnumField(ModelNameEnum)
    prompt = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    messages: fields.ReverseRelation["Message"]

    class Meta:
        table = "interactions"
        ordering = ["-created_at", "-updated_at"]


class Message(models.Model):
    id = fields.UUIDField(pk=True)
    interaction: fields.ForeignKeyRelation[Interaction] = fields.ForeignKeyField(
        model_name="models.Interaction", related_name="messages"
    )
    role = fields.CharEnumField(RoleEnum, default=RoleEnum.HUMAN)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "messages"
