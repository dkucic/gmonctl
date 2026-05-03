# gmonctl

Move all GNOME Wayland application windows to the primary monitor.
Useful when secondary monitors are turned off as gnome does not seem to have native functionality to move the windows to main screen.

```bash
gmonctl rescue    # move all windows to primary monitor
gmonctl list      # list open windows as JSON
gmonctl monitors  # list monitors as JSON
```

Requires GNOME 45+ on Wayland. No X11 dependencies.

---

## Architecture

| Component | Role |
|-----------|------|
| Python CLI | Parse args, call D-Bus, print output |
| GNOME Shell extension | Enumerate windows, move via Mutter, return data |

---

## Installation

### 1. Install the GNOME Shell extension

```bash
EXT_DIR="$HOME/.local/share/gnome-shell/extensions/gmonctl@local"
mkdir -p "$EXT_DIR"
cp extension/metadata.json extension/extension.js "$EXT_DIR/"
```

Enable the extension:

```bash
gnome-extensions enable gmonctl@local
```

Or open **Extensions** (GNOME Extensions app) and toggle **GMonCtl** on.

Verify it is running:

```bash
gnome-extensions info gmonctl@local
```

Alternatively run ./install.sh to follow the instructions and install and ./uninstall.sh to remove the extensions and tool.

### 2. Install the Python CLI

**Option A — portable single-file executable (recommended)**

Build a self-contained `gmonctl.pyz` using Python's built-in `zipapp` module. No pip, no extra dependencies.

```bash
make build
```

Or without `make`:

```bash
mkdir -p _build
cp -r gmonctl _build/
python3 -m zipapp _build -m "gmonctl.cli:main" -p "/usr/bin/env python3" -o gmonctl.pyz
rm -rf _build
chmod +x gmonctl.pyz
```

Copy it anywhere on your `PATH`:

```bash
cp gmonctl.pyz ~/.local/bin/gmonctl
```

**Option B — pip install**

```bash
pip install --user .
```

This installs `gmonctl` to `~/.local/bin/`. Make sure that directory is on your `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Option C — run directly from the repo (no install)**

```bash
python3 -m gmonctl rescue
```

---

## Usage

```bash
# Move all open application windows to the primary monitor
gmonctl rescue

# List all open normal windows
gmonctl list

# List all connected monitors
gmonctl monitors
```

### Example output

```bash
$ gmonctl rescue
Moved 4 window(s) to primary monitor.

$ gmonctl monitors
[
  {
    "index": 0,
    "primary": true,
    "x": 0,
    "y": 0,
    "width": 2560,
    "height": 1440
  },
  {
    "index": 1,
    "primary": false,
    "x": 2560,
    "y": 0,
    "width": 1920,
    "height": 1080
  }
]

$ gmonctl list
[
  {
    "title": "Firefox",
    "wm_class": "firefox",
    "monitor": 1,
    "x": 2560,
    "y": 100,
    "width": 1400,
    "height": 900
  }
]
```

---

## Dependencies

- GNOME Shell 45 or later
- Wayland session
- `gdbus` (provided by `libglib2.0-bin` on Ubuntu)
- Python 3.10+

Ubuntu (it was already present on ubuntu26.04 LTS):

```bash
sudo apt install libglib2.0-bin
```

## File layout

```
gmonctl/
  extension/
    metadata.json      # GNOME extension manifest (uuid: gmonctl@local)
    extension.js       # GNOME Shell extension — all window logic lives here
  gmonctl/
    __init__.py
    __main__.py        # python -m gmonctl entry point
    cli.py             # argument parsing + D-Bus calls
  Makefile             # `make build` produces gmonctl.pyz
  pyproject.toml
  README.md
  install.sh           # install
  uninstall.sh         # uninstall
```
