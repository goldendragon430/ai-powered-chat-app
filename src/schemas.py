from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.enums import ModelNameEnum, RoleEnum
from src.models import Message


class MessageSchemaIn(BaseModel):
    content: str


class MessageSchemaOut(BaseModel):
    id: UUID
    created_at: datetime
    role: RoleEnum
    content: str

    @classmethod
    async def serialize_obj(cls, obj: Message) -> "MessageSchemaOut":
        """Serialize a single message object into a MessageSchemaOut"""
        return MessageSchemaOut(
            id=obj.id,
            created_at=obj.created_at,
            role=obj.role,
            content=obj.content,
        )

    @classmethod
    async def serialize_queryset(cls, queryset) -> list["MessageSchemaOut"]:
        """Serialize a message queryset into a list of MessageSchemaOut"""
        return [await cls.serialize_obj(obj) async for obj in queryset]


class MessageResponseSchemaOut(BaseModel):
    message: MessageSchemaOut
    response: MessageSchemaOut


class InteractionSchemaIn(BaseModel):
    ai_model_name: ModelNameEnum = Field(alias="model_name")
    prompt: str


class InteractionSettings(BaseModel):
    ai_model_name: ModelNameEnum = Field(alias="model_name")
    prompt: str


class SimpleInteractionSchemaOut(BaseModel):
    id: UUID
    created_at: datetime
    role: RoleEnum = RoleEnum.SYSTEM
    settings: InteractionSettings

    @classmethod
    async def serialize_obj(cls, obj) -> "SimpleInteractionSchemaOut":
        """Serialize a single interaction object into a SimpleInteractionSchemaOut"""
        return SimpleInteractionSchemaOut(
            id=obj.id,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            settings=InteractionSettings(
                model_name=obj.ai_model_name, prompt=obj.prompt
            ),
        )


class InteractionSchemaOut(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    role: RoleEnum = RoleEnum.SYSTEM
    settings: InteractionSettings
    messages: list[MessageSchemaOut]

    @classmethod
    async def serialize_queryset(cls, queryset) -> list["InteractionSchemaOut"]:
        """
        Serialize a interaction queryset into a list of InteractionSchemaOut

        Each item includes the list of related messages.
        """
        return [
            InteractionSchemaOut(
                id=obj.id,
                created_at=obj.created_at,
                updated_at=obj.updated_at,
                settings=InteractionSettings(
                    model_name=obj.ai_model_name, prompt=obj.prompt
                ),
                messages=[
                    await MessageSchemaOut.serialize_obj(msg) for msg in obj.messages
                ],
            )
            async for obj in queryset
        ]
