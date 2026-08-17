from fastapi import FastAPI

from app.middleware import register_middleware

app = FastAPI(
    title="Self-hosted LLM services",
    description="Self-hosted LLM services",
    version="0.0.1",
    openapi_url="/openapi.json",
    docs_url_prefix="/docs",
    redoc_url_prefix="/redoc",
)

# Add middleware
register_middleware(app)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
