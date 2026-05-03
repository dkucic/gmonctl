# CLAUDE.md

You are building a minimal GNOME Wayland utility named `gmonctl`.

The only required user-facing feature is:

```bash
gmonctl rescue
```

This command must move all normal open application windows to the primary monitor.

This repository is an MVP, not a framework.

Keep the implementation aggressively simple.

---

## Hard Technical Constraints

This project targets:

- GNOME Shell
- Mutter
- Wayland
- Ubuntu GNOME

Do not use:

- X11
- xrandr
- wmctrl
- xdotool
- accessibility hacks
- screenshot-based logic

Wayland clients cannot move arbitrary windows.

Therefore all real window management must happen inside a GNOME Shell extension using Mutter APIs.

Python is only a thin CLI wrapper.

---

## Architecture Rules

There are only two components:

### 1. Python CLI frontend

Responsible only for:

- parsing command line arguments
- calling D-Bus methods
- printing results
- returning exit codes

Do not put window movement logic in Python.

Python must stay thin.

### 2. GNOME Shell extension backend

Responsible for:

- enumerating windows
- finding primary monitor
- computing safe positions
- moving windows
- returning counts/data over D-Bus

All actual behavior belongs here.

---

## MVP Scope

Only implement these commands:

```bash
gmonctl rescue
gmonctl list
gmonctl monitors
```

Do not add:

- app-specific move commands
- monitor toggling
- daemon watchers
- config files
- GUI
- logging frameworks
- plugin systems

Finish the MVP first.

---

## Coding Discipline

Favor direct readable code over abstractions.

Do not create abstractions unless code duplication appears at least 3 times.

Prefer fewer files.

Prefer straightforward loops.

Avoid class hierarchies unless technically necessary.

Keep total Python code small.

Keep GNOME extension code small.

Do not over-engineer D-Bus serialization.

JSON strings are acceptable.

---

## Python Rules

Use Python 3 stdlib only unless absolutely necessary.

Preferred modules:

```python
argparse
subprocess
json
sys
```

Use:

- type hints
- docstrings on public functions
- explicit return codes

Do not use:

- broad bare except
- silent failures
- hidden globals

After every Python modification run:

```bash
pylint gmonctl
```

Python code is not complete unless Pylint passes.

---

## GNOME Extension Rules

Use Mutter/GNOME Shell APIs directly.

Expected APIs include:

```js
global.get_window_actors()
global.display.get_primary_monitor()
global.display.get_monitor_geometry()
MetaWindow.get_frame_rect()
MetaWindow.move_frame()
```

Skip:

- desktop windows
- docks
- panels
- system internal windows

Only normal application windows should move.

Preserve window size.

Clamp coordinates safely inside visible bounds.

Do not create complex async behavior unless required for D-Bus export.

---

## D-Bus Contract

Keep D-Bus API fixed and simple.

Service:

```text
org.local.GMonCtl
```

Object path:

```text
/org/local/GMonCtl
```

Interface:

```text
org.local.GMonCtl
```

Methods:

```text
RescueWindows() -> int
ListWindows() -> string
ListMonitors() -> string
```

Do not rename these without strong reason.

Python and extension must stay compatible.

---

## File Creation Rules

Do not create extra files unless necessary.

Expected Python layout should stay close to:

```text
gmonctl/
  __init__.py
  __main__.py
  cli.py
```

Expected GNOME extension layout should stay minimal.

Avoid scattering logic.

---

## Editing Workflow

When making changes:

1. inspect existing code first
2. modify existing files before creating new ones
3. keep diffs small
4. do not refactor unrelated parts
5. keep MVP working after each change

Do not perform speculative cleanups.

Do not redesign working code without necessity.

---

## Definition of Done

The repository is done when:

- `gmonctl rescue` moves all normal windows to the primary monitor
- `gmonctl list` returns window JSON
- `gmonctl monitors` returns monitor JSON
- Python CLI passes Pylint > 9
- no X11 tooling exists anywhere
- codebase remains small and understandable

Everything else is secondary.
