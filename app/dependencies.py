from fastapi import Request

from app.services.llama_service import LlamaCppService


def get_llama_service(
    request: Request,
) -> LlamaCppService:
    return request.app.state.llama_service
