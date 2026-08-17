from collections.abc import AsyncIterator
from typing import Protocol

from app.schemas.request import ChatCompletionRequest
from app.schemas.response import ChatCompletionResponse


class LLMService(Protocol):

    async def chat(
        self,
        request: ChatCompletionRequest,
    ) -> ChatCompletionResponse: ...

    async def stream_chat(
        self,
        request: ChatCompletionRequest,
    ) -> AsyncIterator[str]: ...
