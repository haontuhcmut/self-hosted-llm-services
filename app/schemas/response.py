from typing import Literal

from pydantic import BaseModel


class ChatCompletionMessage(BaseModel):
    role: Literal["assistant"]
    content: str | None = None


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatCompletionMessage
    finish_reason: str | None = None


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: Literal["chat.completion"]
    created: int
    model: str

    choices: list[ChatCompletionChoice]

    usage: Usage | None = None