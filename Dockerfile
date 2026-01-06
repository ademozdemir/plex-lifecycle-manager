FROM python:3.11-slim

LABEL maintainer="PlexLifecycle"
LABEL description="Smart Plex Lifecycle Manager with Web UI"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements_docker.txt .
RUN pip install --no-cache-dir -r requirements_docker.txt

# Copy application files
COPY app/ /app/
COPY config/ /config/
COPY reports/ /reports/

# Create necessary directories
RUN mkdir -p /config /reports /logs

# Expose web UI port
EXPOSE 8765

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8765/health')" || exit 1

# Run the application
CMD ["python", "web_ui.py"]
