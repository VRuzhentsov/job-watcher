# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using UV
RUN uv sync --frozen

# Copy source code and migrations
COPY src/ ./src/
COPY migrations/ ./migrations/

# Copy and make entrypoint script executable
COPY docker/entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Install netcat for database readiness check
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

# Expose port 5000
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Set default environment variables
ENV FLASK_APP=src/app.py
ENV PYTHONPATH=/app

ENTRYPOINT ["./entrypoint.sh"]
