ubuntu@ip-172-31-23-109:~/flaskfullstack-tictactoe$ cat Dockerfile
FROM python:3.11-slim
WORKDIR /app
# System deps (NO mysql client needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x wait-for-it.sh

RUN addgroup --system appgroup && adduser --system --group appuser
USER appuser

EXPOSE 8000
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "wsgi:app"]