import g4f

from src.enums import ModelNameEnum, RoleEnum
from src.models import Interaction

AI_CHAT_MODELS = {
    ModelNameEnum.GPT3_5: g4f.models.gpt_35_turbo,
    ModelNameEnum.GPT4: g4f.models.gpt_4,
}


async def get_response_from_ai_model(interaction: Interaction, content: str) -> str:
    """
    Generates a response baesd on interaction settings (Model and Initial prompt).

    It also includes the existing chat history of the interaction for a more specific response.
    """
    chat_history = [{"role": "system", "content": interaction.prompt}]
    chat_history += [
        {
            "role": "user" if msg.role == RoleEnum.HUMAN else "assistant",
            "content": msg.content,
        }
        async for msg in interaction.messages.all()
    ]

    response = await g4f.ChatCompletion.create_async(
        model=AI_CHAT_MODELS[interaction.ai_model_name],
        messages=chat_history + [{"role": "user", "content": content}],
    )
    return response
