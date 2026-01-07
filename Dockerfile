# 1️⃣ Base image
FROM python:3.11-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install system dependencies (optional but safe)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copy requirements first (layer caching)
COPY requirements.txt .

# 5️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy application code
COPY . .

# 7️⃣ Expose Flask port
EXPOSE 8000

# 8️⃣ Run app with Gunicorn (IMPORTANT)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
