from fastapi import FastAPI

from app.api.v1.chat import router as chat_router
from app.lifespan import lifespan
from app.middleware import register_middleware

app = FastAPI(
    title="Self-hosted LLM services",
    description="Self-hosted LLM services",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url_prefix="/docs",
    redoc_url_prefix="/redoc",
    lifespan=lifespan,
)

# Add middleware
register_middleware(app)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


app.include_router(
    chat_router,
    prefix="/v1",
    tags=["chat"],
)
