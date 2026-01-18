# ================================
# PaperBOT - Production Dockerfile
# ================================
# Compatible with: Docker, Railway, Render, Hugging Face Spaces
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory for user
WORKDIR $HOME/app

# Copy requirements first (for Docker cache optimization)
COPY --chown=user requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY --chown=user . .

# Create directories for uploads and data
RUN mkdir -p uploads data

# Expose port (7860 for HF Spaces, 8000 for others)
EXPOSE 7860 8000

# Run the application
CMD ["python", "app.py"]
