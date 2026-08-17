FROM python:3.14-alpine

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY app ./app

RUN chmod +x /app/app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/app/entrypoint.sh"]