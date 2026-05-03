Read CLAUDE.md and follow it strictly.

Build the MVP now.

Implement the complete working repository for `gmonctl`:

- Python CLI frontend
- GNOME Shell extension backend
- D-Bus communication between them
- working `gmonctl rescue`
- working `gmonctl list`
- working `gmonctl monitors`

Requirements:

- GNOME 45 through GNOME 50+
- GNOME Wayland only
- Use ESM (ECMAScript Modules) syntax
- no X11 tooling
- no placeholder code
- no pseudocode
- no TODO stubs
- repository should be runnable when finished

Implementation expectations:

- create all required files
- include installation instructions in README.md
- include exact GNOME extension install path
- include exact Python CLI usage
- ensure Python code passes pylint
- keep code minimal per CLAUDE.md

For rescue behavior:

- move all NORMAL and DIALOG application windows to the primary monitor
- center each safely inside primary monitor bounds
- skip shell internal/non-app windows

After writing code:

1. run pylint
2. fix issues
3. show final repository tree
4. show exact commands needed to install and test

Do not ask for confirmation.
Start implementing immediately.
