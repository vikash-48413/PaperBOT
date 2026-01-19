# ================================
# PaperBOT - Production Dockerfile
# ================================
# Compatible with: Docker, Railway, Render, Hugging Face Spaces
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Hugging Face model cache directory (persisted in HF Spaces)
    HF_HOME=/home/user/.cache/huggingface \
    TRANSFORMERS_CACHE=/home/user/.cache/huggingface \
    # Use faster tokenizers
    TOKENIZERS_PARALLELISM=false

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory for user
WORKDIR $HOME/app

# Create cache directories with proper permissions
RUN mkdir -p /home/user/.cache/huggingface

# Copy requirements first (for Docker cache optimization)
COPY --chown=user requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Pre-download the embedding model during build to speed up startup
# This caches the model in the Docker image
ARG PRELOAD_MODEL=false
RUN if [ "$PRELOAD_MODEL" = "true" ]; then \
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-large-en-v1.5')" || true; \
    fi

# Copy application code
COPY --chown=user . .

# Create directories for uploads and data
RUN mkdir -p uploads data

# Expose port (7860 for HF Spaces, 8000 for others)
EXPOSE 7860 8000

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:7860/ping || curl -f http://localhost:8000/ping || exit 1

# Run the application
CMD ["python", "app.py"]
