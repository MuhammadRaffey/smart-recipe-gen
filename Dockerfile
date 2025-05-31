# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Update system packages and install uv (fast Python package manager)
RUN apt-get update && apt-get upgrade -y \
    && pip install --no-cache-dir uv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Copy .env file if present (for local dev, override at runtime for prod)
COPY .env .env

# Expose default Chainlit port (change if needed)
EXPOSE 8000

# Set environment variables (optional, can be overridden at runtime)
# ENV OPENAI_API_KEY=your-key-here
# ENV GEMINI_API_KEY=your-gemini-api-key

# Default command
CMD ["uv", "run", "chainlit", "run", "./main.py", "-h"] 