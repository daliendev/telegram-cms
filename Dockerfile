FROM python:3.12.4-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

ENV PIPENV_VENV_IN_PROJECT=1 \
    PIPENV_CUSTOM_VENV_NAME=.venv
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install
FROM python:3.12.4-slim-bookworm
WORKDIR /app
COPY --from=builder /app/.venv .venv/
COPY . .
EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
