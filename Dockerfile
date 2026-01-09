FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user (security)
RUN addgroup --system appgroup && adduser --system --group appuser
USER appuser

# Expose app port
EXPOSE 8000

# Run using gunicorn
CMD ["gunicorn", "--workers", "3", "--timeout", "120", "--bind", "0.0.0.0:8000", "wsgi:app"]
