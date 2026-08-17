from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal[
        "system",
        "user",
        "assistant",
        "tool",
    ]
    content: str | None = None
    name: str | None = None
    tool_call_id: str | None = None


class ChatCompletionRequest(BaseModel):
    model: str

    messages: list[ChatMessage]

    stream: bool = False

    temperature: float | None = Field(
        default=None,
        ge=0,
        le=2,
    )

    top_p: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    max_tokens: int | None = Field(
        default=None,
        gt=0,
    )

    stop: str | list[str] | None = None

    seed: int | None = None

    frequency_penalty: float | None = Field(
        default=None,
        ge=-2,
        le=2,
    )

    presence_penalty: float | None = Field(
        default=None,
        ge=-2,
        le=2,
    )

    user: str | None = None
