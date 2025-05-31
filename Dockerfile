# syntax=docker/dockerfile:1
FROM python:3.11-slim

# 1. Install uv – you already do this
RUN pip install --no-cache-dir uv

# 2. Copy the project and install deps into .venv
WORKDIR /app
COPY . .
RUN uv sync              # creates .venv and installs everything

# 3. Make sure Railway can connect locally if you docker-run the image
EXPOSE 8000

# 4. Start Chainlit *inside* the venv
#    -h          → headless
#    --host 0.0.0.0 → bind all interfaces
#    --port ${PORT:-8000} → use Railway’s $PORT or 8000 locally
CMD ["sh", "-c", "uv run chainlit run main.py -h --host 0.0.0.0 --port ${PORT:-8000}"]
