# Use an optimized, secure Python runtime footprint
FROM python:3.11-slim

WORKDIR /app

# Install system utilities needed for production packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Cache dependencies layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bring over source code and initialize directories
COPY src/ ./src/
RUN mkdir -p models

# Pre-train the model inside the build step so the asset is baked into the image layers
RUN python src/train.py

EXPOSE 8000

ENV ENV=production
ENV PYTHONUNBUFFERED=1

# Initialize web engine on startup
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]