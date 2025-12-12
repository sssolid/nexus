#!/bin/sh
set -e

: "${POSTGRES_HOST:?POSTGRES_HOST not set}"
: "${POSTGRES_PORT:?POSTGRES_PORT not set}"
: "${REDIS_HOST:?REDIS_HOST not set}"
: "${REDIS_PORT:?REDIS_PORT not set}"

: "${SERVICE_ROLE:=web}"   # default

wait_for_service() {
  HOST="$1"
  PORT="$2"
  NAME="$3"

  echo "Waiting for $NAME at $HOST:$PORT..."
  for i in $(seq 1 60); do
    nc -z "$HOST" "$PORT" && break
    sleep 1
  done
}

# ------------------------------------------------------------
# Wait for dependencies
# ------------------------------------------------------------

wait_for_service "$POSTGRES_HOST" "$POSTGRES_PORT" "PostgreSQL"
wait_for_service "$REDIS_HOST" "$REDIS_PORT" "Redis"

# ------------------------------------------------------------
# Non-web services wait for migrations
# ------------------------------------------------------------

if [ "$SERVICE_ROLE" != "web" ]; then
  echo "SERVICE_ROLE=$SERVICE_ROLE -> waiting for migrations..."
  for i in $(seq 1 60); do
    [ -f /app/.migrations_done ] && break
    sleep 1
  done
  exec "$@"
fi

# ------------------------------------------------------------
# Web-only init phase
# ------------------------------------------------------------

if [ "${MIGRATE:-true}" = "false" ]; then
  echo "MIGRATE=false, skipping init."
  exec "$@"
fi

echo "Applying database migrations..."
python manage.py migrate --noinput
touch /app/.migrations_done

echo "Collecting static files..."
python manage.py collectstatic --noinput

# ------------------------------------------------------------
# One-time setup
# ------------------------------------------------------------

if [ ! -f /app/.pages_setup_done ]; then
  echo "Running setup_pages..."
  python manage.py setup_pages
  touch /app/.pages_setup_done
fi

if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.development" ]; then
  echo "Running bootstrap_dev..."
  python manage.py bootstrap_dev
fi

# ------------------------------------------------------------
# Start process
# ------------------------------------------------------------

echo "Starting service..."
exec "$@"
