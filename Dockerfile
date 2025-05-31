# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Install uv + project deps
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY . .
RUN uv sync

EXPOSE 8000         # only matters for local docker use

# ----  ⬇️  critical change  ⬇️  ----
# -h  : headless   --host 0.0.0.0 : bind to all IFs
# --port ${PORT:-8000} : use Railway’s $PORT if it exists, else 8000 (local)
CMD ["sh", "-c", "chainlit run main.py -h --host 0.0.0.0 --port ${PORT:-8000}"]
