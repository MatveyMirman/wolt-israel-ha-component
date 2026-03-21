#!/bin/bash
set -e

cd /workspaces/wolt-isr-ha

if [ "$1" = "-f" ]; then
    echo "==> Tailing Home Assistant logs (follow mode)..."
    docker compose -f .devcontainer/docker-compose.yml logs -f homeassistant
else
    echo "==> Last 50 lines of Home Assistant logs:"
    docker compose -f .devcontainer/docker-compose.yml logs --tail=50 homeassistant
fi
