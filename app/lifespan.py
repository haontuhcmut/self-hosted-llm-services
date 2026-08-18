from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.config import settings
from app.services.llama_service import LlamaCppService


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = httpx.AsyncClient(
        timeout=None,
    )

    app.state.llama_service = LlamaCppService(
        base_url=settings.LLAMA_URL,
        client=client,
    )

    yield

    await client.aclose()
