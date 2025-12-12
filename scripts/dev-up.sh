#!/usr/bin/env bash
set -euo pipefail

export ENV_FILE=".env.development"

docker compose \
  -f docker-compose.yml \
  -f docker-compose.dev.yml \
  up "$@"
