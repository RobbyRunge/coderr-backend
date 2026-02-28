#!/bin/bash
# Dieses Script wird auf dem Hetzner-Server ausgeführt.
# Es kann auch manuell gestartet werden: bash deploy.sh

set -e

DEPLOY_PATH="/srv/coderr"   # <-- Pfad zum Projekt auf dem Server anpassen

echo "==> Pulling latest code..."
cd "$DEPLOY_PATH"
git pull origin main

echo "==> Building Docker images..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache

echo "==> Restarting containers..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans

echo "==> Cleaning up unused images..."
docker image prune -f

echo "==> Deployment complete!"
