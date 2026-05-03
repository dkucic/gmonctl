// ESM extension for GNOME 45+. Exposes org.local.GMonCtl on the session bus.
import Gio from 'gi://Gio';
import Meta from 'gi://Meta';

const IFACE_XML = `
<node>
  <interface name="org.local.GMonCtl">
    <method name="RescueWindows">
      <arg type="i" direction="out" name="count"/>
    </method>
    <method name="ListWindows">
      <arg type="s" direction="out" name="json"/>
    </method>
    <method name="ListMonitors">
      <arg type="s" direction="out" name="json"/>
    </method>
  </interface>
</node>`;

function isAppWindow(win) {
    const t = win.get_window_type();
    return t === Meta.WindowType.NORMAL || t === Meta.WindowType.DIALOG;
}

export default class GMonCtlExtension {
    constructor() {
        this._exported = null;
        this._nameId = 0;
    }

    enable() {
        this._exported = Gio.DBusExportedObject.wrapJSObject(IFACE_XML, this);
        this._exported.export(Gio.DBus.session, '/org/local/GMonCtl');
        this._nameId = Gio.bus_own_name(
            Gio.BusType.SESSION,
            'org.local.GMonCtl',
            Gio.BusNameOwnerFlags.NONE,
            null, null, null,
        );
    }

    disable() {
        if (this._exported) {
            this._exported.unexport();
            this._exported = null;
        }
        if (this._nameId > 0) {
            Gio.bus_unown_name(this._nameId);
            this._nameId = 0;
        }
    }

    RescueWindows() {
        const display = global.display;
        const primaryIdx = display.get_primary_monitor();
        const geo = display.get_monitor_geometry(primaryIdx);
        let count = 0;

        for (const actor of global.get_window_actors()) {
            const win = actor.get_meta_window();
            if (!isAppWindow(win))
                continue;
            if (win.get_monitor() === primaryIdx)
                continue;

            // Unmaximize before moving — maximized windows snap back otherwise.
            const maxFlags =
                (win.maximized_horizontally ? Meta.MaximizeFlags.HORIZONTAL : 0) |
                (win.maximized_vertically   ? Meta.MaximizeFlags.VERTICAL   : 0);
            if (maxFlags)
                win.unmaximize(Meta.MaximizeFlags.BOTH);

            const frame = win.get_frame_rect();
            let x = geo.x + Math.floor((geo.width - frame.width) / 2);
            let y = geo.y + Math.floor((geo.height - frame.height) / 2);

            // Clamp so the window stays fully inside the monitor.
            x = Math.max(geo.x, Math.min(x, geo.x + geo.width - frame.width));
            y = Math.max(geo.y, Math.min(y, geo.y + geo.height - frame.height));

            win.move_frame(true, x, y);

            if (maxFlags)
                win.maximize(maxFlags);

            count++;
        }

        return count;
    }

    ListWindows() {
        const windows = [];
        for (const actor of global.get_window_actors()) {
            const win = actor.get_meta_window();
            if (!isAppWindow(win))
                continue;
            const frame = win.get_frame_rect();
            windows.push({
                title: win.get_title(),
                wm_class: win.get_wm_class() ?? '',
                monitor: win.get_monitor(),
                x: frame.x,
                y: frame.y,
                width: frame.width,
                height: frame.height,
            });
        }
        return JSON.stringify(windows);
    }

    ListMonitors() {
        const display = global.display;
        const n = display.get_n_monitors();
        const primary = display.get_primary_monitor();
        const monitors = [];
        for (let i = 0; i < n; i++) {
            const geo = display.get_monitor_geometry(i);
            monitors.push({
                index: i,
                primary: i === primary,
                x: geo.x,
                y: geo.y,
                width: geo.width,
                height: geo.height,
            });
        }
        return JSON.stringify(monitors);
    }
}
