FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy Django project files
COPY . .

# Collect static files (won't fail build if not configured)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Start Django with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "news_project.wsgi:application"]