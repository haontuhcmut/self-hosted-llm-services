import httpx

from app.schemas.request import ChatCompletionRequest
from app.schemas.response import ChatCompletionResponse


class LlamaCppService:

    def __init__(
        self,
        base_url: str,
        client: httpx.AsyncClient,
    ):
        self.base_url = base_url
        self.client = client

    async def chat(
        self,
        request: ChatCompletionRequest,
    ) -> ChatCompletionResponse:

        response = await self.client.post(
            f"{self.base_url}/v1/chat/completions",
            json=request.model_dump(exclude_none=True),
        )

        response.raise_for_status()

        return ChatCompletionResponse.model_validate(response.json())

    async def stream_chat(
        self,
        request: ChatCompletionRequest,
    ):
        payload = request.model_dump(exclude_none=True)

        async with self.client.stream(
            "POST",
            f"{self.base_url}/v1/chat/completions",
            json=payload,
        ) as response:

            response.raise_for_status()

            async for line in response.aiter_lines():

                if not line:
                    continue

                yield f"{line}\n\n"
        return StreamingResponse(
            service.stream_chat(request),
            media_type="text/event-stream",
        )