#!/bin/bash
set -e

cd /workspaces/wolt-isr-ha
CONFIG_DIR="$(pwd)/config"

echo "==> Devcontainer post-create setup"

echo "==> Creating HACS custom_components directory..."
mkdir -p "$CONFIG_DIR/custom_components/hacs"

HACS_CUSTOM="$CONFIG_DIR/custom_components/hacs"

if [ ! -f "$HACS_CUSTOM/hacs.py" ]; then
    echo "==> Downloading HACS..."
    curl -sL https://get.hacs.xyz | bash -s -- --dir "$HACS_CUSTOM"
else
    echo "==> HACS already installed."
fi

echo "==> Creating HACS config..."
cat > "$CONFIG_DIR/hacs.cfg" << 'EOF'
# HACS Configuration
# https://github.com/hacs/integration

EOF

echo "==> Ensuring wolt symlink exists in config..."
mkdir -p "$CONFIG_DIR/custom_components"
if [ -d "$CONFIG_DIR/custom_components/wolt" ] && [ ! -L "$CONFIG_DIR/custom_components/wolt" ]; then
    rm -rf "$CONFIG_DIR/custom_components/wolt"
    ln -sf /workspaces/wolt-isr-ha/custom_components/wolt "$CONFIG_DIR/custom_components/wolt"
    echo "==> Replaced copy with symlink: custom_components/wolt -> /workspaces/wolt-isr-ha/custom_components/wolt"
elif [ ! -L "$CONFIG_DIR/custom_components/wolt" ]; then
    ln -sf /workspaces/wolt-isr-ha/custom_components/wolt "$CONFIG_DIR/custom_components/wolt"
    echo "==> Created symlink: custom_components/wolt -> /workspaces/wolt-isr-ha/custom_components/wolt"
else
    echo "==> Symlink already exists."
fi

echo "==> Ensuring configuration.yaml has homeassistant: key..."
if ! grep -q "^homeassistant:" "$CONFIG_DIR/configuration.yaml" 2>/dev/null; then
    echo "homeassistant:" >> "$CONFIG_DIR/configuration.yaml"
    echo "==> Added 'homeassistant:' to configuration.yaml"
else
    echo "==> 'homeassistant:' already present in configuration.yaml"
fi

echo ""
echo "==> Setup complete!"
echo "    To start Home Assistant:"
echo "    ./scripts/start-ha.sh"
echo "    HA will be available at: http://localhost:8123"
echo ""
echo "    After first start, set your home location in HA:"
echo "    Settings -> System -> General -> Set home location"
echo ""
echo "    Then add a Wolt venue:"
echo "    Settings -> Devices & Services -> Add Integration -> Search 'Wolt'"
