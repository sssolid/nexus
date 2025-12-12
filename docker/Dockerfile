FROM python:3.12-slim

# Environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

# Create app structure
RUN mkdir -p /app/src \
           /var/log/django \
           /app/staticfiles \
           /app/media

WORKDIR /app/src

# System dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc g++ build-essential \
    curl git \
    openjdk-21-jdk \
    libmagic1 \
    libjpeg-dev libpng-dev libwebp-dev \
    libxml2-dev libxslt1-dev \
    openssh-client \
    unixodbc unixodbc-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements/base.txt requirements/development.txt /app/requirements/
RUN pip install --upgrade pip && \
    pip install -r /app/requirements/development.txt

# Copy project
COPY . /app/src

# ------------------------------------------------------------
# Entrypoint (MUST be before USER switch)
# ------------------------------------------------------------
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create non-root user & permissions
RUN useradd -m -u 1000 django && \
    chown django:django /app && \
    chmod 755 /app && \
    chown -R django:django \
        /var/log/django \
        /app/staticfiles \
        /app/media \
        /app/entrypoint.sh

USER django

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
