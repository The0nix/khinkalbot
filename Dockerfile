FROM python:3.11-slim AS builder

RUN pip install --no-cache-dir "uv>=0.9.6,<0.10.0"

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Install dependencies first so this layer is cached until the lockfile changes
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY src ./src
RUN uv sync --locked --no-dev --no-editable


FROM python:3.11-slim

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

# The SQLite database (users_data.db) is created in the working directory
WORKDIR /data
VOLUME /data

ENTRYPOINT ["khinkalbot"]
CMD ["start"]
