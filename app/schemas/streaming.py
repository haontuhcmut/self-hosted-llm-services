from typing import Literal

from pydantic import BaseModel


class DeltaMessage(BaseModel):
    role: Literal["assistant"] | None = None
    content: str | None = None


class ChatCompletionChunkChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: str | None = None


class ChatCompletionChunk(BaseModel):
    id: str
    object: Literal["chat.completion.chunk"]
    created: int
    model: str

    choices: list[ChatCompletionChunkChoice]
