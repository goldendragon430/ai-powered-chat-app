# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401
from unittest import mock

from g4f import ChatCompletion
from httpx import AsyncClient
from tortoise.contrib import test

from src.enums import ModelNameEnum, RoleEnum
from src.main import app
from src.models import Interaction, Message


class InteractionTestCase(test.IsolatedTestCase):
    async def test_create_interaction(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/interactions",
                json={"model_name": "gpt3_5", "prompt": "My name is Shahriar"},
            )
        assert response.status_code == 200
        data = response.json()
        assert data["settings"]["model_name"] == "gpt3_5"
        assert data["settings"]["prompt"] == "My name is Shahriar"
        assert "id" in data
        interaction_id = data["id"]

        created_obj = await Interaction.get(id=interaction_id)
        assert created_obj.ai_model_name.value == "gpt3_5"
        assert created_obj.prompt == "My name is Shahriar"

    @mock.patch.object(ChatCompletion, "create_async")
    async def test_create_message(self, ai_response):
        ai_response.return_value = "Hello Shahriar. What can I do for you?"

        interaction = await Interaction.create(
            ai_model_name=ModelNameEnum.GPT4, prompt="My name is Shahriar"
        )

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                f"/interactions/{interaction.id}/messages", json={"content": "Hi"}
            )
        assert response.status_code == 200
        data = response.json()
        assert data["message"]["content"] == "Hi"
        assert data["message"]["role"] == "human"
        assert data["response"]["content"] == "Hello Shahriar. What can I do for you?"
        assert data["response"]["role"] == "ai"

        assert "id" in data["message"]
        assert "id" in data["response"]
        message_id = data["message"]["id"]
        response_id = data["response"]["id"]

        message_obj = await Message.get(id=message_id)
        assert message_obj.content == "Hi"
        assert message_obj.role == RoleEnum.HUMAN

        response_obj = await Message.get(id=response_id)
        assert response_obj.content == "Hello Shahriar. What can I do for you?"
        assert response_obj.role == RoleEnum.AI

    async def test_get_messages(self):
        interaction = await Interaction.create(
            ai_model_name=ModelNameEnum.GPT4, prompt="My name is Shahriar"
        )
        message1 = await Message.create(
            interaction=interaction,
            role=RoleEnum.HUMAN,
            content="Hi",
        )
        message2 = await Message.create(
            interaction=interaction,
            role=RoleEnum.AI,
            content="Hello there. How can I help you?",
        )

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/interactions/{interaction.id}/messages")
        assert response.status_code == 200
        data = response.json()

        assert data[0]["id"] == str(message1.id)
        assert data[0]["content"] == "Hi"
        assert data[0]["role"] == "human"

        assert data[1]["id"] == str(message2.id)
        assert data[1]["content"] == "Hello there. How can I help you?"
        assert data[1]["role"] == "ai"

    async def test_get_interactions(self):
        interaction1 = await Interaction.create(
            ai_model_name=ModelNameEnum.GPT4, prompt="Hello World"
        )
        interaction2 = await Interaction.create(
            ai_model_name=ModelNameEnum.GPT3_5, prompt="Act like a therapist"
        )
        message1 = await Message.create(
            interaction=interaction1,
            role=RoleEnum.HUMAN,
            content="Hi",
        )
        message2 = await Message.create(
            interaction=interaction1,
            role=RoleEnum.AI,
            content="Hello there. How can I help you?",
        )

        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/interactions")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        format_dt = lambda dt: dt.isoformat().replace("+00:00", "Z")
        self.maxDiff = None
        self.assertListEqual(
            data,
            [
                {
                    "id": str(interaction2.id),
                    "created_at": format_dt(interaction2.created_at),
                    "updated_at": format_dt(interaction2.updated_at),
                    "role": RoleEnum.SYSTEM.value,
                    "settings": {
                        "model_name": interaction2.ai_model_name.value,
                        "prompt": interaction2.prompt,
                    },
                    "messages": [],
                },
                {
                    "id": str(interaction1.id),
                    "created_at": format_dt(interaction1.created_at),
                    "updated_at": format_dt(interaction1.updated_at),
                    "role": RoleEnum.SYSTEM.value,
                    "settings": {
                        "model_name": interaction1.ai_model_name.value,
                        "prompt": interaction1.prompt,
                    },
                    "messages": [
                        {
                            "id": str(message1.id),
                            "role": message1.role.value,
                            "content": message1.content,
                            "created_at": format_dt(message1.created_at),
                        },
                        {
                            "id": str(message2.id),
                            "role": message2.role.value,
                            "content": message2.content,
                            "created_at": format_dt(message2.created_at),
                        },
                    ],
                },
            ],
        )
