import httpx
import pytest

from app.config import settings
from app.schemas.request import ChatCompletionRequest, ChatMessage
from app.schemas.response import ChatCompletionResponse
from app.services.llama_service import LlamaCppService


@pytest.mark.asyncio
async def test_chat():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert str(request.url) == (f"{settings.LLAMA_URL}/v1/chat/completions")

        return httpx.Response(
            status_code=200,
            json={
                "id": "chatcmpl-test",
                "object": "chat.completion",
                "created": 1755500000,
                "model": "test-model",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "Hello!",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 5,
                    "completion_tokens": 2,
                    "total_tokens": 7,
                },
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        service = LlamaCppService(
            base_url=settings.LLAMA_URL,
            client=client,
        )

        request = ChatCompletionRequest(
            model="test-model",
            messages=[
                ChatMessage(
                    role="user",
                    content="Hello",
                )
            ],
        )

        response = await service.chat(request)

    assert isinstance(response, ChatCompletionResponse)
    assert response.id == "chatcmpl-test"
    assert response.model == "test-model"
    assert response.choices[0].message.content == "Hello!"
    assert response.choices[0].finish_reason == "stop"


@pytest.mark.asyncio
async def test_stream_chat():
    sse_body = (
        'data: {"id":"chatcmpl-test","object":"chat.completion.chunk"}\n\n'
        'data: {"choices":[{"delta":{"content":"Hello"}}]}\n\n'
        'data: {"choices":[{"delta":{"content":" world"}}]}\n\n'
        "data: [DONE]\n\n"
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"

        return httpx.Response(
            status_code=200,
            headers={
                "content-type": "text/event-stream",
            },
            content=sse_body,
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        service = LlamaCppService(
            base_url="http://llama-service:8080",
            client=client,
        )

        request = ChatCompletionRequest(
            model="test-model",
            messages=[
                ChatMessage(
                    role="user",
                    content="Say hello",
                )
            ],
            stream=True,
        )

        chunks = []

        async for chunk in service.stream_chat(request):
            chunks.append(chunk)

    assert chunks == [
        'data: {"id":"chatcmpl-test","object":"chat.completion.chunk"}',
        'data: {"choices":[{"delta":{"content":"Hello"}}]}',
        'data: {"choices":[{"delta":{"content":" world"}}]}',
        "data: [DONE]",
    ]


@pytest.mark.asyncio
async def test_chat_raises_for_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=500,
            json={"error": "llama server error"},
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport) as client:
        service = LlamaCppService(
            base_url="http://llama-service:8080",
            client=client,
        )

        request = ChatCompletionRequest(
            model="test-model",
            messages=[
                ChatMessage(
                    role="user",
                    content="Hello",
                )
            ],
        )

        with pytest.raises(httpx.HTTPStatusError):
            await service.chat(request)
