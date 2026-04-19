import os
import subprocess
from gi.repository import Nemo, Gtk, Gdk, GObject, GLib, Gio

NEMO_SUSHI = "/usr/bin/sushi"


class SushiPreview(GObject.Object, Nemo.LocationWidgetProvider):
    def __init__(self):
        super().__init__()
        self._window_dirs = {}
        GLib.timeout_add(500, self._connect_windows)

    def _connect_windows(self):
        for w in Gtk.Window.list_toplevels():
            if not hasattr(w, '_sushi_active'):
                w.connect('key-press-event', self._on_key_press)
                w._sushi_active = True
        return True

    def get_widget(self, uri, window):
        if not hasattr(window, '_sushi_active'):
            window.connect('key-press-event', self._on_key_press)
            window._sushi_active = True
        if uri.startswith('file://'):
            self._window_dirs[id(window)] = Gio.File.new_for_uri(uri).get_path()
        return None

    def _find(self, widget, *type_names):
        if type(widget).__name__ in type_names:
            return widget
        if hasattr(widget, 'get_children'):
            for child in widget.get_children():
                result = self._find(child, *type_names)
                if result:
                    return result
        return None

    def _get_selection(self, window):
        container = self._find(window, 'NemoIconViewContainer')
        if not container:
            return []
        atk = container.get_accessible()
        if not hasattr(atk, 'get_selection_count'):
            return []
        current_dir = self._window_dirs.get(id(window), '')
        if not current_dir:
            return []
        files = []
        for i in range(atk.get_selection_count()):
            child = atk.ref_selection(i)
            if child and child.get_name():
                files.append(os.path.join(current_dir, child.get_name()))
        return files

    def _on_key_press(self, window, event):
        if event.keyval == Gdk.KEY_space:
            files = self._get_selection(window)
            if files:
                subprocess.Popen([NEMO_SUSHI, files[0]], start_new_session=True)
                return True
        return False
