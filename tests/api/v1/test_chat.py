import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.chat import router
from app.dependencies import get_llama_service
from app.services.llama_service import LlamaCppService


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()

    app.include_router(
        router,
        prefix="/v1",
    )

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture
def llama_service() -> LlamaCppService:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
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
    )

    client = httpx.AsyncClient(
        transport=transport,
    )

    return LlamaCppService(
        base_url="http://test-llama:8080",
        client=client,
    )


def test_chat_completion(
    client: TestClient,
    llama_service: LlamaCppService,
):
    client.app.dependency_overrides[get_llama_service] = lambda: llama_service

    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "test-model",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello",
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == "chatcmpl-test"
    assert data["object"] == "chat.completion"
    assert data["model"] == "test-model"
    assert data["choices"][0]["message"]["role"] == "assistant"
    assert data["choices"][0]["message"]["content"] == "Hello!"
    assert data["choices"][0]["finish_reason"] == "stop"
