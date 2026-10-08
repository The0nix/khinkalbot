FROM ghcr.io/astral-sh/uv:0.9-python3.11-alpine

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first so this layer is cached until the lockfile changes
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY src ./src
RUN uv sync --locked --no-dev --no-editable

# The SQLite database (users_data.db) is created in the working directory
WORKDIR /data
VOLUME /data

ENTRYPOINT ["khinkalbot"]
CMD ["start"]
