#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

if [ "${MIGRATE:-true}" = "false" ]; then
  echo "MIGRATE=false, skipping init (migrate/collectstatic/setup/bootstrap)."
  exec "$@"
fi

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run setup pages ON FIRST SUCCESSFUL RUN ONLY
if [ ! -f /app/.pages_setup_done ]; then
  echo "Running setup_pages..."
  python manage.py setup_pages
  touch /app/.pages_setup_done
fi

if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.development" ]; then
  echo "Running bootstrap_dev..."
  python manage.py bootstrap_dev
fi

echo "Starting service..."
exec "$@"
