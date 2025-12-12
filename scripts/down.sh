#!/usr/bin/env bash
set -euo pipefail

echo "======================================"
echo "Stopping Crown Nexus"
echo "======================================"

docker compose down
