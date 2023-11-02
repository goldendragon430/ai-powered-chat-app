# pylint: disable=E0611,E0401
from uuid import UUID

from fastapi import FastAPI
from starlette.exceptions import HTTPException
from tortoise.contrib.fastapi import register_tortoise
from tortoise.query_utils import Prefetch

from src import settings
from src.enums import RoleEnum
from src.models import Interaction, Message
from src.schemas import (
    InteractionSchemaIn,
    InteractionSchemaOut,
    MessageResponseSchemaOut,
    MessageSchemaIn,
    MessageSchemaOut,
    SimpleInteractionSchemaOut,
)
from src.utils import get_response_from_ai_model

app = FastAPI(title="AI-Powered Chat Application")


@app.get("/interactions")
async def get_interactions() -> list[InteractionSchemaOut]:
    """
    Get a list of all interaction that includes the messages.
    """
    return await InteractionSchemaOut.serialize_queryset(
        Interaction.all().prefetch_related(Prefetch("messages", queryset=Message.all()))
    )


@app.post("/interactions")
async def create_interaction(
    interaction: InteractionSchemaIn,
) -> SimpleInteractionSchemaOut:
    """
    Create a new interaction with the specified model name and initial prompt (instructions)

    The model name could be one of the *ModelNameEnum* items.
    """
    interaction_obj = await Interaction.create(
        **interaction.model_dump(exclude_unset=True)
    )
    return await SimpleInteractionSchemaOut.serialize_obj(interaction_obj)


@app.get("/interactions/{interaction_id}/messages")
async def get_messages(interaction_id: UUID) -> list[MessageSchemaOut]:
    """
    Get all the messages of an interaction.
    """
    interaction_obj = await Interaction.get_or_none(id=interaction_id)
    if not interaction_obj:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return await MessageSchemaOut.serialize_queryset(interaction_obj.messages.all())


@app.post("/interactions/{interaction_id}/messages")
async def create_message(
    interaction_id: UUID, message: MessageSchemaIn
) -> MessageResponseSchemaOut:
    """
    Create a new message inside the interaction.

    The original message and the respone which is gerenated by the AI will be returned.
    """
    interaction_obj = await Interaction.get_or_none(id=interaction_id)
    if not interaction_obj:
        raise HTTPException(status_code=404, detail="Interaction not found")

    response = await get_response_from_ai_model(
        interaction=interaction_obj, content=message.content
    )

    message_obj = await Message.create(
        interaction_id=interaction_id, **message.model_dump(exclude_unset=True)
    )
    response_obj = await Message.create(
        interaction_id=interaction_id,
        role=RoleEnum.AI,
        content=response,
    )

    return MessageResponseSchemaOut(
        message=await MessageSchemaOut.serialize_obj(message_obj),
        response=await MessageSchemaOut.serialize_obj(response_obj),
    )


register_tortoise(
    app,
    settings.TORTOISE_ORM,
    add_exception_handlers=True,
)
