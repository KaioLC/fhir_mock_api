FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock* ./

RUN uv pip install --system --no-cache -r pyproject.toml

COPY . .

EXPOSE 9123

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9123"]
