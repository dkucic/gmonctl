"""CLI commands for gmonctl — thin D-Bus wrapper over the GNOME extension."""
import argparse
import json
import re
import subprocess
import sys
from typing import NoReturn


DBUS_DEST = 'org.local.GMonCtl'
DBUS_PATH = '/org/local/GMonCtl'
DBUS_IFACE = 'org.local.GMonCtl'


def _die(message: str) -> NoReturn:
    """Print an error message and exit with code 1."""
    print(message, file=sys.stderr)
    sys.exit(1)


def gdbus_call(method: str) -> str:
    """Call a D-Bus method on the gmonctl service and return raw gdbus output.

    Raises RuntimeError on D-Bus failure so callers (CLI or GUI) can handle it.
    """
    cmd = [
        'gdbus', 'call',
        '--session',
        '--dest', DBUS_DEST,
        '--object-path', DBUS_PATH,
        '--method', f'{DBUS_IFACE}.{method}',
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f'D-Bus call failed for {method}.\n'
            f'Is the gmonctl GNOME extension enabled?\n'
            f'{exc.stderr.strip()}'
        ) from exc
    except FileNotFoundError as exc:
        raise RuntimeError(
            'gdbus not found. Install glib2-tools (Ubuntu: apt install libglib2.0-bin).'
        ) from exc


def parse_int_variant(output: str) -> int:
    """Parse a GLib variant integer from gdbus output such as '(int32 42,)'."""
    numbers = re.findall(r'\d+', output)
    if not numbers:
        raise ValueError(f'Cannot parse integer from gdbus output: {output!r}')
    return int(numbers[-1])


def parse_string_variant(output: str) -> str:
    """Parse a GLib variant string from gdbus output such as \"('...',)\"."""
    s = output.strip()
    if s.startswith('(') and s.endswith(',)'):
        s = s[1:-2].strip()
    if s.startswith("'") and s.endswith("'"):
        s = s[1:-1]
    return s.replace("\\'", "'")


def cmd_rescue(_args: argparse.Namespace) -> int:
    """Move all normal windows to the primary monitor."""
    try:
        count = parse_int_variant(gdbus_call('RescueWindows'))
        print(f'Moved {count} window(s) to primary monitor.')
        return 0
    except (RuntimeError, ValueError) as exc:
        _die(str(exc))


def cmd_list(_args: argparse.Namespace) -> int:
    """List all normal windows as JSON."""
    try:
        windows = json.loads(parse_string_variant(gdbus_call('ListWindows')))
        print(json.dumps(windows, indent=2))
        return 0
    except (RuntimeError, ValueError) as exc:
        _die(str(exc))


def cmd_monitors(_args: argparse.Namespace) -> int:
    """List all monitors as JSON."""
    try:
        monitors = json.loads(parse_string_variant(gdbus_call('ListMonitors')))
        print(json.dumps(monitors, indent=2))
        return 0
    except (RuntimeError, ValueError) as exc:
        _die(str(exc))


def main() -> int:
    """Entry point for the gmonctl CLI."""
    parser = argparse.ArgumentParser(
        prog='gmonctl',
        description='Control GNOME Wayland windows via D-Bus.',
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    subparsers.add_parser('rescue', help='Move all windows to the primary monitor.')
    subparsers.add_parser('list', help='List all normal windows as JSON.')
    subparsers.add_parser('monitors', help='List all monitors as JSON.')

    args = parser.parse_args()
    dispatch = {
        'rescue': cmd_rescue,
        'list': cmd_list,
        'monitors': cmd_monitors,
    }
    return dispatch[args.command](args)
