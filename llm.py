from typing import Any

from crewai import BaseLLM
from groq import Groq

from config import MODEL_NAME, get_groq_api_key


class GroqCrewLLM(BaseLLM):
    """
    CrewAI-native adapter around the official Groq Python SDK.

    CrewAI remains responsible for agents, tasks, context passing, and
    sequential orchestration. Groq provides the actual LLM inference.
    """

    def __init__(
        self,
        model: str = MODEL_NAME,
        temperature: float = 0.2,
    ):
        super().__init__(model=model, temperature=temperature)
        self.client = Groq(api_key=get_groq_api_key())

    def call(
        self,
        messages: Any,
        tools: list[dict] | None = None,
        callbacks: list[Any] | None = None,
        available_functions: dict[str, Any] | None = None,
        from_task: Any | None = None,
        from_agent: Any | None = None,
        response_model: Any | None = None,
    ) -> str:
        normalized_messages = []

        if isinstance(messages, str):
            normalized_messages = [{"role": "user", "content": messages}]
        elif isinstance(messages, list):
            for message in messages:
                if isinstance(message, dict):
                    role = message.get("role", "user")
                    content = message.get("content", "")
                else:
                    role = getattr(message, "role", "user")
                    content = getattr(message, "content", "")

                normalized_messages.append(
                    {
                        "role": str(role),
                        "content": str(content),
                    }
                )
        else:
            normalized_messages = [
                {"role": "user", "content": str(messages)}
            ]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=normalized_messages,
            temperature=self.temperature,
            max_tokens=3000,
        )

        content = completion.choices[0].message.content or ""

        if response_model is not None:
            try:
                return response_model.model_validate_json(content)
            except Exception:
                return content

        return content
