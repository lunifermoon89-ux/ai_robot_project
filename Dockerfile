FROM python:3.12-slim

WORKDIR /app

# Install build dependencies needed for numpy/statsmodels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app

# Build-time model generation: run the training script to produce
# `traffic_predictor_model.pkl` inside the image so the runtime can
# load it without requiring the model to be generated at container start.
RUN python train_model_h.py

EXPOSE 8080

# Use gunicorn for production
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080", "--workers", "2"]
