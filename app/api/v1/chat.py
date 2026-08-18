from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies import get_llama_service
from app.schemas.request import ChatCompletionRequest
from app.schemas.response import ChatCompletionResponse
from app.services.llama_service import LlamaCppService

router = APIRouter()


@router.post(
    "/chat/completions",
    response_model=ChatCompletionResponse,
)
async def chat_completion(
    request: ChatCompletionRequest,
    service: Annotated[
        LlamaCppService,
        Depends(get_llama_service),
    ],
) -> ChatCompletionResponse:
    request.stream = False

    return await service.chat(request)


@router.post("/chat/completions/stream")
async def chat_completion_stream(
    request: ChatCompletionRequest,
    service: Annotated[
        LlamaCppService,
        Depends(get_llama_service),
    ],
) -> StreamingResponse:
    request.stream = True

    return StreamingResponse(
        service.stream_chat(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
