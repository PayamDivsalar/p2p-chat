# Stage 1: Build stage - Install dependencies
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /build

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime stage - Lightweight production image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/
COPY .env.example .env

# Create directories for downloads and user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/downloads && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (configurable via .env)
EXPOSE 9000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run the application
CMD ["python", "src/main.py"]
