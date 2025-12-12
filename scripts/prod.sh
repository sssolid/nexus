#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f ".env.production" ]]; then
  echo "ERROR: .env.production not found"
  exit 1
fi

read -p "Start PRODUCTION containers? (yes/no): " confirm
if [[ "$confirm" != "yes" ]]; then
  echo "Aborted."
  exit 1
fi

echo "======================================"
echo "Starting Crown Nexus (PRODUCTION)"
echo "======================================"

export ENV_FILE=".env.production"

docker compose \
  -f docker-compose.yml \
  -f docker-compose.prod.yml \
  up "$@"
