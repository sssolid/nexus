FROM python:3.12-slim

# Environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app structure
RUN mkdir -p /app/src \
           /var/log/django \
           /app/staticfiles \
           /app/media

# Set work directory
WORKDIR /app/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    g++ \
    build-essential \
    curl \
    git \
    libmagic1 \
    libjpeg-dev \
    libpng-dev \
    libwebp-dev \
    libxml2-dev \
    libxslt1-dev \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements/base.txt requirements/development.txt /app/requirements/
RUN pip install --upgrade pip && \
    pip install -r /app/requirements/development.txt

# Copy project
COPY . /app/src

# Create non-root user
RUN useradd -m -u 1000 django && \
    chown -R django:django /app /var/log/django

USER django

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
