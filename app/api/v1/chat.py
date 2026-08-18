from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.schemas.request import ChatCompletionRequest
from app.services.llama_service import LlamaCppService

router = APIRouter()


def get_llama_service() -> LlamaCppService:
    return LlamaCppService(
        base_url="http://llama-service:8080",
        # client=...
    )


@router.post("/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
    service: Annotated[
        LlamaCppService,
        Depends(get_llama_service),
    ],
):
    if request.stream:
        return StreamingResponse(
            service.stream_chat(request),
            media_type="text/event-stream",
        )

    return await service.chat(request)