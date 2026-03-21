#!/bin/bash
set -e

cd /workspaces/wolt-isr-ha

echo "==> Starting Home Assistant container..."
docker compose -f .devcontainer/docker-compose.yml up -d homeassistant

echo "==> Waiting for Home Assistant to be ready..."
sleep 5

# Wait for HA to respond
for i in {1..30}; do
    if curl -sf http://localhost:8123/manifest.json > /dev/null 2>&1; then
        echo "==> Home Assistant is ready at http://localhost:8123"
        exit 0
    fi
    echo "    Waiting... ($i/30)"
    sleep 5
done

echo "==> WARNING: Home Assistant may not be ready yet. Check logs with: ./scripts/logs-ha.sh"
