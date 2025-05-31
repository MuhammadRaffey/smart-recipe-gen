# syntax=docker/dockerfile:1
FROM python:3.11-slim

RUN pip install --no-cache-dir uv

WORKDIR /app
COPY . .
RUN uv sync

# Expose default Chainlit port (for local docker use only)
EXPOSE 8000

CMD ["sh", "-c", "chainlit run main.py -h --host 0.0.0.0 --port ${PORT:-8000}"]
