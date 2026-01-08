FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (add/remove as needed for DB drivers)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       default-libmysqlclient-dev \
       gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first for better caching
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy app source
COPY . .

# Listen on port 8000 (gunicorn default below)
EXPOSE 8000

# Use gunicorn to serve the Flask app via the wsgi entrypoint
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
