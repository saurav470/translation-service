
# FROM python:3.11-slim as base
FROM public.ecr.aws/docker/library/python:3.11-slim as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install uv


WORKDIR /app


COPY pyproject.toml uv.lock ./


RUN uv sync --frozen


COPY . .


RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app


EXPOSE 8000


CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


