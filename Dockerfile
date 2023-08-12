# Use a slim Python version for smaller image size
FROM python:3.11.4-slim

# Set environment variables
# Avoids .pyc files and ensures that Python output is sent straight to terminal without being buffered.
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

# Set working directory in the container
WORKDIR /app

# Install system dependencies
# These might change based on specific Python packages that require system-level dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application files to the container
COPY . /app/

CMD ["python", "run.py"]
