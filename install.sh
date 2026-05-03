#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXT_DIR="$HOME/.local/share/gnome-shell/extensions/gmonctl@local"
BIN_DIR="$HOME/.local/bin"

# Build zipapp only if not already present next to this script
if [[ ! -f "$SCRIPT_DIR/gmonctl.pyz" ]]; then
    TMP="$(mktemp -d)"
    trap 'rm -rf "$TMP"' EXIT
    cp -r "$SCRIPT_DIR/gmonctl" "$TMP/"
    python3 -m zipapp "$TMP" -m "gmonctl.cli:main" -p "/usr/bin/env python3" -o "$SCRIPT_DIR/gmonctl.pyz"
    chmod +x "$SCRIPT_DIR/gmonctl.pyz"
fi

# Install the CLI binary
cp "$SCRIPT_DIR/gmonctl.pyz" "$BIN_DIR/gmonctl"

# Install GNOME extension
mkdir -p "$EXT_DIR"
cp "$SCRIPT_DIR/extension/metadata.json" "$SCRIPT_DIR/extension/extension.js" "$EXT_DIR/"
if ! gnome-extensions enable gmonctl@local 2>/dev/null; then
    echo "Note: GNOME Shell has not loaded the extension yet."
    echo "Log out and back in, then run: gnome-extensions enable gmonctl@local, afterwards run gmonctl rescue"
fi
