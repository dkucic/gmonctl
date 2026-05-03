#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXT_DIR="$HOME/.local/share/gnome-shell/extensions/gmonctl@local"
BIN_DIR="$HOME/.local/bin"

# Disable and remove GNOME extension
gnome-extensions disable gmonctl@local 2>/dev/null || true
rm -rf "$EXT_DIR"

# Remove installed binary
rm -f "$BIN_DIR/gmonctl"

# Remove built zipapp
rm -f "$SCRIPT_DIR/gmonctl.pyz"

echo "Done. Log out and back in to fully unload the extension."
